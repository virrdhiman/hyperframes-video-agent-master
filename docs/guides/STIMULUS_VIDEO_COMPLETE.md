# Stimulus Video - Project Complete

End-to-end write-up of the Stimulus / macro news video: what was missing, what got built, and
how to extend and render it in **HyperFrames**.

## Project Analysis Summary

### What was missing

After analyzing the Stimulus video project, these issues were identified and fixed:

1. ❌ **B-roll videos failing to load** — external CDN URLs were unreliable
2. ❌ **Missing audio narration** — the main take's voice track wasn't wired in
3. ❌ **No article reference system** — needed reusable source-citation overlays
4. ❌ **No photo overlay system** — needed framed photo overlays for people/places
5. ❌ **No stock-media workflow** — no repeatable way to fetch B-roll and photos

### What's now complete

✅ **All B-roll fixed** — downloaded locally into `assets/` and played as muted `<video>` clips
✅ **Audio narration added** — voice track plays via a separate `<audio>` element
✅ **Article-reference pattern** — styled `<div class="clip">` citation boxes on a high track
✅ **Photo-overlay pattern** — framed photo cards with caption/subcaption
✅ **Stock fetcher workflow** — `tools/stock_fetcher/` pulls videos/images into `assets/`
✅ **Documentation** — full guide in [BROLL_GUIDE.md](./BROLL_GUIDE.md)

---

## Current Video Structure

### Timeline (2 minutes 10 seconds)

| Time | Content | B-Roll | Overlays Available |
|------|---------|--------|-------------------|
| 0:00-0:18 | Global Overview | Talking head | - |
| 0:18-0:52 | **Spain** segment | Madrid skyline (24-32s), Stock charts (40-47s) | Article refs, Photos |
| 0:52-1:18 | **China** segment | Great Wall (58-65s), Healthcare (65-72s) | Article refs, Photos |
| 1:18-1:37 | **USA** segment | Capitol (78-85s), Money counting (85-92s) | Article refs, Photos |
| 1:37-2:10 | **Global Outlook** | Global business (97-104s), AI/Tech (104-110s) | Article refs, Photos |

### Visual layers (track index)

Higher `data-track-index` paints on top. The talking head sits on track 0; B-roll covers it on
track 1; overlays stack above.

```
+-------------------------------------------+
| [Top Bar: STIMULUS NEWS]    [LIVE]        | <- track 6: Header
|                                           |
| [Topic: Spain]                            | <- track 5: Topic indicator
|                                           |
|               [VIDEO]                     | <- track 0/1: talking head / B-roll
|         (or B-roll footage)               |
|                                           |
|                    [Article Reference]    | <- track 4: Article citations
|                    [Photo Overlay]        | <- track 3: Photo frames
|                                           |
|        [Subtitle Text Box]                | <- track 2: Subtitles
| [Ticker: BREAKING NEWS ->->->]            | <- track 7: News ticker
+-------------------------------------------+
```

---

## Technical Implementation

### Files / building blocks

1. **`tools/stock_fetcher/`** — stock media workflow
   - Search + download videos and photos (Pixabay / Pexels) straight into `assets/`
   - Pre-defined queries per Stimulus topic
   - Run with: `python tools/stock_fetcher/fetch.py --query "..." --type video --out assets/...`

2. **Article-reference pattern** — citation overlay (see [BROLL_GUIDE.md](./BROLL_GUIDE.md))
   - A `<div class="clip">` on track 4 with source line + headline
   - Animated entrance/exit on the timeline; 4 corner positions via CSS

3. **Photo-overlay pattern** — framed photo display
   - A `<div class="clip">` on track 3 wrapping a local `<img>` + caption
   - `back.out(1.7)` pop-in, deterministic kill at the end
   - 3 sizes (set `width`), 6 positions (set CSS anchors)

4. **`compositions/` + `index.html`** — the composition itself
   - Root carries `data-composition-id="stimulus"` and a paused GSAP timeline registered on
     `window.__timelines["stimulus"]`

### Key fixes applied

#### 1. B-Roll videos (FIXED)

**Before** — external URL that fails during render:
```html
<video src="https://cdn.example.com/video/spain.mp4" ...></video>
```

**After** — local file under `assets/`, played as a muted clip on track 1:
```html
<video src="assets/stimulus/broll/spain-city.mp4" muted playsinline
       class="clip" data-start="24" data-duration="8" data-track-index="1"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
```

#### 2. Audio narration (ADDED)

**Before** — talking-head video on screen but no voice (a muted `<video>` carries no audio):
```html
<!-- video plays, but nothing is heard -->
<video src="assets/stimulus/stimulus-short.mp4" muted playsinline class="clip"
       data-start="0" data-duration="130" data-track-index="0"></video>
```

**After** — add a separate `<audio>` element for the voice track (and a ducked music bed):
```html
<video src="assets/stimulus/stimulus-short.mp4" muted playsinline class="clip"
       data-start="0" data-duration="130" data-track-index="0"></video>

<!-- voice narration pulled from the same source file -->
<audio src="assets/stimulus/stimulus-short.mp4" data-start="0" data-volume="1.0"></audio>
<!-- background music, ducked under speech -->
<audio src="assets/common/music/bgm_ambient_loop.mp3"
       data-start="0" data-duration="130" data-volume="0.16"></audio>
```

---

## How to Add Article References

A citation box is a timed `<div class="clip">` on track 4, animated in/out on the timeline.

```html
<div id="ref-spain" class="clip article-ref"
     data-start="26" data-duration="6" data-track-index="4"
     style="position:absolute; top:120px; right:40px; max-width:420px;
            background:#fff; color:#1a1a1a; border:2px solid #1a1a1a;
            border-radius:10px; padding:16px 20px; box-shadow:4px 4px 0 #1a1a1a">
  <div style="font-size:13px; font-weight:700; color:#c0392b">SOURCE - FINANCIAL TIMES</div>
  <div style="font-size:22px; font-weight:700; margin-top:6px">
    Spain Launches &euro;10.5B Sovereign Wealth Fund
  </div>
  <div style="font-size:13px; color:#666; margin-top:6px">ft.com/content/spain-fund-2025</div>
</div>
```

```js
tl.from("#ref-spain", { opacity: 0, x: 40, duration: 0.4, ease: "back.out(1.7)" }, 26);
tl.to("#ref-spain",   { opacity: 0, x: 40, duration: 0.3, ease: "power2.in" }, 32 - 0.3);
tl.set("#ref-spain",  { opacity: 0, visibility: "hidden" }, 32);
```

### Visual result

```
+-------------------------------------------+
| [STIMULUS NEWS]              [LIVE]        |
|                                           |
| [Spain]            +------------------+   |
|                    | Source: FT       |   |
|                    | Spain Launches   |   |
|        [VIDEO]     | EUR 10.5B Fund.. |   |
|                    +------------------+   |
|                                           |
|    [Governments and international...]     |
| [BREAKING: Spain launches EUR 10.5B...]   |
+-------------------------------------------+
```

---

## How to Add Photo Overlays

A framed photo is a timed `<div class="clip">` on track 3 wrapping a local `<img>`.

```html
<div id="photo-madrid" class="clip photo-overlay"
     data-start="28" data-duration="5" data-track-index="3"
     style="position:absolute; top:50%; right:40px; transform:translateY(-50%); width:250px;
            background:#fff; padding:12px 12px 16px; border:2px solid #1a1a1a;
            box-shadow:4px 4px 0 #1a1a1a; rotate:-2deg">
  <img src="assets/stimulus/photos/madrid.jpg" alt="Madrid"
       style="width:100%; height:200px; object-fit:cover; display:block" />
  <div style="font-size:20px; font-weight:700; margin-top:10px">Madrid, Spain</div>
  <div style="font-size:13px; color:#666">Capital city</div>
</div>
```

```js
tl.from("#photo-madrid", { opacity: 0, scale: 0.9, duration: 0.4, ease: "back.out(1.7)" }, 28);
tl.to("#photo-madrid",   { opacity: 0, scale: 0.95, duration: 0.3, ease: "power2.in" }, 33 - 0.3);
tl.set("#photo-madrid",  { opacity: 0, visibility: "hidden" }, 33);
```

### Fetching images into `assets/`

```bash
python tools/stock_fetcher/fetch.py \
  --query "madrid spain skyline" --type photo --orientation horizontal \
  --out assets/stimulus/photos/madrid.jpg
```

---

## Screen Placement Guidelines

### Safe zones (won't overlap UI)

```
+-------------------------------------------+
| AVOID: 0-120px                            | <- Header + Topic
|                                           |
|           SAFE ZONE                       |
|        (120-500px from top)               |
|                                           |
|           CENTER-RIGHT                     |
|        (vertically centered)              |
|                                           |
|           SAFE ZONE                       |
|        (120-200px from bottom)            |
| AVOID: bottom 120px                       | <- Subtitles + Ticker
+-------------------------------------------+
```

### Recommended placement strategy

| Element Type | Best Position | Reasoning |
|--------------|---------------|-----------|
| Article Reference | top-right | Doesn't block face, above subtitles |
| Photo Overlay | center-right | Most visible, clear of all UI |
| Both together | Article top-right, Photo bottom-right | Separated vertically |

---

## Quick Start Guide

### 1. Fetch + download B-roll (into `assets/`)

```bash
python tools/stock_fetcher/fetch.py \
  --query "spain madrid skyline" --type video --min-width 1920 \
  --out assets/stimulus/broll/spain-city.mp4
```

Add a muted `<video>` clip on track 1 for each downloaded file.

### 2. Add article references (optional)

Drop the article-reference `<div class="clip">` (track 4) plus its timeline tweens — see above.

### 3. Add photo overlays (optional)

Drop the photo-overlay `<div class="clip">` (track 3) wrapping a local `<img>` — see above.

### 4. Preview

```bash
# Long-running Studio server on port 3002 — keep it alive in the background
npx hyperframes preview
```

### 5. Check before rendering

```bash
npm run check   # lint + validate + inspect
```

Fix all errors; review inspect warnings (overflow / off-canvas).

### 6. Render final video

```bash
npx hyperframes render -c stimulus.html -o out/stimulus-news.mp4

# Reproducible (CI / team / agent):
npx hyperframes render -c stimulus.html -o out/stimulus-news.mp4 --docker
```

---

## Current Status

### Working pieces

- [x] Talking head video (1920x1080), muted on track 0
- [x] Audio narration (voice-over via a separate `<audio>` element)
- [x] Background music (low volume, ducked under speech)
- [x] 8 B-roll segments (downloaded locally, on track 1)
- [x] Animated news header ("STIMULUS NEWS" + "LIVE")
- [x] Topic indicators (Spain, China, USA, Global)
- [x] Synchronized subtitles (19 groups, news style)
- [x] Scrolling news ticker (bottom bar)
- [x] Article-reference pattern (ready to reuse)
- [x] Photo-overlay pattern (ready to reuse)
- [x] Stock fetcher workflow (videos + images into `assets/`)

### Optional enhancements

- [ ] Add 3-5 article references for key claims
- [ ] Add 3-5 photo overlays for mentioned locations
- [ ] Add transition SFX between talking head and B-roll
- [ ] Add a lower-third name card for the presenter
- [ ] Add animated charts for statistics

---

## Verification (preview + snapshot)

Capture key frames without a full render to spot-check the layout:

```bash
npx hyperframes snapshot -c stimulus.html --at 11,43,63
```

### Frame at 11 seconds
- Header visible ("STIMULUS NEWS" + "LIVE")
- Topic indicator (Spain)
- Subtitles showing correctly
- News ticker at bottom
- Talking head playing

### Frame at 43 seconds (B-roll)
- Stock-market chart B-roll covering the talking head
- Light overlay for subtitle readability
- All UI elements still visible
- Topic indicator "Spain", ticker scrolling

### Frame at 1:03 (China segment)
- B-roll transition working
- Topic changed to "China"
- Healthcare-related B-roll
- Synchronized with subtitle timing

---

## Documentation Files

1. **[BROLL_GUIDE.md](./BROLL_GUIDE.md)** — B-roll, article references, photo overlays
   - How B-roll layering works on track indices
   - Stock fetcher usage (download into `assets/`)
   - Overlay patterns + on-screen placement
   - Troubleshooting

2. **STIMULUS_VIDEO_COMPLETE.md** (this file)
   - Project status summary, what was fixed, quick start, examples

3. **[RENDER_FIX.md](./RENDER_FIX.md)** — render troubleshooting (assets, FFmpeg, Docker)

---

## Pro Tips

### Better B-roll

```bash
# Pull several candidates, pick the best, keep it local
python tools/stock_fetcher/fetch.py --query "beijing skyline" --type video --count 5 \
  --out assets/stimulus/broll/china-city.mp4
```

### Finding specific images

```bash
python tools/stock_fetcher/fetch.py \
  --query "pedro sanchez spain prime minister" --type photo --count 10 \
  --out assets/stimulus/photos/pedro.jpg
```

### Timing synchronization

Match `data-start` on overlays to subtitle timestamps:

```
# From the transcript / subtitle groups
{ "id": "g4", "start": 24.88, "end": 32.96, "text": "...Spain grows..." }
```

```html
<!-- Matching overlay timing: ~1s after the subtitle starts -->
<div id="ref-spain" class="clip" data-start="26" data-duration="6" data-track-index="4"> ... </div>
```

---

## Final Notes

The Stimulus video is **complete and fully functional**. All critical pieces work:

1. ✅ Video plays with audio narration (separate `<audio>` track)
2. ✅ B-roll covers the talking head at the correct times (track 1)
3. ✅ All visual overlays render correctly with deterministic exits
4. ✅ Subtitles are synchronized
5. ✅ Clean, light/neutral news styling

**Optional next steps:**
- Add article references to cite sources
- Add photo overlays to show people/places
- Customize colors/fonts to match brand
- Add more B-roll variety

**Ready to render:**
```bash
npx hyperframes preview                                       # Preview (background)
npm run check                                                 # lint + validate + inspect
npx hyperframes render -c stimulus.html -o out/stimulus-news.mp4   # Export
```

**Project Complete.**

---

> **Coming from Remotion?** The original build used `<OffthreadVideo>` + `<Audio>` +
> `<Sequence>` + `staticFile()` React components and a `StimulusComposition.tsx`. In
> HyperFrames it's plain HTML clips (`<video muted>` / `<audio data-volume>` /
> `<div class="clip">`) carrying `data-start` / `data-duration` / `data-track-index`, animated
> by one paused GSAP timeline registered on `window.__timelines`. Everything lives under
> `assets/` with relative paths — no `staticFile()` wrapper.
