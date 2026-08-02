# Quick Composition Guide

> **Read this first.** Everything needed to build a video composition in **HyperFrames** (HTML + GSAP) — editorial approach, pacing, structure, and code patterns.
>
> HyperFrames is the framework. Its conventions are authoritative — when this guide expresses an aesthetic opinion, that's the *project's editorial style*, not a rule that overrides the framework. For technical questions (timing, `data-*` attributes, the timeline contract), defer to the `/hyperframes` skill, `CLAUDE.md`, and `npx hyperframes docs <topic>`.

---

## The Editor's Mindset

Before writing any HTML, remember: **you are a YouTube video editor.** Your job is to make viewers stop scrolling. Your primary tools are:

1. **Typography** — Words on screen, synced to narration
2. **Real footage** — YouTube B-roll, talking head
3. **Timing** — When things appear and disappear
4. **Contrast** — Visual variety between scenes

Catalog blocks and components (data cards, lower-thirds, etc.) are useful for specific moments — but if more than 40% of your scenes lean on them, the video will feel robotic.

---

## File Locations

This is a HyperFrames project — a video is an HTML document, not a React app. Everything lives at the project root alongside `index.html`.

| What | Path |
|------|------|
| Root composition (entry point) | `index.html` |
| Sub-compositions (scenes) | `compositions/*.html` — loaded via `data-composition-src` |
| Catalog components / overlays | `compositions/components/*.html` |
| Assets (video, audio, images) | `assets/` — reference with relative paths |
| Source footage (read-only) | `raw/` |
| Per-project briefs & subtitles | `projects/<project-name>/` |
| Style profiles | `editing-styles/` |
| Workflow guides | `docs/guides/` |

Compositions are plain HTML files at the project root. There is no source directory, no central registry file, and no `public/` folder — you register each composition's timeline on `window.__timelines` and reference assets by relative path.

---

## Pacing — The Most Important Thing

### Visual Energy Levels

Assign an energy level to each scene:

| Energy | What It Looks Like | Duration |
|--------|-------------------|----------|
| **Rapid** | Word-by-word text, quick cuts, reaction clips | 0.5-1.5s per visual |
| **Medium** | Staggered lists, split screen, B-roll with overlay | 2-4s per visual |
| **Sustained** | Custom SVG animation, B-roll hold, talking head | 4-8s |
| **Breather** | Clean single word, section number, pause | 1-2s |

**Rule: Never have 3+ consecutive scenes at the same energy level.**

### The Modern Pacing Model

```
Section A (High Energy - 8 seconds):
  0.0s: B-roll full screen (2s)
  2.0s: Word "TOUCH" on B-roll (1.5s)
  3.5s: Talking head (1.5s)
  5.0s: Split: icon / TH (2s)
  7.0s: Split: hand X / TH (1s)

Section B (Breathing Room - 6 seconds):
  8.0s: Mini impact word "LIMITATION" (1.5s)
  9.5s: Staggered objects: tomato → glass → sponge (6.5s)

Section C (Buildup - 8 seconds):
  16.0s: B-roll + logo reveal (3s)
  19.0s: Title card typography (3s)
  22.0s: Custom SVG animation (2s)

Section D (Climax - 8 seconds):
  24.0s: Data labels popping in (4s)
  28.0s: Impact cascade: SEE → HEAR → FEEL (4s)

Section E (Resolution - 4 seconds):
  32.0s: CTA with particles (4s)
```

Notice the sections have different energies: high → breathing → buildup → climax → resolution. This is **narrative pacing**, not scene sequencing. Before implementing, declare your rhythm out loud (e.g. `fast-fast-SLOW-fast-SHADER-hold`) — see the `/hyperframes` beat-direction reference.

### The 2-3 Second Rule

Within any scene longer than 3 seconds, something must CHANGE:
- A new list item appears (a clip enters at a later `data-start`)
- A new element enters
- Text changes
- Camera drifts (Ken Burns — a slow `gsap.to()` scale/translate on a wrapper)
- A counter ticks
- A bar fills

If nothing moves after the initial animation, the viewer will leave.

---

## Scene Type Hierarchy

**Try these in order. Stop at the first one that fits:**

### Tier 1: Raw Typography (Use Most Often)
| Scene Type | When to Use |
|------------|-------------|
| Single word flash | Narrator says a key word — put JUST that word on screen |
| Word-by-word sentence build | Words accumulate one at a time, building a statement |
| Section number header | "1." with underline — chapter break between topics |
| Impact word cascade | Multiple keywords appearing and STAYING ("SEE" → "HEAR" → "FEEL") |

### Tier 2: Real Footage (Use Liberally)
| Scene Type | When to Use |
|------------|-------------|
| B-roll full bleed | YouTube footage fills entire screen, light vignette, text overlay |
| B-roll + typography | Full-screen footage with large text floating on top |
| Talking head | Speaker on camera, Ken Burns drift |
| Talking head + impact word | Speaker with emphasized word appearing |
| Talking head + floating symbols | Transparent overlay (math, code chars) over speaker |

### Tier 3: Editorial Compositions (Key Moments)
| Scene Type | When to Use |
|------------|-------------|
| Split screen (TH bottom) | Content top 55%, speaker bottom 45% |
| Staggered vertical list | Items stack vertically, revealing one by one |
| Editorial collage | Mixed media: cutout photos, icons, blob shapes, text at different sizes |
| Connected elements | Icons/logos connected by SVG curved lines |

### Tier 4: Data & Technical (Explanations)
| Scene Type | When to Use |
|------------|-------------|
| Custom SVG diagram | Animated technical illustration (the "signature scene") |
| Data card stack | Horizontal data rows with label + value + accent color |
| Progress/gauge | Animated fill bar or circular gauge |
| Comparison split | Screen divided showing two states |

### Tier 5: Catalog Components (Use Sparingly — 2-3 per video MAX)
HyperFrames ships ~111 pre-made blocks and components. Pull these in for specific moments instead of building them by hand. Browse with `npx hyperframes catalog`, install with `npx hyperframes add <name>`.

| Moment | Catalog Pick | When to Use |
|--------|--------------|-------------|
| Captions | `caption-highlight` (and 14 other caption styles) | Word-synced subtitles |
| Reaction / commentary | `x-post`, `reddit-post`, `macos-notification` | Quoting a post on screen |
| Social CTA (portrait) | `instagram-follow`, `tiktok-follow`, `spotify-card` | Follow prompt / closing |
| Code / terminal | `code-snippet-*` (24 themes) | Dev tutorials, command demos |
| Data | `data-chart`, `us-map*`, `world-map` | Stats and explainer segments |
| Device mockup | `vfx-iphone-device`, `ios26-liquid-glass` | App/product showcase |
| Branding | `logo-outro`, `app-showcase` | Outro / hero reveal |
| Finishing layers | `grain-overlay`, `vignette`, `shimmer-sweep` | Polish over any scene |
| Scene transitions | shader transitions (glitch, light-leak, whip-pan, …) | Cutting between two scenes |

See `COMPONENT_CATALOG.md` for the detailed registry walkthrough.

---

## Composition Structure

A composition is an **HTML file**: structure + `data-*` timing + a **paused** GSAP timeline registered on `window.__timelines` + CSS.

### Root composition (`index.html`)

The root div sits **directly in `<body>`** (no `<template>` wrapper on the root). It needs `data-composition-id`, `data-width`, and `data-height`. For short-form, use **1080×1920** (9:16). Render at **30fps** by default.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; }
    </style>
  </head>
  <body>
    <div data-composition-id="main" data-start="0" data-duration="40" data-width="1080" data-height="1920">

      <!-- BASE LAYER: talking head, mounted continuously. Wrap the video so we can
           animate the WRAPPER for Ken Burns (never animate the video element itself). -->
      <div id="th-wrap" style="position:absolute; inset:0; z-index:0;">
        <video id="th" data-start="0" data-track-index="0"
               src="assets/talking_head.mp4" muted playsinline
               style="width:100%; height:100%; object-fit:cover;"></video>
      </div>
      <!-- Audio is ALWAYS a separate element (never use video for audio) -->
      <audio id="th-audio" data-start="0" data-track-index="9"
             src="assets/talking_head.mp4" data-volume="1"></audio>

      <!-- OVERLAY SCENES: each is a sub-composition that occupies a time window.
           Same track-index can't overlap in time; use different indices for
           overlapping layers and set CSS z-index for stacking. -->
      <div id="s-broll" data-composition-id="broll" data-composition-src="compositions/broll-hook.html"
           data-start="2" data-duration="1.5" data-track-index="1" style="z-index:1;"></div>
      <div id="s-word" data-composition-id="word" data-composition-src="compositions/single-word.html"
           data-start="3.5" data-duration="1.5" data-track-index="1" style="z-index:1;"></div>

      <!-- CAPTIONS: install caption-highlight from the catalog, embed as a sub-comp -->
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/components/caption-highlight.html"
           data-start="0" data-duration="40" data-track-index="2" style="z-index:5;"></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });

      // Ken Burns on the talking-head WRAPPER (slow drift over the whole video)
      tl.fromTo("#th-wrap",
        { scale: 1.08, x: -15 },
        { scale: 1.14, x: 15, duration: 40, ease: "none" }, 0);

      // Final scene only may fade out
      tl.to("#th-wrap", { opacity: 0, duration: 1.5 }, 38.5);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
```

### Sub-composition (`compositions/single-word.html`)

Sub-comps **are** wrapped in `<template>`, load their own GSAP, and register their own timeline keyed by `data-composition-id`. Build the timeline **synchronously**. In sub-comps prefer `gsap.fromTo()` over `gsap.from()`. Reference root assets with `../`.

```html
<template id="single-word-template">
  <div data-composition-id="word" data-width="1080" data-height="1920">
    <div class="scene-content" style="width:100%;height:100%;display:flex;
         align-items:center;justify-content:center;padding:160px;box-sizing:border-box;">
      <h1 id="w" class="clip" data-start="0" data-duration="1.5" data-track-index="0"
          style="font-size:140px;font-weight:800;text-align:center;">TOUCH</h1>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#w", { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.1);
      window.__timelines["word"] = tl;
    </script>
  </div>
</template>
```

**Key contract points** (see the `/hyperframes` skill and `CLAUDE.md` for the full list):
- Every visible timed `img`/`div` needs `class="clip"`. **Omit** `class="clip"` on `<video>` and `<audio>`.
- `data-start` in seconds (or a clip-id reference like `"intro + 2"`). `data-duration` required for img/div/sub-comps; video/audio default to source length.
- `data-track-index` groups timeline overlap (same-track clips can't overlap in time). For visual stacking, set CSS `z-index` explicitly.
- Timelines are `{ paused: true }`, registered on `window.__timelines["<id>"]`, built synchronously.
- **Deterministic only:** no `Math.random()` (use a seeded PRNG), no `Date.now()`, no timers, no `repeat: -1` (compute a finite repeat count).

---

## Making Each Video Unique — For Real

**Uniqueness means different visual APPROACHES, not different colors on the same cards.**

If a `design.md` / `DESIGN.md` exists in the project, it is the source of truth for brand colors and fonts — use its exact values. The ideas below are the project's editorial guidance for varying *approach* within those brand constraints.

### What Real Variety Looks Like

For each video, design a completely different visual identity:

1. **Unique color palette** — Design colors that match the topic (stay in the light/neutral family unless `design.md` says otherwise):
   - Robotics: Cyan + Amber on warm white
   - AI/Tech: Electric blue + Green on light grey
   - Business: Deep purple + Gold on warm beige
   - Health: Teal + Coral on clean white

2. **Different scene type mix** — Each video should emphasize different visual approaches:
   - Tech explainer: Heavy custom SVG + B-roll + data visualization
   - Product review: Heavy B-roll + split screen + staggered lists
   - Opinion piece: Heavy talking head + impact words + typography
   - News story: Heavy B-roll + `x-post`/`reddit-post` cards + split screen

3. **Signature scene** — Every video needs at least ONE completely custom visual specific to its topic (custom SVG diagram, unique animation, topic-specific composition).

4. **Different animation vocabulary** — Don't use the same ease for everything. Vary at least 3 eases per scene:
   - Cinematic fade: `gsap.fromTo(el, {opacity:0}, {opacity:1, duration:0.6, ease:"power2.inOut"})`
   - Snappy pop: `ease:"back.out(2)"`
   - Smooth reveal: `ease:"power3.out"`
   - Bouncy: `ease:"elastic.out(1, 0.5)"`
   - Floating: a finite-repeat yoyo tween on `y` (e.g. `repeat: N, yoyo:true`)
   - Settle/overshoot: `ease:"back.out(1.7)"`

### What Fake Variety Looks Like (Don't Do This)
- Same background + dot grid + floating shapes on every scene with only a different accent color
- Same card layout with different icons
- Same ease on every element

---

## Common Errors & Fixes

### Error: "No composition found" / scene doesn't render
**Fix**: The root element needs `data-composition-id` (plus `data-width`/`data-height`). For sub-comps, also confirm `window.__timelines["<id>"]` is registered with a key that **exactly** matches the `data-composition-id`.

### Error: Sub-composition renders blank
**Fix**: Sub-comps must be wrapped in `<template>` and load their own GSAP. The **root** `index.html` must NOT wrap its composition in `<template>` (that hides everything). Build the timeline synchronously — never inside `async`/`setTimeout`/`Promise`.

### Error: Video/image doesn't appear (asset not found)
**Fix**: Asset path is wrong or the file isn't under the project root. Reference assets with relative paths from the project root (`assets/clip.mp4`); from inside a sub-comp use `../assets/clip.mp4`. There is no asset-resolution helper and no `public/` folder — paths resolve relative to the project on disk.

### Error: Lint flags `data-layer` / `data-end`
**Fix**: Those attributes are banned. Use `data-track-index` instead of `data-layer`, and `data-duration` instead of `data-end`.

### Error: Scene timing off
**Fix**: `data-start`/`data-duration` are in **seconds** (not frames). The frame clock is `time = floor(frame)/fps`, so just author in seconds. Confirm overlapping clips don't share a `data-track-index`.

### Error: Video has no sound / "video for audio"
**Fix**: Video must be `muted playsinline`. Audio is ALWAYS a separate `<audio>` element pointing at the same source. Never call `play()`/`pause()`/`seek()` — the framework owns playback.

### Error: Overlay covers talking head when it shouldn't
**Fix**: Overlay sub-comps only occupy their `data-start`→`data-start + data-duration` window. For a "talking-head-only" beat, simply leave no overlay clip in that window.

### Error: Ken Burns / overlay does nothing
**Fix**: Never animate a `<video>`'s width/height/top/left. Wrap the video in a non-timed `<div>` and animate the wrapper's transform.

---

## Pre-Flight Checklist

Before rendering:

- [ ] Assets in `assets/`, referenced with relative paths
- [ ] Root `index.html` has `data-composition-id` directly on a `<body>` div (no `<template>` on root)
- [ ] Every sub-comp registers `window.__timelines["<id>"]` (key matches `data-composition-id`)
- [ ] Every visible timed element has `class="clip"`; video/audio do NOT
- [ ] Timing covers the entire video duration; overlapping clips use different `data-track-index`
- [ ] Captions installed from catalog (`caption-highlight`) and synced
- [ ] Ken Burns applied to a wrapper, not the video element, with per-scene variation
- [ ] **Visual change every 2-3 seconds throughout**
- [ ] **No two consecutive scenes share the same visual approach**
- [ ] **At least 50% of scenes are NOT catalog components**
- [ ] **Unique color palette for this video** (within `design.md` if present)
- [ ] `npm run check` passes (lint + validate + inspect)

---

## Design Tips

- **Keep impact words off the edges** — inset content with padding (e.g. 15%+ from top). Never use `position:absolute; top:Npx` on a content container; use padding on `.scene-content`.
- **Ken Burns must be visible** — scale 1.08+, translate 15px+, on the wrapper. Use two cycle speeds for organic drift.
- **Vertical stack > horizontal row** — for 9:16, stack vertically.
- **Unique accent colors per card** — each item in a list gets its own color (within the palette family).
- **Mobile-first font sizes** — headlines 60px+, body 20px+, labels 16px+ (HyperFrames guardrail). For 9:16 short-form go larger: titles 80px+, body 44px+.
- **Avoid full-screen linear gradients** — they cause H.264 banding. Use radial gradients or a solid color with a localized glow.
- **Light video backgrounds on busy scenes** — drop a muted `<video>` behind text at reduced opacity, with Ken Burns on its wrapper.
- **Reusable backgrounds & finishing layers** — pull `grain-overlay`, `vignette`, or `shimmer-sweep` from the catalog. See `COMMON_ASSETS.md` for shared media.

---

## Next Steps

1. Start from `index.html` (or scaffold a fresh project with `npx hyperframes init`)
2. Use `SCENE_SNIPPETS.md` for copy-paste HTML+GSAP blocks (modern techniques listed first)
3. See `COMPONENT_CATALOG.md` for the catalog walkthrough and component details
4. Preview live with `npx hyperframes preview` (port 3002, keep it running in the background)
5. Validate with `npm run check`, then render with `npx hyperframes render -c index.html -o out/video.mp4`
