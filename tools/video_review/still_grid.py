#!/usr/bin/env python3
"""
still_grid.py — FAST QA. Render specific frames as Remotion STILLS (no full video
render) and montage them into one labeled grid.

Use this to iterate on a scene quickly: render a handful of frames at the moments
you care about instead of rendering the whole ~70s video. Each still re-bundles,
so keep the count small (~3–8 frames). For a full-video audit of a finished
render, use grid_review.py instead.

Usage:
  # by frame number (composition is 30fps):
  python3 tools/video_review/still_grid.py NvidiaRTXSparkMain-v1 --frames 1450,1600,1750
  # by FINAL-time seconds (converted with --fps), also label raw VO time:
  python3 tools/video_review/still_grid.py NvidiaRTXSparkMain-v1 --times 52,56,60,64 --speed 1.10
  python3 tools/video_review/still_grid.py <CompId> --frames 100,200 --out logs/s_grid.jpg
"""
import argparse
import os
import subprocess
import sys
import tempfile

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow required: pip install pillow")

GREEN = (118, 185, 0)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render Remotion stills at chosen frames and grid them for QA.")
    ap.add_argument("comp", help="composition id, e.g. NvidiaRTXSparkMain-v1")
    ap.add_argument("--entry", default="src/index.ts")
    ap.add_argument("--frames", help="comma list of frame numbers")
    ap.add_argument("--times", help="comma list of FINAL-time seconds (uses --fps)")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--speed", type=float, default=1.0, help="A-roll speed; also label raw VO time = final*speed")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--width", type=int, default=300, help="tile width px")
    ap.add_argument("--safezones", action="store_true", help="overlay IG/Shorts safe zones (red=unsafe UI bands, green=safe box, orange=caption band)")
    ap.add_argument("--gl", default="angle", help="GL backend for remotion still (angle = works for both 2D and 3D/three.js headless)")
    ap.add_argument("--out", default="logs/still_grid.jpg")
    a = ap.parse_args()

    if a.frames:
        frames = [int(float(x)) for x in a.frames.split(",")]
    elif a.times:
        frames = [int(round(float(x) * a.fps)) for x in a.times.split(",")]
    else:
        sys.exit("provide --frames or --times")

    tiles = []
    for f in frames:
        png = tempfile.mktemp(suffix=".png")
        cmd = ["npx", "remotion", "still", a.entry, a.comp, png, f"--frame={f}"]
        if a.gl:
            cmd.append(f"--gl={a.gl}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if not os.path.exists(png):
            print(f"  still failed @ frame {f}: {r.stderr[-300:]}")
            continue
        im = Image.open(png).convert("RGB")
        w = a.width
        im = im.resize((w, int(im.height * w / im.width)))
        if a.safezones:
            sx = w / 1080.0
            W, H = im.size
            t, b, l, r = int(220 * sx), int(440 * sx), int(60 * sx), int(130 * sx)
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            red = (255, 40, 40, 70)
            od.rectangle([0, 0, W, t], fill=red)
            od.rectangle([0, H - b, W, H], fill=red)
            od.rectangle([0, 0, l, H], fill=red)
            od.rectangle([W - r, 0, W, H], fill=red)
            od.rectangle([l, t, W - r, H - b], outline=(118, 185, 0, 255), width=2)
            # caption band (orange) — motion graphics must NOT enter this
            ct, cb = int(1280 * sx), int(1490 * sx)
            od.rectangle([0, ct, W, cb], fill=(255, 165, 0, 45))
            od.rectangle([0, ct, W, cb], outline=(255, 165, 0, 255), width=2)
            im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
        d = ImageDraw.Draw(im)
        lab = f"f{f} ({round(f / a.fps, 1)}s" + (f" / raw {round(f / a.fps * a.speed, 1)}" if a.speed != 1.0 else "") + ")"
        d.rectangle([0, 0, w, 18], fill=(0, 0, 0))
        d.text((4, 3), lab, fill=GREEN)
        tiles.append(im)
        os.remove(png)
    if not tiles:
        sys.exit("no stills rendered")

    tw, th = tiles[0].size
    cols = min(a.cols, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 6) + 6, rows * (th + 6) + 6), (15, 15, 15))
    for i, im in enumerate(tiles):
        sheet.paste(im, (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    sheet.save(a.out)
    print(f"{len(tiles)} stills → {a.out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
