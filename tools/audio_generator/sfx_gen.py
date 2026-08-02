#!/usr/bin/env python3
"""
sfx_gen.py — Generate bespoke sound effects via ElevenLabs sound-generation
(text-to-SFX). Builds a curated, reusable pack in assets/common/sfx/ so every
video has rich, varied transition / riser / impact / UI sounds.

  python3 tools/audio_generator/sfx_gen.py --pack                 # curated set
  python3 tools/audio_generator/sfx_gen.py --prompt "deep cinematic boom" --out assets/common/sfx/boom.mp3 --duration 2
"""
import argparse
import json
import os
import sys
import urllib.request

API = "https://api.elevenlabs.io/v1/sound-generation"


def load_key() -> str:
    # from env or .env
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("XI_API_KEY")
    if not key:
        env = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        if os.path.exists(env):
            for line in open(env):
                line = line.strip()
                if line.startswith(("ELEVENLABS_API_KEY", "XI_API_KEY")) and "=" in line:
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not key:
        sys.exit("ELEVENLABS_API_KEY not found (env or .env)")
    return key


def generate(prompt: str, out: str, duration: float | None, influence: float, key: str) -> None:
    body = {"text": prompt, "prompt_influence": influence}
    if duration:
        body["duration_seconds"] = duration
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print(f"  → {out} ({len(data) / 1024:.0f} KB)")


PACK = [
    ("el_transition_swish", "fast clean whoosh swish transition, short", 1.0),
    ("el_riser", "short rising tension riser sweep building up to a hit", 2.0),
    ("el_glitch", "short digital glitch zap, crisp", 0.8),
    ("el_deep_impact", "deep cinematic impact boom with sub bass", 2.0),
    ("el_sparkle_reveal", "bright magical sparkle shimmer reveal, short", 1.2),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate SFX via ElevenLabs sound-generation.")
    ap.add_argument("--prompt")
    ap.add_argument("--out")
    ap.add_argument("--duration", type=float)
    ap.add_argument("--influence", type=float, default=0.4, help="prompt_influence 0-1 (higher = closer to prompt)")
    ap.add_argument("--pack", action="store_true", help="generate the curated reusable pack into assets/common/sfx/")
    ap.add_argument("--outdir", default="assets/common/sfx")
    a = ap.parse_args()
    key = load_key()

    if a.pack:
        for name, prompt, dur in PACK:
            out = os.path.join(a.outdir, f"{name}.mp3")
            if os.path.exists(out):
                print(f"  skip {out} (exists)")
                continue
            print(f"generating {name}: {prompt}")
            generate(prompt, out, dur, a.influence, key)
        return 0

    if not a.prompt or not a.out:
        sys.exit("provide --prompt and --out, or --pack")
    generate(a.prompt, a.out, a.duration, a.influence, key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
