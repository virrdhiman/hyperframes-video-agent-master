#!/usr/bin/env python3
"""
generate_bottled_water_v2.py — Generate all scene illustrations for
"The Insane Economics of Bottled Water" v2.

Key changes from v1:
  - NO TEXT in any generated image (all text is added via Remotion)
  - More images per scene for faster visual pacing (~28 images)
  - Some images designed for split-screen comparisons
  - Key scenes will be animated with wan-2.2 i2v separately
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
    "IMPORTANT: Do NOT include any text, labels, numbers, words, or captions in the image. "
)

SCENES = [
    # ── HOOK (0s - 10.5s) ─────────────────────────────────────────────────
    {
        "id": "s01_character_shocked",
        "prompt": (
            "A bearded man with styled hair wearing a blazer, standing with arms spread wide "
            "and a shocked/confused expression. Question marks and exclamation marks floating "
            "around his head. White background."
        ),
    },
    {
        "id": "s02_bitcoin_crossed",
        "prompt": (
            "A large Bitcoin coin symbol with a big red X drawn over it. "
            "Simple, centered on white background."
        ),
    },
    {
        "id": "s03_water_bottle_spotlight",
        "prompt": (
            "A single plastic water bottle standing upright on a pedestal, "
            "with a dramatic spotlight beam shining on it from above. "
            "White background, the bottle is the center of attention."
        ),
    },
    {
        "id": "s04_money_rain",
        "prompt": (
            "Dollar bills and coins raining down from the sky around a plastic water bottle. "
            "The bottle is in the center, money is flying everywhere. White background."
        ),
    },
    {
        "id": "s05_rain_catching",
        "prompt": (
            "A person standing outside in the rain with their mouth open, catching raindrops. "
            "Rain clouds above. The person looks happy. Simple outdoor scene, white background."
        ),
    },

    # ── 1970s CONTEXT (10.5s - 19s) ──────────────────────────────────────
    {
        "id": "s06_1970s_kitchen",
        "prompt": (
            "A retro 1970s style kitchen. A happy bearded man standing at the sink, "
            "turning on the faucet with water flowing out. A vintage calendar on the wall. "
            "Retro cabinets and tiles. Cozy domestic scene."
        ),
    },
    {
        "id": "s07_happy_glass",
        "prompt": (
            "A happy person holding up a glass of clear water and smiling contentedly. "
            "Simple, peaceful scene. White background."
        ),
    },

    # ── PERRIER / FANCY WATER (19s - 35s) ─────────────────────────────────
    {
        "id": "s08_french_perrier",
        "prompt": (
            "An elegant French person wearing a beret and scarf, proudly holding up "
            "a fancy green glass bottle with sparkles and stars around it. "
            "A small French flag in the corner. White background."
        ),
    },
    {
        "id": "s09_bottle_sparkle",
        "prompt": (
            "Close-up of a fancy sparkling water bottle with sparkle effects, stars, "
            "and shine lines radiating from it. The bottle looks premium and luxurious. "
            "White background."
        ),
    },
    {
        "id": "s10_fancy_party",
        "prompt": (
            "A group of sophisticated-looking people at an upscale party, "
            "all holding fancy water bottles and glasses. They look pretentious and pleased. "
            "Minimalist party scene."
        ),
    },
    {
        "id": "s11_queue_buying",
        "prompt": (
            "A long line of eager cartoon people queuing up, each holding dollar bills, "
            "all reaching toward a water bottle at the end of the line. "
            "Everyone looks excited and desperate to buy. White background."
        ),
    },

    # ── PRICE COMPARISON (35s - 48s) — designed for split-screen ─────────
    {
        "id": "s12_tap_faucet",
        "prompt": (
            "A simple kitchen faucet with water flowing from it into a glass below. "
            "Clean, minimal, centered. White background."
        ),
    },
    {
        "id": "s13_bottle_pedestal",
        "prompt": (
            "A fancy plastic water bottle sitting on a golden pedestal under a spotlight. "
            "It looks expensive and overpriced. White background."
        ),
    },
    {
        "id": "s14_mind_blown",
        "prompt": (
            "A bearded man character with a mind-blown expression — eyes wide, hands on head, "
            "with explosion/shock lines radiating from his head. "
            "His jaw is dropped. White background."
        ),
    },

    # ── GASOLINE COMPARISON (48s - 53.5s) — designed for split-screen ────
    {
        "id": "s15_gas_pump",
        "prompt": (
            "A gas station fuel pump, simple illustration. The pump has a nozzle "
            "and looks like a standard petrol/gas pump. White background."
        ),
    },
    {
        "id": "s16_angry_gas",
        "prompt": (
            "An angry person at a gas station, fuming with rage while filling their car. "
            "Steam coming from their ears, clenched fists. White background."
        ),
    },

    # ── $350 BILLION (53.5s - 65s) ───────────────────────────────────────
    {
        "id": "s17_money_mountain",
        "prompt": (
            "A massive mountain made entirely of stacked dollar bills and coins. "
            "A tiny water bottle sits at the very top like a king on a throne. "
            "The mountain is enormous. White background."
        ),
    },
    {
        "id": "s18_globe_tiny",
        "prompt": (
            "A world globe/map with tiny country outlines. Some small countries "
            "are highlighted and look very tiny compared to a huge water bottle "
            "towering over them. White background."
        ),
    },
    {
        "id": "s19_water_splash_dramatic",
        "prompt": (
            "A dramatic splash of water erupting upward like a fountain or geyser. "
            "Dynamic motion, water droplets flying everywhere. "
            "Clean, dramatic composition. White background."
        ),
    },

    # ── TASTE TEST (65s - 77s) — will animate with wan-2.2 ───────────────
    {
        "id": "s20_blindfold_taste",
        "prompt": (
            "A blindfolded person sitting at a table with two identical glasses of water. "
            "The person is tasting from one glass with a focused expression. "
            "Simple table setup. White background."
        ),
    },
    {
        "id": "s21_confused_tasting",
        "prompt": (
            "A person looking confused and puzzled while tasting water from a glass. "
            "A big question mark floats above their head. They can't decide. White background."
        ),
    },
    {
        "id": "s22_trophy_tap",
        "prompt": (
            "A kitchen faucet/tap wearing a gold winner's medal and standing on a podium, "
            "looking victorious. A fancy water bottle standing next to it looking sad and defeated "
            "on a lower podium spot. White background."
        ),
    },

    # ── CORPORATIONS (77s - 82s) ─────────────────────────────────────────
    {
        "id": "s23_corporate_scheming",
        "prompt": (
            "A man in a business suit sitting behind a large desk, rubbing his hands together "
            "with a mischievous evil grin. A profit chart going up sharply behind him. "
            "Stacks of money on the desk. White background."
        ),
    },

    # ── 40% FILTERED TAP (82s - 89s) — will animate with wan-2.2 ────────
    {
        "id": "s24_factory_pipeline",
        "prompt": (
            "A simple factory assembly line illustration. On the left a regular tap/faucet "
            "with water flowing. In the middle a basic water filter. On the right, "
            "a conveyor belt with plastic water bottles being filled. "
            "Arrows showing the flow direction. White background."
        ),
    },

    # ── SAME PIPES (89s - 96.5s) ─────────────────────────────────────────
    {
        "id": "s25_underground_pipes",
        "prompt": (
            "A cross-section view showing underground water pipes. On the left, "
            "a house connected to the pipe. On the right, a factory also connected "
            "to the exact same pipe. Both getting identical water. White background."
        ),
    },
    {
        "id": "s26_filter_simple",
        "prompt": (
            "A simple water filter device with water going in from one side "
            "and coming out the other side looking exactly the same. "
            "Very basic, nothing special. White background."
        ),
    },

    # ── OUTRO (96.5s - 101.4s) ───────────────────────────────────────────
    {
        "id": "s27_character_desk_shrug",
        "prompt": (
            "A bearded man with styled hair wearing a blazer, sitting at a modern desk "
            "with a laptop. He's holding a fancy water bottle in one hand and shrugging "
            "with a sarcastic smirk. White background."
        ),
    },
    {
        "id": "s28_character_wave",
        "prompt": (
            "A bearded man with styled hair wearing a blazer, waving goodbye "
            "with a friendly smile. Simple, clean pose. White background."
        ),
    },
]


def generate_scene(scene: dict, character_path: Path) -> Path | None:
    scene_id = scene["id"]
    out_path = OUT_DIR / f"{scene_id}.jpg"

    if out_path.exists():
        print(f"  [skip] {scene_id} already exists", flush=True)
        return out_path

    full_prompt = STYLE_PREFIX + scene["prompt"]
    print(f"  [gen] {scene_id}...", flush=True)
    print(f"        prompt: {scene['prompt'][:80]}...", flush=True)

    try:
        start = time.time()
        character_file = open(character_path, "rb")
        output = replicate.run(
            "google/nano-banana",
            input={
                "prompt": full_prompt,
                "image_input": [character_file],
                "aspect_ratio": "16:9",
                "output_format": "jpg",
            },
        )
        character_file.close()
        elapsed = time.time() - start
        print(f"        done in {elapsed:.1f}s", flush=True)

        if hasattr(output, "read"):
            image_bytes = output.read()
        elif isinstance(output, str):
            image_bytes = urlopen(output, timeout=30).read()
        else:
            print(f"  [WARN] Unexpected output type: {type(output)}", flush=True)
            return None

        with open(out_path, "wb") as f:
            f.write(image_bytes)

        size_kb = out_path.stat().st_size / 1024
        print(f"        saved: {out_path.name} ({size_kb:.0f} KB)", flush=True)
        return out_path

    except Exception as e:
        print(f"  [ERROR] {scene_id}: {e}", file=sys.stderr, flush=True)
        return None


def animate_scene(image_path: Path, prompt: str, out_name: str) -> Path | None:
    """Animate a static image using wan-2.2 i2v."""
    out_path = OUT_DIR / out_name
    if out_path.exists():
        print(f"  [skip] {out_name} already exists", flush=True)
        return out_path

    print(f"  [animate] {out_name}...", flush=True)
    print(f"        prompt: {prompt[:80]}...", flush=True)

    try:
        start = time.time()
        output = replicate.run(
            "wan-video/wan-2.2-i2v-fast",
            input={
                "image": open(image_path, "rb"),
                "prompt": prompt,
            },
        )
        elapsed = time.time() - start
        print(f"        done in {elapsed:.1f}s", flush=True)

        if hasattr(output, "read"):
            video_bytes = output.read()
        elif isinstance(output, str):
            video_bytes = urlopen(output, timeout=60).read()
        else:
            print(f"  [WARN] Unexpected output type: {type(output)}", flush=True)
            return None

        with open(out_path, "wb") as f:
            f.write(video_bytes)

        size_kb = out_path.stat().st_size / 1024
        print(f"        saved: {out_name} ({size_kb:.0f} KB)", flush=True)
        return out_path

    except Exception as e:
        print(f"  [ERROR] animate {out_name}: {e}", file=sys.stderr, flush=True)
        return None


ANIMATIONS = [
    {
        "source_id": "s17_money_mountain",
        "out_name": "anim_money_mountain.mp4",
        "prompt": (
            "Camera slowly zooms into a massive mountain of money with a water bottle "
            "sitting on top. Bills gently flutter in the wind. Dramatic reveal."
        ),
    },
    {
        "source_id": "s20_blindfold_taste",
        "out_name": "anim_taste_test.mp4",
        "prompt": (
            "A blindfolded person slowly tastes water from a glass, looks confused, "
            "puts it down, picks up another glass. Subtle head movements and expressions."
        ),
    },
    {
        "source_id": "s24_factory_pipeline",
        "out_name": "anim_factory_pipeline.mp4",
        "prompt": (
            "Water flows from a tap through a filter and into plastic bottles on a conveyor belt. "
            "Smooth flowing animation showing the pipeline process left to right."
        ),
    },
]


def main():
    print(f"[pipeline] Phase 1: Generating {len(SCENES)} scene images (no text)", flush=True)
    print(f"[pipeline] Character: {CHARACTER_PATH.name}", flush=True)
    print(f"[pipeline] Output: {OUT_DIR}", flush=True)
    print(flush=True)

    img_success = 0
    for i, scene in enumerate(SCENES, 1):
        print(f"[{i}/{len(SCENES)}]", flush=True)
        result = generate_scene(scene, CHARACTER_PATH)
        if result:
            img_success += 1
        print(flush=True)

    print(f"[pipeline] Phase 1 done: {img_success}/{len(SCENES)} images generated", flush=True)
    print(flush=True)

    # Phase 2: Animate key scenes
    print(f"[pipeline] Phase 2: Animating {len(ANIMATIONS)} scenes with wan-2.2", flush=True)
    print(flush=True)

    anim_success = 0
    for i, anim in enumerate(ANIMATIONS, 1):
        print(f"[anim {i}/{len(ANIMATIONS)}]", flush=True)
        source_path = OUT_DIR / f"{anim['source_id']}.jpg"
        if not source_path.exists():
            print(f"  [skip] source image not found: {source_path.name}", flush=True)
            continue
        result = animate_scene(source_path, anim["prompt"], anim["out_name"])
        if result:
            anim_success += 1
        print(flush=True)

    print(f"[pipeline] Phase 2 done: {anim_success}/{len(ANIMATIONS)} animations generated", flush=True)
    print(flush=True)
    print(f"[pipeline] COMPLETE: {img_success} images + {anim_success} animations", flush=True)


if __name__ == "__main__":
    main()
