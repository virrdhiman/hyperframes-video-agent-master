#!/usr/bin/env python3
"""
contact_grid.py — Build labeled N×M frame grids from a video for motion-graphic analysis.

Use case (editor workflow):
  1. Coarse grid over full video → spot *when* motion graphics appear
  2. Fine grid over a short window → study *how* an animation plays out

Examples:
  # Full video overview (16 frames, ~52s apart on a 14min video)
  python3 tools/motion_ref/contact_grid.py \\
    assets/inspo/motion-ref-Guufmu3rIx4/reference.mp4 \\
    --rows 4 --cols 4 --out assets/inspo/motion-ref-Guufmu3rIx4/grids/00_full_4x4.jpg

  # Zoom: 3.2s window at 2:15 with 16 frames (~0.2s apart)
  python3 tools/motion_ref/contact_grid.py \\
    assets/inspo/motion-ref-Guufmu3rIx4/reference.mp4 \\
    --start 135 --end 138.2 --rows 4 --cols 4 \\
    --out assets/inspo/motion-ref-Guufmu3rIx4/grids/zoom_135s_4x4.jpg
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str]) -> None:
    print("[run]", " ".join(cmd))
    subprocess.run(cmd, check=True)


def probe_duration(video: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        text=True,
    ).strip()
    return float(out)


def probe_size(video: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=p=0",
            str(video),
        ],
        text=True,
    ).strip()
    w, h = out.split(",")
    return int(w), int(h)


def format_ts(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h >= 1:
        return f"{int(h):d}:{int(m):02d}:{s:05.2f}"
    return f"{int(m):d}:{s:05.2f}"


def build_grid(
    video: Path,
    out_path: Path,
    rows: int,
    cols: int,
    start: float,
    end: float,
    thumb_w: int,
    keep_frames: bool,
) -> list[dict]:
    n = rows * cols
    if end <= start:
        raise ValueError("end must be greater than start")
    duration = end - start
    step = duration / n

    work = out_path.parent / f".{out_path.stem}_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    frame_paths: list[Path] = []

    for i in range(n):
        t = start + step * i + step * 0.5  # sample center of each bin
        t = min(t, end - 0.04)
        label = format_ts(t)
        fname = work / f"{i:02d}_{label.replace(':', '-')}.jpg"
        run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t:.3f}",
                "-i",
                str(video),
                "-vframes",
                "1",
                "-q:v",
                "2",
                str(fname),
            ]
        )
        frame_paths.append(fname)
        manifest.append({"index": i, "time_sec": round(t, 3), "label": label, "file": fname.name})

    # Label + tile with ImageMagick montage
    labeled_dir = work / "labeled"
    labeled_dir.mkdir(exist_ok=True)
    labeled_paths: list[Path] = []
    for i, fp in enumerate(frame_paths):
        entry = manifest[i]
        labeled = labeled_dir / f"labeled_{i:02d}.jpg"
        # Caption bar under thumb
        run(
            [
                "convert",
                str(fp),
                "-gravity",
                "south",
                "-background",
                "black",
                "-splice",
                "0x36",
                "-fill",
                "white",
                "-pointsize",
                "18",
                "-annotate",
                "+0+6",
                f"{entry['label']}  ({entry['time_sec']:.2f}s)",
                str(labeled),
            ]
        )
        labeled_paths.append(labeled)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    montage_cmd = [
        "montage",
        *[str(p) for p in labeled_paths],
        "-tile",
        f"{cols}x{rows}",
        "-geometry",
        f"{thumb_w}x+2+2",
        "-background",
        "#111111",
        str(out_path),
    ]
    run(montage_cmd)

    manifest_path = out_path.with_suffix(".json")
    manifest_path.write_text(
        json.dumps(
            {
                "video": str(video),
                "start_sec": start,
                "end_sec": end,
                "rows": rows,
                "cols": cols,
                "step_sec": round(step, 4),
                "frames": manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    if not keep_frames:
        shutil.rmtree(work)

    return manifest


def main() -> None:
    p = argparse.ArgumentParser(description="Build labeled contact sheet from video")
    p.add_argument("video", type=Path, help="Input video path")
    p.add_argument("--rows", type=int, default=4)
    p.add_argument("--cols", type=int, default=4)
    p.add_argument("--start", type=float, default=None, help="Start time (seconds)")
    p.add_argument("--end", type=float, default=None, help="End time (seconds)")
    p.add_argument("--out", type=Path, required=True, help="Output JPG path")
    p.add_argument("--thumb-w", type=int, default=420, help="Thumbnail width per cell")
    p.add_argument("--keep-frames", action="store_true", help="Keep extracted frames dir")
    args = p.parse_args()

    video = args.video if args.video.is_absolute() else ROOT / args.video
    if not video.exists():
        print(f"Video not found: {video}", file=sys.stderr)
        sys.exit(1)

    duration = probe_duration(video)
    start = 0.0 if args.start is None else args.start
    end = duration if args.end is None else args.end

    w, h = probe_size(video)
    print(f"Video: {video.name} | {w}x{h} | {duration:.1f}s ({format_ts(duration)})")
    print(f"Grid: {args.rows}x{args.cols} = {args.rows * args.cols} frames | window {format_ts(start)} → {format_ts(end)}")

    out = args.out if args.out.is_absolute() else ROOT / args.out
    build_grid(video, out, args.rows, args.cols, start, end, args.thumb_w, args.keep_frames)
    print(f"Wrote {out}")
    print(f"Manifest {out.with_suffix('.json')}")


if __name__ == "__main__":
    main()
