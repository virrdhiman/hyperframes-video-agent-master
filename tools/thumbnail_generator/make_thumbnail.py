#!/usr/bin/env python3
"""
make_thumbnail.py — Generate a video thumbnail with nano-banana on Replicate.

Sends a FACE screenshot (from the raw talking-head) + optional LOGO PNGs as
reference images, plus a concept/expression/elements prompt. nano-banana keeps
the creator's likeness and composes the thumbnail around it.

  python3 tools/thumbnail_generator/make_thumbnail.py \
    --face /tmp/face.png \
    --logos public/<slug>/logos/nvidia_001.png public/<slug>/logos/apple_001.png \
    --prompt "shocked expression, glowing green chip, NVIDIA vs Apple versus layout, dark dramatic, leave top space for title, no text" \
    --ratio 16:9 \
    --out public/<slug>/thumbnails/thumb_v1.jpg

Workflow / prompt tips: see the thumbnail-generation note in agent memory.
Ratio: 16:9 = YouTube thumbnail; 9:16 = short/Reel cover.
"""
import argparse
import os
import sys
from urllib.request import urlopen

try:
    import replicate
except ImportError:
    sys.exit("pip install replicate")


def load_token() -> None:
    if os.environ.get("REPLICATE_API_TOKEN"):
        return
    env = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if os.path.exists(env):
        for line in open(env):
            s = line.strip()
            if s.startswith("REPLICATE_API_TOKEN") and "=" in s:
                os.environ["REPLICATE_API_TOKEN"] = s.split("=", 1)[1].strip().strip('"').strip("'")
                return


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a thumbnail via nano-banana on Replicate.")
    ap.add_argument("--face", required=True, help="reference screenshot of the creator's face/expression (from the raw talking-head)")
    ap.add_argument("--logos", nargs="*", default=[], help="optional logo PNGs to composite")
    ap.add_argument("--prompt", required=True, help="concept + expression + elements to add")
    ap.add_argument("--out", required=True, help="output .jpg path (public/<slug>/thumbnails/...)")
    ap.add_argument("--ratio", default="16:9", help="16:9 (YouTube) or 9:16 (short cover)")
    ap.add_argument("--model", default="google/nano-banana")
    a = ap.parse_args()

    load_token()
    if not os.environ.get("REPLICATE_API_TOKEN"):
        sys.exit("REPLICATE_API_TOKEN not found (env or .env)")

    refs = [a.face] + list(a.logos)
    for r in refs:
        if not os.path.exists(r):
            sys.exit(f"reference image not found: {r}")

    files = [open(r, "rb") for r in refs]
    try:
        model_input = {
            "prompt": a.prompt,
            "aspect_ratio": a.ratio,
            "output_format": "jpg",
            "image_input": files,
        }
        print(f"nano-banana ({a.model}) · {len(files)} ref(s) · {a.ratio}")
        output = replicate.run(a.model, input=model_input)
    finally:
        for f in files:
            f.close()

    data = output.read() if hasattr(output, "read") else urlopen(output, timeout=60).read()
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "wb") as f:
        f.write(data)
    print(f"→ {a.out} ({len(data) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
