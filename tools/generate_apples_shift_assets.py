#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
from urllib.request import urlopen

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

import replicate

OUT_DIR = ROOT / "public" / "apples-shift"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STYLE_PREFIX = (
    "Highly realistic, cinematic lighting, photorealistic, professional documentary photography style. "
    "IMPORTANT: Do NOT include any text, labels, numbers, words, or captions in the image. "
)

SCENES = [
    {
        "id": "s01_servers",
        "prompt": (
            "Massive dark server racks glowing with intense blue and neon lights in a vast data center, "
            "ominous scale, intimidating computing power. Clean geometric shapes, high tech."
        ),
    },
    {
        "id": "s02_minimalist_chip",
        "prompt": (
            "A dark, minimalist sleek table with a single glowing futuristic microchip on it. "
            "Sleek stealthy design, depth of field focusing on the intricate details of the chip. Elegant."
        ),
    },
    {
        "id": "s03_siri_orb",
        "prompt": (
            "An abstract luminous sphere with beautiful iridescent pastel colors floating "
            "in a pristine dark space, representing a smart digital assistant. Smooth glassmorphic texture."
        ),
    },
    {
        "id": "s04_ondevice_ai",
        "prompt": (
            "Macro photography of a beautiful futuristic CPU chip glowing softly inside a translucent smartphone frame. "
            "High-tech engineering, elegant Apple-like design, moody dramatic lighting."
        ),
    },
    {
        "id": "s05_lifestyle",
        "prompt": (
            "A person's hand holding a sleek futuristic smartphone that glows softly, resting on a table "
            "in a modern minimalist dark coffee shop. Warm cinematic lighting blending with high-tech coolness, everyday life."
        ),
    }
]

ANIMATIONS = [
    {
        "source_id": "s01_servers",
        "out_name": "anim_servers.mp4",
        "prompt": (
            "Camera slowly pans across the massive dark server racks glowing with intense blue lights. "
            "Lights blink constantly."
        ),
    },
    {
        "source_id": "s02_minimalist_chip",
        "out_name": "anim_minimalist_chip.mp4",
        "prompt": (
            "Subtle camera zoom towards the glowing futuristic microchip, with the glow pulsing softly."
        ),
    },
    {
        "source_id": "s03_siri_orb",
        "out_name": "anim_siri_orb.mp4",
        "prompt": (
            "The iridescent abstract sphere softly changes shape, colors shifting dynamically with a gentle floating motion."
        ),
    },
    {
        "source_id": "s04_ondevice_ai",
        "out_name": "anim_ondevice_ai.mp4",
        "prompt": (
            "The futuristic CPU chip inside the smartphone pulses with light, camera slowly drifts over the details."
        ),
    },
    {
        "source_id": "s05_lifestyle",
        "out_name": "anim_lifestyle.mp4",
        "prompt": (
            "Cinematic subtle movement, people slightly moving in the cafe background, phone glow gently shifting."
        ),
    }
]

def generate_scene(scene: dict):
    scene_id = scene["id"]
    out_path = OUT_DIR / f"{scene_id}.jpg"

    if out_path.exists():
        print(f"  [skip] {scene_id} already exists", flush=True)
        return out_path

    full_prompt = STYLE_PREFIX + scene["prompt"]
    print(f"  [gen] {scene_id}...", flush=True)

    try:
        start = time.time()
        output = replicate.run(
            "google/nano-banana",
            input={
                "prompt": full_prompt,
                "aspect_ratio": "9:16",
                "output_format": "jpg",
            },
        )
        elapsed = time.time() - start

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

def animate_scene(image_path: Path, prompt: str, out_name: str):
    out_path = OUT_DIR / out_name
    if out_path.exists():
        print(f"  [skip] {out_name} already exists", flush=True)
        return out_path

    print(f"  [animate] {out_name}...", flush=True)
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

def main():
    print(f"[pipeline] Phase 1: Generating {len(SCENES)} scene images", flush=True)
    img_success = 0
    for scene in SCENES:
        if generate_scene(scene):
            img_success += 1

    print(f"[pipeline] Phase 1 done: {img_success}/{len(SCENES)} images generated\n", flush=True)

    print(f"[pipeline] Phase 2: Animating {len(ANIMATIONS)} scenes", flush=True)
    anim_success = 0
    for anim in ANIMATIONS:
        source_path = OUT_DIR / f"{anim['source_id']}.jpg"
        if not source_path.exists():
            print(f"  [skip] source image not found: {source_path.name}", flush=True)
            continue
        if animate_scene(source_path, anim["prompt"], anim["out_name"]):
            anim_success += 1

    print(f"[pipeline] COMPLETE: {img_success} images + {anim_success} animations", flush=True)

if __name__ == "__main__":
    main()
