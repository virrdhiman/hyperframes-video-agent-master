#!/usr/bin/env python3
"""
imagen.py — Generate and edit images using Google Nano Banana 2
(gemini-3.1-flash-image-preview) via the Google Gen AI SDK.

Supports text-to-image, image editing with prompts, reference-image
person generation (use your own photo), and infographic creation.

Auth: Uses GOOGLE_API_KEY from .env (Google AI Developer API).
Falls back to cred.json (Vertex AI) if no API key is found.

Usage:
    python3 imagen.py --prompt "your prompt" [options]

Examples:
    # Text-to-image (default 9:16)
    python3 imagen.py --prompt "futuristic city at night, AI neural network overlay"

    # Edit an existing image
    python3 imagen.py --prompt "make the background darker and more cinematic" --image photo.png

    # Use yourself as a person in the generated image
    python3 imagen.py --prompt "a tech entrepreneur presenting on stage" --ref-image me.jpg

    # Generate an infographic
    python3 imagen.py --prompt "how neural networks learn" --infographic

    # Legacy Imagen 3 mode
    python3 imagen.py --prompt "abstract background" --model imagen3 --count 4
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import List, Optional

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
CRED_FILE = ROOT / "cred.json"
DEFAULT_OUT = ROOT / "assets" / "images"

MODEL_MAP = {
    "nano-banana-2": "gemini-3.1-flash-image-preview",
    "nano-banana":   "gemini-2.5-flash-image",
    "imagen3":       "imagen-3.0-fast-generate-001",
}

RATIO_CHOICES = [
    "9:16", "16:9", "1:1",
    "4:3", "3:4", "3:2", "2:3",
    "4:5", "5:4", "21:9",
]


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_client():
    """
    Create a Google Gen AI client.
    Priority: GOOGLE_API_KEY from .env → Vertex AI via cred.json
    """
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)

    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        from google import genai
        print("[imagen] Auth: Google AI API key")
        return genai.Client(api_key=api_key)

    if CRED_FILE.exists():
        with open(CRED_FILE) as f:
            cred = json.load(f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CRED_FILE)
        from google import genai
        print("[imagen] Auth: Vertex AI (service account)")
        return genai.Client(
            vertexai=True,
            project=cred["project_id"],
            location="global",
        )

    print("[ERROR] No auth found. Set GOOGLE_API_KEY in .env or provide cred.json", file=sys.stderr)
    sys.exit(1)


# ── Image loading ─────────────────────────────────────────────────────────────
def load_image_pil(image_path: str):
    """Load a local image file and return a PIL Image."""
    from PIL import Image as PILImage

    path = Path(image_path)
    if not path.exists():
        print(f"[ERROR] Image not found: {path}", file=sys.stderr)
        sys.exit(1)

    img = PILImage.open(path)
    size_kb = path.stat().st_size // 1024
    print(f"[imagen] Loaded image: {path.name} ({size_kb} KB, {img.size[0]}x{img.size[1]})")
    return img


# ── Main generation (Nano Banana) ─────────────────────────────────────────────
def generate(
    prompt: str,
    ratio: str = "9:16",
    model_key: str = "nano-banana-2",
    image_path: Optional[str] = None,
    ref_image_paths: Optional[List[str]] = None,
    infographic: bool = False,
    out_dir: Optional[str] = None,
    prefix: str = "imagen",
    count: int = 1,
):
    from google.genai import types

    client = get_client()

    model_id = MODEL_MAP.get(model_key)
    if not model_id:
        print(f"[ERROR] Unknown model '{model_key}'. Choose from: {list(MODEL_MAP.keys())}", file=sys.stderr)
        sys.exit(1)

    if ratio not in RATIO_CHOICES:
        print(f"[ERROR] Unsupported ratio '{ratio}'. Choose from: {RATIO_CHOICES}", file=sys.stderr)
        sys.exit(1)

    # Legacy Imagen 3 path
    if model_key == "imagen3":
        return _generate_legacy(client, prompt, ratio, count, out_dir, prefix)

    # ── Build contents ────────────────────────────────────────────────────
    contents = []

    if ref_image_paths:
        for ref_path in ref_image_paths:
            contents.append(load_image_pil(ref_path))
        print(f"[imagen] Reference images: {len(ref_image_paths)} loaded")

    if image_path:
        contents.append(load_image_pil(image_path))
        print("[imagen] Edit mode: modifying input image")

    if infographic:
        prompt = (
            f"Create a clear, professional infographic explaining: {prompt}. "
            "Use clean layout, icons, arrows, numbered steps, and readable text. "
            "Use a modern flat design style with good visual hierarchy."
        )

    contents.append(prompt)

    # ── Build config ──────────────────────────────────────────────────────
    config = types.GenerateContentConfig(
        response_modalities=[types.Modality.TEXT, types.Modality.IMAGE],
        image_config=types.ImageConfig(
            aspect_ratio=ratio,
        ),
    )

    mode_label = "Infographic" if infographic else ("Edit" if image_path else "Generate")
    print(f"[imagen] Model: {model_id} (Nano Banana 2)")
    print(f"[imagen] Mode: {mode_label} | Ratio: {ratio}")
    print(f"[imagen] Prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}")
    print(f"[imagen] Generating {count} image(s)...")

    out_path = Path(out_dir) if out_dir else DEFAULT_OUT
    out_path.mkdir(parents=True, exist_ok=True)

    saved = []
    for attempt in range(count):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=contents,
                config=config,
            )
        except Exception as e:
            print(f"[ERROR] Generation failed (attempt {attempt + 1}): {e}", file=sys.stderr)
            continue

        if not response.candidates or not response.candidates[0].content:
            print(f"[WARN] No content in response (attempt {attempt + 1})")
            continue

        for part in response.candidates[0].content.parts:
            if part.text:
                print(f"[imagen] Model note: {part.text[:300]}")
            elif part.inline_data:
                from PIL import Image as PILImage
                image = PILImage.open(BytesIO(part.inline_data.data))

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{prefix}_{timestamp}_{attempt + 1}.png"
                filepath = out_path / filename
                image.save(str(filepath))

                size_kb = filepath.stat().st_size // 1024
                print(f"[imagen] Saved: {filepath} ({image.size[0]}x{image.size[1]}, {size_kb} KB)")
                saved.append(str(filepath))

    print(f"[imagen] Done — {len(saved)} image(s) saved to {out_path}")
    return saved


# ── Legacy Imagen 3 ──────────────────────────────────────────────────────────
def _generate_legacy(client, prompt, ratio, count, out_dir, prefix):
    """Imagen 3 Fast path using the generate_images API."""
    from google.genai import types

    print(f"[imagen] Model: imagen-3.0-fast-generate-001 (legacy)")
    print(f"[imagen] Generating {count} image(s) — ratio: {ratio}")
    print(f"[imagen] Prompt: {prompt}")

    response = client.models.generate_images(
        model="imagen-3.0-fast-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=count,
            aspect_ratio=ratio,
            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            person_generation="ALLOW_ADULT",
        ),
    )

    out_path = Path(out_dir) if out_dir else DEFAULT_OUT
    out_path.mkdir(parents=True, exist_ok=True)

    saved = []
    for i, image in enumerate(response.generated_images):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}_{i+1}.png"
        filepath = out_path / filename

        with open(filepath, "wb") as f:
            f.write(image.image.image_bytes)

        print(f"[imagen] Saved: {filepath}")
        saved.append(str(filepath))

    print(f"[imagen] Done — {len(saved)} image(s) saved to {out_path}")
    return saved


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Generate and edit images with Google Nano Banana 2"
    )
    parser.add_argument(
        "--prompt", "-p", required=True,
        help="Text prompt for image generation or editing instruction"
    )
    parser.add_argument(
        "--ratio", "-r", default="9:16",
        choices=RATIO_CHOICES,
        help="Aspect ratio (default: 9:16)"
    )
    parser.add_argument(
        "--count", "-n", type=int, default=1, choices=range(1, 5),
        help="Number of images to generate (1-4, default: 1)"
    )
    parser.add_argument(
        "--image", "-i", default=None,
        help="Input image path for editing (modify an existing image with your prompt)"
    )
    parser.add_argument(
        "--ref-image", action="append", default=None,
        help="Reference image path (e.g. your photo to appear in the generated image). "
             "Can specify multiple times."
    )
    parser.add_argument(
        "--infographic", action="store_true",
        help="Generate an infographic explaining the topic in the prompt"
    )
    parser.add_argument(
        "--model", "-m", default="nano-banana-2",
        choices=list(MODEL_MAP.keys()),
        help="Model version (default: nano-banana-2)"
    )
    parser.add_argument(
        "--out", "-o", default=None,
        help="Output directory (default: assets/images/)"
    )
    parser.add_argument(
        "--prefix", default="imagen",
        help="Filename prefix (default: imagen)"
    )
    args = parser.parse_args()

    generate(
        prompt=args.prompt,
        ratio=args.ratio,
        model_key=args.model,
        image_path=args.image,
        ref_image_paths=args.ref_image,
        infographic=args.infographic,
        out_dir=args.out,
        prefix=args.prefix,
        count=args.count,
    )


if __name__ == "__main__":
    main()
