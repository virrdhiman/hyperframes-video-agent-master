#!/usr/bin/env python3
from __future__ import annotations
"""
veo.py — Generate videos using Google Veo 3.1 (veo-3.1-generate-preview)
via the Google Gen AI SDK.

Supports text-to-video, image-to-video (animate a starting frame),
and reference images (use a person's photo as an actor in the video).

Auth: Uses GOOGLE_API_KEY from .env (Google AI Developer API).
Falls back to cred.json (Vertex AI) if no API key is found.

Usage:
    python3 veo.py --prompt "your prompt" [options]

Examples:
    # Basic text-to-video (9:16, 8s)
    python3 veo.py --prompt "futuristic city skyline at sunrise, cinematic" --ratio 9:16

    # Image-to-video: animate a still image
    python3 veo.py --prompt "camera slowly pans across the scene" --image photo.png

    # Reference image: use yourself as an actor in the video
    python3 veo.py --prompt "a man walking through a tech conference" --ref-image me.jpg

    # With negative prompt and custom resolution
    python3 veo.py --prompt "ocean waves at sunset" --negative "text, watermark, blurry" --resolution 1080p

    # Legacy Veo 2 mode (if needed)
    python3 veo.py --prompt "your prompt" --model veo2
"""

import argparse
import json
import os
import pprint
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
CRED_FILE = ROOT / "cred.json"
DEFAULT_OUT = ROOT / "assets" / "stock"

MODEL_MAP = {
    "veo3.1": "veo-3.1-generate-preview",
    "veo2":   "veo-2.0-generate-001",
}

RATIO_CHOICES = ["9:16", "16:9", "1:1"]
RESOLUTION_CHOICES = ["720p", "1080p", "4k"]
DURATION_CHOICES_VEO3 = [4, 6, 8]
DURATION_CHOICES_VEO2 = [5, 6, 7, 8]


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_client(model_key: str):
    """
    Create a Google Gen AI client.
    Priority: GOOGLE_API_KEY from .env → Vertex AI via cred.json
    """
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)

    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        from google import genai
        print("[veo] Auth: Google AI API key")
        return genai.Client(api_key=api_key), False

    # Fallback: Vertex AI with service account
    if CRED_FILE.exists():
        with open(CRED_FILE) as f:
            cred = json.load(f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CRED_FILE)
        from google import genai
        location = "us-central1"
        print(f"[veo] Auth: Vertex AI (service account, {location})")
        return genai.Client(
            vertexai=True,
            project=cred["project_id"],
            location=location,
        ), True

    print("[ERROR] No auth found. Set GOOGLE_API_KEY in .env or provide cred.json", file=sys.stderr)
    sys.exit(1)


def _get_field(obj, key):
    """Read a field from an object or dict."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _extract_generated_videos(operation):
    """Handle response shape differences across API and Vertex SDKs."""
    candidates = [
        _get_field(operation, "response"),
        _get_field(operation, "result"),
    ]

    for candidate in candidates:
        if not candidate:
            continue

        for key in ("generated_videos", "videos"):
            videos = _get_field(candidate, key)
            if videos:
                return videos

        nested = [_get_field(candidate, "response"), _get_field(candidate, "result")]
        for child in nested:
            if not child:
                continue
            for key in ("generated_videos", "videos"):
                videos = _get_field(child, key)
                if videos:
                    return videos

    return []


def _debug_operation(operation):
    """Print diagnostic info when the provider returns an unexpected shape."""
    response = _get_field(operation, "response")
    result = _get_field(operation, "result")
    print("[veo] Debug: operation.response type:", type(response))
    print("[veo] Debug: operation.result type:", type(result))
    if isinstance(response, dict):
        print("[veo] Debug: response keys:", sorted(response.keys()))
    if isinstance(result, dict):
        print("[veo] Debug: result keys:", sorted(result.keys()))
    if response and not isinstance(response, dict):
        print("[veo] Debug: response attrs:", [k for k in dir(response) if not k.startswith("_")][:40])
    if result and not isinstance(result, dict):
        print("[veo] Debug: result attrs:", [k for k in dir(result) if not k.startswith("_")][:40])
    if response:
        print("[veo] Debug: response preview:", pprint.pformat(response)[:1200])
    if result:
        print("[veo] Debug: result preview:", pprint.pformat(result)[:1200])


# ── Image loading ─────────────────────────────────────────────────────────────
def load_image(image_path: str):
    """Load a local image file and return a Google Gen AI Image object."""
    from google.genai import types

    path = Path(image_path)
    if not path.exists():
        print(f"[ERROR] Image not found: {path}", file=sys.stderr)
        sys.exit(1)

    ext = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(ext, "image/png")
    image_bytes = path.read_bytes()

    size_kb = len(image_bytes) // 1024
    print(f"[veo] Loaded image: {path.name} ({size_kb} KB, {mime_type})")

    return types.Image(image_bytes=image_bytes, mime_type=mime_type)


# ── Main generation ───────────────────────────────────────────────────────────
def generate(
    prompt: str,
    ratio: str = "9:16",
    duration: int = 8,
    resolution: str | None = None,
    negative_prompt: str | None = None,
    image_path: str | None = None,
    ref_image_paths: list[str] | None = None,
    model_key: str = "veo3.1",
    out_dir: str | None = None,
    prefix: str = "veo",
    poll_interval: int = 10,
    debug_response: bool = False,
):
    from google.genai import types

    client, is_vertex = get_client(model_key)

    model_id = MODEL_MAP.get(model_key)
    if not model_id:
        print(f"[ERROR] Unknown model '{model_key}'. Choose from: {list(MODEL_MAP.keys())}", file=sys.stderr)
        sys.exit(1)

    is_veo3 = model_key == "veo3.1"
    allowed_durations = DURATION_CHOICES_VEO3 if is_veo3 else DURATION_CHOICES_VEO2
    if duration not in allowed_durations:
        print(
            f"[ERROR] Invalid duration {duration}s for {model_key}. Allowed: {allowed_durations}",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── Build config ──────────────────────────────────────────────────────
    config_kwargs: dict = {
        "aspect_ratio": ratio,
        "number_of_videos": 1,
        "person_generation": "allow_all",
    }

    if is_veo3:
        config_kwargs["duration_seconds"] = str(duration)
        if resolution:
            config_kwargs["resolution"] = resolution
        if negative_prompt:
            config_kwargs["negative_prompt"] = negative_prompt
    else:
        config_kwargs["duration_seconds"] = duration
        config_kwargs["person_generation"] = "ALLOW_ADULT"

    # ── Reference images (actor mode) ─────────────────────────────────────
    if ref_image_paths and is_veo3:
        ref_images = []
        for ref_path in ref_image_paths[:3]:  # max 3
            img = load_image(ref_path)
            ref_img = types.VideoGenerationReferenceImage(
                image=img,
                reference_type="asset",
            )
            ref_images.append(ref_img)
        config_kwargs["reference_images"] = ref_images
        # Reference images require duration=8 and allow_adult
        config_kwargs["duration_seconds"] = "8"
        config_kwargs["person_generation"] = "allow_adult"
        print(f"[veo] Reference images: {len(ref_images)} loaded (actor mode)")

    config = types.GenerateVideosConfig(**config_kwargs)

    # ── Starting image (image-to-video) ───────────────────────────────────
    starting_image = None
    if image_path:
        starting_image = load_image(image_path)
        # Image-to-video requires allow_adult
        if is_veo3:
            config_kwargs["person_generation"] = "allow_adult"
            config = types.GenerateVideosConfig(**config_kwargs)

    # ── Submit job ────────────────────────────────────────────────────────
    gen_kwargs: dict = {
        "model": model_id,
        "prompt": prompt,
        "config": config,
    }
    if starting_image:
        gen_kwargs["image"] = starting_image

    print(f"[veo] Model: {model_id}")
    print(f"[veo] Ratio: {ratio} | Duration: {duration}s" +
          (f" | Resolution: {resolution}" if resolution else ""))
    print(f"[veo] Prompt: {prompt}")
    if negative_prompt:
        print(f"[veo] Negative: {negative_prompt}")
    print(f"[veo] Submitting job... (typically 2-5 min, polling every {poll_interval}s)")

    operation = client.models.generate_videos(**gen_kwargs)

    # ── Poll until done ───────────────────────────────────────────────────
    start_time = time.time()
    while not operation.done:
        elapsed = int(time.time() - start_time)
        print(f"[veo] Waiting... ({elapsed}s elapsed)", end="", flush=True)
        time.sleep(poll_interval)
        operation = client.operations.get(operation)

    print()  # newline after polling

    if operation.error:
        print(f"[ERROR] Veo generation failed: {operation.error}", file=sys.stderr)
        sys.exit(1)

    # ── Save results ──────────────────────────────────────────────────────
    out_path = Path(out_dir) if out_dir else DEFAULT_OUT
    out_path.mkdir(parents=True, exist_ok=True)

    generated_videos = _extract_generated_videos(operation)
    if not generated_videos:
        if debug_response:
            _debug_operation(operation)
        print("[ERROR] No videos in response", file=sys.stderr)
        sys.exit(1)

    saved = []
    for i, gen_video in enumerate(generated_videos):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}_{i+1}.mp4"
        filepath = out_path / filename

        video_obj = _get_field(gen_video, "video") or _get_field(gen_video, "file") or gen_video
        wrote_file = False

        # Try Google API / modern SDK file download path first
        try:
            if hasattr(client, "files") and hasattr(client.files, "download"):
                client.files.download(file=video_obj)
                if hasattr(video_obj, "save"):
                    video_obj.save(str(filepath))
                    wrote_file = True
        except Exception:
            wrote_file = False

        # Fallback: direct bytes path
        if not wrote_file:
            video_bytes = (
                _get_field(video_obj, "video_bytes")
                or _get_field(gen_video, "video_bytes")
                or _get_field(video_obj, "bytes")
            )
            if video_bytes:
                filepath.write_bytes(video_bytes)
                wrote_file = True

        if not wrote_file:
            print("[ERROR] Could not extract downloadable video bytes from SDK response.", file=sys.stderr)
            if debug_response:
                print("[veo] Debug gen_video preview:", pprint.pformat(gen_video)[:1200])
            sys.exit(1)

        size_mb = filepath.stat().st_size / (1024 * 1024)
        elapsed = int(time.time() - start_time)
        print(f"[veo] Saved: {filepath} ({size_mb:.1f} MB, {elapsed}s total)")
        saved.append(str(filepath))

    print(f"[veo] Done — {len(saved)} video(s) saved to {out_path}")
    return saved


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Generate videos with Google Veo 3.1 / Veo 2"
    )
    parser.add_argument(
        "--prompt", "-p", required=True,
        help="Text prompt for video generation"
    )
    parser.add_argument(
        "--ratio", "-r", default="9:16",
        choices=RATIO_CHOICES,
        help="Aspect ratio (default: 9:16)"
    )
    parser.add_argument(
        "--duration", "-d", type=int, default=8,
        help="Duration in seconds (Veo 3.1: 4/6/8, Veo 2: 5-8, default: 8)"
    )
    parser.add_argument(
        "--resolution", default=None,
        choices=RESOLUTION_CHOICES,
        help="Video resolution — Veo 3.1 only (default: auto)"
    )
    parser.add_argument(
        "--negative", default=None,
        help="Negative prompt — things to avoid (e.g. 'text, watermark, blurry')"
    )
    parser.add_argument(
        "--image", "-i", default=None,
        help="Starting image path for image-to-video (animate a still frame)"
    )
    parser.add_argument(
        "--ref-image", action="append", default=None,
        help="Reference image path for actor mode (can specify up to 3 times). "
             "Use your photo to appear as an actor in the generated video."
    )
    parser.add_argument(
        "--model", "-m", default="veo3.1",
        choices=list(MODEL_MAP.keys()),
        help="Model version (default: veo3.1)"
    )
    parser.add_argument(
        "--out", "-o", default=None,
        help="Output directory (default: assets/stock/)"
    )
    parser.add_argument(
        "--prefix", default="veo",
        help="Filename prefix (default: veo)"
    )
    parser.add_argument(
        "--poll", type=int, default=10,
        help="Poll interval in seconds (default: 10)"
    )
    parser.add_argument(
        "--debug-response", action="store_true",
        help="Print provider response details if no videos are returned"
    )
    args = parser.parse_args()

    generate(
        prompt=args.prompt,
        ratio=args.ratio,
        duration=args.duration,
        resolution=args.resolution,
        negative_prompt=args.negative,
        image_path=args.image,
        ref_image_paths=args.ref_image,
        model_key=args.model,
        out_dir=args.out,
        prefix=args.prefix,
        poll_interval=args.poll,
        debug_response=args.debug_response,
    )


if __name__ == "__main__":
    main()
