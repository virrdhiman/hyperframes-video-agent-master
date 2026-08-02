# Scene Redesign — Pipeline & Teaching Architecture

> **Status:** architecture / design spec. This is the blueprint a later implementation
> task builds from. It defines schemas, file layout, and the teaching + QA mechanism —
> not the implementation.
>
> **Migration note:** this spec was authored for the prior Remotion codebase. The
> *asset-request schema, generation tooling, caching, teaching mechanism, and QA gate are
> framework-agnostic and carry over to HyperFrames unchanged.* Only the "consumption" layer
> changes: where the spec shows React/`.tsx` components (`<SvgAsset>`, `<Img staticFile>`,
> `<OffthreadVideo>`), the HyperFrames equivalent is plain HTML — `<img src="assets/…">`,
> inline `<svg>`, `<video muted playsinline>` — timed with `data-start`/`data-duration`/
> `data-track-index` and animated by a paused GSAP timeline on `window.__timelines`. Read
> the `.tsx`/`staticFile()` snippets below as the original design intent, not literal hf code.

## Problem statement

Today the editor agent hand-codes flat SVG and inline shapes inside `.tsx`
compositions. That produces template-y, low-density scenes (single-color backgrounds,
floating text on emptiness, one flat icon). Meanwhile the asset pipeline
(`tools/generate_assets.py` + `scenes.json`) only knows two element kinds — **full-frame
image** (nano-banana) and **image-to-video** (wan). There is no way for a scene to say
"I need a crisp vector icon", "I need a textured background", or "I need a transparent
cutout to layer". So the agent fills the gap by hand and the result looks cheap.

This redesign does two things:

1. **PIPELINE** — extend `scenes.json` so a scene can *declare the specialized visual
   elements it needs* (`elements[]`), and extend the generation tooling
   (`tools/asset_studio/`) to dispatch each element to the right specialized Replicate
   model (SVG vector / raster art / textured bg / transparent cutout / ambient loop),
   with caching, a style-reference system, and cost preview. The agent **requests**
   elements; it does not hand-roll them.

2. **TEACHING** — durably give the editor agent a design language so the scenes it
   composes from those elements are *good by construction*: a `DESIGN_LANGUAGE.md` spec,
   an auto-generated **element catalog**, **few-shot exemplars**, and — the part that
   actually changes behavior — an **enforceable QA gate** (lint rules + the existing
   grid-review step) the agent must pass before a render is considered done.

The whole design is consistent with two non-negotiable repo rules:
- **Never write per-project Python.** All new capability extends shared tools and is
  driven by per-project JSON (`asset-generation.mdc`).
- **Never bake text into generated images.** HyperFrames owns all typography (HTML + CSS). Generated
  elements are *icons / illustrations / backgrounds / cutouts / loops*, never captions.

---

## 1. Asset-request schema (`scenes.json` extension)

### 1.1 Design constraints

- Backward compatible: every existing `scenes.json` (image/video scenes) keeps working
  untouched. `elements` is **additive and optional**.
- Same universal config envelope (`project`, `output_dir`, `style_prefix`,
  `image_defaults`, `parallel_workers`, …). New top-level keys: `element_defaults`,
  `style_refs`.
- A scene's `elements[]` are the discrete visual pieces the **composition will layer** —
  they are *not* a full frame. A scene can still have a `type: "image"`/`"video"`
  full-frame B-roll AND declare `elements`, or be a pure motion-graphic scene
  (`type: "graphic"`) whose entire visual is assembled from elements + HyperFrames typography.

### 1.2 Element object

```jsonc
{
  "id": "ic_lock",                 // unique within project; becomes the filename stem
  "type": "svg-icon",              // see element types below
  "prompt": "a minimal padlock, single closed shackle, geometric, even stroke weight",
  "model": "auto",                 // "auto" → asset_studio picks by type; or pin a model id
  "style_ref": "ink-line",       // optional: key into config.style_refs (see 1.4)
  "recolor": { "stroke": "#FF4A2E", "fill": "none" }, // optional post-gen recolor (SVG only)
  "size": { "w": 512, "h": 512 },  // intrinsic px; for "background"/"loop" use frame size
  "transparent": true,             // request alpha (cutout/icon); ignored where N/A
  "reuse": "shared",               // "shared" → public/common/elements/ ; default "project"
  "tags": ["security", "icon"]     // free-form, surfaces in the element catalog
}
```

#### Element types → capability → default model class

| `type`             | Capability                         | Default model class            | Output                        |
|--------------------|------------------------------------|--------------------------------|-------------------------------|
| `svg-icon`         | True vector icon                   | recraft SVG (`recraft-v4-svg`) | `.svg`                        |
| `hero-illustration`| Raster spot illustration / art     | raster art (`gpt-image-2`)     | `.png` (alpha if requested)   |
| `background`       | Full-frame textured background     | textured bg (`nano-banana-2`)  | `.png` / `.jpg` (frame size)  |
| `cutout`           | Transparent subject cutout         | raster art → background-removal| `.png` (alpha)                |
| `loop`             | Ambient seamless motion loop       | image-to-video (wan / i2v)     | `.mp4` (seamless)             |
| `accent`           | Small decorative vector (rule, blob, arrow, sticker) | recraft SVG  | `.svg`                        |

`model: "auto"` is the norm — the agent picks a **capability** (the `type`), not a model
id. Exact model ids are resolved by `asset_studio/models.py` (a separate research effort
supplies the precise ids; the registry is the single place they live). The agent may pin
`model` to an explicit id to override, but should rarely need to.

> **`cutout`** is a two-step capability: generate the subject (raster art, dark/plain
> backdrop, "isolated subject, no background text"), then run background-removal. The
> studio chains these automatically — `rembg`/model background-removal per the existing
> rule ("background removal: use rembg, never PIL flood-fill").

### 1.3 Where `elements` live in a scene

```jsonc
{
  "id": "s03_security",
  "type": "graphic",               // NEW type: pure motion-graphic, no full-frame B-roll
  "bg": "ic_bg_grid",              // optional: element id used as the scene background layer
  "elements": [ /* … */ ]
}
```

`type: "graphic"` tells the studio there is no nano-banana full-frame render for this
scene — only its `elements`. `type: "image"`/`"video"` scenes keep their existing
behavior and *may* also carry `elements` (e.g. a B-roll scene with an `accent` vector
sticker overlaid). The `bg` field is sugar: it names one element to be treated as the
scene's background layer by the consumption components (§3).

### 1.4 Style-reference system (cross-asset consistency)

Top-level `style_refs` is a named palette of reusable style anchors. Each element points
at one via `style_ref`. This is what keeps 12 icons in a video looking like one set
instead of 12 unrelated clip-arts.

```jsonc
"style_refs": {
  "ink-line": {
    "prompt_suffix": "consistent ink line-art icon set, even 4px stroke, rounded joints, dark ink on transparent, no fill, no text",
    "ref_image": "assets/styleref/ink-line.png",   // optional anchor image (i2i / style transfer)
    "palette": ["#16120E", "#FF4A2E", "#2B59FF"]
  },
  "beige-paper": {
    "prompt_suffix": "torn-paper collage spot illustration, warm beige #EDE6D6 ground, hand-cut edges, risograph texture, no text",
    "palette": ["#EDE6D6", "#1A1A1A", "#D64550"]
  }
}
```

The studio composes the final prompt as:
`style_prefix` (global) → `style_refs[style_ref].prompt_suffix` → element `prompt`.
A given video typically uses **one** `style_ref` for all its `svg-icon`/`accent`
elements so the icon set is coherent.

### 1.5 Concrete example scene

```jsonc
{
  "project": "samsung_s26_privacy",
  "output_dir": "assets/samsung-s26-privacy",
  "characters": [],
  "style_prefix": "Warm editorial mood on a light paper ground, coral and cobalt accents. NO text, labels, numbers, or words in the image.",
  "image_model": "google/nano-banana",
  "video_model": "wan-video/wan-2.2-i2v-fast",
  "image_defaults": { "aspect_ratio": "9:16", "output_format": "jpg" },
  "video_defaults": { "resolution": "720p", "frames_per_second": 30 },

  "element_defaults": { "transparent": true, "frame": { "w": 1080, "h": 1920 } },
  "style_refs": {
    "ink-line": {
      "prompt_suffix": "clean ink line-art icon, even 4px stroke, rounded joints, dark ink on transparent, no fill, no text",
      "palette": ["#16120E", "#FF4A2E", "#2B59FF"]
    }
  },

  "parallel_workers": 4,
  "max_retries": 3,
  "retry_delay_sec": 10,

  "scenes": [
    {
      "id": "s01_hook",
      "type": "video",
      "source": "s01_hook_img",
      "prompt": "Slow push toward a phone resting on a bright desk."
    },
    {
      "id": "s01_hook_img",
      "type": "image",
      "prompt": "A smartphone resting alone on a bright desk, soft daylight, shallow depth."
    },

    {
      "id": "s03_three_risks",
      "type": "graphic",
      "bg": "bg_grid_paper",
      "elements": [
        {
          "id": "bg_grid_paper",
          "type": "background",
          "prompt": "warm paper surface with a faint perspective grid, soft vignette, subtle noise texture",
          "size": { "w": 1080, "h": 1920 },
          "transparent": false,
          "reuse": "shared",
          "tags": ["paper", "grid", "background"]
        },
        {
          "id": "ic_mic",
          "type": "svg-icon",
          "prompt": "a microphone, geometric, single even stroke",
          "style_ref": "ink-line",
          "size": { "w": 400, "h": 400 },
          "tags": ["audio", "privacy"]
        },
        {
          "id": "ic_eye",
          "type": "svg-icon",
          "prompt": "an open eye with a slash through it, geometric",
          "style_ref": "ink-line",
          "recolor": { "stroke": "#FF4A2E" },
          "size": { "w": 400, "h": 400 },
          "tags": ["camera", "privacy"]
        },
        {
          "id": "ic_location",
          "type": "svg-icon",
          "prompt": "a map pin with a pulse ring, geometric",
          "style_ref": "ink-line",
          "size": { "w": 400, "h": 400 },
          "tags": ["location", "privacy"]
        }
      ]
    },

    {
      "id": "s05_villain",
      "type": "graphic",
      "bg": "bg_grid_paper",
      "elements": [
        {
          "id": "cut_exec",
          "type": "cutout",
          "prompt": "a corporate executive in a suit, mid-gesture, soft side light, isolated subject",
          "transparent": true,
          "size": { "w": 900, "h": 1400 },
          "tags": ["person", "cutout"]
        },
        {
          "id": "accent_arrow",
          "type": "accent",
          "prompt": "a hand-drawn circular arrow, single stroke",
          "style_ref": "ink-line",
          "size": { "w": 300, "h": 300 },
          "tags": ["arrow", "decor"]
        }
      ]
    }
  ]
}
```

Notes that keep it consistent with current conventions:
- `s01_hook` / `s01_hook_img` is the **exact existing** image→video pattern (`source`).
- New scenes (`s03`, `s05`) add `elements` without changing that.
- `reuse: "shared"` on `bg_grid_paper` means it is written to `public/common/elements/`
  and can be referenced by future videos (see §2.3) — one shared dark grid background,
  not regenerated per project.

---

## 2. Generation tooling — `tools/asset_studio/`

A new package, dispatched from `generate_assets.py` (no per-project scripts). It owns
everything `elements[]` related; the existing image/video paths are untouched.

### 2.1 File layout

```
tools/asset_studio/
  __init__.py
  models.py        # capability → Replicate model-id registry (single source of truth)
  studio.py        # dispatch: element → right model; chaining (cutout = gen + bg-removal)
  cache.py         # prompt-hash dedup + manifest read/write
  styleref.py      # resolve style_refs → prompt suffix + optional ref image
  recolor.py       # post-gen SVG recolor (stroke/fill swap)
  cost.py          # per-capability cost table (consumed by scenes_dryrun)
  manifest.py      # public/<slug>/elements/manifest.json + catalog emit
```

`generate_assets.py` gains a **Phase 0.5: ELEMENTS** between voiceover and images, and a
flag `--elements-only`. It iterates every scene's `elements`, calls
`asset_studio.studio.generate_element(...)`, reusing the existing
`run_parallel`/retry/`--force` machinery (same worker pool, same retry semantics). No new
concurrency model.

### 2.2 Model dispatch (`models.py`)

```python
# Capability → Replicate model id. Exact ids filled by the model-research effort.
CAPABILITY_MODELS = {
    "svg-icon":          "recraft-ai/recraft-v4-svg",
    "accent":            "recraft-ai/recraft-v4-svg",
    "hero-illustration": "openai/gpt-image-2",
    "background":        "google/nano-banana-2",
    "cutout":            ("openai/gpt-image-2", "<background-removal-model-id>"),  # chain
    "loop":              "wan-video/wan-2.2-i2v-fast",
}
```

`studio.generate_element` resolves `model: "auto"` through this table; an explicit
`model` in the element overrides. `cutout` runs the two-stage chain (generate → remove
background). `loop` reuses the existing image-to-video path but post-processes for a
seamless boundary (crossfade tail→head via ffmpeg) and a short duration (~3–5s) so it
tiles cleanly when looped in the composition.

### 2.3 Output layout + reuse

```
public/<slug>/elements/
  ic_lock.svg
  bg_grid_paper.png         # (project-scoped)
  cut_exec.png             # alpha
  manifest.json            # per-project element manifest

public/common/elements/    # reuse:"shared" elements promoted here
  backgrounds/bg_grid_paper.png
  icons/ink-line/ic_mic.svg
  manifest.json            # shared catalog, accumulated across videos
```

- `reuse: "project"` (default) → `public/<slug>/elements/<id>.<ext>`.
- `reuse: "shared"` → written to `public/common/elements/<bucket>/…` and registered in
  the shared manifest. A later video referencing the same `id`+prompt-hash gets a **cache
  hit** and skips generation entirely (§2.4). This is how the element library grows over
  time instead of every video re-paying for a dark grid background.

### 2.4 Caching / dedup (`cache.py`)

- **Key** = `sha1(model_id + final_prompt + style_ref_resolved + size + recolor + transparent)`.
- A global index `public/common/elements/_cache/<hash>.<ext>` stores the canonical
  output; per-project/shared paths are hardlinks/copies pointing at it.
- On generate: if the hash exists, copy from cache (no API call). `--force` bypasses.
- The per-project `manifest.json` records, for each element:
  `{id, type, model, prompt, style_ref, hash, path, bytes, created_at, tags}`.
- This makes regenerating one project free for any element already produced anywhere,
  and gives the dry-run an exact "cache hit vs will-generate" count.

### 2.5 Cost preview (extend `scenes_dryrun.py`)

`scenes_dryrun.py` learns about `elements`:
- Add per-capability prices to the existing env-overridable table
  (`PRICE_SVG_USD`, `PRICE_GPTIMAGE_USD`, `PRICE_BG_USD`, `PRICE_CUTOUT_USD`,
  `PRICE_LOOP_USD`), sourced from `asset_studio.cost`.
- For each element: compute its hash, check the cache, print
  `✓ cached` / `○ todo` with model + capability + price, exactly like image/video rows.
- Summary gains an `elements` block:
  `elements  N total   K cached   M todo   ~$X.XX`.
- This is the **cost-check before generating** the repo rule already mandates — now it
  covers elements too.

---

## 3. HyperFrames consumption

Goal: the agent never inlines a `<svg>` by hand again. It references generated elements
by id through a small set of layout/layer components that **enforce good design by
construction** (a flat single-color scene becomes hard to build; a dense, depth-layered
scene becomes the path of least resistance).

### 3.1 How each element type is consumed

| Element     | Consumption in TSX                                                                 |
|-------------|-----------------------------------------------------------------------------------|
| `svg-icon`  | `<SvgAsset id="ic_lock" />` — fetches `staticFile()` SVG, inlines it so it can be CSS-recolored/animated. Vectors stay crisp at any scale. |
| `accent`    | Same as `svg-icon` (decorative).                                                  |
| `hero-illustration` | `<Img src={staticFile(...)} />` inside an `<AssetCard>` (shadow + tilt). |
| `background`| `<BackgroundLayer id="bg_grid_paper" />` — covers the frame behind everything, with slow Ken-Burns drift.    |
| `cutout`    | `<Img>` with alpha inside a `<DepthLayer>` (drop shadow, parallax offset).         |
| `loop`      | `<OffthreadVideo loop muted>` inside `<BackgroundLayer kind="loop">` (ambient).    |

Decision: **inline SVG for `svg-icon`/`accent`** (via a fetch-and-inline `<SvgAsset>`),
**`<Img staticFile>` for raster** (`hero-illustration`, `cutout`),
**`<OffthreadVideo>` for `loop`**. Inlining the SVG (not `<img src>`) is what lets the
agent animate `stroke-dashoffset`, recolor via `currentColor`, and spring individual
paths. All paths use `staticFile()` — never raw URLs (deterministic-render rule).

### 3.2 New shared component library — `src/components/asset-system/`

A *style-neutral* layer library (works across light/editorial aesthetics). These are the
"good design by construction" primitives.

```
src/components/asset-system/
  index.ts
  SvgAsset.tsx        # fetch + inline a generated SVG by element id; props: recolor, animateIn
  AssetCard.tsx       # raster element in a tilted card with thick drop shadow (house style)
  BackgroundLayer.tsx # background OR ambient loop as the bottom layer; enforces non-flat bg
  DepthLayer.tsx      # z-stacked wrapper: parallax offset + shadow → fakes depth from flat cutouts
  SceneGrid.tsx       # 6-col / 8-row safe-area grid; children snap to cells, never free-float
  StageFill.tsx       # dev-only: warns if a graphic stage is <X% filled (feeds QA, §4.4)
  useElement.ts       # resolve element id → {path, type, meta} from the project manifest
```

Key behaviors that *enforce* the design language:

- **`SceneGrid`** exposes a 6×8 grid with built-in safe margins (top 220 / bottom 440 /
  sides 60–130 px — the same numbers `still_grid.py --safezones` draws). Children are
  placed by `col/row/span`, not absolute pixels. **You cannot accidentally collide text
  with the unsafe UI bands or float an element in dead center with everything else empty**
  — the grid won't let you, and an unfilled grid is visibly sparse (caught by QA).
- **`BackgroundLayer`** *requires* either a `background`/`loop` element id or an explicit
  gradient/texture token. There is no "solid color" prop. This makes "flat single-color
  background" structurally awkward — the QA lint (§4.4) then makes it fail.
- **`DepthLayer`** auto-applies the house drop shadow (`4px 4px 0px`) and a small parallax
  translate so layered cutouts read as foreground/midground/background.
- **`AssetCard`** auto-applies the ±3–4° rotation + thick shadow from the house style.

These align with existing theme tokens (per-aesthetic palettes) — the
asset-system reads accent palettes from whichever theme the composition imports; it does
not introduce a competing color system.

### 3.3 Example consumption (matches the §1.5 scene)

```tsx
import { SceneGrid, BackgroundLayer, SvgAsset, DepthLayer } from "../components/asset-system";

const ThreeRisks: React.FC = () => (
  <BackgroundLayer id="bg_grid_paper">
    <SceneGrid>
      <SceneGrid.Cell col={1} row={2} span={6}>
        <!-- HyperFrames typography (HTML + CSS) — never baked into the image -->
        <ImpactWord text="3 WAYS IT LISTENS" />
      </SceneGrid.Cell>
      <SceneGrid.Cell col={1} row={4} span={2}>
        <SvgAsset id="ic_mic" animateIn="spring" />
      </SceneGrid.Cell>
      <SceneGrid.Cell col={3} row={4} span={2}>
        <SvgAsset id="ic_eye" animateIn="spring" />
      </SceneGrid.Cell>
      <SceneGrid.Cell col={5} row={4} span={2}>
        <SvgAsset id="ic_location" animateIn="spring" />
      </SceneGrid.Cell>
    </SceneGrid>
  </BackgroundLayer>
);
```

No hand-rolled `<svg>`. No flat background. Icons are real vectors from the studio,
recolored/animated in TSX. The grid guarantees placement in the safe area.

---

## 4. Teaching mechanism (the core ask)

Three of these four artifacts are *prose the agent reads*; the fourth (the QA gate) is
*checks the agent must pass*. Prose shapes intent; checks change behavior. We need both,
and the checks are what make the teaching durable rather than aspirational.

### 4.1 `docs/guides/DESIGN_LANGUAGE.md` (the spec)

A single canonical spec, linked from `CLAUDE.md`'s "Read-before-acting" list so it loads
every session. Sections (each written as **rules with numbers**, not vibes, so they can
double as lint assertions):

1. **Grid** — 6 cols × 8 rows, safe margins (220/440/60/130). Every element snaps to a
   cell. Min 2 occupied "regions" per graphic scene.
2. **Type scale** — title ≥56, subtitle ≥32, body/label ≥44 (from MEMORY.md); letter-
   spacing 2–6 on uppercase; max 2 brand cards per video.
3. **Color** — pull accents from the composition's theme tokens; each data card a unique
   accent; never two adjacent scenes the same flat hue. Background is **never** a single
   flat fill.
4. **Depth recipes** — every foreground element gets a `4px 4px 0px` shadow; cutouts go in
   a `DepthLayer`; ≥2 z-layers per graphic scene (bg + at least one mid/fore).
5. **Motion choreography** — bouncy springs (`damping 12–14`); reveal text **on** the
   spoken word; image changes every 2–5s; never 3 same-energy scenes in a row; hard cuts
   only (no crossfades).
6. **Density** — each graphic stage must fill ≥40% non-empty area (the StageFill metric).
   Dead center + empty edges = fail.
7. **Do / Don't** — explicit table (e.g. *Don't* inline a flat SVG when an `svg-icon`
   element exists; *Do* request it. *Don't* use glassmorphism (house rule)).

Every numeric in this doc is deliberately also a threshold in §4.4, so the prose and the
gate cannot drift.

### 4.2 Element catalog (`docs/guides/ELEMENT_CATALOG.md` — generated)

Auto-emitted by `asset_studio.manifest` from the shared + per-project manifests. For each
element: thumbnail (contact-grid tile), id, type, tags, style_ref, and the exact
`<SvgAsset id="…">` / `<BackgroundLayer id="…">` snippet to consume it. Regenerated by
`python3 tools/asset_studio/manifest.py --catalog`. This is how the agent *discovers what
already exists* (and reuses shared elements) instead of regenerating or hand-rolling.
It's the element-level analog of the existing `COMPONENT_CATALOG.md`.

### 4.3 Few-shot exemplars (`docs/guides/SCENE_EXEMPLARS.md`)

3–5 fully-worked "good scene" examples, each = scene JSON (`elements`) **+** the TSX that
consumes it **+** the contact-grid screenshot proving it passes the gate. At least one per aesthetic (e.g. line-art, editorial). These extend the existing `SCENE_SNIPPETS.md` philosophy
("check before reinventing") to the new element-driven pattern. The agent copies an
exemplar and swaps content, rather than starting from a blank stage.

### 4.4 QA gate (checks, not prose) — `tools/asset_studio/design_lint.py`

This is the enforceable core. Two complementary checks the agent **must** run and pass
before declaring a render done. Wired into `npm run lint` (static) and the existing
grid-review step (rendered).

#### (a) Static lint — `python3 tools/asset_studio/design_lint.py src/<Comp>.tsx`

AST/source checks on the composition + its scenes.json. Fails (non-zero exit) on:

- `LINT001 no-handrolled-svg` — a `<svg>`/`<path>` literal in a composition when an
  equivalent `svg-icon` element exists, or any inline `<svg>` with >1 `<path>` (icons
  must come from the studio).
- `LINT002 no-flat-background` — a scene root whose background is a single solid color
  (`backgroundColor: "#xxx"` with no `BackgroundLayer`/gradient/texture/loop).
- `LINT003 static-file-only` — any `<Img>`/`<Video>` `src` that isn't `staticFile()`.
- `LINT004 element-exists` — every `id` referenced by `SvgAsset`/`BackgroundLayer`/
  `useElement` resolves to a real file in the project/shared manifest.
- `LINT005 type-scale` — font sizes below the §4.1 minimums.
- `LINT006 safe-area` — absolutely-positioned text whose box enters the red unsafe bands.

#### (b) Rendered lint — extend `grid_review.py` / `still_grid.py` with `--rubric`

Operates on the contact-grid frames the QA step already produces. Computes per-frame
metrics and emits a pass/fail rubric so "scan the grid" becomes "the grid scores itself":

- `RUBRIC-FILL` — **every graphic stage must fill ≥40% non-empty** (variance/edge-density
  of the frame minus the caption band). Flat/empty frame → fail. (Implements §4.1 #6.)
- `RUBRIC-NO-OVERLAP` — detect two high-contrast text blocks whose bounding boxes overlap
  (connected-component analysis on the text band) → fail. ("No two text blocks may
  overlap.")
- `RUBRIC-NOT-FLAT` — frame color histogram entropy below threshold ⇒ flat single-color
  background → fail. (Catches what LINT002 misses at runtime, e.g. a loop that didn't
  load.)
- `RUBRIC-MOTION` — adjacent sampled frames identical for >Ns ⇒ frozen B-roll / single
  visual held too long → fail. (Reuses the existing "frozen B-roll" review heuristic.)
- `RUBRIC-DENSITY-RUN` — ≥3 consecutive scenes with near-identical fill/energy ⇒ pacing
  fail ("never 3 same-energy scenes in a row").

Output: a small JSON + an annotated grid (failing tiles boxed red), e.g.
`logs/<slug>_rubric.json` → `{ "pass": false, "fails": ["RUBRIC-FILL@22.4s", …] }`.

#### How it becomes a gate, not a suggestion

- `CLAUDE.md` render section gains a hard step: a render is **not done** until
  `design_lint.py` (static) exits 0 **and** `grid_review.py --rubric` reports `pass: true`.
  The agent loops fix→re-render→re-grid until green — exactly the loop `grid_review.py`'s
  docstring already describes, now with an objective stop condition.
- `npm run lint` calls `design_lint.py` so static violations also fail CI/`eslint+tsc`.
- The few-shot exemplars (§4.3) each ship with a passing `rubric.json`, so the agent has a
  concrete "what green looks like" reference.

### 4.5 Why this is durable

- **Spec** (DESIGN_LANGUAGE.md) loads every session via CLAUDE.md → intent is set.
- **Catalog** is generated from manifests → never goes stale, always reflects real assets.
- **Exemplars** give copy-paste starting points → low-friction good defaults.
- **Gate** is executable → the agent cannot *declare done* on a flat, sparse, or
  hand-SVG'd scene. Behavior is enforced by exit codes, not goodwill.

---

## 5. Rollout (informs the larger plan; not implemented here)

1. Add `asset_studio/models.py` registry + `studio.generate_element` for `svg-icon` and
   `background` only (highest-leverage: kills hand-rolled SVG + flat backgrounds).
2. Wire Phase 0.5 into `generate_assets.py`; extend `scenes_dryrun.py` cost table.
3. Ship `src/components/asset-system/` (`SvgAsset`, `BackgroundLayer`, `SceneGrid`).
4. Write `DESIGN_LANGUAGE.md`; generate first `ELEMENT_CATALOG.md`.
5. Add `design_lint.py` (static LINT001–006) to `npm run lint`.
6. Add `--rubric` to `grid_review.py`; convert one existing video as the first exemplar.
7. Add `cutout` + `loop` capabilities; promote shared backgrounds into
   `public/common/elements/`.

---

## Appendix — touch list (files this design adds or extends)

**Extend (no per-project scripts):**
- `tools/generate_assets.py` — Phase 0.5 ELEMENTS + `--elements-only`.
- `tools/scenes_dryrun.py` — element capability rows + cost.
- `tools/video_review/grid_review.py`, `still_grid.py` — `--rubric`.
- the asset-generation rule + `CLAUDE.md` — document `elements[]`, the gate.

**Add:**
- `tools/asset_studio/` (models, studio, cache, styleref, recolor, cost, manifest, design_lint).
- `src/components/asset-system/` (SvgAsset, AssetCard, BackgroundLayer, DepthLayer, SceneGrid, StageFill, useElement).
- `docs/guides/DESIGN_LANGUAGE.md`, `docs/guides/ELEMENT_CATALOG.md` (generated), `docs/guides/SCENE_EXEMPLARS.md`.
- `public/<slug>/elements/` + `public/common/elements/` output trees.
