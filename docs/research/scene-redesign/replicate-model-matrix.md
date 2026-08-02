# Replicate Model Matrix — Scene Graphics for 9:16 HyperFrames Videos

> Goal: replace hand-coded flat SVG (the "programmatic navy-void" look) with output from
> specialized Replicate models — true SVG vectors, rich raster art, textured backgrounds,
> transparent cutouts, and short ambient B-roll loops.
>
> **All `owner/name` ids below were confirmed live against `GET https://api.replicate.com/v1/models/<id>` → HTTP 200**
> on 2026-06-06 (input schemas read from each model's `latest_version.openapi_schema`).
> Pricing is **not** exposed in the model JSON — it is sourced from Replicate model pages, the
> official Recraft pricing doc, and pricing aggregators (see Sources). Treat $ figures as
> close estimates, not contractual.

---

## 1. Verified models (HTTP 200) + schema

### Vector / SVG (the headline capability)

| id | output | key inputs | price (est.) | notes for us |
|----|--------|-----------|--------------|--------------|
| **`recraft-ai/recraft-v4-svg`** | SVG (URI) | `prompt`, `size` (15 presets incl. portrait `1024x1820`, `1024x2048`), `aspect_ratio` | ~**$0.08 / image** | Newest "design-taste" vector model. Clean geometry, structured/editable layers. No `style` enum (v4 infers). **Best for hero vector illustration + logos.** 33k runs (new). |
| **`recraft-ai/recraft-v3-svg`** | SVG (URI) | `prompt`, `size`, `style` (`any`,`engraving`,`line_art`,`line_circuit`,`linocut`), `aspect_ratio` | ~**$0.08 / image** | Proven workhorse (421k runs). `style="line_art"` maps almost 1:1 onto the current line-art aesthetic. **Best for composable icons/glyphs** — recolor by editing SVG fill inline in the HTML. |
| `recraft-ai/recraft-20b-svg` | SVG (URI) | similar | ~$0.044 / image | Cheaper/older SVG tier. Use only if cost-sensitive batch icons. |
| **`recraft-ai/recraft-vectorize`** | SVG (URI) | `image` | ~**$0.008 / image** | Raster→clean SVG paths. **Pipeline glue**: generate raster with flux/nano-banana, vectorize for crisp recolorable paths. |
| `recraft-ai/recraft-crisp-upscale` | PNG | `image` | ~$0.006 / image | Sharpen/clean. Cheap finishing pass on any raster before compositing. |

`size` portrait presets useful for 9:16: `1024x1820`, `1024x2048`, `1024x1707`, `1024x1536`, `1024x1434`, `1024x1365`, `1024x1280`.

### Raster image generation

| id | output | key inputs | price (est.) | notes for us |
|----|--------|-----------|--------------|--------------|
| **`google/nano-banana-2`** | JPG/PNG | `prompt`, `image_input[]`, `aspect_ratio` (`match_input_image` default), `resolution` (`1K`/`2K`/`4K`), `output_format`, `google_search`, `image_search` | **$0.067 / 1K**, $0.101 / 2K, $0.151 / 4K | Gemini-3 image. Excellent prompt-adherence, multi-image edits, character/object **consistency across scenes**. **Best for hero raster art + textured backgrounds + iterative edits.** |
| `google/nano-banana` | JPG/PNG | `prompt`, `image_input[]`, `aspect_ratio`, `output_format` | ~**$0.02–0.039 / image** | Cheaper previous gen. Fast cutout subjects + backgrounds when 2 isn't needed. |
| `openai/gpt-image-1` | webp/PNG | `prompt`, `quality`, `background` (`transparent`!), `aspect_ratio`, `input_images[]`, `input_fidelity`, `output_format` | ~**$0.04 (medium) / $0.17 (high)** | Strong **text + layout + diagram** rendering. `background:"transparent"` gives native transparent PNG — handy for labeled UI mockups / chart frames. Slower. |
| `openai/gpt-image-1-mini` | webp/PNG | similar | ~$0.01–0.02 / image | Cheaper gpt-image for quick text-bearing accents. |
| `openai/gpt-image-2` | webp/PNG | similar | ~$0.04 (med) / $0.17 (high) | Newer OpenAI tier; same transparent-bg trick, better fidelity. |
| **`black-forest-labs/flux-1.1-pro`** | webp/PNG | `prompt`, `aspect_ratio`, `width/height`, `image_prompt`, `prompt_upsampling`, `output_format` | **$0.04 / image** | Best photoreal/abstract **textured backgrounds** (gradient-with-grain, depth) to kill flat navy. |
| `black-forest-labs/flux-dev` | webp/PNG | `prompt`, `aspect_ratio`, `num_outputs`, steps | ~**$0.025 / image** | Mid-cost flux; fine for backgrounds in bulk. |
| `black-forest-labs/flux-schnell` | webp/PNG | `prompt`, `aspect_ratio`, `num_outputs`, `go_fast`, `megapixels` | **~$0.003 / image** | Dirt-cheap, fast. **Best for high-volume background/texture exploration**; finish winners with upscale. |
| `ideogram-ai/ideogram-v3-turbo` | PNG | `prompt`, `aspect_ratio`, `resolution`, `style_type`, `style_preset`, `style_reference_images[]`, `magic_prompt_option`, `mask` | ~**$0.03 / image** | Best-in-class **text-in-image** (rare correct words). Use only if a graphic genuinely needs baked words — but CLAUDE.md says **never bake caption text** (the HyperFrames caption pipeline does type). Reserve for stylized signage/logos. |
| `google/imagen-4` | PNG | `prompt`, `aspect_ratio` | ~$0.04 / image | Alternative high-quality raster; good backgrounds. |

### Background removal / cutout

| id | output | key inputs | price (est.) | notes for us |
|----|--------|-----------|--------------|--------------|
| **`recraft-ai/recraft-remove-background`** | transparent PNG | `image` | ~**$0.006 / image** | Tuned for AI-generated content + product/portrait. Cleanest match since our sources are AI raster. **Primary cutout tool.** 1M+ runs. |
| `bria/remove-background` | transparent PNG | `image` | ~$0.04 / image | Commercial-grade, very clean edges on hair/complex. Pricier. |
| `851-labs/background-remover` | transparent PNG | `image` | ~$0.0008 / run | Cheapest viable. Good fallback for simple objects. |
| `men1scus/birefnet` | transparent PNG / mask | `image` | ~$0.01 / run | BiRefNet SOTA matting; best edges on tricky subjects. |
| `lucataco/remove-bg`, `cjwbw/rembg`, `pollinations/modnet`, `smoretalk/rembg-enhance` | transparent PNG | `image` | ~$0.0005–0.01 | All live; rembg-class. CLAUDE.md already standardizes on `rembg`. |

### Image-to-video (short ambient loops behind text)

| id | output | key inputs | price (est.) | notes for us |
|----|--------|-----------|--------------|--------------|
| **`bytedance/seedance-1-lite`** | MP4 | `image`, `prompt`, `duration` (5), `resolution` (720p), `aspect_ratio`, `fps` (24), `camera_fixed`, `last_frame_image` | ~**$0.018/s → ~$0.09 / 5s 720p** | Cheap, fast, supports **`camera_fixed`** = subtle ambient motion (ideal behind text). **Best default loop engine.** 3.4M runs. |
| `wan-video/wan-2.2-i2v-a14b` | MP4 | `image`, `prompt`, `num_frames`, `resolution` (480p default), `frames_per_second`, `sample_steps` | ~**$0.05 / run (480p)** | Already referenced in repo guides (wan-2.2 line-art prompts). Cheap, on-brand. Low-res default. |
| `kwaivgi/kling-v1.6-standard` | MP4 | `prompt`, `start_image`, `duration` (5), `aspect_ratio`, `cfg_scale`, `reference_images[]` | ~**$0.05/s → ~$0.25–0.49 / 5s** | Smoother, more cinematic motion. Use for hero loops where quality matters. |
| `bytedance/seedance-1-pro` | MP4 | `image`, `prompt`, `duration`, `resolution` (up to 1080p) | ~$0.06/s | 1080p quality tier of seedance. |
| `minimax/hailuo-02` | MP4 | `first_frame_image`, `last_frame_image`, `prompt`, `duration` (6), `resolution` (1080p) | ~$0.045/s+ | Strong 1080p motion, first+last frame control (good for true loops). |
| `lightricks/ltx-video` | MP4 | `image`, `prompt`, `length`, `aspect_ratio`, `target_size` | ~$0.02–0.06 / run | Fast/cheap; lower fidelity. Exploration tier. |
| `kwaivgi/kling-v2.5-turbo-pro`, `luma/ray-2-720p`, `google/veo-3-fast` | MP4 | i2v / t2v | $0.10–0.40+/s | Premium tiers — overkill for background loops, reserve for a marquee shot. |

### 404 / not found (do not use these exact ids)

- `recraft-ai/recraft-v4` raster **exists (200)** — but if you want the standalone raster id it's `recraft-ai/recraft-v3` / `recraft-ai/recraft-v4`. (No 404.)
- `wavespeedai/wan-2.2-i2v-720p` → **404**. Use `wan-video/wan-2.2-i2v-a14b` instead (200) and set `resolution:"720p"`.
- `luma/ray` → **404**. Use `luma/ray-2-720p` (200).
- `abhisekmanna/rmbg` → **404**. Use `recraft-ai/recraft-remove-background` or `men1scus/birefnet`.
- No special-access gating hit on any 200 model during schema reads (metadata only; no predictions run).

---

## 2. Scene-need → best-tool mapping

| # | Scene need | Primary pick | Why | Fallback |
|---|-----------|--------------|-----|----------|
| 1 | **Vector icons / logos / glyphs** (cloud, GPU, chip, arrow) — composable, recolorable | `recraft-ai/recraft-v3-svg` (`style:"line_art"`) | True SVG → drop into TSX, recolor `fill`/`stroke` at render. Style matches existing line-art house look. | `recraft-ai/recraft-v4-svg` for richer geometry |
| 2 | **Hero conceptual illustration** (doorway / death-star / metaphor centerpiece) | `recraft-ai/recraft-v4-svg` | Best "design taste" + clean editable vector → animate paths in HyperFrames (GSAP stroke-dashoffset). | `google/nano-banana-2` if a *raster* painterly hero is wanted |
| 3 | **Rich textured / photographic backgrounds** (kill flat navy) | `black-forest-labs/flux-1.1-pro` | Best abstract depth + gradient-with-grain; cheap at $0.04. Explore with `flux-schnell` ($0.003) then finish. | `google/nano-banana-2` (2K) for art-directed bg |
| 4 | **Transparent product / object / character cutouts** | `google/nano-banana-2` (generate, consistent) → `recraft-ai/recraft-remove-background` | nano-banana-2 keeps subject consistent across scenes; recraft RMBG is tuned for AI raster → clean alpha PNG. | `gpt-image-1` w/ `background:"transparent"` (one-shot) |
| 5 | **Short looping ambient B-roll** (subtle motion behind text) | `bytedance/seedance-1-lite` (`camera_fixed:true`) | Cheapest controllable subtle motion, 720p, ~$0.09/5s. Feed it a flux/nano-banana still. | `wan-video/wan-2.2-i2v-a14b` (on-brand line-art loops, ~$0.05) |
| 6 | **Data-viz embellishment / decorative accents** | `recraft-ai/recraft-v3-svg` (`style:"line_circuit"`) | Vector accents/connectors/circuit motifs as editable SVG. | `gpt-image-1` (transparent) for chart frames w/ correct labels |

---

## 3. Recommended starter kit (4–6 models)

| id | role | one-line rationale | est. cost/asset |
|----|------|--------------------|-----------------|
| **`recraft-ai/recraft-v4-svg`** | hero vectors + logos | Headline capability — production SVG with design taste, animatable in TSX. | ~$0.08 |
| **`recraft-ai/recraft-v3-svg`** | icon/glyph + decorative accent factory | `style:"line_art"`/`"line_circuit"` matches house look; recolorable SVG. | ~$0.08 |
| **`black-forest-labs/flux-1.1-pro`** | textured backgrounds | Kills the flat navy void with grainy/depthy abstract fields at $0.04. | ~$0.04 (explore @ $0.003 w/ schnell) |
| **`google/nano-banana-2`** | hero raster + consistent cutout subjects | Best prompt-adherence + cross-scene consistency for objects/characters. | ~$0.067 (1K) |
| **`recraft-ai/recraft-remove-background`** | alpha cutouts | Tuned for AI-generated raster → clean transparent PNG to layer over scenes. | ~$0.006 |
| **`bytedance/seedance-1-lite`** | ambient B-roll loops | Cheap subtle motion (`camera_fixed`) behind text to remove dead air. | ~$0.09 / 5s |

**Optional 7th:** `gpt-image-1` (transparent bg + correct text) only when a graphic genuinely needs legible baked words/labels — but per CLAUDE.md, captions stay in the HyperFrames caption pipeline, so keep this rare.

### Realistic per-video cost envelope
A typical short (≈12 scenes) using ~6 vector icons, 2 hero pieces, 4 textured backgrounds,
3 cutouts, 2 ambient loops:

- 6 × SVG icon ($0.08) = $0.48
- 2 × hero (v4-svg + nano-banana-2) ≈ $0.15
- 4 × flux bg ($0.04) = $0.16 (or $0.012 exploring with schnell)
- 3 × generate+RMBG (nano-banana $0.039 + $0.006) ≈ $0.13
- 2 × seedance-lite loop ($0.09) = $0.18

**≈ $1.10 of generation per video** at full quality; under $0.50 if backgrounds use flux-schnell.

---

## 4. Minimal example calls

### SVG icon (recraft-v3-svg) — curl
```bash
TOKEN=$(grep REPLICATE_API_TOKEN .env | cut -d= -f2)
curl -s -X POST https://api.replicate.com/v1/models/recraft-ai/recraft-v3-svg/predictions \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d '{"input":{"prompt":"single minimal line-art cloud icon, thin even strokes, no text",
                "style":"line_art","size":"1024x1024"}}'
# -> output: URL to .svg
```

### Hero vector (recraft-v4-svg, portrait) — replicate python
```python
import replicate
out = replicate.run("recraft-ai/recraft-v4-svg", input={
    "prompt": "a glowing doorway opening onto a starfield, conceptual, flat vector, layered",
    "size": "1024x1820",         # 9:16-ish
})
print(out)  # .svg URI
```

### Textured background (flux-1.1-pro)
```python
import replicate
out = replicate.run("black-forest-labs/flux-1.1-pro", input={
    "prompt": "deep navy abstract gradient field with fine film grain, soft volumetric depth, no subject",
    "aspect_ratio": "9:16", "output_format": "png", "prompt_upsampling": True,
})
```

### Consistent raster + cutout (nano-banana-2 → recraft RMBG)
```python
import replicate
raw = replicate.run("google/nano-banana-2", input={
    "prompt": "a sleek GPU card, 3/4 view, studio lighting, on plain background",
    "aspect_ratio": "1:1", "resolution": "1K", "output_format": "png",
})
cut = replicate.run("recraft-ai/recraft-remove-background", input={"image": raw})
print(cut)  # transparent PNG
```

### Ambient loop (seedance-1-lite, subtle motion)
```python
import replicate
clip = replicate.run("bytedance/seedance-1-lite", input={
    "image": "<flux_background_url>",
    "prompt": "very subtle drifting grain and slow parallax, no camera cuts",
    "duration": 5, "resolution": "720p", "aspect_ratio": "9:16",
    "camera_fixed": True, "fps": 24,
})  # -> MP4; loop in a HyperFrames <video muted playsinline>
```

---

## 5. Integration notes for this repo

- Pipe outputs through `tools/generate_assets.py` (extend it — do **not** write per-project scripts; CLAUDE.md rule). Save to `assets/<slug>/` and reference from the composition HTML.
- SVG outputs are URIs → fetch into `assets/<slug>/svg/` and inline them directly in the HTML (or `<img>` the file) so you can animate/recolor paths with GSAP.
- Never bake caption text into generated images — the HyperFrames caption pipeline handles type. That's why `ideogram-v3-turbo`/`gpt-image-1` text strength is **reserved**, not default.
- For green-screen talking heads keep the existing chromakey→alpha-WebM flow; these models are for B-roll/graphics, not the A-roll.
- Run `tools/scenes_dryrun.py` to preview prompts + cost before any paid batch.

---

## Sources
- Live Replicate API: `GET /v1/models/<id>` (HTTP status + `latest_version.openapi_schema`), 2026-06-06.
- [Recraft official API pricing](https://www.recraft.ai/docs/api-reference/pricing) — raster $0.04 / vector $0.08 per image.
- [Replicate pricing](https://replicate.com/pricing) · [pricepertoken.com/image](https://pricepertoken.com/image) — recraft-v3 $0.04, flux-1.1-pro $0.04, ideogram-v3-turbo $0.05, nano-banana $0.02, gpt-image-1 (medium) ~$0.04.
- [Nano Banana 2 pricing](https://replicate.com/google/nano-banana-2) and guides — 1K $0.045–0.067 / 2K $0.101 / 4K $0.151.
- [Replicate image-to-video collection](https://replicate.com/collections/image-to-video) · [Kling 1.6 I2V pricing](https://blogs.novita.ai/kling-1-6-i2v/) — kling-v1.6 ~$0.46–0.49/5s; seedance-lite ~$0.01–0.018/s.
