#!/usr/bin/env python3
"""
grid_review.py — Render a finished video's frames into ONE labeled contact-sheet
grid for AI / visual review.

This is the standard QA step after every Remotion render. Build the grid, then
visually scan it for:
  • empty / half-black frames (dead air)
  • text or graphics colliding with the B-roll subject (bad placement)
  • frozen B-roll (identical adjacent frames)
  • a single visual held too long (static, not flashy)
  • mistimed reveals (text appearing before the spoken word)
Treat what you find as feedback, fix the composition, re-render, and re-grid
until the sheet looks clean.

Usage:
  python3 tools/video_review/grid_review.py out/<slug>/video.mp4
  python3 tools/video_review/grid_review.py out/<slug>/video.mp4 --interval 0.8 --cols 7
  # label raw VO time too (final * speed), useful when the comp plays A-roll sped up:
  python3 tools/video_review/grid_review.py out/<slug>/video.mp4 --speed 1.10
  # densely sample the B-roll / motion-graphic windows (FINAL-time start-end seconds):
  python3 tools/video_review/grid_review.py out/<slug>/video.mp4 --scenes 14-28,58-68 --scene-interval 0.4
  python3 tools/video_review/grid_review.py out/<slug>/video.mp4 --out logs/<slug>_grid.jpg

Output: a single JPG grid (default <video>_grid.jpg). Open / Read it to review.
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


def video_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "format=duration", "-of",
         "default=nokey=1:noprint_wrappers=1", path],
        capture_output=True, text=True,
    ).stdout.strip()
    try:
        return float(out.splitlines()[0])
    except (ValueError, IndexError):
        return 0.0


def grab_frame(path: str, t: float, w: int):
    tmp = tempfile.mktemp(suffix=".jpg")
    subprocess.run(
        ["ffmpeg", "-y", "-ss", f"{t}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:-1", tmp],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return tmp if os.path.exists(tmp) else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a labeled contact-sheet grid of a video for AI review.")
    ap.add_argument("video")
    ap.add_argument("--interval", type=float, default=0.8, help="seconds between sampled frames (default 0.8)")
    ap.add_argument("--scenes", help="comma list of FINAL-time start-end windows to densely sample, e.g. 14-28,58-68")
    ap.add_argument("--scene-interval", type=float, default=0.4, help="sampling interval inside --scenes windows")
    ap.add_argument("--cols", type=int, default=7)
    ap.add_argument("--width", type=int, default=200, help="tile width in px")
    ap.add_argument("--speed", type=float, default=1.0, help="A-roll speed multiplier; also label raw VO time = final*speed")
    ap.add_argument("--out", help="output JPG path (default <video>_grid.jpg)")
    a = ap.parse_args()

    dur = video_duration(a.video)
    if dur <= 0:
        sys.exit(f"could not read duration of {a.video}")

    times = set()
    t = 0.0
    while t < dur:
        times.add(round(t, 2))
        t += a.interval
    if a.scenes:
        for win in a.scenes.split(","):
            s, e = (float(x) for x in win.split("-"))
            t = s
            while t < min(e, dur):
                times.add(round(t, 2))
                t += a.scene_interval
    times = sorted(times)

    tiles = []
    for t in times:
        p = grab_frame(a.video, t, a.width)
        if not p:
            continue
        im = Image.open(p).convert("RGB")
        d = ImageDraw.Draw(im)
        label = f"{t}s" + (f" / raw {round(t * a.speed, 1)}" if a.speed != 1.0 else "")
        d.rectangle([0, 0, im.width, 16], fill=(0, 0, 0))
        d.text((3, 3), label, fill=GREEN)
        tiles.append(im)
        os.remove(p)
    if not tiles:
        sys.exit("no frames extracted (is ffmpeg installed?)")

    tw, th = tiles[0].size
    cols = a.cols
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 6) + 6, rows * (th + 6) + 6), (15, 15, 15))
    for i, im in enumerate(tiles):
        sheet.paste(im, (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))

    out = a.out or (os.path.splitext(a.video)[0] + "_grid.jpg")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    sheet.save(out)
    print(f"{len(tiles)} frames → {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
