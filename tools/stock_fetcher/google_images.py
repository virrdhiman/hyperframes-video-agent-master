#!/usr/bin/env python3
from __future__ import annotations
"""
google_images.py — Search and download images via Serper.dev /images endpoint.

Reads SERPER_API_KEY from the .env file at the project root.
Downloads to assets/stock/images/ by default.

Usage:
    python3 google_images.py --query "your search" [options]

Examples:
    # List image search results without downloading
    python3 google_images.py -q "The Indian Express logo png" --list

    # Download top 3 images for a logo
    python3 google_images.py -q "VCCircle logo png transparent" -n 3

    # Download a person's portrait photo
    python3 google_images.py -q "Deepak Puri Moser Baer founder" -n 2 --prefix deepak_puri

    # Download product images to a specific project folder
    python3 google_images.py -q "Moser Baer 8GB pen drive" -n 3 -o projects/moser_baer/assets

    # Filter by minimum dimensions
    python3 google_images.py -q "solar panels isometric 3d" --min-width 500 --min-height 500

    # Prefer PNG (transparent background) results
    python3 google_images.py -q "home theater system png" --filetype png
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_IMAGE_OUT = ROOT / "assets" / "stock" / "images"

SERPER_URL = "https://google.serper.dev/images"

# Generous timeout for image downloads (some servers are slow)
DOWNLOAD_TIMEOUT = 30

# User agent to avoid 403s from image hosts
HEADERS_DOWNLOAD = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    load_dotenv(ENV_FILE)
    key = os.getenv("SERPER_API_KEY")
    if not key:
        print(f"[ERROR] SERPER_API_KEY not found in {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    return key


# ── Search via Serper.dev ─────────────────────────────────────────────────────
def search_images(
    query: str,
    count: int,
    api_key: str,
    filetype: str | None = None,
) -> list[dict]:
    """Search Google Images via Serper.dev /images endpoint."""
    search_query = query
    if filetype:
        search_query = f"{query} filetype:{filetype}"

    payload = {
        "q": search_query,
        "num": min(count * 3, 30),  # fetch extra for fallback / filtering
    }
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    print(f"[google_images] Searching — query: '{search_query}'")
    resp = requests.post(SERPER_URL, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("images", [])
    print(f"[google_images] Found {len(results)} results")
    return results


# ── Filter results ────────────────────────────────────────────────────────────
def filter_results(
    results: list[dict],
    min_width: int,
    min_height: int,
) -> list[dict]:
    """Filter images by minimum dimensions."""
    filtered = []
    for r in results:
        w = r.get("imageWidth", 0)
        h = r.get("imageHeight", 0)
        if w >= min_width and h >= min_height:
            filtered.append(r)
    if len(filtered) < len(results):
        print(f"[google_images] Filtered {len(results)} → {len(filtered)} (min {min_width}x{min_height})")
    return filtered


# ── Print helpers ─────────────────────────────────────────────────────────────
def print_result_list(results: list[dict]):
    print(f"\n{'#':<4} {'Title':<45} {'Size':<14} {'Source':<20} URL")
    print("-" * 130)
    for i, r in enumerate(results, 1):
        title = r.get("title", "?")[:44]
        w = r.get("imageWidth", "?")
        h = r.get("imageHeight", "?")
        size = f"{w}x{h}"
        source = r.get("source", "?")[:19]
        url = r.get("imageUrl", "")[:60]
        print(f"{i:<4} {title:<45} {size:<14} {source:<20} {url}")


# ── Download ──────────────────────────────────────────────────────────────────
def guess_extension(url: str, content_type: str | None) -> str:
    """Guess file extension from URL path or Content-Type header."""
    # Try from URL path first
    path = urlparse(url).path.lower()
    for ext in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp"):
        if path.endswith(ext):
            return ext

    # Fallback to Content-Type
    if content_type:
        ct = content_type.lower()
        if "png" in ct:
            return ".png"
        if "jpeg" in ct or "jpg" in ct:
            return ".jpg"
        if "webp" in ct:
            return ".webp"
        if "gif" in ct:
            return ".gif"
        if "svg" in ct:
            return ".svg"

    return ".jpg"  # safe default


def download_image(url: str, dest_path: Path) -> Path | None:
    """Download a single image. Returns actual saved path or None on failure."""
    try:
        resp = requests.get(url, headers=HEADERS_DOWNLOAD, timeout=DOWNLOAD_TIMEOUT, stream=True)
        resp.raise_for_status()

        # Determine extension
        content_type = resp.headers.get("Content-Type", "")
        ext = guess_extension(url, content_type)

        # Ensure correct extension on dest path
        final_path = dest_path.with_suffix(ext)
        final_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(final_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        size_kb = final_path.stat().st_size / 1024
        if size_kb < 1:
            # Suspiciously small — probably a 1x1 pixel or error page
            print(f"[WARN] Skipping {final_path.name} — too small ({size_kb:.1f} KB)", file=sys.stderr)
            final_path.unlink(missing_ok=True)
            return None

        print(f"[google_images]   → {final_path.name} ({size_kb:.0f} KB, {ext})")
        return final_path

    except requests.RequestException as e:
        print(f"[WARN] Download failed for {url[:80]}... — {e}", file=sys.stderr)
        return None


# ── Main ──────────────────────────────────────────────────────────────────────
def run(
    query: str,
    count: int,
    out_dir: str | None,
    prefix: str,
    list_only: bool,
    min_width: int,
    min_height: int,
    filetype: str | None,
) -> list[str]:
    api_key = get_api_key()
    results = search_images(query, count, api_key, filetype=filetype)

    if not results:
        print("[google_images] No results found.")
        return []

    # Apply dimension filters
    results = filter_results(results, min_width, min_height)

    if list_only:
        print_result_list(results)
        return []

    out_path = Path(out_dir) if out_dir else DEFAULT_IMAGE_OUT
    out_path.mkdir(parents=True, exist_ok=True)

    saved = []
    attempts = 0

    for i, result in enumerate(results, 1):
        if len(saved) >= count:
            break

        image_url = result.get("imageUrl", "")
        if not image_url:
            continue

        title = result.get("title", "Unknown")[:50]
        w = result.get("imageWidth", "?")
        h = result.get("imageHeight", "?")
        source = result.get("source", "?")

        attempts += 1
        print(f"\n[google_images] [{len(saved)+1}/{count}] \"{title}\" ({w}x{h}, {source})")

        # Build filename: prefix_001, prefix_002, etc.
        dest = out_path / f"{prefix}_{len(saved)+1:03d}"
        downloaded = download_image(image_url, dest)

        if downloaded:
            saved.append(str(downloaded))
        elif attempts > count * 3:
            # Bail out if too many failures
            print("[google_images] Too many download failures — stopping.")
            break

    print(f"\n[google_images] Done — {len(saved)} image(s) saved to {out_path}")
    for s in saved:
        print(f"  {s}")
    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Search and download Google Images via Serper.dev"
    )
    parser.add_argument("--query",      "-q", required=True,
                        help="Search query")
    parser.add_argument("--count",      "-n", type=int, default=1,
                        help="Number of images to download (default: 1)")
    parser.add_argument("--out",        "-o", default=None,
                        help="Output directory (default: assets/stock/images/)")
    parser.add_argument("--prefix",           default="img",
                        help="Filename prefix (default: img)")
    parser.add_argument("--list",       "-l", action="store_true",
                        help="List search results without downloading")
    parser.add_argument("--min-width",        type=int, default=0,
                        help="Minimum image width in pixels (default: 0)")
    parser.add_argument("--min-height",       type=int, default=0,
                        help="Minimum image height in pixels (default: 0)")
    parser.add_argument("--filetype",         default=None,
                        choices=["png", "jpg", "gif", "svg", "webp"],
                        help="Prefer a specific file type (appends filetype: to query)")

    args = parser.parse_args()

    run(
        query=args.query,
        count=args.count,
        out_dir=args.out,
        prefix=args.prefix,
        list_only=args.list,
        min_width=args.min_width,
        min_height=args.min_height,
        filetype=args.filetype,
    )


if __name__ == "__main__":
    main()
