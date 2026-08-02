#!/usr/bin/env python3
"""Generate Apple Shift BGM + transition SFX via ElevenLabs sound-generation API.

Reads API key from .env (ELEVENLABS_API_KEY or XI_API_KEY).

Usage:
  python3 tools/audio_generator/generate_apple_shift_elevenlabs.py

Writes shared assets:
  - public/common/music/bgm_ambient_loop.mp3
  - public/common/sfx/el_soft_whoosh.mp3
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env"
OUT_MUSIC = ROOT / "public" / "common" / "music"
OUT_SFX = ROOT / "public" / "common" / "sfx"
API = os.getenv("ELEVENLABS_API_BASE", "https://api.elevenlabs.io").rstrip("/")


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip("'\"")
        if k and k not in os.environ:
            os.environ[k] = v


def api_key() -> str:
    load_env()
    for name in ("ELEVENLABS_API_KEY", "XI_API_KEY"):
        v = os.getenv(name)
        if v:
            return v
    print("[ERROR] Set ELEVENLABS_API_KEY or XI_API_KEY in .env", file=sys.stderr)
    sys.exit(1)


def sound_generation(
    text: str,
    out_path: Path,
    *,
    duration_seconds: float | None = None,
    loop: bool = False,
    prompt_influence: float = 0.35,
    output_format: str = "mp3_44100_128",
) -> None:
    key = api_key()
    body: dict = {
        "text": text,
        "prompt_influence": prompt_influence,
        "model_id": "eleven_text_to_sound_v2",
    }
    if duration_seconds is not None:
        body["duration_seconds"] = duration_seconds
    if loop:
        body["loop"] = True

    url = f"{API}/v1/sound-generation?output_format={output_format}"
    req = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
            "Accept": "application/octet-stream",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=120) as resp:
            data = resp.read()
    except HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        raise
    except URLError as e:
        print(f"[ERROR] Network: {e}", file=sys.stderr)
        raise

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    print(f"[OK] {out_path.name} ({len(data) // 1024} KB)")


def main() -> None:
    OUT_MUSIC.mkdir(parents=True, exist_ok=True)
    OUT_SFX.mkdir(parents=True, exist_ok=True)

    sound_generation(
        "Soft minimal ambient tech underscore, wide airy synthesizer pads, very subtle low pulse, "
        "no drums, no melody hooks, calm corporate keynote mood safe under spoken voiceover",
        OUT_MUSIC / "bgm_ambient_loop.mp3",
        duration_seconds=28.0,
        loop=True,
        prompt_influence=0.32,
    )

    sound_generation(
        "Soft cinematic air whoosh transition, gentle airy sweep, subtle high frequency shimmer, "
        "not aggressive, no harsh noise",
        OUT_SFX / "el_soft_whoosh.mp3",
        duration_seconds=2.5,
        loop=False,
        prompt_influence=0.35,
    )


if __name__ == "__main__":
    main()
