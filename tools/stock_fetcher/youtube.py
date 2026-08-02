#!/usr/bin/env python3
from __future__ import annotations
"""
youtube.py — Search YouTube via Serper.dev, download via yt-dlp, smart-trim via transcript.

Reads SERPER_API_KEY from the .env file at the project root.
Downloads to assets/stock/videos/ by default.

Usage:
    python3 youtube.py --query "your search" [options]

Examples:
    # List YouTube search results without downloading
    python3 youtube.py -q "samsung s26 ultra review" --list

    # Download 1 video, auto-trim to where "privacy display" is discussed
    python3 youtube.py -q "samsung s26 ultra review" --topic "privacy display" --duration 8

    # Download a YouTube Short (vertical b-roll)
    python3 youtube.py -q "samsung s26 ultra" --shorts -n 1

    # Manual trim: grab 10 seconds starting at 0:45
    python3 youtube.py -q "samsung s26 ultra review" --start 45 --duration 10

    # Download full video + transcript, no trimming
    python3 youtube.py -q "samsung s26 ultra review" --prefix scene7
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_VIDEO_OUT = ROOT / "assets" / "stock" / "videos"
TEMP_DIR = ROOT / "temp"

SERPER_URL = "https://google.serper.dev/videos"

_local_ytdlp = Path(__file__).parent / "yt-dlp"
YTDLP_BIN = str(_local_ytdlp) if _local_ytdlp.exists() else (__import__("shutil").which("yt-dlp") or "yt-dlp")
FFMPEG_BIN = "ffmpeg"

def _detect_proxy():
    import os, socket
    p = os.environ.get("YT_PROXY")
    if p:
        return p or None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(0.5)
    try:
        return "socks5://127.0.0.1:1080" if s.connect_ex(("127.0.0.1", 1080)) == 0 else None
    finally:
        s.close()
YT_PROXY = _detect_proxy()

# Default yt-dlp format: best up to 1080p, merged as mp4
DEFAULT_FORMAT = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    load_dotenv(ENV_FILE)
    key = os.getenv("SERPER_API_KEY")
    if not key:
        print(f"[ERROR] SERPER_API_KEY not found in {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    return key


# ── YouTube URL helpers ───────────────────────────────────────────────────────
def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/").split("/")[0]
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith(("/embed/", "/v/", "/shorts/")):
            return parsed.path.split("/")[2] if len(parsed.path.split("/")) > 2 else None
    return None


def is_youtube_url(url: str) -> bool:
    """Check if a URL is a valid YouTube video link."""
    return extract_video_id(url) is not None


# ── Search via Serper.dev ─────────────────────────────────────────────────────
def search_youtube(query: str, count: int, shorts: bool, api_key: str) -> list[dict]:
    """Search YouTube videos via Serper.dev /videos endpoint."""
    site_prefix = "site:youtube.com/shorts" if shorts else "site:youtube.com"
    payload = {"q": f"{site_prefix} {query}"}
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    print(f"[youtube] Searching {'Shorts' if shorts else 'videos'} — query: '{query}'")
    resp = requests.post(SERPER_URL, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("videos", [])
    # Filter to only actual YouTube URLs
    results = [r for r in results if is_youtube_url(r.get("link", ""))]
    return results[:count * 2]  # fetch extra for fallback


# ── Print helpers ─────────────────────────────────────────────────────────────
def print_result_list(results: list[dict]):
    print(f"\n{'#':<4} {'Title':<50} {'Channel':<20} {'Duration':<10} URL")
    print("-" * 120)
    for i, r in enumerate(results, 1):
        title = r.get("title", "?")[:49]
        channel = r.get("channel", "?")[:19]
        duration = r.get("duration", "?")
        link = r.get("link", "")
        print(f"{i:<4} {title:<50} {channel:<20} {duration:<10} {link}")


# ── SRT parsing (reused from caption_generator/parse_srt.py) ─────────────────
def tc_to_seconds(tc: str) -> float:
    """Convert SRT timecode '00:00:02,381' to seconds."""
    tc = tc.strip().replace(",", ".")
    parts = tc.split(":")
    h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
    return h * 3600 + m * 60 + s


def parse_srt_file(srt_path: Path) -> list[dict]:
    """Parse SRT file into list of {id, start, end, text} dicts."""
    content = srt_path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", content.strip())
    segments = []

    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        try:
            seg_id = int(lines[0])
        except ValueError:
            continue

        tc_match = re.match(
            r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})",
            lines[1],
        )
        if not tc_match:
            continue

        start = tc_to_seconds(tc_match.group(1))
        end = tc_to_seconds(tc_match.group(2))
        text = " ".join(lines[2:])
        segments.append({"id": seg_id, "start": round(start, 3), "end": round(end, 3), "text": text})

    return segments


# ── Smart transcript-based segment finder ─────────────────────────────────────
def find_best_segment(srt_path: Path, topic: str, duration: float) -> tuple[float, float] | None:
    """
    Find the best segment in a transcript where the topic is most discussed.

    Uses a sliding window approach:
    1. Tokenize topic into keywords
    2. Slide a window of `duration` seconds across the transcript
    3. Score each window by keyword match density
    4. Return the (start, end) of the highest-scoring window
    """
    segments = parse_srt_file(srt_path)
    if not segments:
        print("[youtube] No transcript segments found — skipping smart trim")
        return None

    keywords = [w.lower() for w in topic.split() if len(w) > 2]
    if not keywords:
        return None

    total_duration = segments[-1]["end"]
    best_score = 0
    best_start = 0.0

    # Slide window in 1-second steps
    step = 1.0
    t = 0.0
    while t + duration <= total_duration:
        window_end = t + duration
        # Collect all text in this window
        window_text = " ".join(
            seg["text"].lower()
            for seg in segments
            if seg["start"] < window_end and seg["end"] > t
        )
        # Score by keyword matches
        score = sum(window_text.count(kw) for kw in keywords)
        if score > best_score:
            best_score = score
            best_start = t
        t += step

    if best_score == 0:
        print(f"[youtube] Topic '{topic}' not found in transcript — skipping smart trim")
        return None

    # Snap to nearest subtitle boundary for cleaner cuts
    closest_seg = min(segments, key=lambda s: abs(s["start"] - best_start))
    snapped_start = max(0, closest_seg["start"] - 0.5)

    print(f"[youtube] Found topic '{topic}' — best window at {snapped_start:.1f}s (score: {best_score})")

    # Show the transcript text in that window for verification
    window_text_segments = [
        seg["text"]
        for seg in segments
        if seg["start"] < snapped_start + duration and seg["end"] > snapped_start
    ]
    print(f"[youtube] Transcript in window: \"{' '.join(window_text_segments)}\"")

    return (snapped_start, snapped_start + duration)


# ── Download via yt-dlp ───────────────────────────────────────────────────────
def download_video(url: str, dest: Path, format_str: str, needs_subs: bool = True) -> tuple[Path | None, Path | None]:
    """
    Download a YouTube video + optionally auto-generated subtitles via yt-dlp.
    Returns (video_path, srt_path) — srt_path may be None if no subs available.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)

    # yt-dlp output template (without extension — yt-dlp adds it)
    output_template = str(dest.with_suffix(""))

    cmd = [
        YTDLP_BIN,
        url,
        "-o", f"{output_template}.%(ext)s",
        "-f", format_str,
        "--merge-output-format", "mp4",
    ]
    if YT_PROXY:
        cmd.extend(["--proxy", YT_PROXY])
    
    if needs_subs:
        cmd.extend([
            "--write-auto-subs",
            "--sub-lang", "en",
            "--sub-format", "srt",
        ])
        
    cmd.extend([
        "--no-playlist",
        "--no-overwrites",
        "--quiet",
        "--progress",
    ])

    print(f"[youtube] Downloading: {url}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        stderr = result.stderr.strip()
        print(f"[WARN] yt-dlp failed: {stderr[:200]}", file=sys.stderr)
        return None, None

    # Find the actual downloaded files
    video_path = dest.with_suffix(".mp4")
    if not video_path.exists():
        # yt-dlp might have used a different extension
        candidates = list(dest.parent.glob(f"{dest.stem}.*"))
        video_candidates = [c for c in candidates if c.suffix in (".mp4", ".mkv", ".webm")]
        video_path = video_candidates[0] if video_candidates else None

    # Find SRT file (yt-dlp names it: <name>.en.srt)
    srt_path = None
    srt_candidates = list(dest.parent.glob(f"{dest.stem}*.srt"))
    if srt_candidates:
        srt_path = srt_candidates[0]

    if video_path and video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"[youtube]   → {video_path.name} ({size_mb:.1f} MB)")
    else:
        print("[WARN] Video file not found after download", file=sys.stderr)
        return None, None

    if srt_path:
        print(f"[youtube]   → Transcript: {srt_path.name}")
    else:
        print("[youtube]   → No transcript available")

    return video_path, srt_path


# ── Trim via ffmpeg ───────────────────────────────────────────────────────────
def trim_video(input_path: Path, output_path: Path, start: float, duration: float) -> bool:
    """Trim a video using ffmpeg copy (fast, no re-encoding)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        FFMPEG_BIN,
        "-ss", str(start),
        "-t", str(duration),
        "-i", str(input_path),
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        "-y",  # overwrite
        str(output_path),
    ]

    print(f"[youtube] Trimming: {start:.1f}s → {start + duration:.1f}s ({duration:.0f}s clip)")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        print(f"[WARN] ffmpeg trim failed: {result.stderr[:200]}", file=sys.stderr)
        return False

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[youtube]   → Trimmed: {output_path.name} ({size_mb:.1f} MB)")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────
def run(
    query: str,
    count: int,
    out_dir: str | None,
    prefix: str,
    list_only: bool,
    shorts: bool,
    topic: str | None,
    start: float | None,
    duration: float,
    format_str: str,
    keep_full: bool,
):
    api_key = get_api_key()
    results = search_youtube(query, count, shorts, api_key)

    if not results:
        print("[youtube] No results found.")
        return []

    if list_only:
        print_result_list(results)
        return []

    out_path = Path(out_dir) if out_dir else DEFAULT_VIDEO_OUT
    out_path.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    needs_trim = topic or start is not None
    saved = []

    for i, result in enumerate(results[:count], 1):
        url = result.get("link", "")
        vid_id = extract_video_id(url) or f"unknown_{i}"
        title = result.get("title", "Unknown")
        channel = result.get("channel", "Unknown")

        print(f"\n[youtube] [{i}/{count}] \"{title}\" by {channel}")

        # Download to temp if trimming, else directly to output
        if needs_trim:
            dl_dest = TEMP_DIR / f"{prefix}_{vid_id}_{i}"
        else:
            dl_dest = out_path / f"{prefix}_{vid_id}_{i}"

        needs_subs = topic is not None
        video_path, srt_path = download_video(url, dl_dest, format_str, needs_subs)
        if not video_path:
            continue

        # ── Determine trim range ──────────────────────────────────────────
        trim_start = None
        trim_dur = duration

        if start is not None:
            # Manual trim
            trim_start = start
        elif topic and srt_path:
            # Smart transcript-based trim
            segment = find_best_segment(srt_path, topic, duration)
            if segment:
                trim_start, trim_end = segment
                trim_dur = trim_end - trim_start

        # ── Trim if needed ────────────────────────────────────────────────
        if trim_start is not None:
            final_name = f"{prefix}_{vid_id}_{i}.mp4"
            final_path = out_path / final_name

            if trim_video(video_path, final_path, trim_start, trim_dur):
                saved.append(str(final_path))
                # Clean up full video unless --keep-full
                if not keep_full:
                    video_path.unlink(missing_ok=True)
                    if srt_path:
                        srt_path.unlink(missing_ok=True)
                else:
                    # Move full video to output dir
                    full_dest = out_path / f"{prefix}_{vid_id}_{i}_full.mp4"
                    video_path.rename(full_dest)
                    print(f"[youtube]   → Full video kept: {full_dest.name}")
            else:
                # Trim failed — keep full video
                final_path = out_path / f"{prefix}_{vid_id}_{i}.mp4"
                video_path.rename(final_path)
                saved.append(str(final_path))
        else:
            # No trimming — move from temp if needed
            if needs_trim:
                final_path = out_path / f"{prefix}_{vid_id}_{i}.mp4"
                video_path.rename(final_path)
                saved.append(str(final_path))
            else:
                saved.append(str(video_path))

        # Copy SRT to output dir if it exists and we're keeping things
        if srt_path and srt_path.exists():
            srt_dest = out_path / f"{prefix}_{vid_id}_{i}.srt"
            if srt_path != srt_dest:
                srt_path.rename(srt_dest)

    print(f"\n[youtube] Done — {len(saved)} video(s) saved to {out_path}")
    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Search YouTube via Serper.dev and download via yt-dlp with smart transcript trimming"
    )
    parser.add_argument("--query",    "-q", required=True, help="Search query")
    parser.add_argument("--count",    "-n", type=int, default=1,
                        help="Number of videos to download (default: 1)")
    parser.add_argument("--out",      "-o", default=None,
                        help="Output directory (default: assets/stock/videos/)")
    parser.add_argument("--prefix",         default="yt",
                        help="Filename prefix (default: yt)")
    parser.add_argument("--list",     "-l", action="store_true",
                        help="List search results without downloading")
    parser.add_argument("--shorts",         action="store_true",
                        help="Search YouTube Shorts only")
    parser.add_argument("--topic",    "-t", default=None,
                        help="Keywords to find in transcript for smart trim (e.g. 'privacy display')")
    parser.add_argument("--start",    "-s", type=float, default=None,
                        help="Manual trim start time in seconds (overrides --topic)")
    parser.add_argument("--duration", "-d", type=float, default=8.0,
                        help="Trim duration in seconds (default: 8)")
    parser.add_argument("--format",   "-f", default=DEFAULT_FORMAT,
                        help="yt-dlp format string (default: best 1080p mp4)")
    parser.add_argument("--keep-full",      action="store_true",
                        help="Keep the full downloaded video alongside trimmed clip")

    args = parser.parse_args()

    run(
        query=args.query,
        count=args.count,
        out_dir=args.out,
        prefix=args.prefix,
        list_only=args.list,
        shorts=args.shorts,
        topic=args.topic,
        start=args.start,
        duration=args.duration,
        format_str=args.format,
        keep_full=args.keep_full,
    )


if __name__ == "__main__":
    main()
