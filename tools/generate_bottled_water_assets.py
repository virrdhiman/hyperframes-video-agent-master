#!/usr/bin/env python3
"""
Generate all scene illustrations for the Bottled Water video
using Replicate's nano-banana model with the character as style reference.
"""

import os
import sys
import time
from pathlib import Path
from urllib.request import urlopen

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

import replicate

OUT_DIR = ROOT / "public" / "bottled-water"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTER_PATH = ROOT / "replicate-prediction-g6863j6nh9rmy0cxjnfta3n3b4.webp"

STYLE_PREFIX = (
    "Minimalist black-and-white line art illustration, clean vector style, "
    "simple character design with black outlines on white background, "
    "modern cartoon illustration style matching the reference character. "
)

SCENES = [
    {
        "id": "scene_01_hook",
        "prompt": (
            "A bearded man with styled hair wearing a blazer, standing with arms spread wide, "
            "question marks and exclamation marks floating around him. "
            "Large bold text says 'BIGGEST SCAM?' above him. White background."
        ),
    },
    {
        "id": "scene_02_not_crypto",
        "prompt": (
            "Split scene: on the left, a Bitcoin symbol with an X over it. "
            "On the right, a plastic water bottle with a spotlight on it. "
            "The bearded man in the middle pointing at the water bottle. White background."
        ),
    },
    {
        "id": "scene_03_1970s_tap",
        "prompt": (
            "A retro 1970s kitchen scene. A happy person turning on a kitchen faucet with water flowing. "
            "A calendar on the wall shows '1975'. Simple line art, clean, white background."
        ),
    },
    {
        "id": "scene_04_perrier",
        "prompt": (
            "An elegant French person with a beret and scarf, holding up a fancy green glass bottle "
            "with a proud expression. Sparkles and stars around the bottle. "
            "A small French flag in the corner. Line art illustration, white background."
        ),
    },
    {
        "id": "scene_05_everyone_buying",
        "prompt": (
            "A long line of simple cartoon people queuing up eagerly, each holding dollar bills, "
            "all reaching toward a single water bottle on a pedestal. "
            "Price tag shows '$3'. Line art illustration, white background."
        ),
    },
    {
        "id": "scene_06_price_comparison",
        "prompt": (
            "Two items side by side with price tags. Left: a kitchen faucet with tap water, "
            "price tag '$0.004'. Right: a plastic water bottle, price tag '$7.00'. "
            "A large 'VS' between them. Bold text '1750x' below. Clean line art, white background."
        ),
    },
    {
        "id": "scene_07_gasoline",
        "prompt": (
            "A gas pump next to a water bottle. The gas pump has a speech bubble saying '50%' "
            "while the water bottle has one saying '4000%'. "
            "A confused person looking at both. Line art illustration, white background."
        ),
    },
    {
        "id": "scene_08_350billion",
        "prompt": (
            "A massive mountain of money bills and coins with a water bottle sitting on top like a throne. "
            "Bold text '$350 BILLION' above. Small country outlines of Denmark and Singapore below "
            "looking tiny in comparison. Clean line art illustration, white background."
        ),
    },
    {
        "id": "scene_09_taste_test",
        "prompt": (
            "A blindfolded person at a table with two identical glasses of water labeled 'A' and 'B'. "
            "The person is tasting and looking confused with a question mark above their head. "
            "One glass secretly labeled 'tap' and the other 'bottled'. Line art, white background."
        ),
    },
    {
        "id": "scene_10_corporations",
        "prompt": (
            "A man in a business suit sitting behind a desk, rubbing hands together with a mischievous grin. "
            "Behind him, a chart showing profits going up sharply. Water bottles on the desk. "
            "Dollar signs floating around. Clean line art, white background."
        ),
    },
    {
        "id": "scene_11_filtered_tap",
        "prompt": (
            "A simple factory pipeline illustration: water flowing from a regular tap/faucet, "
            "through a basic kitchen filter, then into a fancy plastic bottle with a premium label. "
            "Arrows showing the flow. Text '40%' with an asterisk. Clean line art, white background."
        ),
    },
    {
        "id": "scene_12_same_pipes",
        "prompt": (
            "Underground water pipes connecting a house and a bottled water factory. "
            "Both getting water from the same source. The factory has a '1700x' price tag. "
            "A person looking underground and seeing the pipes, looking shocked. Line art, white background."
        ),
    },
    {
        "id": "scene_13_outro",
        "prompt": (
            "A bearded man with styled hair wearing a blazer, sitting at a modern desk with a laptop, "
            "holding up a fancy water bottle with a smug/sarcastic expression and shrugging. "
            "Text bubble says 'Worth it?' Clean line art illustration, white background."
        ),
    },
]


def generate_scene(scene: dict, character_file) -> Path | None:
    """Generate a single scene image using nano-banana."""
    scene_id = scene["id"]
    out_path = OUT_DIR / f"{scene_id}.jpg"

    if out_path.exists():
        print(f"  [skip] {scene_id} already exists")
        return out_path

    full_prompt = STYLE_PREFIX + scene["prompt"]
    print(f"  [gen] {scene_id}...")
    print(f"        prompt: {scene['prompt'][:80]}...")

    try:
        start = time.time()
        output = replicate.run(
            "google/nano-banana",
            input={
                "prompt": full_prompt,
                "image_input": [character_file],
                "aspect_ratio": "16:9",
                "output_format": "jpg",
            },
        )
        elapsed = time.time() - start
        print(f"        done in {elapsed:.1f}s")

        if hasattr(output, "read"):
            image_bytes = output.read()
        elif isinstance(output, str):
            image_bytes = urlopen(output, timeout=30).read()
        else:
            print(f"  [WARN] Unexpected output type: {type(output)}")
            return None

        with open(out_path, "wb") as f:
            f.write(image_bytes)

        size_kb = out_path.stat().st_size / 1024
        print(f"        saved: {out_path.name} ({size_kb:.0f} KB)")
        return out_path

    except Exception as e:
        print(f"  [ERROR] {scene_id}: {e}", file=sys.stderr)
        return None


def main():
    print(f"[pipeline] Generating {len(SCENES)} scene images")
    print(f"[pipeline] Character: {CHARACTER_PATH.name}")
    print(f"[pipeline] Output: {OUT_DIR}")
    print()

    character_file = open(CHARACTER_PATH, "rb")

    success = 0
    for i, scene in enumerate(SCENES, 1):
        print(f"[{i}/{len(SCENES)}]")
        # Reopen the file for each call since replicate may consume it
        character_file = open(CHARACTER_PATH, "rb")
        result = generate_scene(scene, character_file)
        character_file.close()
        if result:
            success += 1
        print()

    print(f"[pipeline] Done: {success}/{len(SCENES)} images generated")


if __name__ == "__main__":
    main()
