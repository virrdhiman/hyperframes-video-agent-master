#!/usr/bin/env python3
from __future__ import annotations
"""
background_remover.py — Remove backgrounds from images using Replicate's 851-labs model.

Reads REPLICATE_API_TOKEN from the .env file at the project root.
Outputs transparent PNG by default.

Usage:
    python3 background_remover.py --input <image_path_or_url> [options]

Examples:
    # Remove background from a local image
    python3 background_remover.py --input assets/images/portrait.jpg

    # Remove background and save to specific path
    python3 background_remover.py --input assets/images/portrait.jpg --output assets/images/portrait_nobg.png

    # Remove background from a URL
    python3 background_remover.py --input "https://example.com/photo.jpg" --output assets/images/clean.png

    # Keep only the background (reverse mode)
    python3 background_remover.py --input assets/images/scene.jpg --reverse

    # Custom threshold for edge detection
    python3 background_remover.py --input assets/images/logo.png --threshold 128

    # Batch process all JPGs in a folder
    python3 background_remover.py --batch assets/images/people/ --suffix _nobg
"""

import argparse
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import replicate
import requests as http_requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_OUT = ROOT / "assets" / "images"

MODEL_ID = "851-labs/background-remover:a029dff38972b5fda4ec5d75d7d1cd25aeff621d2cf4946a41055d7db66b80bc"


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_api_token() -> str:
    load_dotenv(ENV_FILE)
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        print(f"[ERROR] REPLICATE_API_TOKEN not found in {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    return token


# ── Helpers ───────────────────────────────────────────────────────────────────
def is_url(s: str) -> bool:
    """Check if string looks like a URL."""
    parsed = urlparse(s)
    return parsed.scheme in ("http", "https")


def resolve_input(input_path: str) -> str | Path:
    """Resolve input to a URL string or a local file Path."""
    if is_url(input_path):
        return input_path
    p = Path(input_path)
    if not p.is_absolute():
        p = ROOT / p
    if not p.exists():
        print(f"[ERROR] Input file not found: {p}", file=sys.stderr)
        sys.exit(1)
    return p


def build_output_path(input_path: str, output: str | None, suffix: str) -> Path:
    """Determine the output file path."""
    if output:
        out = Path(output)
        if not out.is_absolute():
            out = ROOT / out
        return out

    # Auto-generate from input filename
    if is_url(input_path):
        url_path = urlparse(input_path).path
        stem = Path(url_path).stem or "image"
    else:
        stem = Path(input_path).stem

    out = DEFAULT_OUT / f"{stem}{suffix}.png"
    return out


# ── Core ──────────────────────────────────────────────────────────────────────
def remove_background(
    input_source: str | Path,
    output_path: Path,
    reverse: bool = False,
    threshold: int = 0,
    bg_type: str = "rgba",
    fmt: str = "png",
) -> Path | None:
    """Remove background from an image using Replicate 851-labs model.

    Args:
        input_source: URL string or local file Path
        output_path: Where to save the result
        reverse: If True, keep background and remove foreground
        threshold: Edge detection threshold (0 = auto)
        bg_type: Background type — "rgba" (transparent), "white", "black", "blur"
        fmt: Output format — "png" or "webp"

    Returns:
        Path to saved file, or None on failure.
    """
    # Prepare the image input
    if isinstance(input_source, Path):
        image_input = open(input_source, "rb")
        source_label = input_source.name
    else:
        image_input = input_source
        source_label = input_source[:80]

    print(f"[bg_remover] Processing: {source_label}")
    print(f"[bg_remover] Model: 851-labs/background-remover")
    print(f"[bg_remover] Settings: reverse={reverse}, threshold={threshold}, bg={bg_type}, format={fmt}")

    try:
        start = time.time()
        output = replicate.run(
            MODEL_ID,
            input={
                "image": image_input,
                "format": fmt,
                "reverse": reverse,
                "threshold": threshold,
                "background_type": bg_type,
            },
        )
        elapsed = time.time() - start
        print(f"[bg_remover] Replicate returned in {elapsed:.1f}s")

        # Read the output — may be a URL string or a FileOutput with .read()
        if isinstance(output, str):
            # It's a URL — download the result
            print(f"[bg_remover] Downloading result from URL...")
            resp = http_requests.get(output, timeout=30)
            resp.raise_for_status()
            image_bytes = resp.content
        elif hasattr(output, "read"):
            image_bytes = output.read()
        else:
            print(f"[ERROR] Unexpected output type: {type(output)}", file=sys.stderr)
            return None

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the result
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        size_kb = output_path.stat().st_size / 1024
        print(f"[bg_remover] Saved: {output_path} ({size_kb:.0f} KB)")
        return output_path

    except Exception as e:
        print(f"[ERROR] Background removal failed: {e}", file=sys.stderr)
        return None
    finally:
        # Close file handle if we opened one
        if isinstance(input_source, Path) and hasattr(image_input, "close"):
            image_input.close()


# ── Batch mode ────────────────────────────────────────────────────────────────
def process_batch(
    input_dir: str,
    suffix: str,
    reverse: bool,
    threshold: int,
    bg_type: str,
    fmt: str,
) -> list[str]:
    """Process all images in a directory."""
    dir_path = Path(input_dir)
    if not dir_path.is_absolute():
        dir_path = ROOT / dir_path

    if not dir_path.is_dir():
        print(f"[ERROR] Not a directory: {dir_path}", file=sys.stderr)
        sys.exit(1)

    extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
    images = sorted(
        f for f in dir_path.iterdir()
        if f.suffix.lower() in extensions and suffix not in f.stem
    )

    if not images:
        print(f"[bg_remover] No images found in {dir_path}")
        return []

    print(f"[bg_remover] Found {len(images)} image(s) in {dir_path}")
    saved = []

    for i, img in enumerate(images, 1):
        out_path = img.parent / f"{img.stem}{suffix}.png"
        print(f"\n[bg_remover] [{i}/{len(images)}] {img.name}")
        result = remove_background(
            input_source=img,
            output_path=out_path,
            reverse=reverse,
            threshold=threshold,
            bg_type=bg_type,
            fmt=fmt,
        )
        if result:
            saved.append(str(result))

    print(f"\n[bg_remover] Batch done — {len(saved)}/{len(images)} processed")
    return saved


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Remove image backgrounds using Replicate (851-labs/background-remover)"
    )

    # Input modes (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input", "-i",
        help="Path to local image or URL"
    )
    input_group.add_argument(
        "--batch", "-b",
        help="Directory of images to batch process"
    )

    # Output
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output file path (default: auto-generated from input name)"
    )
    parser.add_argument(
        "--suffix", default="_nobg",
        help="Suffix for output filenames in batch mode (default: _nobg)"
    )

    # Model settings
    parser.add_argument(
        "--reverse", action="store_true",
        help="Keep background, remove foreground"
    )
    parser.add_argument(
        "--threshold", type=int, default=0,
        help="Edge detection threshold, 0 = auto (default: 0)"
    )
    parser.add_argument(
        "--bg-type", default="rgba",
        choices=["rgba", "white", "black", "blur"],
        help="Background type (default: rgba = transparent)"
    )
    parser.add_argument(
        "--format", dest="fmt", default="png",
        choices=["png", "webp"],
        help="Output format (default: png)"
    )

    args = parser.parse_args()

    # Set up auth
    os.environ["REPLICATE_API_TOKEN"] = get_api_token()

    if args.batch:
        # Batch mode
        process_batch(
            input_dir=args.batch,
            suffix=args.suffix,
            reverse=args.reverse,
            threshold=args.threshold,
            bg_type=args.bg_type,
            fmt=args.fmt,
        )
    else:
        # Single image mode
        input_source = resolve_input(args.input)
        output_path = build_output_path(args.input, args.output, args.suffix)

        remove_background(
            input_source=input_source,
            output_path=output_path,
            reverse=args.reverse,
            threshold=args.threshold,
            bg_type=args.bg_type,
            fmt=args.fmt,
        )


if __name__ == "__main__":
    main()
