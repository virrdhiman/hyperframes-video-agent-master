#!/usr/bin/env python3
"""
generate_assets.py — Universal asset generation pipeline.

Reads a scenes.json file and generates all images (nano-banana) and videos
(wan-2.2) with parallel processing, automatic retries, and progress tracking.

Usage:
    # Generate all assets for a project
    python3 tools/generate_assets.py projects/bottled_water/scenes.json

    # Generate only specific scenes by ID
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --only s01_character_shocked s02_bitcoin_crossed

    # Generate only images (skip videos)
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --images-only

    # Generate only videos (skip images)
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --videos-only

    # Override parallel workers
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --workers 6

    # Force regenerate (ignore existing files)
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --force

    # Dry run (show what would be generated)
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --dry-run

    # Generate voiceover
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --voiceover

    # Stitch final video with ffmpeg
    python3 tools/generate_assets.py projects/bottled_water/scenes.json --stitch
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import urlopen

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

import replicate


# ── Schema ────────────────────────────────────────────────────────────────────

def load_config(path: str) -> dict:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    if not p.exists():
        print(f"[ERROR] scenes.json not found: {p}", file=sys.stderr)
        sys.exit(1)
    with open(p) as f:
        return json.load(f)


def resolve_path(rel: str) -> Path:
    p = Path(rel)
    if not p.is_absolute():
        p = ROOT / p
    return p


# ── Image generation ──────────────────────────────────────────────────────────

def generate_image(
    scene: dict,
    config: dict,
    out_dir: Path,
    force: bool = False,
) -> tuple[str, bool, str]:
    """Generate a single image. Returns (scene_id, success, message)."""
    scene_id = scene["id"]
    ext = config.get("image_defaults", {}).get("output_format", "jpg")
    out_path = out_dir / f"{scene_id}.{ext}"

    if out_path.exists() and not force:
        return (scene_id, True, "skipped (exists)")

    # Character refs optional — use `"characters": []` and omit `"character"` for text-only nano-banana (same as apples-shift standalone script).
    if "characters" in config:
        raw_ch = config["characters"]
        characters = raw_ch if isinstance(raw_ch, list) else [raw_ch]
    else:
        ch = config.get("character")
        characters = [ch] if ch else []

    scene_chars = scene.get("characters", characters)
    if isinstance(scene_chars, str):
        scene_chars = [scene_chars]
    scene_chars = [c for c in scene_chars if c]

    style = config.get("style_prefix", "")
    full_prompt = f"{style} {scene['prompt']}".strip()
    model = config.get("image_model", "google/nano-banana")
    defaults = config.get("image_defaults", {})

    try:
        start = time.time()
        char_files = []
        try:
            for c in scene_chars:
                char_files.append(open(resolve_path(c), "rb"))
            model_input = {
                "prompt": full_prompt,
                "aspect_ratio": defaults.get("aspect_ratio", "16:9"),
                "output_format": defaults.get("output_format", "jpg"),
            }
            if char_files:
                model_input["image_input"] = char_files
            output = replicate.run(model, input=model_input)
        finally:
            for cf in char_files:
                cf.close()

        if hasattr(output, "read"):
            data = output.read()
        elif isinstance(output, str):
            data = urlopen(output, timeout=30).read()
        else:
            return (scene_id, False, f"unexpected output type: {type(output)}")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)

        elapsed = time.time() - start
        size_kb = out_path.stat().st_size / 1024

        if out_path.stat().st_size < 1000:
            out_path.unlink()
            return (scene_id, False, "file too small, likely corrupt")

        return (scene_id, True, f"done in {elapsed:.1f}s ({size_kb:.0f} KB)")

    except Exception as e:
        if out_path.exists() and out_path.stat().st_size < 1000:
            out_path.unlink()
        return (scene_id, False, str(e))


# ── Video generation ──────────────────────────────────────────────────────────

def generate_video(
    scene: dict,
    config: dict,
    out_dir: Path,
    force: bool = False,
) -> tuple[str, bool, str]:
    """Generate a video from a source image. Returns (scene_id, success, message)."""
    scene_id = scene["id"]
    out_path = out_dir / f"{scene_id}.mp4"

    if out_path.exists() and not force:
        return (scene_id, True, "skipped (exists)")

    source_id = scene.get("source")
    if not source_id:
        return (scene_id, False, "no 'source' field for video scene")

    ext = config.get("image_defaults", {}).get("output_format", "jpg")
    source_path = out_dir / f"{source_id}.{ext}"
    if not source_path.exists():
        return (scene_id, False, f"source image not found: {source_path.name}")

    model = config.get("video_model", "wan-video/wan-2.2-i2v-fast")
    video_defaults = config.get("video_defaults", {})

    try:
        start = time.time()
        vid_input = {
            "prompt": scene["prompt"],
        }
        if video_defaults.get("resolution"):
            vid_input["resolution"] = video_defaults["resolution"]
        if video_defaults.get("num_frames"):
            vid_input["num_frames"] = video_defaults["num_frames"]
        if video_defaults.get("frames_per_second") is not None:
            vid_input["frames_per_second"] = video_defaults["frames_per_second"]
        # Allow per-scene overrides
        if scene.get("resolution"):
            vid_input["resolution"] = scene["resolution"]
        if scene.get("frames_per_second") is not None:
            vid_input["frames_per_second"] = scene["frames_per_second"]

        img_fh = open(source_path, "rb")
        try:
            vid_input["image"] = img_fh
            output = replicate.run(model, input=vid_input)
        finally:
            img_fh.close()

        if hasattr(output, "read"):
            data = output.read()
        elif isinstance(output, str):
            data = urlopen(output, timeout=60).read()
        else:
            return (scene_id, False, f"unexpected output type: {type(output)}")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)

        elapsed = time.time() - start
        size_kb = out_path.stat().st_size / 1024
        return (scene_id, True, f"done in {elapsed:.1f}s ({size_kb:.0f} KB)")

    except Exception as e:
        return (scene_id, False, str(e))


# ── Voiceover generation ─────────────────────────────────────────────────────

def generate_voiceover(config: dict) -> bool:
    vo = config.get("voiceover")
    if not vo:
        print("[vo] No voiceover config found in scenes.json")
        return False

    out_path = resolve_path(vo["output"])
    if out_path.exists():
        print(f"[vo] Already exists: {out_path}")
        return True

    script_path = resolve_path(vo["script"])
    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}", file=sys.stderr)
        return False

    cmd = [
        sys.executable, str(ROOT / "tools" / "audio_generator" / "elevenlabs.py"),
        "tts",
        "--voice-id", vo["voice_id"],
        "--text-file", str(script_path),
        "--model", vo.get("model", "eleven_multilingual_v2"),
        "--output", str(out_path),
        "--timeout", "120",
    ]
    if "stability" in vo:
        cmd.extend(["--stability", str(vo["stability"])])
    if "similarity_boost" in vo:
        cmd.extend(["--similarity-boost", str(vo["similarity_boost"])])
    if "style" in vo:
        cmd.extend(["--style", str(vo["style"])])
    if "speed" in vo:
        cmd.extend(["--speed", str(vo["speed"])])

    print(f"[vo] Generating voiceover...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Voiceover failed: {result.stderr}", file=sys.stderr)
        return False

    print(result.stdout.strip())
    return True


# ── Stitch ────────────────────────────────────────────────────────────────────

def stitch_video(config: dict) -> bool:
    """Create a simple slideshow video from all images + voiceover using ffmpeg."""
    out_dir = resolve_path(config["output_dir"])
    project = config["project"]
    vo_path = resolve_path(config["voiceover"]["output"]) if config.get("voiceover") else None

    images = sorted(out_dir.glob("s*.jpg"))
    if not images:
        print("[stitch] No scene images found")
        return False

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(vo_path)],
        capture_output=True, text=True,
    )
    audio_dur = float(probe.stdout.strip()) if probe.returncode == 0 and vo_path else 60.0
    dur_per_image = audio_dur / len(images)

    list_file = out_dir / "_ffmpeg_list.txt"
    with open(list_file, "w") as f:
        for img in images:
            f.write(f"file '{img.name}'\n")
            f.write(f"duration {dur_per_image:.3f}\n")
        f.write(f"file '{images[-1].name}'\n")

    out_video = out_dir / f"{project}_stitched.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white",
        "-r", "30", "-pix_fmt", "yuv420p",
    ]
    if vo_path and vo_path.exists():
        cmd.extend(["-i", str(vo_path), "-c:a", "aac", "-shortest"])

    cmd.extend(["-c:v", "libx264", "-preset", "fast", str(out_video)])

    print(f"[stitch] Creating {out_video.name} from {len(images)} images...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    list_file.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"[ERROR] ffmpeg failed: {result.stderr[-500:]}", file=sys.stderr)
        return False

    size_mb = out_video.stat().st_size / (1024 * 1024)
    print(f"[stitch] Saved: {out_video} ({size_mb:.1f} MB)")
    return True


# ── Parallel runner with retries ──────────────────────────────────────────────

def run_parallel(
    scenes: list[dict],
    generator_fn,
    config: dict,
    out_dir: Path,
    workers: int,
    max_retries: int,
    retry_delay: float,
    force: bool,
    label: str,
) -> dict:
    """Run generation in parallel with automatic retries. Returns stats dict."""
    total = len(scenes)
    if total == 0:
        return {"total": 0, "success": 0, "failed": 0, "results": {}}

    results: dict[str, tuple[bool, str]] = {}
    pending = list(scenes)
    attempt = 0

    while pending and attempt <= max_retries:
        if attempt > 0:
            retry_ids = [s["id"] for s in pending]
            print(
                f"\n[retry {attempt}/{max_retries}] Retrying {len(pending)} failed {label}(s) "
                f"in {retry_delay}s: {', '.join(retry_ids[:5])}{'...' if len(retry_ids) > 5 else ''}",
                flush=True,
            )
            time.sleep(retry_delay)

        batch_results: dict[str, tuple[bool, str]] = {}

        with ThreadPoolExecutor(max_workers=min(workers, len(pending))) as pool:
            futures = {
                pool.submit(generator_fn, scene, config, out_dir, force): scene
                for scene in pending
            }
            for future in as_completed(futures):
                scene = futures[future]
                scene_id, success, msg = future.result()

                status = "OK" if success else "FAIL"
                print(f"  [{status}] {scene_id}: {msg}", flush=True)
                batch_results[scene_id] = (success, msg)

        results.update(batch_results)
        pending = [s for s in pending if not batch_results.get(s["id"], (False,))[0]]
        attempt += 1

    success_count = sum(1 for ok, _ in results.values() if ok)
    failed_count = total - success_count

    return {
        "total": total,
        "success": success_count,
        "failed": failed_count,
        "results": results,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Universal asset generation pipeline — reads scenes.json, generates images & videos"
    )
    parser.add_argument("scenes_json", help="Path to scenes.json file")
    parser.add_argument("--only", nargs="+", default=None, help="Generate only these scene IDs")
    parser.add_argument("--images-only", action="store_true", help="Only generate images")
    parser.add_argument("--videos-only", action="store_true", help="Only generate videos")
    parser.add_argument("--voiceover", action="store_true", help="Generate voiceover")
    parser.add_argument("--stitch", action="store_true", help="Stitch final video with ffmpeg")
    parser.add_argument("--workers", type=int, default=None, help="Override parallel worker count")
    parser.add_argument("--retries", type=int, default=None, help="Override max retry count")
    parser.add_argument("--force", action="store_true", help="Regenerate even if files exist")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without generating")
    args = parser.parse_args()

    config = load_config(args.scenes_json)
    out_dir = resolve_path(config["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    workers = args.workers or config.get("parallel_workers", 4)
    max_retries = args.retries if args.retries is not None else config.get("max_retries", 3)
    retry_delay = config.get("retry_delay_sec", 10)

    all_scenes = config.get("scenes", [])

    if args.only:
        only_set = set(args.only)
        all_scenes = [s for s in all_scenes if s["id"] in only_set]
        if not all_scenes:
            print(f"[ERROR] No matching scene IDs: {args.only}", file=sys.stderr)
            sys.exit(1)

    image_scenes = [s for s in all_scenes if s.get("type") == "image"]
    video_scenes = [s for s in all_scenes if s.get("type") == "video"]

    if args.images_only:
        video_scenes = []
    if args.videos_only:
        image_scenes = []

    print(f"{'=' * 60}", flush=True)
    print(f"  Project:     {config['project']}", flush=True)
    print(f"  Output:      {out_dir}", flush=True)
    print(f"  Images:      {len(image_scenes)}", flush=True)
    print(f"  Videos:      {len(video_scenes)}", flush=True)
    print(f"  Workers:     {workers}", flush=True)
    print(f"  Max retries: {max_retries}", flush=True)
    print(f"  Force:       {args.force}", flush=True)
    print(f"{'=' * 60}", flush=True)

    if args.dry_run:
        print("\n[DRY RUN] Would generate:", flush=True)
        for s in image_scenes:
            ext = config.get("image_defaults", {}).get("output_format", "jpg")
            exists = (out_dir / f"{s['id']}.{ext}").exists()
            status = "EXISTS" if exists and not args.force else "GENERATE"
            print(f"  [img] [{status}] {s['id']}: {s['prompt'][:60]}...", flush=True)
        for s in video_scenes:
            exists = (out_dir / f"{s['id']}.mp4").exists()
            status = "EXISTS" if exists and not args.force else "GENERATE"
            print(f"  [vid] [{status}] {s['id']}: {s['prompt'][:60]}...", flush=True)
        return

    # Phase 0: Voiceover
    if args.voiceover:
        print(f"\n{'─' * 60}", flush=True)
        print(f"  PHASE 0: VOICEOVER", flush=True)
        print(f"{'─' * 60}", flush=True)
        generate_voiceover(config)

    # Phase 1: Images (parallel)
    if image_scenes:
        print(f"\n{'─' * 60}", flush=True)
        print(f"  PHASE 1: IMAGES ({len(image_scenes)} scenes, {workers} workers)", flush=True)
        print(f"{'─' * 60}", flush=True)

        img_stats = run_parallel(
            image_scenes, generate_image, config, out_dir,
            workers, max_retries, retry_delay, args.force, "image",
        )
        print(
            f"\n[images] {img_stats['success']}/{img_stats['total']} succeeded, "
            f"{img_stats['failed']} failed",
            flush=True,
        )

        if img_stats["failed"] > 0 and video_scenes:
            failed_sources = {
                s["source"] for s in video_scenes
                if s.get("source") in {
                    sid for sid, (ok, _) in img_stats["results"].items() if not ok
                }
            }
            if failed_sources:
                video_scenes = [
                    s for s in video_scenes if s.get("source") not in failed_sources
                ]
                print(
                    f"[warn] Skipping {len(failed_sources)} video(s) whose source images failed",
                    flush=True,
                )

    # Phase 2: Videos (parallel, after images complete)
    if video_scenes:
        print(f"\n{'─' * 60}", flush=True)
        print(f"  PHASE 2: VIDEOS ({len(video_scenes)} scenes, {workers} workers)", flush=True)
        print(f"{'─' * 60}", flush=True)

        vid_stats = run_parallel(
            video_scenes, generate_video, config, out_dir,
            workers, max_retries, retry_delay, args.force, "video",
        )
        print(
            f"\n[videos] {vid_stats['success']}/{vid_stats['total']} succeeded, "
            f"{vid_stats['failed']} failed",
            flush=True,
        )

    # Phase 3: Stitch
    if args.stitch:
        print(f"\n{'─' * 60}", flush=True)
        print(f"  PHASE 3: STITCH", flush=True)
        print(f"{'─' * 60}", flush=True)
        stitch_video(config)

    # Summary
    print(f"\n{'=' * 60}", flush=True)
    total_images = len(list(out_dir.glob("s*.jpg"))) + len(list(out_dir.glob("s*.png")))
    total_videos = len(list(out_dir.glob("*.mp4")))
    print(f"  DONE: {total_images} images, {total_videos} videos in {out_dir}", flush=True)
    print(f"{'=' * 60}", flush=True)


if __name__ == "__main__":
    main()
