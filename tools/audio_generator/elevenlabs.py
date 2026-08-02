#!/usr/bin/env python3
from __future__ import annotations
"""
elevenlabs.py — Search, explore, and generate audio with the ElevenLabs API.

Reads the API key from the project `.env` file. Supported env var names:
    - ELEVENLABS_API_KEY
    - XI_API_KEY

Usage:
    python3 tools/audio_generator/elevenlabs.py models [options]
    python3 tools/audio_generator/elevenlabs.py voices [options]
    python3 tools/audio_generator/elevenlabs.py shared-voices [options]
    python3 tools/audio_generator/elevenlabs.py tts --voice-id <id> --text "Hello"

Examples:
    # List available TTS models
    python3 tools/audio_generator/elevenlabs.py models --tts-only

    # Search voices in your account/workspace
    python3 tools/audio_generator/elevenlabs.py voices --query "narrator" --limit 20

    # Explore public/shared voices
    python3 tools/audio_generator/elevenlabs.py shared-voices --query "calm female" --language en

    # Generate speech and save it under assets/audio/
    python3 tools/audio_generator/elevenlabs.py tts \
      --voice-id JBFqnCBsd6RMkjVDRZzb \
      --text "The first move is what sets everything in motion."

    # Generate speech from a text file with voice settings
    python3 tools/audio_generator/elevenlabs.py tts \
      --voice-id JBFqnCBsd6RMkjVDRZzb \
      --text-file projects/demo/script.txt \
      --model eleven_multilingual_v2 \
      --stability 0.45 \
      --similarity-boost 0.8 \
      --style 0.2 \
      --speed 1.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_OUT = ROOT / "assets" / "audio"
DEFAULT_API_BASE = "https://api.elevenlabs.io"
COMMON_TIMEOUT_SECS = 60

SUPPORTED_API_KEY_NAMES = (
    "ELEVENLABS_API_KEY",
    "XI_API_KEY",
)


# ── Env loading ───────────────────────────────────────────────────────────────
def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs from a .env file without extra dependencies."""
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

    expected = ", ".join(SUPPORTED_API_KEY_NAMES)
    print(
        f"[ERROR] ElevenLabs API key not found in {ENV_FILE}. "
        f"Set one of: {expected}",
        file=sys.stderr,
    )
    sys.exit(1)


def get_api_base() -> str:
    load_env_file(ENV_FILE)
    return os.getenv("ELEVENLABS_API_BASE", DEFAULT_API_BASE).rstrip("/")


# ── HTTP helpers ──────────────────────────────────────────────────────────────
def build_url(path: str, query: dict[str, Any] | None = None) -> str:
    base = get_api_base()
    url = f"{base}{path}"
    if query:
        filtered = {k: v for k, v in query.items() if v is not None and v != ""}
        if filtered:
            url = f"{url}?{urlencode(filtered, doseq=True)}"
    return url


def _read_error_message(exc: HTTPError) -> str:
    try:
        raw = exc.read().decode("utf-8", errors="replace")
    except Exception:
        return str(exc)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw.strip() or str(exc)

    if isinstance(payload, dict):
        detail = payload.get("detail")
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list):
            return json.dumps(detail, ensure_ascii=True)
        message = payload.get("message")
        if isinstance(message, str):
            return message

    return raw.strip() or str(exc)


def request_json(
    method: str,
    path: str,
    *,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = COMMON_TIMEOUT_SECS,
) -> Any:
    url = build_url(path, query)
    payload: bytes | None = None

    headers = {
        "xi-api-key": get_api_key(),
        "Accept": "application/json",
        "User-Agent": "retrofit-ai-elevenlabs-tool/1.0",
    }

    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url=url, data=payload, headers=headers, method=method.upper())

    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        print(
            f"[ERROR] ElevenLabs API request failed ({exc.code}) for {path}: "
            f"{_read_error_message(exc)}",
            file=sys.stderr,
        )
        sys.exit(1)
    except URLError as exc:
        print(f"[ERROR] Network error while calling ElevenLabs: {exc}", file=sys.stderr)
        sys.exit(1)


def request_bytes(
    method: str,
    path: str,
    *,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = COMMON_TIMEOUT_SECS,
) -> bytes:
    url = build_url(path, query)
    payload: bytes | None = None

    headers = {
        "xi-api-key": get_api_key(),
        "Accept": "application/octet-stream",
        "User-Agent": "retrofit-ai-elevenlabs-tool/1.0",
    }

    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url=url, data=payload, headers=headers, method=method.upper())

    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    except HTTPError as exc:
        print(
            f"[ERROR] ElevenLabs audio generation failed ({exc.code}) for {path}: "
            f"{_read_error_message(exc)}",
            file=sys.stderr,
        )
        sys.exit(1)
    except URLError as exc:
        print(f"[ERROR] Network error while calling ElevenLabs: {exc}", file=sys.stderr)
        sys.exit(1)


# ── Display helpers ───────────────────────────────────────────────────────────
def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=True))


def shorten(text: str | None, max_len: int) -> str:
    if not text:
        return ""
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    return f"{clean[: max_len - 3]}..."


def truthy_mark(value: Any) -> str:
    return "yes" if value else "no"


def format_languages(model: dict[str, Any]) -> str:
    languages = model.get("languages") or []
    names = [lang.get("name") for lang in languages if isinstance(lang, dict) and lang.get("name")]
    return ", ".join(names[:3]) + ("..." if len(names) > 3 else "")


def print_models(models: list[dict[str, Any]]) -> None:
    print(f"\n{'MODEL ID':<28} {'TTS':<5} {'STYLE':<7} {'BOOST':<7} NAME")
    print("-" * 96)
    for model in models:
        print(
            f"{model.get('model_id', ''):<28} "
            f"{truthy_mark(model.get('can_do_text_to_speech')):<5} "
            f"{truthy_mark(model.get('can_use_style')):<7} "
            f"{truthy_mark(model.get('can_use_speaker_boost')):<7} "
            f"{shorten(model.get('name'), 40)}"
        )


def print_voices(voices: list[dict[str, Any]]) -> None:
    print(f"\n{'VOICE ID':<24} {'CATEGORY':<13} {'TYPE':<11} NAME")
    print("-" * 96)
    for voice in voices:
        labels = voice.get("labels") or {}
        voice_type = voice.get("voice_type") or labels.get("voice_type") or ""
        print(
            f"{voice.get('voice_id', ''):<24} "
            f"{str(voice.get('category', '')):<13} "
            f"{str(voice_type):<11} "
            f"{shorten(voice.get('name'), 44)}"
        )


def print_shared_voices(voices: list[dict[str, Any]]) -> None:
    print(f"\n{'VOICE ID':<24} {'CATEGORY':<13} {'LANG':<10} NAME")
    print("-" * 96)
    for voice in voices:
        print(
            f"{voice.get('voice_id', ''):<24} "
            f"{str(voice.get('category', '')):<13} "
            f"{str(voice.get('language', '')):<10} "
            f"{shorten(voice.get('name'), 42)}"
        )


# ── API operations ────────────────────────────────────────────────────────────
def list_models(tts_only: bool, show_json: bool) -> None:
    models = request_json("GET", "/v1/models")
    if tts_only:
        models = [m for m in models if m.get("can_do_text_to_speech")]

    if show_json:
        print_json(models)
        return

    print_models(models)
    print(f"\n[elevenlabs] {len(models)} model(s)")


def list_voices(
    query: str | None,
    limit: int,
    sort: str | None,
    sort_direction: str | None,
    voice_type: str | None,
    category: str | None,
    show_json: bool,
) -> None:
    data = request_json(
        "GET",
        "/v2/voices",
        query={
            "page_size": limit,
            "search": query,
            "sort": sort,
            "sort_direction": sort_direction,
            "voice_type": voice_type,
            "category": category,
            "include_total_count": "true",
        },
    )

    if show_json:
        print_json(data)
        return

    voices = data.get("voices") or []
    print_voices(voices)
    total = data.get("total_count")
    if total is not None:
        print(f"\n[elevenlabs] showing {len(voices)} voice(s) | total_count={total}")
    else:
        print(f"\n[elevenlabs] showing {len(voices)} voice(s)")


def list_shared_voices(
    query: str | None,
    limit: int,
    category: str | None,
    gender: str | None,
    age: str | None,
    language: str | None,
    accent: str | None,
    show_json: bool,
) -> None:
    data = request_json(
        "GET",
        "/v1/shared-voices",
        query={
            "page_size": limit,
            "search": query,
            "category": category,
            "gender": gender,
            "age": age,
            "language": language,
            "accent": accent,
        },
    )

    if show_json:
        print_json(data)
        return

    voices = data.get("voices") or []
    print_shared_voices(voices)
    print(f"\n[elevenlabs] showing {len(voices)} shared voice(s)")


def resolve_text(text: str | None, text_file: str | None) -> str:
    if bool(text) == bool(text_file):
        print(
            "[ERROR] Provide exactly one of --text or --text-file for tts.",
            file=sys.stderr,
        )
        sys.exit(1)

    if text is not None:
        value = text.strip()
    else:
        text_path = Path(text_file or "")
        if not text_path.is_absolute():
            text_path = ROOT / text_path
        if not text_path.exists():
            print(f"[ERROR] Text file not found: {text_path}", file=sys.stderr)
            sys.exit(1)
        value = text_path.read_text(encoding="utf-8").strip()

    if not value:
        print("[ERROR] Input text is empty.", file=sys.stderr)
        sys.exit(1)

    return value


def build_voice_settings(args: argparse.Namespace) -> dict[str, Any] | None:
    settings: dict[str, Any] = {}

    if args.stability is not None:
        settings["stability"] = args.stability
    if args.similarity_boost is not None:
        settings["similarity_boost"] = args.similarity_boost
    if args.style is not None:
        settings["style"] = args.style
    if args.speed is not None:
        settings["speed"] = args.speed
    if args.speaker_boost:
        settings["use_speaker_boost"] = True

    return settings or None


def output_suffix(output_format: str) -> str:
    return output_format.split("_", 1)[0]


def resolve_output_path(output: str | None, output_format: str, prefix: str) -> Path:
    if output:
        out_path = Path(output)
        if not out_path.is_absolute():
            out_path = ROOT / out_path
        return out_path

    DEFAULT_OUT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = output_suffix(output_format)
    return DEFAULT_OUT / f"{prefix}_{timestamp}.{suffix}"


def generate_tts(args: argparse.Namespace) -> Path:
    text = resolve_text(args.text, args.text_file)
    out_path = resolve_output_path(args.output, args.output_format, args.prefix)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    body: dict[str, Any] = {
        "text": text,
        "model_id": args.model,
    }

    if args.language_code:
        body["language_code"] = args.language_code
    if args.seed is not None:
        body["seed"] = args.seed

    voice_settings = build_voice_settings(args)
    if voice_settings:
        body["voice_settings"] = voice_settings

    audio_bytes = request_bytes(
        "POST",
        f"/v1/text-to-speech/{args.voice_id}",
        query={"output_format": args.output_format},
        body=body,
        timeout=max(COMMON_TIMEOUT_SECS, args.timeout),
    )

    out_path.write_bytes(audio_bytes)
    size_kb = out_path.stat().st_size / 1024

    print(f"[elevenlabs] voice: {args.voice_id}")
    print(f"[elevenlabs] model: {args.model}")
    print(f"[elevenlabs] format: {args.output_format}")
    print(f"[elevenlabs] chars: {len(text)}")
    print(f"[elevenlabs] saved: {out_path} ({size_kb:.1f} KB)")
    return out_path


# ── CLI ───────────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search, explore, and generate audio with the ElevenLabs API"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    models_parser = subparsers.add_parser(
        "models",
        help="List available ElevenLabs models",
    )
    models_parser.add_argument(
        "--tts-only",
        action="store_true",
        help="Show only models that support text-to-speech",
    )
    models_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )

    voices_parser = subparsers.add_parser(
        "voices",
        help="Search voices in your ElevenLabs account/workspace",
    )
    voices_parser.add_argument("--query", "-q", default=None, help="Search term")
    voices_parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=10,
        help="Max voices to fetch (default: 10, max API limit is 100)",
    )
    voices_parser.add_argument(
        "--sort",
        choices=["created_at_unix", "name"],
        default=None,
        help="Sort field",
    )
    voices_parser.add_argument(
        "--sort-direction",
        choices=["asc", "desc"],
        default=None,
        help="Sort direction",
    )
    voices_parser.add_argument(
        "--voice-type",
        choices=["personal", "community", "default", "workspace", "non-default", "saved"],
        default=None,
        help="Voice type filter",
    )
    voices_parser.add_argument(
        "--category",
        choices=["premade", "cloned", "generated", "professional"],
        default=None,
        help="Voice category filter",
    )
    voices_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )

    shared_parser = subparsers.add_parser(
        "shared-voices",
        help="Explore public/shared ElevenLabs voices",
    )
    shared_parser.add_argument("--query", "-q", default=None, help="Search term")
    shared_parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=10,
        help="Max shared voices to fetch (default: 10, max API limit is 100)",
    )
    shared_parser.add_argument(
        "--category",
        choices=["professional", "famous", "high_quality"],
        default=None,
        help="Shared voice category filter",
    )
    shared_parser.add_argument("--gender", default=None, help="Gender filter")
    shared_parser.add_argument("--age", default=None, help="Age filter")
    shared_parser.add_argument("--language", default=None, help="Language filter")
    shared_parser.add_argument("--accent", default=None, help="Accent filter")
    shared_parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )

    tts_parser = subparsers.add_parser(
        "tts",
        help="Generate speech audio from text",
    )
    tts_parser.add_argument("--voice-id", required=True, help="ElevenLabs voice ID")
    text_group = tts_parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument("--text", help="Text to convert to speech")
    text_group.add_argument(
        "--text-file",
        help="Path to a UTF-8 text file to convert to speech",
    )
    tts_parser.add_argument(
        "--model",
        default="eleven_multilingual_v2",
        help="Model ID (default: eleven_multilingual_v2)",
    )
    tts_parser.add_argument(
        "--output-format",
        default="mp3_44100_128",
        choices=[
            "alaw_8000",
            "mp3_22050_32",
            "mp3_24000_48",
            "mp3_44100_32",
            "mp3_44100_64",
            "mp3_44100_96",
            "mp3_44100_128",
            "mp3_44100_192",
            "opus_48000_32",
            "opus_48000_64",
            "opus_48000_96",
            "opus_48000_128",
            "opus_48000_192",
            "pcm_8000",
            "pcm_16000",
            "pcm_22050",
            "pcm_24000",
            "pcm_32000",
            "pcm_44100",
            "pcm_48000",
            "ulaw_8000",
            "wav_8000",
            "wav_16000",
            "wav_22050",
            "wav_24000",
            "wav_32000",
            "wav_44100",
            "wav_48000",
        ],
        help="Audio output format (default: mp3_44100_128)",
    )
    tts_parser.add_argument(
        "--language-code",
        default=None,
        help="Optional ISO 639-1 language code",
    )
    tts_parser.add_argument(
        "--stability",
        type=float,
        default=None,
        help="Voice stability override (0-1)",
    )
    tts_parser.add_argument(
        "--similarity-boost",
        type=float,
        default=None,
        help="Voice similarity boost override (0-1)",
    )
    tts_parser.add_argument(
        "--style",
        type=float,
        default=None,
        help="Voice style exaggeration override (0-1)",
    )
    tts_parser.add_argument(
        "--speed",
        type=float,
        default=None,
        help="Speech speed override (default provider value if omitted)",
    )
    tts_parser.add_argument(
        "--speaker-boost",
        action="store_true",
        help="Enable speaker boost in voice settings",
    )
    tts_parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional deterministic seed (0 to 4294967295)",
    )
    tts_parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: assets/audio/auto-generated)",
    )
    tts_parser.add_argument(
        "--prefix",
        default="elevenlabs",
        help="Filename prefix for auto-generated output files",
    )
    tts_parser.add_argument(
        "--timeout",
        type=int,
        default=COMMON_TIMEOUT_SECS,
        help=f"HTTP timeout in seconds (default: {COMMON_TIMEOUT_SECS})",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "models":
        list_models(tts_only=args.tts_only, show_json=args.json)
        return

    if args.command == "voices":
        list_voices(
            query=args.query,
            limit=min(max(args.limit, 1), 100),
            sort=args.sort,
            sort_direction=args.sort_direction,
            voice_type=args.voice_type,
            category=args.category,
            show_json=args.json,
        )
        return

    if args.command == "shared-voices":
        list_shared_voices(
            query=args.query,
            limit=min(max(args.limit, 1), 100),
            category=args.category,
            gender=args.gender,
            age=args.age,
            language=args.language,
            accent=args.accent,
            show_json=args.json,
        )
        return

    if args.command == "tts":
        generate_tts(args)
        return

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
