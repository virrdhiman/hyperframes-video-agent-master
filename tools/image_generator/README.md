> **DEPRECATED (2026-06-11): the Google API key is SUSPENDED — this tool is dead. Use `tools/ai_assets/replicate_gen.py` (Nano Banana 2 via Replicate) instead.**

# Image Generator — Nano Banana 2 (Google Gemini)

Generates and edits images using **Google Nano Banana 2** (`gemini-3.1-flash-image-preview`) via the Google Gen AI SDK.

**Script:** `tools/image_generator/imagen.py`
**Auth:** Uses `GOOGLE_API_KEY` from `.env` (preferred), falls back to `cred.json` (Vertex AI).
**Default output:** `assets/images/`

---

## Quick Start

```bash
cd tools/image_generator

# Generate one 9:16 image (default)
python3 imagen.py --prompt "futuristic Indian city skyline at night"

# Generate 4 images in 16:9
python3 imagen.py --prompt "AI neural network visualization" --ratio 16:9 --count 4

# Edit an existing image
python3 imagen.py --prompt "make the background darker and more cinematic" --image ../../assets/images/photo.png

# Use yourself as a person in the image
python3 imagen.py --prompt "a tech entrepreneur presenting on stage at a conference" --ref-image ../../assets/images/me.jpg

# Generate an infographic
python3 imagen.py --prompt "how large language models work" --infographic --ratio 16:9

# Legacy Imagen 3 (if needed)
python3 imagen.py --prompt "abstract background" --model imagen3 --count 4
```

---

## Arguments

| Argument | Short | Default | Description |
|---|---|---|---|
| `--prompt` | `-p` | required | Text prompt for generation or editing instruction |
| `--ratio` | `-r` | `9:16` | Aspect ratio (see table below) |
| `--count` | `-n` | `1` | Number of images (1-4) |
| `--image` | `-i` | — | Input image path for editing (modify with prompt) |
| `--ref-image` | | — | Reference image (e.g. your photo). Can specify multiple times |
| `--infographic` | | off | Generate an infographic explaining the topic |
| `--model` | `-m` | `nano-banana-2` | Model: `nano-banana-2`, `nano-banana`, or `imagen3` |
| `--out` | `-o` | `assets/images/` | Output directory |
| `--prefix` | | `imagen` | Filename prefix |

---

## Generation Modes

### 1. Text-to-Image (default)
Standard prompt-to-image generation with world knowledge, reasoning, and excellent text rendering.

```bash
python3 imagen.py --prompt "professional portrait of an Indian tech CEO, modern office"
```

### 2. Image Editing
Pass an existing image with `--image` and describe the edit in `--prompt`.

```bash
python3 imagen.py --prompt "change the background to a sunset beach" --image input.png
python3 imagen.py --prompt "remove the person on the left" --image group.jpg
python3 imagen.py --prompt "make it look more cinematic with warm color grading" --image scene.png
```

### 3. Reference Image (Person Generation)
Use `--ref-image` to include a person's photo. The model will place that person into the generated scene.

```bash
python3 imagen.py --prompt "a man walking through Times Square at night" --ref-image me.jpg
python3 imagen.py --prompt "portrait in a futuristic lab" --ref-image me.jpg --ratio 9:16
```

### 4. Infographic Generation
Use `--infographic` to create visual explanations of complex topics. Nano Banana 2's text rendering makes it excellent for readable infographics.

```bash
python3 imagen.py --prompt "how neural networks learn through backpropagation" --infographic
python3 imagen.py --prompt "comparison of AI chip architectures: GPU vs TPU vs NPU" --infographic --ratio 16:9
python3 imagen.py --prompt "India's AI market growth 2020-2030" --infographic --ratio 1:1
```

---

## Aspect Ratios

| Ratio | Use Case |
|---|---|
| `9:16` | YouTube Shorts, Instagram Reels, TikTok (portrait) |
| `16:9` | YouTube, landscape thumbnails, infographics |
| `1:1` | Instagram posts, profile images |
| `4:3` | Standard landscape |
| `3:4` | Portrait, book covers |
| `3:2` / `2:3` | Photo aspect ratios |
| `4:5` / `5:4` | Instagram portrait / landscape |
| `21:9` | Ultra-wide cinematic |

---

## Model Details

| Property | Value |
|---|---|
| Default model | `gemini-3.1-flash-image-preview` (Nano Banana 2) |
| Provider | Google Gen AI SDK (API key or Vertex AI) |
| Max images per call | 4 (via `--count`) |
| Output format | PNG |
| Text rendering | Pro-quality (readable text in images) |
| Person support | Up to 5 consistent characters |
| Object accuracy | Up to 14 distinct objects |
| Resolution | Up to 4K |

| Model key | Model ID | Notes |
|---|---|---|
| `nano-banana-2` | `gemini-3.1-flash-image-preview` | Latest, best quality (default) |
| `nano-banana` | `gemini-2.5-flash-image` | Previous generation |
| `imagen3` | `imagen-3.0-fast-generate-001` | Legacy, uses older API |

---

## Prompt Tips

- **Text in images**: Nano Banana 2 renders text accurately — include exact text you want in the prompt
- **Infographics**: Specify the layout (e.g. "numbered steps", "comparison chart", "timeline")
- **Lighting**: "cinematic lighting", "golden hour", "neon glow", "backlit"
- **Style**: "photorealistic", "4K", "flat design", "illustration", "3D render"
- **People**: For best results with `--ref-image`, describe the person's pose and setting clearly
- **Editing**: Be specific about what to change and what to keep ("leave the background unchanged")

---

## Agent Workflow Integration

When the agent reads an `editing_brief.json` and finds `"source_type": "ai_image"`:

1. Extract the `ai_prompt` from the scene's `visual` object
2. Run with that prompt and the appropriate `--ratio` and `--prefix`
3. For infographic scenes, add `--infographic`
4. For person-in-scene shots, use `--ref-image` with the person's photo
5. Save to `assets/images/` or the project's asset folder
6. Update the brief to mark `"generated": true` and fill in `"file"` path

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `No auth found` | Missing API key and cred.json | Set `GOOGLE_API_KEY` in `.env` or add `cred.json` |
| `403 Permission denied` | API not enabled | Enable Gemini API in Google Cloud Console |
| `No content in response` | Safety filter or empty result | Rephrase prompt to be less ambiguous |
| `Generation failed` | Rate limit or model issue | Wait and retry |
