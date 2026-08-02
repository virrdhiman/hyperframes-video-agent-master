#!/usr/bin/env python3
"""
elevenlabs_transcribe.py — Transcribe audio using ElevenLabs Speech-to-Text API

Reads the API key from the project `.env` file. Supported env var names:
    - ELEVENLABS_API_KEY
    - XI_API_KEY

Usage:
    python3 tools/transcription/elevenlabs_transcribe.py <input_audio> [options]

Examples:
    python3 tools/transcription/elevenlabs_transcribe.py public/diogenes/voiceover_v2.mp3
    python3 tools/transcription/elevenlabs_transcribe.py public/diogenes/voiceover_v2.mp3 --out projects/diogenes_minimalism/subtitles_v2.json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
import urllib.request
from urllib.error import HTTPError, URLError

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_API_BASE = "https://api.elevenlabs.io"
COMMON_TIMEOUT_SECS = 120

SUPPORTED_API_KEY_NAMES = (
    "ELEVENLABS_API_KEY",
    "XI_API_KEY",
)

# ── Env loading ───────────────────────────────────────────────────────────────
def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value and ((value[0] == value[-1]) and value[0] in {"'", '"'}):
            value = value[1:-1]
        os.environ.setdefault(key, value)

def get_api_key() -> str:
    load_env_file(ENV_FILE)
    for env_name in SUPPORTED_API_KEY_NAMES:
        value = os.getenv(env_name)
        if value:
            return value
    print(f"[ERROR] ElevenLabs API key not found in {ENV_FILE}.", file=sys.stderr)
    sys.exit(1)

def get_api_base() -> str:
    load_env_file(ENV_FILE)
    return os.getenv("ELEVENLABS_API_BASE", DEFAULT_API_BASE).rstrip("/")

# ── Multipart Form Data Helper ───────────────────────────────────────────────
def encode_multipart_formdata(fields: dict, files: dict) -> tuple[bytes, str]:
    import uuid
    boundary = uuid.uuid4().hex
    lines = []
    
    for key, value in fields.items():
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{key}"')
        lines.append('')
        lines.append(str(value))
        
    for key, (filename, file_content) in files.items():
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"')
        lines.append('Content-Type: application/octet-stream')
        lines.append('')
        lines.append(file_content.decode('latin1')) # Hack to handle binary in string list
        
    lines.append(f"--{boundary}--")
    lines.append('')
    
    body = '\r\n'.join(lines).encode('latin1')
    content_type = f'multipart/form-data; boundary={boundary}'
    
    return body, content_type

# ── API operations ────────────────────────────────────────────────────────────
def transcribe_audio(audio_path: Path, model_id: str = "scribe_v1") -> dict:
    url = f"{get_api_base()}/v1/speech-to-text"
    
    with open(audio_path, 'rb') as f:
        file_content = f.read()
        
    fields = {"model_id": model_id}
    files = {"file": (audio_path.name, file_content)}
    
    body, content_type = encode_multipart_formdata(fields, files)
    
    headers = {
        "xi-api-key": get_api_key(),
        "Content-Type": content_type,
    }
    
    request = urllib.request.Request(url=url, data=body, headers=headers, method="POST")
    
    try:
        print(f"Transcribing {audio_path.name} using ElevenLabs ({model_id})...")
        with urllib.request.urlopen(request, timeout=COMMON_TIMEOUT_SECS) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        print(f"[ERROR] API request failed ({exc.code}): {exc.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except URLError as exc:
        print(f"[ERROR] Network error: {exc}", file=sys.stderr)
        sys.exit(1)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using ElevenLabs API")
    parser.add_argument("input", help="Path to input audio file")
    parser.add_argument("--out", "-o", default=None, help="Output JSON path")
    parser.add_argument("--model", default="scribe_v1", help="Model ID (default: scribe_v1)")
    args = parser.parse_args()

    audio_path = Path(args.input)
    if not audio_path.exists():
        print(f"[ERROR] File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    result = transcribe_audio(audio_path, args.model)
    
    # Format to match our word-level timestamp JSON
    words = []
    if "words" in result:
        for w in result["words"]:
            if w["type"] == "word":
                words.append({
                    "text": w["text"],
                    "start": w["start"],
                    "end": w["end"]
                })
    
    output = json.dumps(words, indent=2, ensure_ascii=False)
    
    out_path = Path(args.out) if args.out else audio_path.with_suffix(".json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    
    print(f"Done! {len(words)} words written to {out_path}")

if __name__ == "__main__":
    main()
