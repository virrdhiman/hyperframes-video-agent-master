> **DEPRECATED (2026-06-11): the Google API key is SUSPENDED — this tool is dead. Use `tools/ai_assets/replicate_gen.py` (Wan i2v via Replicate) instead.**

# Video Generator — Veo 3.1 (Google Gen AI)

Generates short AI videos using **Google Veo 3.1** (`veo-3.1-generate-preview`) by default.

**Script:** `tools/video_generator/veo.py`  
**Default output:** `assets/stock/`

---

## Auth

`veo.py` uses this priority:

1. `GOOGLE_API_KEY` from `.env` (Google AI API)
2. `cred.json` service account (Vertex AI fallback)

When using Vertex fallback:
- `veo3.1` uses `global`
- `veo2` uses `us-central1`

---

## Quick Start

```bash
cd tools/video_generator

# Veo 3.1 text-to-video (default model)
python3 veo.py --prompt "close up of a laptop webcam shutter closing" --ratio 9:16 --duration 8

# Veo 3.1 image-to-video
python3 veo.py --prompt "hand closes laptop lid naturally" --image ../../assets/images/frame.png --ratio 9:16 --duration 8

# Veo 3.1 with negative prompt
python3 veo.py --prompt "security desk scene" --negative "text, watermark, blurry" --duration 8

# Legacy Veo 2 fallback
python3 veo.py --model veo2 --prompt "cybersecurity concept scene" --ratio 9:16 --duration 8
```

---

## Arguments

| Argument | Short | Default | Description |
|---|---|---|---|
| `--prompt` | `-p` | required | Video generation prompt |
| `--model` | `-m` | `veo3.1` | `veo3.1` or `veo2` |
| `--ratio` | `-r` | `9:16` | `9:16`, `16:9`, `1:1` |
| `--duration` | `-d` | `8` | `veo3.1`: `4/6/8`; `veo2`: `5/6/7/8` |
| `--resolution` | | auto | `veo3.1` only: `720p`, `1080p`, `4k` |
| `--negative` | | none | `veo3.1` negative prompt |
| `--image` | `-i` | none | Starting image for image-to-video |
| `--ref-image` | | none | Reference image(s), can repeat up to 3 |
| `--out` | `-o` | `assets/stock/` | Output directory |
| `--prefix` | | `veo` | Output filename prefix |
| `--poll` | | `10` | Polling interval seconds |
| `--debug-response` | | off | Print provider response details when no videos are returned |

---

## Output

MP4 naming pattern:

```
<prefix>_<timestamp>_<index>.mp4
```

Example:

```
tapecam_beige_lidclose_20260303_170326_1.mp4
```

---

## Practical Prompting Tips

For physically accurate action clips, include:

- Exact motion order (for example: slide shutter first, then close lid)
- Biomechanics (wrist rotation, finger contact, hinge resistance)
- Camera behavior (locked tripod, subtle handheld, macro close-up)
- Material details (anodized aluminum, reflections, contact shadows)
- Artifacts to avoid in `--negative` (extra fingers, warped hinge, text)

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `No auth found` | Missing API key and `cred.json` | Add `GOOGLE_API_KEY` to `.env` or provide `cred.json` |
| `No videos in response` | Provider returned an unexpected response shape | Re-run with `--debug-response`; simplify prompt; retry |
| `Invalid duration` | Duration not allowed for model | Use `4/6/8` for `veo3.1` or `5/6/7/8` for `veo2` |
| Long wait times | Async generation queue | Keep process running; increase `--poll` if needed |
| Safety blocked | Prompt policy issue | Rephrase prompt with neutral language |

