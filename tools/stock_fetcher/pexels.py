#!/usr/bin/env python3
"""
pexels.py — Search and download stock photos and videos from Pexels.

Reads PEXELS_API_KEY from the .env file at the project root.
Downloads to assets/stock/images/ or assets/stock/videos/ by default.

Usage:
    python3 pexels.py --query "your search" --type photo [options]
    python3 pexels.py --query "your search" --type video [options]

Examples:
    # Download 3 portrait photos of Indian tech city
    python3 pexels.py --query "Bangalore skyline" --type photo --count 3 --ratio 9:16

    # Download 2 landscape videos of coding
    python3 pexels.py --query "developer coding" --type video --count 2 --ratio 16:9

    # Download and save with a custom prefix for a specific scene
    python3 pexels.py --query "Indian college students hackathon" --type photo --prefix scene7

    # Just search and print results without downloading
    python3 pexels.py --query "AI technology" --type video --list
"""

import argparse
import json
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_IMAGE_OUT = ROOT / "assets" / "stock" / "images"
DEFAULT_VIDEO_OUT = ROOT / "assets" / "stock" / "videos"

PEXELS_PHOTO_URL = "https://api.pexels.com/v1/search"
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"

DOWNLOAD_HEADERS = {
    "User-Agent": "retrofit-ai/1.0",
    "Referer": "https://www.pexels.com/",
}

# Pexels orientation map
ORIENTATION_MAP = {
    "9:16": "portrait",
    "16:9": "landscape",
    "1:1":  "square",
}

# Photo size preference order per orientation
PHOTO_SIZE_PREF = {
    "portrait":  ["portrait", "large2x", "large", "medium"],
    "landscape": ["landscape", "large2x", "large", "medium"],
    "square":    ["large2x", "large", "medium"],
}

# Video quality preference
VIDEO_QUALITY_PREF = ["hd", "sd"]


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    load_dotenv(ENV_FILE)
    key = os.getenv("PEXELS_API_KEY")
    if not key:
        print(f"[ERROR] PEXELS_API_KEY not found in {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    return key


# ── Search ────────────────────────────────────────────────────────────────────
def search_photos(query: str, count: int, orientation: str, api_key: str) -> list[dict]:
    params = {
        "query": query,
        "per_page": min(count * 2, 20),  # fetch extra to allow filtering
        "orientation": orientation,
    }
    resp = requests.get(PEXELS_PHOTO_URL, headers={"Authorization": api_key}, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("photos", [])


def search_videos(query: str, count: int, orientation: str, api_key: str) -> list[dict]:
    params = {
        "query": query,
        "per_page": min(count * 2, 20),
        "orientation": orientation,
        "size": "medium",
    }
    resp = requests.get(PEXELS_VIDEO_URL, headers={"Authorization": api_key}, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("videos", [])


# ── Best file picker ──────────────────────────────────────────────────────────
def best_photo_url(photo: dict, orientation: str) -> str:
    src = photo.get("src", {})
    for key in PHOTO_SIZE_PREF.get(orientation, ["large2x", "large", "medium"]):
        if src.get(key):
            return src[key]
    return src.get("original", "")


def best_video_file(video: dict):
    files = video.get("video_files", [])
    # prefer HD, then SD; within quality prefer higher resolution
    for quality in VIDEO_QUALITY_PREF:
        candidates = [f for f in files if f.get("quality") == quality]
        if candidates:
            return max(candidates, key=lambda f: f.get("width", 0) * f.get("height", 0))
    return files[0] if files else None


# ── Download ──────────────────────────────────────────────────────────────────
def download_file(url: str, dest: Path, api_key: str) -> bool:
    try:
        headers = {**DOWNLOAD_HEADERS, "Authorization": api_key}
        with requests.get(url, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"[WARN] Download failed for {url}: {e}", file=sys.stderr)
        return False


# ── Print helpers ─────────────────────────────────────────────────────────────
def print_photo_list(photos: list[dict], orientation: str):
    print(f"\n{'#':<4} {'ID':<10} {'Photographer':<20} {'W':<6} {'H':<6} URL")
    print("-" * 80)
    for i, p in enumerate(photos, 1):
        url = best_photo_url(p, orientation)
        print(f"{i:<4} {p['id']:<10} {p['photographer'][:19]:<20} {p['width']:<6} {p['height']:<6} {url[:50]}")


def print_video_list(videos: list[dict]):
    print(f"\n{'#':<4} {'ID':<10} {'User':<20} {'Duration':<10} {'W':<6} {'H':<6}")
    print("-" * 80)
    for i, v in enumerate(videos, 1):
        best = best_video_file(v)
        w = best.get("width", "?") if best else "?"
        h = best.get("height", "?") if best else "?"
        user = v.get("user", {}).get("name", "unknown")[:19]
        print(f"{i:<4} {v['id']:<10} {user:<20} {v['duration']:<10} {w:<6} {h}")


# ── Main ──────────────────────────────────────────────────────────────────────
def run(query: str, media_type: str, ratio: str, count: int,
        out_dir, prefix: str, list_only: bool):

    api_key = get_api_key()
    orientation = ORIENTATION_MAP.get(ratio, "landscape")

    if media_type == "photo":
        print(f"[pexels] Searching photos — query: '{query}', orientation: {orientation}")
        results = search_photos(query, count, orientation, api_key)

        if not results:
            print("[pexels] No results found.")
            return []

        if list_only:
            print_photo_list(results, orientation)
            return []

        out_path = Path(out_dir) if out_dir else DEFAULT_IMAGE_OUT
        out_path.mkdir(parents=True, exist_ok=True)

        saved = []
        for i, photo in enumerate(results[:count], 1):
            url = best_photo_url(photo, orientation)
            if not url:
                continue
            ext = url.split("?")[0].split(".")[-1] or "jpg"
            filename = f"{prefix}_{photo['id']}_{i}.{ext}"
            dest = out_path / filename
            print(f"[pexels] Downloading photo {i}/{count}: {filename}")
            if download_file(url, dest, api_key):
                size_kb = dest.stat().st_size // 1024
                print(f"[pexels]   → {dest} ({size_kb} KB) | by {photo['photographer']}")
                saved.append(str(dest))

        print(f"[pexels] Done — {len(saved)} photo(s) saved to {out_path}")
        return saved

    elif media_type == "video":
        print(f"[pexels] Searching videos — query: '{query}', orientation: {orientation}")
        results = search_videos(query, count, orientation, api_key)

        if not results:
            print("[pexels] No results found.")
            return []

        if list_only:
            print_video_list(results)
            return []

        out_path = Path(out_dir) if out_dir else DEFAULT_VIDEO_OUT
        out_path.mkdir(parents=True, exist_ok=True)

        saved = []
        for i, video in enumerate(results[:count], 1):
            best = best_video_file(video)
            if not best:
                continue
            url = best.get("link", "")
            filename = f"{prefix}_{video['id']}_{i}.mp4"
            dest = out_path / filename
            user = video.get("user", {}).get("name", "unknown")
            print(f"[pexels] Downloading video {i}/{count}: {filename} ({best.get('width')}x{best.get('height')} {best.get('quality')})")
            if download_file(url, dest, api_key):
                size_mb = dest.stat().st_size / (1024 * 1024)
                print(f"[pexels]   → {dest} ({size_mb:.1f} MB) | by {user}")
                saved.append(str(dest))

        print(f"[pexels] Done — {len(saved)} video(s) saved to {out_path}")
        return saved


def main():
    parser = argparse.ArgumentParser(
        description="Search and download stock photos/videos from Pexels"
    )
    parser.add_argument("--query",  "-q", required=True, help="Search query")
    parser.add_argument("--type",   "-t", required=True, choices=["photo", "video"],
                        help="Media type: photo or video")
    parser.add_argument("--ratio",  "-r", default="16:9",
                        choices=list(ORIENTATION_MAP.keys()),
                        help="Aspect ratio — maps to Pexels orientation (default: 16:9)")
    parser.add_argument("--count",  "-n", type=int, default=1,
                        help="Number of items to download (default: 1)")
    parser.add_argument("--out",    "-o", default=None,
                        help="Output directory (default: assets/stock/images/ or videos/)")
    parser.add_argument("--prefix", default="pexels",
                        help="Filename prefix (default: pexels)")
    parser.add_argument("--list",   "-l", action="store_true",
                        help="List results without downloading")
    args = parser.parse_args()

    run(
        query=args.query,
        media_type=args.type,
        ratio=args.ratio,
        count=args.count,
        out_dir=args.out,
        prefix=args.prefix,
        list_only=args.list,
    )


if __name__ == "__main__":
    main()
