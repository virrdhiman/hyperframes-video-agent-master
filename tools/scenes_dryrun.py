#!/usr/bin/env python3
"""
scenes_dryrun.py — preview prompts and estimated cost before generating.

Read a scenes.json file and print, for each scene:
  - the full prompt that would be sent (style_prefix + scene.prompt)
  - the model that would be invoked
  - whether the output file already exists (would be skipped)
  - an estimated cost

Then a summary: total scenes, how many already exist, estimated $ to generate
the missing ones.

Usage:
    python3 tools/scenes_dryrun.py projects/<slug>/scenes.json
    python3 tools/scenes_dryrun.py projects/<slug>/scenes.json --only s01 s02
    python3 tools/scenes_dryrun.py projects/<slug>/scenes.json --images-only
    python3 tools/scenes_dryrun.py projects/<slug>/scenes.json --no-color

Cost estimates are *approximate* (based on Replicate pricing as of writing).
Set environment variables to override:
    PRICE_NANO_BANANA_USD   default 0.039 per image
    PRICE_WAN22_USD         default 0.20  per video clip
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent

# ── ANSI colors ──────────────────────────────────────────────────────────────

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

def disable_colors() -> None:
    for attr in list(C.__dict__):
        if not attr.startswith("_") and isinstance(getattr(C, attr), str):
            setattr(C, attr, "")


# ── Model registry & pricing ────────────────────────────────────────────────

PRICE_NANO_BANANA = float(os.environ.get("PRICE_NANO_BANANA_USD", "0.039"))
PRICE_WAN22 = float(os.environ.get("PRICE_WAN22_USD", "0.20"))

def estimate_cost(scene_type: str, model: str) -> float:
    """Best-effort per-call cost estimate. Override via env vars."""
    if scene_type == "image":
        if "nano-banana" in model:
            return PRICE_NANO_BANANA
        return PRICE_NANO_BANANA  # treat unknown image models as same ballpark
    if scene_type == "video":
        if "wan-2.2" in model or "wan2.2" in model:
            return PRICE_WAN22
        return PRICE_WAN22
    return 0.0


# ── Path resolution (mirrors generate_assets.py conventions) ────────────────

def resolve_path(rel: str) -> Path:
    p = Path(rel)
    return p if p.is_absolute() else ROOT / p


def output_path_for(scene: dict, output_dir: Path, image_ext: str = "jpg") -> Path:
    sid = scene["id"]
    if scene["type"] == "video":
        return output_dir / f"{sid}.mp4"
    return output_dir / f"{sid}.{image_ext}"


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenes_json", help="Path to projects/<slug>/scenes.json")
    ap.add_argument("--only", nargs="+", help="Only show these scene IDs")
    ap.add_argument("--images-only", action="store_true")
    ap.add_argument("--videos-only", action="store_true")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--no-prompts", action="store_true",
                    help="Hide prompts, just show summary")
    args = ap.parse_args()

    if args.no_color or not sys.stdout.isatty():
        disable_colors()

    cfg_path = resolve_path(args.scenes_json)
    if not cfg_path.exists():
        print(f"[ERROR] not found: {cfg_path}", file=sys.stderr)
        return 1

    with open(cfg_path) as f:
        cfg: dict[str, Any] = json.load(f)

    project = cfg.get("project", "?")
    output_dir = resolve_path(cfg["output_dir"])
    style_prefix = cfg.get("style_prefix", "").strip()
    image_model = cfg.get("image_model", "google/nano-banana")
    video_model = cfg.get("video_model", "wan-video/wan-2.2-i2v-fast")
    image_ext = cfg.get("image_defaults", {}).get("output_format", "jpg")
    workers = cfg.get("parallel_workers", 4)

    print(f"{C.BOLD}{C.CYAN}╔══ scenes.json dry-run ══════════════════════════════════════════════════════╗{C.RESET}")
    print(f"  project:      {C.BOLD}{project}{C.RESET}")
    print(f"  output_dir:   {output_dir}")
    print(f"  image_model:  {image_model}")
    print(f"  video_model:  {video_model}")
    print(f"  workers:      {workers}")
    if style_prefix:
        print(f"  style_prefix: {C.DIM}{style_prefix[:120]}{'…' if len(style_prefix) > 120 else ''}{C.RESET}")
    print(f"{C.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{C.RESET}\n")

    scenes = cfg.get("scenes", [])
    if args.only:
        scenes = [s for s in scenes if s["id"] in args.only]
    if args.images_only:
        scenes = [s for s in scenes if s["type"] == "image"]
    if args.videos_only:
        scenes = [s for s in scenes if s["type"] == "video"]

    n_total = len(scenes)
    n_existing = 0
    n_to_generate = 0
    cost_existing = 0.0
    cost_to_generate = 0.0

    by_type: dict[str, dict[str, int]] = {
        "image": {"total": 0, "exists": 0},
        "video": {"total": 0, "exists": 0},
    }

    for scene in scenes:
        sid = scene["id"]
        stype = scene["type"]
        model = image_model if stype == "image" else video_model
        cost = estimate_cost(stype, model)
        out = output_path_for(scene, output_dir, image_ext)
        exists = out.exists()

        by_type.setdefault(stype, {"total": 0, "exists": 0})
        by_type[stype]["total"] += 1
        if exists:
            n_existing += 1
            cost_existing += cost
            by_type[stype]["exists"] += 1
            status = f"{C.GREEN}✓ exists{C.RESET}"
        else:
            n_to_generate += 1
            cost_to_generate += cost
            status = f"{C.YELLOW}○ todo  {C.RESET}"

        type_color = C.MAGENTA if stype == "video" else C.BLUE
        type_label = f"{type_color}[{stype:5s}]{C.RESET}"

        if args.no_prompts:
            print(f"  {status} {type_label} {sid}  {C.DIM}(${cost:.3f}){C.RESET}")
            continue

        # Full effective prompt = style_prefix + scene.prompt
        prompt = scene.get("prompt", "")
        full = f"{style_prefix} {prompt}".strip() if style_prefix else prompt
        source = scene.get("source")
        source_str = f"  {C.DIM}← source: {source}{C.RESET}" if source else ""

        print(f"  {status} {type_label} {C.BOLD}{sid}{C.RESET}  {C.DIM}(${cost:.3f}){C.RESET}{source_str}")
        # Wrap prompt at ~110 chars for terminal readability
        wrap = 110
        line = ""
        for word in full.split():
            if len(line) + len(word) + 1 > wrap:
                print(f"      {C.DIM}{line}{C.RESET}")
                line = word
            else:
                line = f"{line} {word}".strip()
        if line:
            print(f"      {C.DIM}{line}{C.RESET}")
        print()

    # Summary
    print(f"{C.BOLD}{C.CYAN}── summary ─────────────────────────────────────────────────────────────────{C.RESET}")
    for stype, counts in by_type.items():
        if counts["total"] == 0:
            continue
        miss = counts["total"] - counts["exists"]
        print(f"  {stype:6s}  {counts['total']:3d} total   {C.GREEN}{counts['exists']:3d} done{C.RESET}   {C.YELLOW}{miss:3d} todo{C.RESET}")
    print()
    print(f"  total scenes:        {n_total}")
    print(f"  already generated:   {C.GREEN}{n_existing}{C.RESET}  ({C.DIM}~${cost_existing:.2f} sunk{C.RESET})")
    print(f"  would generate now:  {C.YELLOW}{n_to_generate}{C.RESET}")
    print(f"  estimated cost:      {C.BOLD}${cost_to_generate:.2f}{C.RESET}  {C.DIM}(approx — set PRICE_NANO_BANANA_USD / PRICE_WAN22_USD to refine){C.RESET}")
    if n_to_generate > 0:
        print()
        print(f"  next: {C.CYAN}python3 tools/generate_assets.py {args.scenes_json}{C.RESET}")
    else:
        print()
        print(f"  {C.GREEN}✓ all scenes already generated.{C.RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
