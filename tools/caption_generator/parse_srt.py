#!/usr/bin/env python3
"""
parse_srt.py — Parse an SRT file into JSON format compatible with
the Remotion Subtitles component (SubtitleSegment[]).

Output JSON shape (matches my-video/src/Subtitles.tsx):
  [
    { "id": 1, "start": 0.2, "end": 2.381, "text": "Everyone is talking about AI…" },
    ...
  ]

Usage:
    python3 parse_srt.py <input.srt>
    python3 parse_srt.py <input.srt> --out <output.json>
    python3 parse_srt.py <input.srt> --print         # just print, don't save
    python3 parse_srt.py <input.srt> --merge 3       # merge every 3 segments into one

Examples:
    python3 parse_srt.py ../../raw_videos/India_AI_caption.srt
    python3 parse_srt.py ../../raw_videos/India_AI_caption.srt --out ../../projects/india_ai/subtitles.json
    python3 parse_srt.py ../../raw_videos/India_AI_caption.srt --merge 2 --print
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ── Timecode parser ──────────────────────────────────────────────────────────
def tc_to_seconds(tc: str) -> float:
    """Convert SRT timecode '00:00:02,381' to seconds (float)."""
    tc = tc.strip().replace(",", ".")
    parts = tc.split(":")
    h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
    return h * 3600 + m * 60 + s


# ── SRT parser ───────────────────────────────────────────────────────────────
def parse_srt(content: str) -> list[dict]:
    """Parse raw SRT string into list of SubtitleSegment dicts."""
    # Split into blocks separated by blank lines
    blocks = re.split(r"\n\s*\n", content.strip())
    segments = []

    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue

        # Line 0: index number
        try:
            seg_id = int(lines[0])
        except ValueError:
            continue

        # Line 1: timecode range  "00:00:00,200 --> 00:00:02,381"
        tc_match = re.match(
            r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})",
            lines[1],
        )
        if not tc_match:
            continue

        start = tc_to_seconds(tc_match.group(1))
        end = tc_to_seconds(tc_match.group(2))

        # Lines 2+: subtitle text (may span multiple lines)
        text = " ".join(lines[2:])

        segments.append({"id": seg_id, "start": round(start, 3), "end": round(end, 3), "text": text})

    return segments


# ── Merge helper ─────────────────────────────────────────────────────────────
def merge_segments(segments: list[dict], every: int) -> list[dict]:
    """
    Merge every N consecutive SRT segments into one.
    Useful for short caption bursts that should display together.
    """
    if every <= 1:
        return segments

    merged = []
    for i in range(0, len(segments), every):
        chunk = segments[i : i + every]
        merged.append({
            "id": i // every + 1,
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
            "text": " ".join(s["text"] for s in chunk),
        })
    return merged


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Convert SRT subtitle file to Remotion SubtitleSegment JSON"
    )
    parser.add_argument("input", help="Path to input .srt file")
    parser.add_argument(
        "--out", "-o", default=None,
        help="Output JSON path (default: same name as input with .json extension)",
    )
    parser.add_argument(
        "--print", "-p", action="store_true",
        help="Print JSON to stdout instead of saving to file",
    )
    parser.add_argument(
        "--merge", "-m", type=int, default=1,
        help="Merge every N segments into one (default: 1 = no merging)",
    )
    args = parser.parse_args()

    srt_path = Path(args.input)
    if not srt_path.exists():
        print(f"[ERROR] File not found: {srt_path}", file=sys.stderr)
        sys.exit(1)

    content = srt_path.read_text(encoding="utf-8-sig")  # utf-8-sig strips BOM if present
    segments = parse_srt(content)

    if not segments:
        print("[ERROR] No segments parsed — check the SRT file format.", file=sys.stderr)
        sys.exit(1)

    if args.merge > 1:
        segments = merge_segments(segments, args.merge)

    output = json.dumps(segments, indent=2, ensure_ascii=False)

    if args.print:
        print(output)
        return

    out_path = Path(args.out) if args.out else srt_path.with_suffix(".json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")

    print(f"[parse_srt] {len(segments)} segment(s) written to {out_path}")
    print(f"[parse_srt] Duration: {segments[0]['start']:.2f}s → {segments[-1]['end']:.2f}s")


if __name__ == "__main__":
    main()
