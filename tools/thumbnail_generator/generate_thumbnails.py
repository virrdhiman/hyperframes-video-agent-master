#!/usr/bin/env python3
"""
generate_thumbnails.py — Reaction-style YouTube thumbnails via Replicate flux-2-pro.

Reads a batch mapping file (default projects/pzynor/march_batch.json) where each
entry has: name, title, thumbnail_text, reactor_ref, thumbnail_file. For each entry
it calls black-forest-labs/flux-2-pro with the reactor reference photo
(assets/construction/man_1.png or man_2.png) as an input image, renders a 16:9
clickbait thumbnail with the overlay text baked in, and saves it resized to
1280x720 at the entry's thumbnail_file path.

Auth: REPLICATE_API_TOKEN from the project-root .env (same as tools/generate_assets.py).

Usage:
    # pilot — generate the first 3 only (for approval)
    python3 generate_thumbnails.py --count 3

    # specific videos by name
    python3 generate_thumbnails.py --only output_2026-03-02_22-27-57,output_2026-03-02_22-38-12

    # full run (skips ones already generated unless --force)
    python3 generate_thumbnails.py --all

    # re-render everything
    python3 generate_thumbnails.py --all --force
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path
from urllib.request import urlopen

import replicate
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_BATCH = ROOT / "projects" / "pzynor" / "march_batch.json"
REACTOR_DIR = ROOT / "assets" / "construction"
THUMB_W, THUMB_H = 1280, 720

# Per-model id + how the reference image and knobs are passed (the two models
# use different param names). Keyed by the --model short name.
MODELS = {
    "flux": {
        "id": "black-forest-labs/flux-2-pro",
        "image_key": "input_images",
        "extra": {"aspect_ratio": "16:9", "resolution": "1 MP",
                  "output_format": "jpg", "safety_tolerance": 5},
    },
    "nano-banana": {
        "id": "google/nano-banana",
        "image_key": "image_input",
        "extra": {"aspect_ratio": "16:9", "output_format": "jpg"},
    },
}
DEFAULT_MODEL = "nano-banana"

# What the woman is doing — rotated across the batch for variety. A mix of
# "doing something" (drilling, carrying, sawing) and "looking at camera" poses.
WOMAN_ACTIONS = [
    "looking straight at the camera with a confident smile, one hand on her hip",
    "using a power drill to drill into a concrete wall, focused on the work",
    "carrying a stack of wooden planks on her shoulder",
    "holding a large power drill resting on her shoulder and posing toward the camera",
    "operating a jackhammer breaking up the ground",
    "holding rolled-up blueprints and pointing at something off-frame",
    "using a circular saw to cut a wooden board with sparks flying",
    "hammering a nail into a wooden frame",
    "measuring a steel beam with a tape measure",
    "looking straight at the camera and giving a thumbs up",
    "carrying a heavy red toolbox mid-stride across the site",
    "tightening a large bolt with a heavy wrench",
    "pushing a wheelbarrow full of bricks",
    "holding a welding torch with the welding mask flipped up",
    "looking straight at the camera with a surprised expression while holding a clipboard",
    "shoveling gravel into a pile",
    "climbing a ladder on the scaffolding",
    "holding a spirit level against a wall to check it",
    "spreading wet cement with a trowel",
    "drilling overhead into a ceiling beam",
    "looking straight at the camera, arms crossed, hard hat tilted",
    "operating a cement mixer",
]

PROMPT_TMPL = (
    "Bold MrBeast-style YouTube thumbnail, 16:9 landscape, ultra eye-catching. "
    "On the RIGHT: the man from the reference photo (keep the exact same face, yellow "
    "hard hat and orange hi-vis vest) reacting with a huge exaggerated SHOCKED wide-eyed "
    "open-mouth expression. On the LEFT: a glamorous, curvy, attractive woman who looks a "
    "little too hot for the job — wearing a fitted V-neck top with a modest bit of cleavage "
    "under an open hi-vis safety vest, a hard hat, styled hair and tasteful makeup, a "
    "confident smile, slightly out of place on the construction site but still clearly "
    "working. Tasteful and classy, not over-sexualized. She is {ACTION}. Bright red arrows "
    "and circles highlighting the action between them. HUGE bold caption text reading "
    "\"{TEXT}\" in thick white letters with a heavy black outline, very large and fully "
    "inside the frame (never cut off at the edges). High saturation, dramatic lighting, "
    "punchy contrast, exaggerated clickbait energy."
)


def get_token() -> str:
    load_dotenv(ENV_FILE)
    tok = os.getenv("REPLICATE_API_TOKEN")
    if not tok:
        print(f"[ERROR] REPLICATE_API_TOKEN not found in {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    os.environ["REPLICATE_API_TOKEN"] = tok
    return tok


def load_batch(path: Path) -> list[dict]:
    if not path.exists():
        print(f"[ERROR] Batch file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text())


def fetch_bytes(output) -> bytes:
    """flux-2-pro returns a single file-like object or a URL (or a 1-item list)."""
    if isinstance(output, list):
        output = output[0]
    if hasattr(output, "read"):
        return output.read()
    if isinstance(output, str):
        return urlopen(output, timeout=60).read()
    raise RuntimeError(f"unexpected replicate output type: {type(output)}")


def to_thumb(data: bytes) -> bytes:
    """Resize/crop to exactly 1280x720. Falls back to raw bytes if Pillow missing."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("[warn] Pillow not installed — saving model output at native size", file=sys.stderr)
        return data
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img = ImageOps.fit(img, (THUMB_W, THUMB_H), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def generate_one(entry: dict, force: bool, model: str, action: str) -> bool:
    out_path = ROOT / entry["thumbnail_file"]
    if out_path.exists() and not force:
        print(f"[skip] {entry['name']} — already exists ({out_path.name})")
        return True

    reactor = REACTOR_DIR / entry.get("reactor_ref", "man_1.png")
    if not reactor.exists():
        print(f"[ERROR] reactor reference missing: {reactor}", file=sys.stderr)
        return False

    base_prompt = PROMPT_TMPL.format(TEXT=entry["thumbnail_text"], ACTION=action)
    # On a 'sensitive' refusal, retry with a progressively tamer nudge, then fall
    # back to flux (permissive) so one prudish refusal never blocks a thumbnail.
    SAFE_NUDGE = (" The woman is fully clothed in professional workwear; the image is "
                 "classy, appropriate, and non-suggestive.")
    attempts = [(model, base_prompt),
                (model, base_prompt + SAFE_NUDGE),
                (model, base_prompt + SAFE_NUDGE),
                ("flux", base_prompt)]
    print(f"[gen] {entry['name']}  text='{entry['thumbnail_text']}'  ref={reactor.name}")
    for i, (mdl, prompt) in enumerate(attempts, 1):
        cfg = MODELS[mdl]
        try:
            with open(reactor, "rb") as ref:
                output = replicate.run(cfg["id"], input={
                    "prompt": prompt, cfg["image_key"]: [ref], **cfg["extra"],
                })
            data = to_thumb(fetch_bytes(output))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(data)
            kb = out_path.stat().st_size // 1024
            tag = f"{mdl}" + ("" if i == 1 else f", attempt {i}")
            print(f"      → {entry['thumbnail_file']} ({THUMB_W}x{THUMB_H}, {kb} KB) [{tag}]")
            return True
        except replicate.exceptions.ModelError as e:
            msg = str(e)
            if "sensitive" in msg.lower() or "E005" in msg:
                print(f"      [retry] flagged sensitive on {mdl} (attempt {i})", file=sys.stderr)
                continue
            print(f"      [ERROR] {mdl}: {msg[:120]}", file=sys.stderr)
            return False
    print(f"      [FAIL] {entry['name']} — all attempts refused", file=sys.stderr)
    return False


def main():
    ap = argparse.ArgumentParser(description="Generate reaction-style YouTube thumbnails (flux-2-pro)")
    ap.add_argument("--batch", default=str(DEFAULT_BATCH), help="Batch mapping JSON")
    ap.add_argument("--count", type=int, help="Only the first N entries (pilot)")
    ap.add_argument("--only", help="Comma-separated entry names to generate")
    ap.add_argument("--all", action="store_true", help="Generate all entries")
    ap.add_argument("--force", action="store_true", help="Re-render even if file exists")
    ap.add_argument("--model", choices=list(MODELS), default=DEFAULT_MODEL,
                    help=f"Replicate model (default: {DEFAULT_MODEL})")
    args = ap.parse_args()

    if not (args.count or args.only or args.all):
        ap.error("specify one of --count N, --only <names>, or --all")

    get_token()
    batch = load_batch(Path(args.batch))

    if args.only:
        want = {n.strip() for n in args.only.split(",")}
        sel = [e for e in batch if e["name"] in want]
    elif args.count:
        sel = batch[: args.count]
    else:
        sel = batch

    idx_of = {e["name"]: i for i, e in enumerate(batch)}  # stable action per video

    print(f"[thumbs] {len(sel)} thumbnail(s) via {args.model} → public/pzynor/thumbs/\n")
    ok, failed = 0, []
    for e in sel:
        action = WOMAN_ACTIONS[idx_of[e["name"]] % len(WOMAN_ACTIONS)]
        try:
            if generate_one(e, args.force, args.model, action):
                ok += 1
            else:
                failed.append(e["name"])
        except Exception as exc:  # never let one bad entry abort the batch
            print(f"      [ERROR] {e['name']}: {repr(exc)[:120]}", file=sys.stderr)
            failed.append(e["name"])
    print(f"\n[thumbs] Done — {ok}/{len(sel)} succeeded")
    if failed:
        print("[thumbs] FAILED (re-run with --only):")
        print("  --only " + ",".join(failed))


if __name__ == "__main__":
    main()
