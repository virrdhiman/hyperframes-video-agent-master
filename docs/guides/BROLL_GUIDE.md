# B-Roll, Article References, and Photo Overlays Guide

## Overview

This guide explains how to add B-roll footage, article references, and photo overlays to your
HyperFrames videos. Sourcing is done with the **stock fetcher** under `tools/` (Pixabay /
Pexels); on screen, everything is plain HTML clips driven by the paused GSAP timeline.

> **Coming from Remotion?** There are no `<OffthreadVideo>` / `<Sequence>` / `staticFile()`
> wrappers here. A B-roll clip is a muted `<video>` element with `data-start` / `data-duration`
> / `data-track-index`; an overlay is a `<div class="clip">` with the same timing attributes.
> All media lives under `assets/`.

## Understanding B-Roll in HyperFrames

### What is B-Roll?

B-roll is supplementary footage that appears over or instead of the main video to:
- Illustrate what's being discussed
- Add visual interest
- Cover edits or transitions
- Provide context

### How B-Roll works on screen

Instead of a JS component that swaps the source per-frame, you lay B-roll clips on a **higher
track index** than the talking head. While a B-roll clip is "on" (its `data-start` →
`data-start + data-duration` window), it covers the talking head beneath it. The clip below
keeps playing; you just paint over it.

```html
<!-- Track 0: main talking head, full duration, muted (audio comes from a separate <audio>) -->
<video src="assets/stimulus/stimulus-short.mp4"
       muted playsinline
       class="clip" data-start="0" data-duration="130" data-track-index="0"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>

<!-- Track 1: a B-roll clip that covers the talking head from 24s to 32s -->
<video src="assets/stimulus/broll/spain-city.mp4"
       muted playsinline
       class="clip" data-start="24" data-duration="8" data-track-index="1"
       data-media-start="0"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
```

`data-media-start` chooses where inside the source file the clip begins. Add more `<video>`
clips on track 1 for each B-roll moment.

### B-Roll must be local (not external URLs) ⚠️

**External video URLs do not render reliably.** HyperFrames resolves every asset relative to
the project root and seeks it frame-by-frame in headless Chrome — a CDN URL that "works in
preview" will stall or fail during render. **Always download B-roll into `assets/` first.**
See [RENDER_FIX.md](./RENDER_FIX.md).

---

## Sourcing B-Roll with the stock fetcher

The repo ships a stock fetcher under `tools/` (Pixabay / Pexels). Use it to search and
**download** clips straight into `assets/`.

```bash
# Search + download B-roll for each segment into assets/stimulus/broll/
python tools/stock_fetcher/fetch.py \
  --query "spain madrid skyline" \
  --type video --min-width 1920 \
  --out assets/stimulus/broll/spain-city.mp4
```

Guidance:
- **Quality**: request `min-width 1920` for HD.
- **Local only**: download into `assets/` — never reference a CDN URL in the composition.
- **Rate limits**: Pixabay allows ~5000 requests/hour.

Once downloaded, point a `<video>` clip's `src` at the local path
(`assets/stimulus/broll/spain-city.mp4`).

---

## Adding Article References

Article references are citation boxes that show your sources. In HyperFrames they are just a
styled `<div class="clip">` placed on a high track index, animated in/out by the timeline.

### Basic pattern

```html
<!-- Citation box, top-right, visible 26s -> 32s -->
<div id="ref-spain" class="clip article-ref"
     data-start="26" data-duration="6" data-track-index="4"
     style="position:absolute; top:120px; right:40px; max-width:420px;
            background:#ffffff; color:#1a1a1a; border:2px solid #1a1a1a;
            border-radius:10px; padding:16px 20px; box-shadow:4px 4px 0 #1a1a1a">
  <div style="font-size:13px; font-weight:700; letter-spacing:.08em; color:#c0392b">
    SOURCE - FINANCIAL TIMES
  </div>
  <div style="font-size:22px; font-weight:700; margin-top:6px">
    Spain Launches &euro;10.5B Sovereign Wealth Fund
  </div>
  <div style="font-size:13px; color:#666; margin-top:6px">
    ft.com/content/spain-fund-2025
  </div>
</div>
```

```js
// Animate it in and out on the registered timeline
tl.from("#ref-spain", { opacity: 0, x: 40, duration: 0.4, ease: "back.out(1.7)" }, 26);
tl.to("#ref-spain",   { opacity: 0, x: 40, duration: 0.3, ease: "power2.in" }, 32 - 0.3);
tl.set("#ref-spain",  { opacity: 0, visibility: "hidden" }, 32);
```

### Fields to fill in

| Field | Required | Description |
|-------|----------|-------------|
| headline | ✅ | Article headline (the large line) |
| source | ✅ | Publication name (e.g. "Reuters") |
| url | ❌ | Optional URL to display |
| `data-start` | ✅ | When to show (seconds) |
| `data-duration` | ❌ (default 5) | How long to show (seconds) |
| position | ❌ (top-right) | Set via CSS `top/right/bottom/left` |
| thumbnail | ❌ | Optional `<img src="assets/...">` |

### Positions

Set with CSS on the box. Common anchors:
- **top-right** — `top:120px; right:40px` (default)
- **top-left** — `top:120px; left:40px`
- **bottom-right** — `bottom:160px; right:40px`
- **bottom-left** — `bottom:160px; left:40px`

---

## Adding Photo Overlays

Photo overlays show images of people, places, or things mentioned in the video — a framed
photo with a caption. Same idea: a `<div class="clip">` with an `<img>` and caption text.

### Basic pattern

```html
<!-- Photo card, center-right, visible 28s -> 33s -->
<div id="photo-madrid" class="clip photo-overlay"
     data-start="28" data-duration="5" data-track-index="3"
     style="position:absolute; top:50%; right:40px; transform:translateY(-50%);
            width:250px; background:#ffffff; padding:12px 12px 16px;
            border:2px solid #1a1a1a; box-shadow:4px 4px 0 #1a1a1a; rotate:-2deg">
  <img src="assets/stimulus/photos/madrid.jpg" alt="Madrid"
       style="width:100%; height:200px; object-fit:cover; display:block" />
  <div style="font-size:20px; font-weight:700; margin-top:10px; color:#1a1a1a">Madrid, Spain</div>
  <div style="font-size:13px; color:#666">Capital city</div>
</div>
```

```js
tl.from("#photo-madrid", { opacity: 0, scale: 0.9, duration: 0.4, ease: "back.out(1.7)" }, 28);
tl.to("#photo-madrid",   { opacity: 0, scale: 0.95, duration: 0.3, ease: "power2.in" }, 33 - 0.3);
tl.set("#photo-madrid",  { opacity: 0, visibility: "hidden" }, 33);
```

> Use a local image (`assets/stimulus/photos/madrid.jpg`). Download stock images into `assets/`
> with the stock fetcher just like B-roll — don't hotlink a CDN URL.

### Fields to fill in

| Field | Required | Description |
|-------|----------|-------------|
| image | ✅ | `<img src="assets/...">` (local) |
| caption | ✅ | Main text (e.g. person's name) |
| subcaption | ❌ | Secondary text (e.g. title) |
| `data-start` | ✅ | When to show (seconds) |
| `data-duration` | ❌ (default 6) | How long to show (seconds) |
| size | ❌ (medium) | small 180px / medium 250px / large 350px (set `width`) |
| position | ❌ (top-right) | Set via CSS |

### Sizes (set `width` on the card)
- **small** — 180px
- **medium** — 250px (default)
- **large** — 350px

### Fetching photos

```bash
python tools/stock_fetcher/fetch.py \
  --query "madrid spain skyline" --type photo --orientation horizontal \
  --out assets/stimulus/photos/madrid.jpg
```

---

## On-Screen Placement Analysis

### Current layout (frame at 11 seconds)
```
+-------------------------------------------+
| [STIMULUS NEWS]           [LIVE *]        | <- Top bar (40px from top)
|                                           |
| [Spain] <- Topic indicator                | <- 100px from top
|                                           |
|         [Talking Head Video]              |
|                                           |
|     [Subtitle Text Box]                   | <- 80px from bottom
| [BREAKING: News ticker ->->->]            | <- Bottom bar (0-50px)
+-------------------------------------------+
```

### Safe zones for overlays

**SAFE ZONES (won't overlap with UI):**
- **Top Right**: 120-500px from top, 40-450px from right
- **Center Right**: vertically centered, 40-450px from right
- **Bottom Right**: 120-200px from bottom, 40-450px from right

**AVOID:**
- Top 100px (news header + topic indicator)
- Bottom 80px (subtitles + news ticker)
- Left 40px (topic indicator)

### Recommended placement strategy

1. **Article References**: top-right (120px from top)
2. **Photo Overlays**: center-right (vertically centered)
3. **Both at once**: Article top-right, Photo bottom-right

---

## Complete Example: Enhanced Stimulus Video

A trimmed composition skeleton. Talking head on track 0, B-roll on track 1, photos on track 3,
citations on track 4. Light/neutral ground.

```html
<div id="root" data-composition-id="stimulus"
     data-width="1920" data-height="1080"
     data-start="0" data-duration="130"
     style="background:#f5f3ee">

  <!-- Audio: voice narration from the main take + a ducked music bed -->
  <audio src="assets/stimulus/stimulus-short.mp4" data-start="0" data-volume="1.0"></audio>
  <audio src="assets/common/music/bgm_ambient_loop.mp3"
         data-start="0" data-duration="130" data-volume="0.16"></audio>

  <!-- Track 0: talking head (muted; audio comes from the <audio> above) -->
  <video src="assets/stimulus/stimulus-short.mp4" muted playsinline
         class="clip" data-start="0" data-duration="130" data-track-index="0"
         style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>

  <!-- Track 1: B-roll segments -->
  <video src="assets/stimulus/broll/spain-city.mp4" muted playsinline
         class="clip" data-start="24" data-duration="8" data-track-index="1"
         style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
  <video src="assets/stimulus/broll/china-city.mp4" muted playsinline
         class="clip" data-start="58" data-duration="7" data-track-index="1"
         style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>

  <!-- Track 4: article references (see pattern above for each) -->
  <div id="ref-spain" class="clip article-ref" data-start="26" data-duration="6" data-track-index="4"
       style="position:absolute; top:120px; right:40px; max-width:420px; background:#fff;
              color:#1a1a1a; border:2px solid #1a1a1a; border-radius:10px; padding:16px 20px;
              box-shadow:4px 4px 0 #1a1a1a">
    <div style="font-size:13px; font-weight:700; color:#c0392b">SOURCE - FINANCIAL TIMES</div>
    <div style="font-size:22px; font-weight:700; margin-top:6px">Spain Launches &euro;10.5B Fund</div>
  </div>

  <!-- Track 3: photo overlays (see pattern above for each) -->
  <div id="photo-madrid" class="clip photo-overlay" data-start="32" data-duration="6" data-track-index="3"
       style="position:absolute; top:50%; right:40px; transform:translateY(-50%); width:250px;
              background:#fff; padding:12px 12px 16px; border:2px solid #1a1a1a;
              box-shadow:4px 4px 0 #1a1a1a; rotate:-2deg">
    <img src="assets/stimulus/photos/madrid.jpg" alt="Madrid"
         style="width:100%; height:200px; object-fit:cover; display:block" />
    <div style="font-size:20px; font-weight:700; margin-top:10px">Madrid, Spain</div>
  </div>
</div>

<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  tl.from("#ref-spain", { opacity: 0, x: 40, duration: 0.4, ease: "back.out(1.7)" }, 26);
  tl.to("#ref-spain",   { opacity: 0, x: 40, duration: 0.3, ease: "power2.in" }, 32 - 0.3);
  tl.set("#ref-spain",  { opacity: 0, visibility: "hidden" }, 32);

  tl.from("#photo-madrid", { opacity: 0, scale: 0.9, duration: 0.4, ease: "back.out(1.7)" }, 32);
  tl.to("#photo-madrid",   { opacity: 0, scale: 0.95, duration: 0.3, ease: "power2.in" }, 38 - 0.3);
  tl.set("#photo-madrid",  { opacity: 0, visibility: "hidden" }, 38);

  window.__timelines["stimulus"] = tl;
</script>
```

---

## Quick Start Checklist

- [ ] Fetch + download B-roll into `assets/`: `python tools/stock_fetcher/fetch.py ...`
- [ ] Add B-roll `<video>` clips on track 1 with `data-start` / `data-duration`
- [ ] Add article-reference `<div>`s for key claims (track 4)
- [ ] Add photo-overlay `<div>`s for mentioned entities (track 3)
- [ ] Preview: `npx hyperframes preview` (port 3002, keep running in background)
- [ ] Check: `npm run check` (lint + validate + inspect) — fix overflow / overlap
- [ ] Verify timing synchronization against subtitle timestamps
- [ ] Render: `npx hyperframes render -c stimulus.html -o out/stimulus.mp4`

---

## Notes

- **API Rate Limits**: Pixabay allows ~5000 requests/hour
- **Video Quality**: request `min-width 1920` for HD
- **Timing**: `data-start` is in seconds, matching subtitle timestamps
- **Local assets**: download everything under `assets/` — external URLs break renders
- **Determinism**: no `Math.random()` / `Date.now()` / network fetches in composition JS

---

## Troubleshooting

### B-Roll videos not showing / render fails
- Confirm the file exists under `assets/` and the `src` is a **relative path**, not a URL
- Make sure the clip has `class="clip"` plus `data-start` / `data-duration` / `data-track-index`
- Run `npx hyperframes validate` — it flags missing assets and unmuted video
- See [RENDER_FIX.md](./RENDER_FIX.md) for external-URL and asset-path issues

### Article references not showing
- Verify `data-start` is within the composition duration
- Check the box isn't off-canvas — run `npx hyperframes inspect`
- Ensure a matching exit tween + `tl.set(..., {opacity:0, visibility:"hidden"})` at the end

### Photos appear blurry
- Use a large source image and `object-fit: cover`
- Request `min-width` in the fetch; don't stretch a small image past its size
