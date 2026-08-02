# Agent Guide

This is the master guide for the AI agent operating in this **HyperFrames** workspace. Read this file first before taking any action.

> HyperFrames (HTML + GSAP → deterministic video) is the framework, and its conventions are authoritative. The editorial opinions in this guide — pacing, visual hierarchy, the project's working style — are *editorial guidance*, not technical overrides. On anything technical (timing model, `data-*` attributes, the timeline contract, rendering), defer to `CLAUDE.md`, the `/hyperframes` skill, and `npx hyperframes docs <topic>`.

---

## THE FIRST RULE: You Are a Video Editor, Not a UI Designer

Before you do anything else, understand this: **you are editing a YouTube video, not building a SaaS dashboard.** Every visual decision you make should answer one question: *"Would this make a viewer stop scrolling?"*

### The Editor's Test (Run Before Every Scene)
1. **Is this scene DIFFERENT from the previous one?** (layout, color, energy — not just different text in the same card)
2. **Would Ali Abdaal do this?** If it looks like a Figma prototype, redesign it.
3. **What's the SIMPLEST visual that creates this emotion?** (Often just a single word on screen)
4. **Does something CHANGE within this scene every 2-3 seconds?** (Not animate — change)
5. **Am I using real footage where it exists, instead of replacing it with a card?**

### The Project's Working Style (Editorial, Not Framework Law)
This is the look this workspace tends to aim for. It is the *project's* aesthetic preference — HyperFrames' own house style and any `design.md` in the project take precedence on specifics. If those are silent, lean this way: videos should feel organic, tactile, and assembled by a human rather than rendered by a corporate slide deck.

1. **Physics Over Pure Easing:** Don't ease everything with the same spline. Use eases that overshoot and settle (`back.out(1.7)`, `elastic.out(1, 0.5)`) so elements land naturally. Vary at least 3 eases per scene (a HyperFrames guardrail too).
2. **Continuous Imperfect Motion:** Elements needn't freeze after entering. Add subtle continuous float (a finite-repeat `yoyo` tween on `y`) and slight rotational wobble so things feel hand-held and alive. Keep repeats finite — never `repeat: -1`.
3. **Physical Materials:** Treat elements like physical objects — photos as Polaroids/prints (thick borders, uneven padding), text like marker on tape or paper cut-outs. Avoid wispy glows and heavy blur stacks (they also cause preview stutter and H.264 banding).
4. **Solid, Directional Shadows:** Prefer thick, directional drop shadows (e.g. `box-shadow: 4px 4px 0 #1a1a1a`) for physical depth over soft diffuse gradients.
5. **Imperfect Alignment:** Rotate elements slightly (`-3deg` to `3deg`) and stagger them. A perfectly aligned grid looks computer-made.

> This is a **light/neutral** project. Build on warm white, light grey, or beige grounds with bright accents.

### Your Visual Hierarchy (Try in This Order)
When deciding what to show on screen, go down this list and stop at the first one that fits:

1. **Raw Typography** — Single word or phrase on a clean background, synced to narration. THIS IS YOUR DEFAULT.
2. **Real Footage** — YouTube B-roll full-bleed with light vignette and text overlay. Let real footage do the work.
3. **Talking Head** — Speaker on camera with an optional impact word or floating symbols.
4. **Split Screen** — Content in top 55%, talking head visible in bottom 45%.
5. **Editorial Composition** — Staggered vertical list, collage layout, connected elements with SVG lines.
6. **Custom SVG/Diagram** — Technical illustration specific to this video's topic. The "signature scene."
7. **Data Visualization** — Horizontal data rows, progress bars, comparison splits (or catalog `data-chart`/`us-map*`).
8. **Catalog Components** — `caption-highlight`, `x-post`, `code-snippet-*`, etc. Use for 2-3 scenes MAX per video. NOT the default.

### What Bad Editing Looks Like (SaaS / Computer-Generated)
```
Scene 1: Soft glowing shadows + rounded glassmorphism cards
Scene 2: Talking head with a perfectly still floating logo
Scene 3: Perfectly aligned grid of cards with identical easing entries
Scene 4: Talking head
Scene 5: Generic SaaS-style metric cards with blur filters
...every element is perfectly straight, rigidly animated, and looks like a web app.
```

### What Good Editing Looks Like
```
0.0s: YouTube B-roll fills screen — light vignette, slow Ken Burns
2.0s: Single word "TOUCH" fades in over B-roll — 96px, centered
3.5s: Cut to talking head — Ken Burns drift right
5.0s: Split screen — top: eye icon / bottom: talking head
7.0s: Split screen — top: hand icon with red X / bottom: talking head
9.0s: Impact word "LIMITATION" over talking head — wobble
11.0s: Three objects stagger vertically — tomato, glass, sponge
14.0s: B-roll + Meta logo floating reveal
17.0s: "DIGIT 360" — massive typography, accent line draws in
20.0s: Custom SVG: fingertip cross-section with sensors lighting up
25.0s: Data labels slide in: PRESSURE 2.4N / TEXTURE Smooth / SHAPE Spherical
30.0s: Impact cascade: SOFT → SLIPPERY → ROUGH → FRAGILE
33.0s: Split screen — staggered app icons with connector lines
38.0s: Impact sequence — "SEE" → "HEAR" → "FEEL" on a video background
43.0s: CTA with animated particles
```

No two consecutive scenes share the same visual approach. THAT is editing.

---

## BEFORE CREATING A COMPOSITION

**Invoke the `/hyperframes` skill first** — it encodes the framework-specific patterns (the `window.__timelines` contract, `data-*` semantics, layout-before-animation, scene-transition rules) that generic web knowledge does not have. Then read the creative guides:

1. `QUICK_COMPOSITION_GUIDE.md` — composition structure, pacing patterns, scene hierarchy
2. `SCENE_SNIPPETS.md` — copy-paste HTML+GSAP blocks for EVERY scene type (modern techniques first, then catalog components)
3. `COMPONENT_CATALOG.md` — the catalog walkthrough and component details (when you need a specific block)
4. `index.html` — the root composition; copy its structure or `npx hyperframes init` a fresh project

If a `design.md` / `DESIGN.md` exists in the project, read it first — it is the source of truth for brand colors and fonts, and overrides the project working-style notes above.

---

## Project Overview

This workspace is for AI-assisted video production using **HyperFrames** — HTML + GSAP compiled into deterministic, frame-by-frame video. The agent ingests raw footage, generates assets, composes videos as HTML, and renders finished content. No React, no proprietary timeline format: a video is an HTML document whose elements carry `data-*` timing and are animated by a paused GSAP timeline registered on `window.__timelines`.

---

## Directory Structure

Single repository — everything lives at the project root alongside `index.html`.

```
<project-root>/
├── CLAUDE.md / AGENTS.md   ← Authoritative project + agent rules (read first)
├── index.html              ← Root composition (root timeline)
├── compositions/           ← Sub-compositions (scenes) via data-composition-src
│   └── components/          ← Installed catalog components / overlays
├── assets/                 ← Media (video, audio, images) — referenced by relative path
├── raw/                    ← Source footage (read-only)
├── editing-styles/         ← Style profiles (e.g. organic_minimalist_explainer.md)
├── projects/               ← Per-project briefs and subtitles
├── docs/guides/            ← All workflow MD guides (this file, snippets, catalog, …)
├── tools/                  ← AI/utility tool scripts (asset generation, fetching, captions)
│   ├── image_generator/    ← Image generation (Imagen, background remover)
│   ├── video_generator/    ← AI video (Veo)
│   ├── caption_generator/  ← Subtitle/caption creation
│   ├── stock_fetcher/      ← Stock media (Pexels, YouTube, Google Images)
│   ├── audio_generator/    ← Music / SFX
│   └── export/             ← Packaging for upload
├── meta.json               ← Project metadata (id, name)
├── hyperframes.json        ← Registry + path config (blocks/components/assets)
├── package.json            ← npm run dev / check / render / publish
└── transcript.json         ← Whisper word-level transcript (if generated)
```

There is no source directory, no central registry file, and no `public/` folder. Compositions are HTML files; assets live in `assets/` and are referenced by relative path (from a sub-comp, `../assets/...`).

---

## Folder Conventions

### `raw/`
- Drop source footage here. Never modify — read-only.

### `assets/`
- All media the compositions reference: video, audio, images.
- Reference with relative paths (`assets/clip.mp4`; `../assets/clip.mp4` from a sub-comp). No asset-resolution helper is needed — paths resolve relative to the project on disk.

### `projects/`
- One subfolder per project: `projects/<project-name>/`
- Holds editing briefs, subtitles JSON, notes.

### `editing-styles/`
- Reusable style profiles (e.g. `organic_minimalist_explainer.md`, `physical_tech_explainer.md`). Pick one per project to set tone — within whatever a `design.md` mandates.

### `tools/`
**Auth:** Google AI tools use `GOOGLE_API_KEY` from `.env` with fallback to `cred.json`. No extra setup needed.

**Active tools:**

| Script | Tool | Output | Default Output Dir |
|---|---|---|---|
| `tools/image_generator/imagen.py` | Google Nano Banana 2 | PNG images | `assets/` |
| `tools/image_generator/background_remover.py` | Replicate background-remover | Transparent PNG | `assets/` |
| `tools/video_generator/veo.py` | Google Veo 3.1 | MP4 videos (4-8s) | `assets/` |
| `tools/stock_fetcher/pexels.py` | Pexels (stock photos + videos) | JPEG/MP4 | `assets/` |
| `tools/stock_fetcher/youtube.py` | Serper.dev + yt-dlp (YouTube search & download) | MP4 + SRT | `assets/` |
| `tools/stock_fetcher/google_images.py` | Serper.dev Google Images | JPEG/PNG/WebP | `assets/` |

**Secrets:** `.env` and `cred.json` at project root — in `.gitignore`, never commit.

**Quick usage:**
```bash
# Generate a 9:16 image (Nano Banana 2)
python3 tools/image_generator/imagen.py --prompt "your prompt" --ratio 9:16

# Edit an existing image
python3 tools/image_generator/imagen.py --prompt "make background lighter" --image assets/photo.png

# Use yourself in a generated image
python3 tools/image_generator/imagen.py --prompt "person presenting at a conference" --ref-image assets/me.jpg

# Generate an infographic
python3 tools/image_generator/imagen.py --prompt "how neural networks work" --infographic --ratio 16:9

# Generate a 9:16 video (Veo 3.1, takes 2-5 min)
python3 tools/video_generator/veo.py --prompt "your prompt" --ratio 9:16 --duration 8

# Download stock photo from Pexels
python3 tools/stock_fetcher/pexels.py --query "your search" --type photo --ratio 9:16

# Remove background from an image (transparent PNG)
python3 tools/image_generator/background_remover.py --input assets/portrait.jpg

# Download stock video from Pexels
python3 tools/stock_fetcher/pexels.py --query "your search" --type video --ratio 16:9 --count 2

# Search Google Images and list results
python3 tools/stock_fetcher/google_images.py -q "company logo png transparent" --list

# Download top 3 Google Images results
python3 tools/stock_fetcher/google_images.py -q "brand logo png" -n 3 --prefix logo

# Search YouTube and list results
python3 tools/stock_fetcher/youtube.py --query "your search" --list

# Download YouTube video, smart-trim to where a topic is discussed
python3 tools/stock_fetcher/youtube.py --query "product review" --topic "feature name" --duration 8

# Download YouTube Short for vertical b-roll
python3 tools/stock_fetcher/youtube.py --query "your search" --shorts -n 1
```

See each tool's `README.md` for full argument reference.

### `compositions/` — HyperFrames Scenes

- `index.html` (project root) — the root composition / root timeline.
- `compositions/*.html` — sub-compositions (scenes), referenced from the root via `data-composition-src`.
- `compositions/components/*.html` — installed catalog components and reusable overlays.

Each composition is HTML + `data-*` timing + a paused GSAP timeline on `window.__timelines` + CSS. Build the end-state layout first (layout before animation), then add entrances.

#### Catalog Components (Installed On Demand)
HyperFrames ships ~111 pre-made blocks and components. Don't hand-build what already exists.

```bash
npx hyperframes catalog                 # browse the registry
npx hyperframes catalog --tag caption-style --json
npx hyperframes add caption-highlight    # install into compositions/components/
```

Useful families: 15 caption styles (`caption-highlight` is the default social caption), shader transitions, social overlays (`x-post`, `reddit-post`, `instagram-follow`, `tiktok-follow`, `spotify-card`), code/terminal (`code-snippet-*`), data viz (`data-chart`, `us-map*`, `world-map`), device mockups (`vfx-iphone-device`, `ios26-liquid-glass`), and finishing layers (`grain-overlay`, `vignette`, `shimmer-sweep`). For anything not in the catalog, author custom HTML/GSAP.

#### Rendering & Preview
```bash
npx hyperframes preview                                  # Studio live server, hot reload (port 3002)
npx hyperframes render -c index.html -o out/video.mp4    # render the root composition
npx hyperframes render -c compositions/scene3.html -o out/scene3.mp4   # render one scene to review
```

`npx hyperframes preview` is a **long-running** server — run it in the **background** and keep it alive while you edit. `npm run dev` wraps it. Visual output in preview matches the render exactly (though preview can stutter on heavy paint; the render is always clean).

#### Mandatory scene-level review before full render
Every newly built scene must be previewed (or snapshotted with `npx hyperframes snapshot --at <t>`) and reviewed for motion quality, space usage, mobile legibility, and visual consistency before the full render.

#### HyperFrames Authoring Rules (Non-Negotiable)

- Root `index.html` puts `data-composition-id` on a `<body>` div directly — **no `<template>` on the root**. Sub-comps wrap content in `<template>`.
- Every timed visible `img`/`div` needs `data-start`, `data-duration`, `data-track-index`, and `class="clip"`. **Omit** `class="clip"` on `<video>`/`<audio>`.
- Timing is in **seconds**. `data-track-index` groups timeline overlap (same track can't overlap in time); set CSS `z-index` for visual stacking.
- Every composition registers a **paused** timeline: `window.__timelines["<id>"] = gsap.timeline({ paused: true })`. Build it **synchronously** (never inside `async`/`setTimeout`/`Promise`).
- **Continuous base track**: keep A-roll (talking head) mounted continuously; layer overlay scenes on top via separate sub-comps occupying time windows.
- **Video/audio**: video must be `muted playsinline`; audio is ALWAYS a separate `<audio>` element. Never call play/pause/seek — the framework owns playback.
- **Ken Burns**: never animate a `<video>`'s width/height/top/left. Wrap it in a non-timed `<div>` and animate the wrapper's transform (scale 1.08+, translate 15px+; two cycle speeds for organic drift).
- **Split screen**: top/bottom for 9:16 — content top (55%), talking head bottom (45%). Push the speaker's face into the visible area with a `translateY` on the wrapper.
- **B-roll playback**: short clips loop automatically across their window; keep them muted.
- **Captions**: install a caption component (`caption-highlight`) from the catalog and embed it as a sub-comp synced to the transcript.
- **Scene transitions**: ALWAYS transition between scenes (no jump cuts); entrance-animate every element with `gsap.from()`/`fromTo()`; NEVER exit-animate before a transition (the transition IS the exit); only the FINAL scene may fade out.
- **Determinism**: no `Math.random()` (seeded PRNG only), no `Date.now()`, no timers, no `repeat: -1` (finite repeats only).
- **Banned attributes**: `data-layer` (use `data-track-index`), `data-end` (use `data-duration`).
- **Mobile-first sizing**: HyperFrames guardrails are headlines 60px+, body 20px+, labels 16px+. For 9:16 short-form go larger: titles 80px+, body 44px+. Use `font-variant-numeric: tabular-nums` on number columns.

---

## Editing Brief System

Every video project needs an **editing brief** — a shot-by-shot document that plans what to show at each moment.

### Senior editor gate (required)
Before editing starts, validate:
- Hook strength, narrative arc, and payoff
- **Visual variety** — no two consecutive scenes with the same approach
- **Pacing rhythm** — mix of rapid, medium, sustained, and breather energies
- Scene types prioritize raw typography and B-roll over catalog components
- At least one "signature scene" custom to this video's topic
- Style profile fits this specific video's context

### Style-adaptive editing
- Select a style profile per project (from `editing-styles/`), within any `design.md` constraints
- Choose visual approaches based on the content, not by defaulting to cards
- At least 50% of scenes should NOT use catalog components
- Design a unique color palette for each video (light/neutral family)

### Templates
- `projects/EDITING_BRIEF_TEMPLATE.md` — copy into each new project folder

### How to use
1. Create `projects/<project-name>/`
2. Copy template, fill in every section
3. The brief defines shot types, visual sources, visual energy levels, and typography styles
4. Plan visual changes every 2-3 seconds within longer scenes

---

## Agent Workflow — Standard Steps

1. **Ingest** — Copy source footage into `raw/`
2. **Transcribe** — If no transcript exists, generate one (`npx hyperframes transcribe <file>`); if you have one, skip
3. **Parse captions** — Convert SRT to JSON for caption sync:
   ```bash
   python3 tools/caption_generator/parse_srt.py raw/<file>.srt \
     --out projects/<project-name>/subtitles.json
   ```
4. **Read the script and feel it** — Before planning visuals, identify emotional peaks, lists, transitions, and breathing moments
5. **Plan** — Create editing brief. Assign visual energy (RAPID/MEDIUM/SUSTAINED/BREATHER) to each section. Declare scene rhythm. Plan for visual change every 2-3 seconds.
6. **Senior editor review** — Check variety, pacing, visual hierarchy. No editing until approved.
7. **Fetch/generate assets**:
   - **YouTube B-roll** (preferred for real product footage): `tools/stock_fetcher/youtube.py`
   - **Google Images** (logos, portraits): `tools/stock_fetcher/google_images.py`
   - **Background removal** (cutouts for editorial collage): `tools/image_generator/background_remover.py`
   - Stock media: `tools/stock_fetcher/pexels.py`
   - AI images: `tools/image_generator/imagen.py`
   - AI videos (abstract only): `tools/video_generator/veo.py`
   - Save to `assets/`
8. **Compose** — Invoke `/hyperframes`, then build the composition using the visual hierarchy. Start with raw typography and B-roll; install catalog components only when nothing simpler fits. Build layout before animation.
9. **Preview/review each scene** — Use `npx hyperframes preview` (background) or `snapshot --at <t>` and review.
10. **Validate** — Run the full check:
    ```bash
    npm run check        # lint + validate + inspect
    ```
    Fix all lint/validate errors and review inspect warnings before rendering.
11. **Render full video**:
    ```bash
    npx hyperframes render -c index.html -o out/<project-name>_v1.mp4
    ```
12. **Final QA** — Safe areas, subtitle timing, legibility, pacing rhythm, WCAG contrast (`validate` runs this).
13. **Clean up** — Clear scratch artifacts.

---

## Key Rules for the Agent

- **Think like an editor** — Your primary tools are typography, real footage, timing, and contrast. Catalog components are a fallback.
- **Invoke the `/hyperframes` skill** before writing or editing any composition HTML.
- **Visual change every 2-3 seconds** — Something must change on screen (new word, new element, new layout)
- **No two consecutive scenes** with the same visual approach
- **At least 50% of scenes** should NOT use catalog components
- **At least 1 signature scene** that's custom to this video's topic (custom SVG, unique animation)
- **Design a unique color palette** per video (light/neutral family) — within any `design.md`
- **Prefer real footage over AI** — Use YouTube B-roll for product demos. Use AI video only for abstract visuals.
- **Never modify** anything in `raw/`
- **Reference assets by relative path** — `assets/...` (or `../assets/...` from a sub-comp). No asset-resolution helper, no `public/`.
- **Determinism is mandatory** — no `Math.random()`/`Date.now()`/timers/`repeat: -1`/network fetch at render time
- **Mandatory scene preview/snapshot** before full render
- **`npm run check` must pass** before rendering
- **Senior editor approval** required before editing begins

---

## Repo hygiene & scratch artifacts

### Workflow docs

All guides live in `docs/guides/` (this file, `QUICK_COMPOSITION_GUIDE.md`, `SCENE_SNIPPETS.md`, `COMPONENT_CATALOG.md`, `BROLL_GUIDE.md`, `COMMON_ASSETS.md`, and others). `README.md` in that folder links them for discoverability.

### Scratch & temp output
- Render outputs go to `out/` (create as needed). Keep one-off experiments out of `compositions/` so `lint`/`validate` only see real scenes.
- Tool runs that produce logs should write them somewhere ignored by git; never commit `.env` or `cred.json`.

### Validation gate
Before considering any composition task complete, run `npm run check` (lint + validate + inspect) and fix every error. Diagnose environment issues (FFmpeg, Chrome) with `npx hyperframes doctor`.
