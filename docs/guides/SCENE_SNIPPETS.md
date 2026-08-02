# Scene Snippets (HyperFrames)

Copy-paste HyperFrames scene patterns for every scene type. **Modern editing techniques are listed first** — these should be your primary tools. Component / registry-based scenes are at the bottom for specific moments.

Every snippet is a self-contained HyperFrames scene: HTML elements carry `data-start` / `data-duration` / `data-track-index` (all in **seconds**), visible timed elements get `class="clip"`, and a single **paused** GSAP timeline is registered on `window.__timelines`. The framework owns clip visibility, media playback, and timeline sync — you never call `play`/`pause`/`seek` and never animate `visibility`/`display`.

> **Coming from Remotion?** `useCurrentFrame`/`interpolate`/`spring`/`<Sequence>` all collapse into GSAP tweens placed at absolute time positions on the timeline. A Remotion frame `N` at 30fps becomes `N / 30` seconds. `<Img>`→`<img>`, `<Video>`→`<video muted playsinline>` (with a separate `<audio data-volume>` if you need sound), `staticFile('x')`→`assets/x`.

**Preview & render:**

```bash
npx hyperframes preview                              # dev loop, hot reload
npx hyperframes lint && npx hyperframes validate     # timing + WCAG contrast
npx hyperframes inspect                              # headless layout audit
npx hyperframes render -c scene.html -o out.mp4      # final render
```

---

## Table of Contents

### Modern Editing Techniques (Use These Most)
1. [Single Word Flash](#single-word-flash)
2. [Word-by-Word Sentence Build](#word-by-word-sentence-build)
3. [Section Number Header](#section-number-header)
4. [Impact Word Cascade](#impact-word-cascade)
5. [B-Roll Full Bleed](#b-roll-full-bleed)
6. [B-Roll + Typography Overlay](#b-roll-typography-overlay)
6b. [Cutaway Kinetic Headline (Dark-Overlay Takeover)](#cutaway-kinetic-headline-dark-overlay-takeover)
7. [Split Screen (TH Bottom)](#split-screen-th-bottom)
8. [Staggered Vertical List](#staggered-vertical-list)
9. [Editorial Collage](#editorial-collage)
10. [Data Labels Slide-In](#data-labels-slide-in)

### Talking Head Variants
11. [Talking Head Only](#talking-head-only)
12. [Talking Head + Mini Impact](#mini-impact-word)
13. [Talking Head + Floating Symbols](#floating-symbols-overlay)

### Technical & Data Scenes
14. [Custom SVG Diagram](#custom-svg-diagram)
15. [Neural Network SVG](#neural-network-svg-diagram)
16. [Word-by-Word Sentence Building (Token Prediction)](#word-by-word-token-prediction)
17. [Probability Bars](#probability-bars)

### Impact & Transition
18. [Kinetic Flash](#kinetic-flash)
19. [Scene Transitions (CSS vs Shader)](#scene-transitions)

### Registry / Component-Based Scenes (Use Sparingly — 2-3 per video MAX)
20. [Logo Outro](#logo-outro)
21. [Video Card](#video-card)
22. [Headline + Video Combo](#headline-video-combo)
23. [Checklist Card](#checklist-card)
24. [Impact Word (Caption Component)](#impact-word-component)
25. [CTA (Headline Card)](#cta-headline-card)
26. [CTA with Video Background](#cta-with-video-background)
27. [Grid Reveal Card](#grid-reveal-card)
28. [Hero Sphere Card](#hero-sphere-card)
29. [Comparison Grid Card](#comparison-grid-card)
30. [Icon Pyramid](#icon-pyramid)
31. [Data Sources Vertical Stack](#data-sources-vertical-stack)

### Audio
32. [SFX Layer Template](#sfx-layer-template)

---

## Shared Conventions

Every snippet below assumes a light/neutral palette. Define these once near the top of your composition's `<style>` and reuse:

```css
:root {
  --bg: #F5F1E8;        /* warm neutral canvas */
  --bg-alt: #FFFFFF;    /* clean white panels  */
  --ink: #1A1A1A;       /* near-black text     */
  --ink-soft: #5A5A5A;  /* secondary text      */
  --accent: #2563EB;    /* primary accent      */
  --accent-2: #16A34A;  /* positive / green    */
  --accent-3: #D97706;  /* warm / amber        */
}
```

Fonts are embedded by the compiler — just write the `font-family` you want (e.g. `Outfit` for headlines, `Inter` for body). Numbers get `font-variant-numeric: tabular-nums`.

Each standalone scene file looks like this skeleton (the snippets fill in `<!-- content -->` and the timeline body):

```html
<!doctype html>
<html>
  <body>
    <div data-composition-id="scene" data-width="1080" data-height="1920">
      <div class="scene-content">
        <!-- content -->
      </div>
      <style>
        /* :root tokens + scene styles */
        [data-composition-id="scene"] { width: 100%; height: 100%; }
        .scene-content {
          width: 100%; height: 100%; box-sizing: border-box;
          display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          padding: 160px 80px; gap: 24px;
          background: var(--bg);
        }
      </style>
      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });
        /* tweens... */
        window.__timelines["scene"] = tl;
      </script>
    </div>
  </body>
</html>
```

> Dimensions shown are portrait `1080×1920` (short-form). Swap to `1920×1080` for landscape; the flex + padding layout adapts without hardcoded coordinates. Standalone files put the `data-composition-id` div directly in `<body>` (no `<template>` wrapper — that's only for sub-compositions loaded via `data-composition-src`).

---

# MODERN EDITING TECHNIQUES

These are what make videos feel human. Use them for the majority of your scenes.

---

## Single Word Flash

**Use when**: Narrator says a key word — put JUST that word on screen. **This is the most powerful technique in short-form video editing.** No cards. No icons. Just the word.

**Caption shortcut:** for a transcript-driven, full-screen single word, install `caption-kinetic-slam` and drive it from your transcript (see [Word-by-Word](#word-by-word-sentence-build) for the host pattern). Below is the standalone HTML+GSAP version.

```html
<div data-composition-id="word-flash" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="word" class="clip word" data-start="0" data-duration="1.5" data-track-index="0">TOUCH</div>
  </div>

  <style>
    [data-composition-id="word-flash"] { width: 100%; height: 100%; }
    [data-composition-id="word-flash"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; align-items: center; justify-content: center;
      background: var(--bg);
    }
    [data-composition-id="word-flash"] .word {
      font-family: "Outfit"; font-size: 180px; font-weight: 800;
      color: var(--ink); letter-spacing: -2px; text-align: center;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Remotion: smooth fade-in 0→1 over 12 frames + scale 0.92→1  →  one fromTo
    tl.from("#word", { opacity: 0, scale: 0.92, duration: 0.4, ease: "power3.out" }, 0.1);
    window.__timelines["word-flash"] = tl;
  </script>
</div>
```

**Timing:** keep these to 0.5–2s. The `data-duration="1.5"` controls how long the word lives; the tween only describes its entrance. As an overlay over a talking head, give it a `data-track-index` distinct from the video and skip the background fill.

---

## Word-by-Word Sentence Build

**Use when**: Building a statement word by word. Words appear one at a time and STAY on screen. Different from subtitles — these are large, centered, and accumulate. The last word lands in the accent color.

```html
<div data-composition-id="word-build" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div class="phrase">
      <span id="w0" class="clip word"          data-start="0"   data-duration="2.5" data-track-index="0">robots</span>
      <span id="w1" class="clip word"          data-start="0.5" data-duration="2.0" data-track-index="1">can</span>
      <span id="w2" class="clip word"          data-start="0.8" data-duration="1.7" data-track-index="2">now</span>
      <span id="w3" class="clip word accent"   data-start="1.2" data-duration="1.3" data-track-index="3">FEEL</span>
    </div>
  </div>

  <style>
    [data-composition-id="word-build"] { width: 100%; height: 100%; }
    [data-composition-id="word-build"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; align-items: center; justify-content: center;
      padding: 0 80px; background: var(--bg);
    }
    [data-composition-id="word-build"] .phrase {
      display: flex; flex-wrap: wrap; justify-content: center;
      gap: 16px 28px; max-width: 920px;
    }
    [data-composition-id="word-build"] .word {
      font-family: "Outfit"; font-size: 120px; font-weight: 800;
      color: var(--ink); display: inline-block;
    }
    [data-composition-id="word-build"] .accent { color: var(--accent-3); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Each word: Remotion spring pop (damping 12 / stiffness 200) → back.out(1.6) at its delaySec
    const words = [
      { sel: "#w0", at: 0.0 },
      { sel: "#w1", at: 0.5 },
      { sel: "#w2", at: 0.8 },
      { sel: "#w3", at: 1.2 },
    ];
    words.forEach((w) => {
      tl.from(w.sel, { opacity: 0, y: 18, scale: 0.6, duration: 0.45, ease: "back.out(1.6)" }, w.at);
    });
    window.__timelines["word-build"] = tl;
  </script>
</div>
```

**Caption-driven version (recommended for narration).** When the words come from a transcript, render one group at a time and add the mandatory hard exit. This is the HyperFrames caption pattern — a single group container per phrase, a `tl.set` kill at `group.end`:

```js
const GROUPS = [
  { id: "cg-0", text: "robots can now",  start: 2.0, end: 3.1 },
  { id: "cg-1", text: "FEEL",            start: 3.2, end: 4.5 },
];
GROUPS.forEach((g) => {
  const el = document.getElementById(g.id);
  tl.from(el, { opacity: 0, y: 24, scale: 0.85, duration: 0.3, ease: "back.out(1.7)" }, g.start);
  // hard deterministic exit — every group MUST kill itself
  tl.to(el,  { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, g.end - 0.12);
  tl.set(el, { opacity: 0, visibility: "hidden" }, g.end);
});
// self-lint before registering: seek past each group, warn if still visible, then reset
GROUPS.forEach((g) => {
  tl.seek(g.end + 0.01);
  const el = document.getElementById(g.id);
  const cs = getComputedStyle(el);
  if (cs.opacity !== "0" && cs.visibility !== "hidden")
    console.warn("[caption-lint] " + g.id + " still visible at " + (g.end + 0.01).toFixed(2));
});
tl.seek(0);
```

For a ready-made social treatment, install `caption-highlight` (TikTok red sweep) and feed it your transcript; for big single-word hits use `caption-kinetic-slam`.

---

## Section Number Header

**Use when**: Chapter break between topics. Visual palate cleanser. Bold "1." centered with a thin accent underline that draws in.

```html
<div data-composition-id="section-num" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="num"  class="clip num"  data-start="0"   data-duration="1.5" data-track-index="0">1.</div>
    <div id="rule" class="clip rule" data-start="0"   data-duration="1.5" data-track-index="1"></div>
    <div id="sub"  class="clip sub"  data-start="0"   data-duration="1.5" data-track-index="2">HOW IT WORKS</div>
  </div>

  <style>
    [data-composition-id="section-num"] { width: 100%; height: 100%; }
    [data-composition-id="section-num"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 18px; background: var(--bg);
    }
    [data-composition-id="section-num"] .num {
      font-family: "Outfit"; font-size: 240px; font-weight: 900;
      color: var(--ink); letter-spacing: -4px; line-height: 1;
    }
    [data-composition-id="section-num"] .rule {
      width: 160px; height: 5px; background: var(--accent); border-radius: 3px;
      transform-origin: center; /* GSAP scales from 0 */
    }
    [data-composition-id="section-num"] .sub {
      font-family: "Inter"; font-size: 40px; font-weight: 600;
      color: var(--ink-soft); letter-spacing: 4px; text-transform: uppercase;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#num",  { opacity: 0, scale: 0.5, duration: 0.5, ease: "back.out(1.8)" }, 0.1);
    tl.from("#rule", { scaleX: 0, duration: 0.4, ease: "power3.out" }, 0.35);  // line draw-in
    tl.from("#sub",  { opacity: 0, y: 12, duration: 0.45, ease: "power2.out" }, 0.5);
    window.__timelines["section-num"] = tl;
  </script>
</div>
```

**Timing:** 1–2s. Three eases (`back`, `power3`, `power2`) keep the entrance lively.

---

## Impact Word Cascade

**Use when**: Multiple keywords appearing sequentially and STAYING visible. Builds a visual argument — "SEE" stays, "HEAR" appears next, "FEEL" appears below. Light canvas, each word in its own accent.

```html
<div data-composition-id="cascade" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="c0" class="clip word" style="color:var(--accent)"   data-start="0"   data-duration="3.0" data-track-index="0">SEE</div>
    <div id="c1" class="clip word" style="color:var(--accent-2)" data-start="0.8" data-duration="2.2" data-track-index="1">HEAR</div>
    <div id="c2" class="clip word" style="color:var(--accent-3)" data-start="1.6" data-duration="1.4" data-track-index="2">FEEL</div>
  </div>

  <style>
    [data-composition-id="cascade"] { width: 100%; height: 100%; }
    [data-composition-id="cascade"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 28px; background: var(--bg);
    }
    [data-composition-id="cascade"] .word {
      font-family: "Outfit"; font-size: 150px; font-weight: 900; letter-spacing: 6px;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Remotion spring pop + decaying sin() shake → back.out overshoot does the same job deterministically
    [["#c0",0.0],["#c1",0.8],["#c2",1.6]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, scale: 0.5, duration: 0.4, ease: "back.out(2)" }, at);
    });
    window.__timelines["cascade"] = tl;
  </script>
</div>
```

> The original placed footage behind the words at low opacity with a dark vignette. In HyperFrames keep it on the light canvas — or, if you want footage, use [B-Roll Full Bleed](#b-roll-full-bleed) and put these words on a separate overlay track. No dark/neon treatment.

---

## B-Roll Full Bleed

**Use when**: YouTube or stock footage fills the entire screen with a soft top/bottom scrim for legibility. Text overlaid on footage. No card frame. Ken Burns drift on the footage.

**Key rule:** never animate the `<video>` element's dimensions or transforms — wrap it in a non-timed `<div>` and animate the wrapper. The video itself carries no `class="clip"`.

```html
<div data-composition-id="broll-bleed" data-width="1080" data-height="1920">
  <!-- non-timed wrapper carries the Ken Burns transform -->
  <div class="ken">
    <video id="bg" data-start="0" data-duration="3.5" data-track-index="0"
           src="assets/broll-hook.mp4" muted playsinline crossorigin="anonymous"></video>
  </div>
  <div class="scrim"></div>
  <div class="scene-content">
    <div id="ovl"  class="clip ovl"  data-start="0"   data-duration="3.5" data-track-index="1">TOUCH</div>
    <div id="ovls" class="clip ovls" data-start="0"   data-duration="3.5" data-track-index="2">A new sense for machines</div>
  </div>

  <style>
    [data-composition-id="broll-bleed"] { width: 100%; height: 100%; position: relative; background: #000; }
    [data-composition-id="broll-bleed"] .ken { position: absolute; inset: 0; }
    [data-composition-id="broll-bleed"] .ken video { width: 100%; height: 100%; object-fit: cover; }
    /* plain neutral scrim for text legibility — letterbox/contrast only, not a dark-theme style */
    [data-composition-id="broll-bleed"] .scrim {
      position: absolute; inset: 0; pointer-events: none;
      background: linear-gradient(to bottom, rgba(0,0,0,.30) 0%, rgba(0,0,0,.06) 38%, rgba(0,0,0,.06) 62%, rgba(0,0,0,.48) 100%);
    }
    [data-composition-id="broll-bleed"] .scene-content {
      position: absolute; inset: 0; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px;
    }
    [data-composition-id="broll-bleed"] .ovl {
      font-family: "Outfit"; font-size: 150px; font-weight: 800; color: #fff;
      text-shadow: 0 4px 30px rgba(0,0,0,.7);
    }
    [data-composition-id="broll-bleed"] .ovls {
      font-family: "Inter"; font-size: 44px; font-weight: 600; color: rgba(255,255,255,.9);
      text-shadow: 0 2px 15px rgba(0,0,0,.6);
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Ken Burns: scale 1.05→1.12, drift left — on the WRAPPER, not the video
    tl.fromTo(".ken", { scale: 1.05, x: 0 }, { scale: 1.12, x: -15, duration: 3.5, ease: "none" }, 0);
    tl.from("#ovl",  { opacity: 0, y: 24, duration: 0.5, ease: "power3.out" }, 0.3);
    tl.from("#ovls", { opacity: 0, y: 18, duration: 0.45, ease: "power2.out" }, 0.5);
    window.__timelines["broll-bleed"] = tl;
  </script>
</div>
```

> The black `[data-composition-id]` background is letterboxing behind a fullscreen video — not a styling choice. It only shows if the footage doesn't fully cover.

---

## B-Roll Typography Overlay

**Use when**: Full-screen footage with a logo or branded text floating on top. The footage is the background, not contained in a card. Adds a drawing accent rule under the title.

```html
<div data-composition-id="broll-brand" data-width="1080" data-height="1920">
  <div class="ken">
    <video id="bg" data-start="0" data-duration="3.2" data-track-index="0"
           src="assets/broll-2.mp4" muted playsinline crossorigin="anonymous"></video>
  </div>
  <div class="scrim"></div>
  <div class="scene-content">
    <img id="logo" class="clip logo" src="assets/brand-logo.png"
         data-start="0" data-duration="3.2" data-track-index="1" crossorigin="anonymous" alt="">
    <div id="title" class="clip title" data-start="0" data-duration="3.2" data-track-index="2">DIGIT 360</div>
    <div id="rule"  class="clip rule"  data-start="0" data-duration="3.2" data-track-index="3"></div>
    <div id="sub"   class="clip sub"   data-start="0" data-duration="3.2" data-track-index="4">Robotic Fingertip</div>
  </div>

  <style>
    [data-composition-id="broll-brand"] { width: 100%; height: 100%; position: relative; background: #000; }
    [data-composition-id="broll-brand"] .ken { position: absolute; inset: 0; }
    [data-composition-id="broll-brand"] .ken video { width: 100%; height: 100%; object-fit: cover; }
    [data-composition-id="broll-brand"] .scrim {
      position: absolute; inset: 0; pointer-events: none;
      background: linear-gradient(to bottom, rgba(0,0,0,.4) 0%, rgba(0,0,0,.18) 50%, rgba(0,0,0,.5) 100%);
    }
    [data-composition-id="broll-brand"] .scene-content {
      position: absolute; inset: 0; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px;
    }
    [data-composition-id="broll-brand"] .logo { height: 110px; object-fit: contain; margin-bottom: 8px; }
    [data-composition-id="broll-brand"] .title {
      font-family: "Outfit"; font-size: 110px; font-weight: 800; color: #fff;
      text-shadow: 0 4px 30px rgba(0,0,0,.5);
    }
    [data-composition-id="broll-brand"] .rule { width: 240px; height: 4px; background: var(--accent); border-radius: 2px; transform-origin: center; }
    [data-composition-id="broll-brand"] .sub { font-family: "Inter"; font-size: 40px; color: rgba(255,255,255,.85); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.fromTo(".ken", { scale: 1.04 }, { scale: 1.1, duration: 3.2, ease: "none" }, 0);
    tl.from("#logo",  { opacity: 0, scale: 0.85, duration: 0.4, ease: "back.out(1.6)" }, 0.2);
    tl.from("#title", { opacity: 0, y: 20, duration: 0.5, ease: "power3.out" }, 0.4);
    tl.from("#rule",  { scaleX: 0, duration: 0.4, ease: "power2.out" }, 0.6);
    tl.from("#sub",   { opacity: 0, duration: 0.4, ease: "power1.out" }, 0.8);
    window.__timelines["broll-brand"] = tl;
  </script>
</div>
```

---

## Cutaway Kinetic Headline (Dark-Overlay Takeover)

**Use when**: A b-roll beat that needs to *land a phrase hard* — drop a dark overlay over the footage and punch a centered word-by-word headline with one accent "hero" word (a country/brand/number) + optional emoji + an accent/tricolor underline. The headline covers ~60–70% of the frame and OWNS the beat. **Hide the lower-third captions for this window** — the headline IS the caption. Proven on `chatgpt-dreaming-v3` (the "PART THAT MATTERS FOR INDIA 🇮🇳" cutaway).

**Critical gotchas (both cost a silent-invisible bug):**
1. **CSS `z-index`, not track-index, decides paint.** A full-frame overlay sitting over a b-roll `<video>` MUST have a CSS `z-index` ABOVE the b-roll's z-index, or the video paints on top and the whole scene is invisible — while `lint`/`inspect` still report 0 issues (they only check the timeline). Give `.cutaway` an explicit `z-index` above your `.broll`.
2. **Hide captions across the *overlap*, not just starts-inside.** When skipping caption groups for this window, skip any group where `grp.start < HI && grp.end > LO`, or a group that started just before the window leaks a stray pill onto the dark overlay.

All tweens are span-only `tl.fromTo/to` at **absolute** times (seek-safe). Animate the inner words — never the `.clip` element's opacity/visibility; let the clip boundary hard-cut.

```html
<!-- z-index must be ABOVE your b-roll layer (.broll z-index:3 here) -->
<div id="cutaway" class="cutaway clip" data-start="32.20" data-duration="2.80" data-track-index="6">
  <div class="cutaway-dark"></div>
  <div class="cutaway-wrap">
    <div class="cutaway-row">
      <span class="cw" id="cw0">Part</span>
      <span class="cw" id="cw1">that</span>
      <span class="cw" id="cw2">matters</span>
    </div>
    <div class="cutaway-row" style="margin-top:6px;">
      <span class="cw" id="cw3">for</span>
      <span class="cw cw-hero" id="cwHero">India</span>
      <span class="cw-emoji" id="cwEmoji">🇮🇳</span>
    </div>
    <div class="cutaway-rule" id="cwRule"></div>
  </div>

  <style>
    .cutaway { position: absolute; inset: 0; width: 1080px; height: 1920px; z-index: 6; pointer-events: none; }
    .cutaway-dark {
      position: absolute; inset: 0;
      background:
        radial-gradient(124% 82% at 50% 42%, rgba(8,6,22,0.18) 0%, rgba(8,6,22,0.60) 60%, rgba(5,3,14,0.84) 100%),
        linear-gradient(180deg, rgba(8,6,22,0.55) 0%, rgba(8,6,22,0.18) 30%, rgba(8,6,22,0.22) 68%, rgba(6,4,16,0.72) 100%);
    }
    .cutaway-wrap { position: absolute; top: 33%; left: 8%; right: 8%; text-align: center; }
    .cutaway-row  { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: center; gap: 8px 22px; }
    .cw {
      display: inline-block; font-weight: 900; font-size: 116px; line-height: 0.98;
      letter-spacing: -0.02em; color: #fff; text-transform: uppercase;
      text-shadow: 0 6px 30px rgba(6,4,18,0.85), 0 0 40px rgba(8,6,22,0.5);
      opacity: 0; transform-origin: 50% 70%; will-change: transform, opacity;
    }
    .cw-hero {                                   /* the one accent word */
      font-size: 206px; color: var(--accent, #ff9d3d);
      text-shadow: 0 8px 34px rgba(120,50,0,0.6), 0 0 46px rgba(255,157,61,0.55);
    }
    .cw-emoji { display: inline-block; font-size: 116px; line-height: 1; opacity: 0; transform-origin: 50% 70%; }
    .cutaway-rule {                              /* accent (or tricolor) underline */
      height: 12px; width: 0; margin: 22px auto 0; border-radius: 6px;
      background: linear-gradient(90deg, #ff9d3d 0%, #fff 50%, #138808 100%);
      box-shadow: 0 6px 20px rgba(0,0,0,0.4); opacity: 0;
    }
  </style>
</div>
```

```js
// In your single paused root timeline. Times are ABSOLUTE seconds.
window.__timelines = window.__timelines || {};
var tl = window.__timelines["root"];           // your existing root timeline

function cwIn(id, t, big) {                     // word punch-in (back-ease)
  tl.fromTo(id,
    { opacity: 0, y: 34, scale: big ? 0.70 : 0.82, rotate: big ? -3 : 0 },
    { opacity: 1, y: 0, scale: 1, rotate: 0, duration: big ? 0.44 : 0.32, ease: "back.out(2)", overwrite: "auto" },
    t);
}
cwIn("#cw0", 32.30); cwIn("#cw1", 32.50); cwIn("#cw2", 32.74);
cwIn("#cw3", 32.99); cwIn("#cwHero", 33.16, true);                       // hero word lands biggest
tl.fromTo("#cwEmoji", { opacity: 0, scale: 0.4, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2.4)", overwrite: "auto" }, 33.42);
tl.fromTo("#cwRule",  { width: 0, opacity: 0 }, { width: 560, opacity: 1, duration: 0.5, ease: "power3.out", overwrite: "auto" }, 33.40);
tl.to("#cwHero", { scale: 1.05, duration: 0.7, ease: "sine.inOut", repeat: 1, yoyo: true, overwrite: "auto" }, 33.75);  // hero breathes
tl.to(["#cw0","#cw1","#cw2","#cw3","#cwHero","#cwEmoji","#cwRule"],      // clean exit before the clip cut
  { opacity: 0, y: -18, duration: 0.3, ease: "power2.in", overwrite: "auto" }, 34.66);

// Hide captions across the FULL overlap of this window:
// var LO = 32.20, HI = 35.10;
// groupMeta.forEach(g => { if (g.start < HI && g.end > LO) return; /* ...build caption... */ });
```

---

## Split Screen (TH Bottom)

**Use when**: Overlay content in the top ~55%, talking head visible in the bottom ~45%. NOT a card on top — use large typography, an icon, or B-roll. The talking-head video plays on a track underneath in your root composition; this scene only paints the top band.

```html
<div data-composition-id="split-top" data-width="1080" data-height="1920">
  <!-- top band: opaque content panel; bottom band stays transparent so TH shows through -->
  <div class="top-band">
    <div class="scene-content">
      <div id="ring" class="clip ring" data-start="0" data-duration="3.2" data-track-index="0">
        <svg viewBox="0 0 100 100" width="120" height="120" aria-hidden="true">
          <circle cx="50" cy="35" r="18" fill="none" stroke="var(--accent)" stroke-width="6"/>
          <circle cx="50" cy="35" r="6"  fill="var(--accent)"/>
          <path d="M20 60 Q50 90 80 60" fill="none" stroke="var(--accent)" stroke-width="6" stroke-linecap="round"/>
        </svg>
      </div>
      <div id="label" class="clip label" data-start="0" data-duration="3.2" data-track-index="1">AI CAN SEE</div>
    </div>
  </div>

  <style>
    [data-composition-id="split-top"] { width: 100%; height: 100%; position: relative; }
    [data-composition-id="split-top"] .top-band {
      position: absolute; top: 0; left: 0; right: 0; height: 55%;
      background: var(--bg); overflow: hidden;
    }
    [data-composition-id="split-top"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 28px;
    }
    [data-composition-id="split-top"] .ring {
      width: 220px; height: 220px; border-radius: 50%;
      background: rgba(37,99,235,.12);
      display: flex; align-items: center; justify-content: center;
    }
    [data-composition-id="split-top"] .label {
      font-family: "Outfit"; font-size: 72px; font-weight: 800; color: var(--ink);
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#ring",  { opacity: 0, scale: 0.6, duration: 0.5, ease: "back.out(1.7)" }, 0.15);
    tl.from("#label", { opacity: 0, y: 16, duration: 0.45, ease: "power2.out" }, 0.4);
    window.__timelines["split-top"] = tl;
  </script>
</div>
```

> Inline SVG replaces the old icon-library `<Eye>` component — see [Custom SVG Diagram](#custom-svg-diagram) for drawing icons from scratch.

---

## Staggered Vertical List

**Use when**: Items stack vertically, revealing one by one. Each item has its own accent color and an emoji/SVG icon tile. Slides in from the left.

```html
<div data-composition-id="stagger-list" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="title" class="clip title" data-start="0" data-duration="6.7" data-track-index="0">OBJECTS</div>
    <div id="i0" class="clip item" style="--c:#EF4444" data-start="0.4" data-duration="6.3" data-track-index="1">
      <span class="ic">🍅</span><span class="lbl">Ripe Tomato</span>
    </div>
    <div id="i1" class="clip item" style="--c:#2563EB" data-start="1.9" data-duration="4.8" data-track-index="2">
      <span class="ic">🥛</span><span class="lbl">Glass of Water</span>
    </div>
    <div id="i2" class="clip item" style="--c:#D97706" data-start="3.4" data-duration="3.3" data-track-index="3">
      <span class="ic">🧽</span><span class="lbl">Kitchen Sponge</span>
    </div>
  </div>

  <style>
    [data-composition-id="stagger-list"] { width: 100%; height: 100%; }
    [data-composition-id="stagger-list"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 28px; padding: 120px 60px; background: var(--bg);
    }
    [data-composition-id="stagger-list"] .title {
      font-family: "Outfit"; font-size: 84px; font-weight: 900; color: var(--ink);
      text-transform: uppercase; margin-bottom: 16px;
    }
    [data-composition-id="stagger-list"] .item {
      display: flex; align-items: center; gap: 28px; width: 88%;
      padding: 24px 32px; border-radius: 24px;
      background: color-mix(in srgb, var(--c) 8%, white);
      border: 2px solid color-mix(in srgb, var(--c) 28%, white);
    }
    [data-composition-id="stagger-list"] .ic {
      width: 84px; height: 84px; border-radius: 18px; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center; font-size: 42px;
      background: color-mix(in srgb, var(--c) 18%, white);
    }
    [data-composition-id="stagger-list"] .lbl {
      font-family: "Inter"; font-size: 52px; font-weight: 700; color: var(--ink);
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 20, duration: 0.5, ease: "power3.out" }, 0.1);
    [["#i0",0.4],["#i1",1.9],["#i2",3.4]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, x: -70, duration: 0.5, ease: "back.out(1.4)" }, at);
    });
    window.__timelines["stagger-list"] = tl;
  </script>
</div>
```

> `color-mix()` reproduces the original `${accent}12` / `${accent}30` alpha tints against the light canvas. For older render targets, hardcode the tints.

---

## Editorial Collage

**Use when**: Mixed media — cutout photos, simple shapes, text at different sizes and angles. Magazine/editorial aesthetic, not UI cards. Elements stagger in with varied eases. Use `npx hyperframes remove-background` (or your background remover) for cutout photos.

Because the elements are decorative and positioned freely, this is the one scene that legitimately uses `position: absolute` on individual pieces (not on a content container).

```html
<div data-composition-id="collage" data-width="1080" data-height="1920">
  <div id="blob"  class="clip blob"  data-start="0"   data-duration="4" data-track-index="0"></div>
  <img id="cutout" class="clip cutout" src="assets/cutout-photo.png"
       data-start="0.2" data-duration="3.8" data-track-index="1" crossorigin="anonymous" alt="">
  <div id="big"   class="clip big"   data-start="0"   data-duration="4" data-track-index="2">DIGIT<span>360</span></div>
  <div id="rule"  class="clip rule"  data-start="0.2" data-duration="3.8" data-track-index="3"></div>
  <div id="kick"  class="clip kick"  data-start="0.4" data-duration="3.6" data-track-index="4">META ROBOTICS</div>

  <style>
    [data-composition-id="collage"] { width: 100%; height: 100%; position: relative; background: var(--bg); overflow: hidden; }
    [data-composition-id="collage"] .blob {
      position: absolute; top: 15%; right: 10%; width: 340px; height: 340px;
      border-radius: 50%; background: rgba(37,99,235,.10);
    }
    [data-composition-id="collage"] .cutout {
      position: absolute; bottom: 20%; left: 8%; height: 720px;
      filter: grayscale(100%) contrast(1.1);
    }
    [data-composition-id="collage"] .big {
      position: absolute; top: 25%; left: 42%;
      font-family: "Outfit"; font-size: 120px; font-weight: 900; color: var(--ink);
      transform: rotate(-5deg); line-height: 1.0;
    }
    [data-composition-id="collage"] .big span { display: block; } /* second line, no <br> */
    [data-composition-id="collage"] .rule {
      position: absolute; top: 49%; left: 40%; width: 220px; height: 4px;
      background: var(--accent); transform-origin: left center;
    }
    [data-composition-id="collage"] .kick {
      position: absolute; top: 56%; right: 12%;
      font-family: "Inter"; font-size: 34px; font-weight: 600; color: var(--ink-soft);
      letter-spacing: 3px; text-transform: uppercase;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#blob",   { scale: 0, transformOrigin: "center", duration: 0.6, ease: "back.out(1.6)" }, 0.1);
    tl.from("#cutout", { opacity: 0, y: 30, duration: 0.55, ease: "power3.out" }, 0.25);
    tl.from("#big",    { opacity: 0, scale: 0.8, rotation: -10, duration: 0.55, ease: "back.out(1.3)" }, 0.15);
    tl.from("#rule",   { scaleX: 0, duration: 0.4, ease: "power2.out" }, 0.45);
    tl.from("#kick",   { opacity: 0, x: 20, duration: 0.5, ease: "power1.out" }, 0.6);
    window.__timelines["collage"] = tl;
  </script>
</div>
```

> The "DIGIT / 360" stacked title uses a block-level `<span>` for the second line instead of `<br>` — forced breaks fight natural wrapping and can cause overlap.

---

## Data Labels Slide-In

**Use when**: Technical data points sliding in from the side. Each label has a name, a mono-formatted value chip, and an accent color. Clean, technical feel on a light panel.

```html
<div data-composition-id="data-labels" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="d0" class="clip row" style="--c:#2563EB" data-start="0"   data-duration="3" data-track-index="0">
      <span class="name">PRESSURE</span><span class="val">2.4N</span>
    </div>
    <div id="d1" class="clip row" style="--c:#16A34A" data-start="0.6" data-duration="2.4" data-track-index="1">
      <span class="name">TEXTURE</span><span class="val">Smooth</span>
    </div>
    <div id="d2" class="clip row" style="--c:#D97706" data-start="1.2" data-duration="1.8" data-track-index="2">
      <span class="name">SHAPE</span><span class="val">Spherical</span>
    </div>
  </div>

  <style>
    [data-composition-id="data-labels"] { width: 100%; height: 100%; }
    [data-composition-id="data-labels"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: flex-end; justify-content: center;
      gap: 24px; padding: 0 80px; background: var(--bg);
    }
    [data-composition-id="data-labels"] .row { display: flex; align-items: center; gap: 24px; }
    [data-composition-id="data-labels"] .name {
      font-family: "Inter"; font-size: 36px; font-weight: 600; color: var(--ink-soft);
      letter-spacing: 2px; text-transform: uppercase;
    }
    [data-composition-id="data-labels"] .val {
      font-family: ui-monospace, "SF Mono", monospace; font-size: 40px; font-weight: 800;
      color: var(--c); background: color-mix(in srgb, var(--c) 12%, white);
      padding: 10px 24px; border-radius: 14px;
      border: 1px solid color-mix(in srgb, var(--c) 30%, white);
      font-variant-numeric: tabular-nums;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    [["#d0",0.0],["#d1",0.6],["#d2",1.2]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, x: 100, duration: 0.5, ease: "power3.out" }, at);
    });
    window.__timelines["data-labels"] = tl;
  </script>
</div>
```

---

# TALKING HEAD VARIANTS

These assume a talking-head `<video>` clip in your **root** composition on its own track. The overlay scenes here live on higher track indices and have transparent backgrounds.

---

## Talking Head Only

**Use when**: Speaker intro, setup, or narration with no overlay. There's nothing to build — the talking-head video clip carries the segment. Just place it in the root composition:

```html
<!-- in the root composition -->
<video id="th-1" data-start="0" data-duration="3.5" data-track-index="0"
       src="assets/talking-head.mp4" muted playsinline crossorigin="anonymous"></video>
<audio id="th-1-a" data-start="0" data-duration="3.5" data-track-index="9"
       src="assets/talking-head.mp4" data-volume="1"></audio>
```

> Audio is ALWAYS a separate `<audio>` element — never rely on the (muted) video for sound.

---

## Mini Impact Word

**Use when**: Emphasize a single word while the talking head keeps playing. Small, near the top, optional pulse ring. Transparent overlay scene on a higher track than the video.

```html
<div data-composition-id="mini-impact" data-width="1080" data-height="1920">
  <div class="mount">
    <div id="ring" class="clip ring" data-start="0" data-duration="1.8" data-track-index="0"></div>
    <div id="word" class="clip word" data-start="0" data-duration="1.8" data-track-index="1">LIMITATION</div>
  </div>

  <style>
    [data-composition-id="mini-impact"] { width: 100%; height: 100%; }
    [data-composition-id="mini-impact"] .mount {
      position: absolute; top: 22%; left: 0; right: 0;
      display: flex; align-items: center; justify-content: center;
    }
    [data-composition-id="mini-impact"] .word {
      font-family: "Outfit"; font-size: 80px; font-weight: 800; color: var(--ink);
      text-shadow: 0 2px 12px rgba(255,255,255,.6); position: relative; z-index: 1;
    }
    [data-composition-id="mini-impact"] .ring {
      position: absolute; width: 360px; height: 360px; border-radius: 50%;
      border: 4px solid var(--accent); opacity: .5;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#word", { opacity: 0, scale: 0.7, duration: 0.4, ease: "back.out(1.8)" }, 0.05);
    // pulse ring: finite repeat, computed from duration (NEVER repeat:-1)
    const cycle = 0.9, dur = 1.8;
    tl.fromTo("#ring",
      { scale: 0.6, opacity: 0.6 },
      { scale: 1.1, opacity: 0, duration: cycle, ease: "power1.out",
        repeat: Math.ceil(dur / cycle) - 1 },
      0.1);
    window.__timelines["mini-impact"] = tl;
  </script>
</div>
```

---

## Floating Symbols Overlay

**Use when**: A few translucent symbols (math / code characters) drift over the talking head. Keep them clearly visible (not too faint), monospace, accent-colored, with a soft glow. The overlay is `pointer-events: none` and transparent so the TH stays clean.

Use deterministic motion (seeded offsets, not `Math.random()`):

```html
<div data-composition-id="float-symbols" data-width="1080" data-height="1920">
  <div class="layer">
    <span id="s0" class="clip sym" data-start="0" data-duration="4" data-track-index="0">∑</span>
    <span id="s1" class="clip sym" data-start="0" data-duration="4" data-track-index="1">λ</span>
    <span id="s2" class="clip sym" data-start="0" data-duration="4" data-track-index="2">{ }</span>
    <span id="s3" class="clip sym" data-start="0" data-duration="4" data-track-index="3">∞</span>
  </div>

  <style>
    [data-composition-id="float-symbols"] { width: 100%; height: 100%; }
    [data-composition-id="float-symbols"] .layer { position: absolute; inset: 0; pointer-events: none; }
    [data-composition-id="float-symbols"] .sym {
      position: absolute; font-family: ui-monospace, "SF Mono", monospace;
      font-size: 96px; font-weight: 700; color: var(--accent); opacity: .55;
      text-shadow: 0 0 24px rgba(37,99,235,.35);
    }
    [data-composition-id="float-symbols"] #s0 { top: 18%; left: 14%; }
    [data-composition-id="float-symbols"] #s1 { top: 30%; right: 16%; }
    [data-composition-id="float-symbols"] #s2 { top: 60%; left: 18%; }
    [data-composition-id="float-symbols"] #s3 { top: 70%; right: 20%; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    const dur = 4, cyc = 2;
    // each symbol bobs on a sine-like path via yoyo'd tweens (deterministic, finite)
    const syms = [
      { sel: "#s0", x: 18, y: -22 },
      { sel: "#s1", x: -16, y: 20 },
      { sel: "#s2", x: 22, y: 16 },
      { sel: "#s3", x: -20, y: -18 },
    ];
    syms.forEach((s, i) => {
      tl.from(s.sel, { opacity: 0, scale: 0.7, duration: 0.5, ease: "power2.out" }, 0.1 + i * 0.12);
      tl.to(s.sel, { x: s.x, y: s.y, duration: cyc, ease: "sine.inOut",
                     yoyo: true, repeat: Math.ceil(dur / cyc) - 1 }, 0.1);
    });
    window.__timelines["float-symbols"] = tl;
  </script>
</div>
```

---

# TECHNICAL & DATA SCENES

---

## Custom SVG Diagram

**Use when**: An animated technical illustration specific to this video's topic. The "signature scene." Every video should have at least one. Build with inline SVG (`<circle>`, `<rect>`, `<line>`, `<path>`) and animate with GSAP.

Core techniques:
- **`stroke-dashoffset` self-draw** for paths/connectors (measure with `path.getTotalLength()`).
- **`scale` / `opacity` pops** for node reveals (back.out overshoot).
- **`fill` / `stroke` color transitions** for "activation/firing".
- Stagger reveals every ~0.4–0.8s so the diagram assembles in front of the viewer.

```html
<div data-composition-id="svg-diagram" data-width="1080" data-height="1920">
  <svg class="diagram" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
    <!-- connectors draw first -->
    <path id="link" class="clip" data-start="0" data-duration="5" data-track-index="0"
          d="M540 560 C540 760 540 760 540 960" fill="none" stroke="var(--accent)" stroke-width="6" stroke-linecap="round"/>
    <!-- nodes pop in -->
    <circle id="n1" class="clip" data-start="0"   data-duration="5"   data-track-index="1" cx="540" cy="500"  r="90" fill="var(--bg-alt)" stroke="var(--accent)"   stroke-width="6"/>
    <circle id="n2" class="clip" data-start="0.6" data-duration="4.4" data-track-index="2" cx="540" cy="1020" r="90" fill="var(--bg-alt)" stroke="var(--accent-2)" stroke-width="6"/>
    <text id="t1" class="clip lbl" data-start="0.2" data-duration="4.8" data-track-index="3" x="540" y="510"  text-anchor="middle">IN</text>
    <text id="t2" class="clip lbl" data-start="0.8" data-duration="4.2" data-track-index="4" x="540" y="1035" text-anchor="middle">OUT</text>
  </svg>

  <style>
    [data-composition-id="svg-diagram"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="svg-diagram"] .diagram { width: 100%; height: 100%; }
    [data-composition-id="svg-diagram"] .lbl { font-family: "Outfit"; font-size: 56px; font-weight: 800; fill: var(--ink); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });

    // self-draw the connector
    const link = document.querySelector("[data-composition-id='svg-diagram'] #link");
    const len = link.getTotalLength();
    gsap.set(link, { strokeDasharray: len, strokeDashoffset: len });
    tl.to("#link", { strokeDashoffset: 0, duration: 0.9, ease: "power1.inOut" }, 0.3);

    tl.from("#n1", { scale: 0, transformOrigin: "540px 500px",  duration: 0.5, ease: "back.out(1.7)" }, 0.1);
    tl.from("#n2", { scale: 0, transformOrigin: "540px 1020px", duration: 0.5, ease: "back.out(1.7)" }, 0.7);
    tl.from("#t1", { opacity: 0, duration: 0.4, ease: "power1.out" }, 0.3);
    tl.from("#t2", { opacity: 0, duration: 0.4, ease: "power1.out" }, 0.9);

    // "firing" pulse: node 2 stroke color flash (finite yoyo)
    tl.to("#n2", { stroke: "var(--accent-3)", duration: 0.2, yoyo: true, repeat: 1 }, 1.3);

    window.__timelines["svg-diagram"] = tl;
  </script>
</div>
```

---

## Neural Network SVG Diagram

**Use when**: Visualizing layers, neurons, and data flow. Build node positions per layer, connect adjacent layers, and run a "firing wave" left-to-right. Light canvas; each layer gets its own accent.

Build the geometry deterministically in script (no `Math.random()`), then animate:
- **Layer pop-in:** stagger nodes by `layerIndex * 0.4s`, `back.out` ease.
- **Connection reveal:** fade edges in with a small stagger.
- **Firing wave:** brighten one layer at a time in sequence (finite yoyo).

```html
<div data-composition-id="neural-net" data-width="1080" data-height="1920">
  <svg class="net" viewBox="0 0 1080 1920" aria-hidden="true"></svg>

  <style>
    [data-composition-id="neural-net"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="neural-net"] .net { width: 100%; height: 100%; }
    [data-composition-id="neural-net"] .edge { stroke: rgba(37,99,235,.25); stroke-width: 2; fill: none; }
    [data-composition-id="neural-net"] .node { stroke-width: 0; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const svg = document.querySelector("[data-composition-id='neural-net'] .net");
    const COLORS = ["#6D5CE7", "#2563EB", "#16A34A"];   // light-safe layer accents
    const LAYERS = [4, 5, 3];
    const x0 = 220, xStep = 320, yPad = 520, yH = 880;
    const SVGNS = "http://www.w3.org/2000/svg";
    const pos = LAYERS.map((count, li) =>
      Array.from({ length: count }, (_, ni) => ({
        x: x0 + li * xStep,
        y: yPad + (count === 1 ? yH / 2 : (ni * yH) / (count - 1)),
        color: COLORS[li % COLORS.length],
      })));

    const edges = [];
    for (let li = 0; li < pos.length - 1; li++)
      pos[li].forEach((a) => pos[li + 1].forEach((b) => {
        const p = document.createElementNS(SVGNS, "line");
        p.setAttribute("class", "edge");
        p.setAttribute("x1", a.x); p.setAttribute("y1", a.y);
        p.setAttribute("x2", b.x); p.setAttribute("y2", b.y);
        svg.appendChild(p); edges.push(p);
      }));

    const nodes = [];
    pos.forEach((layer, li) => layer.forEach((n) => {
      const c = document.createElementNS(SVGNS, "circle");
      c.setAttribute("class", "node");
      c.setAttribute("cx", n.x); c.setAttribute("cy", n.y); c.setAttribute("r", 34);
      c.setAttribute("fill", n.color);
      svg.appendChild(c); nodes.push({ el: c, li });
    }));

    const tl = gsap.timeline({ paused: true });
    tl.from(edges, { opacity: 0, duration: 0.6, ease: "power1.out", stagger: 0.01 }, 0.2);
    nodes.forEach((n) =>
      tl.from(n.el, { scale: 0, transformOrigin: "center",
        duration: 0.45, ease: "back.out(1.7)" }, 0.1 + n.li * 0.4));
    // firing wave: brighten one layer at a time, finite
    pos.forEach((_, li) =>
      tl.to(nodes.filter((n) => n.li === li).map((n) => n.el),
        { scale: 1.25, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut" },
        1.6 + li * 0.25));

    window.__timelines["neural-net"] = tl;
  </script>
</div>
```

> If you'd rather not hand-roll this, the registry has `data-chart` for stats and `flowchart` for decision trees — `npx hyperframes add data-chart`.

---

## Word-by-Word Token Prediction

**Use when**: Token-prediction visualization / progressive sentence construction. Each step shows the accumulated words plus the newly predicted word; the final token gets a green check. Blinking cursor on incomplete states. Light canvas.

This is a caption-style accumulate pattern — build the sentence once, reveal one token per step:

```html
<div data-composition-id="token-pred" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div class="sentence">
      <span id="k0" class="clip tok"        data-start="0"   data-duration="6"   data-track-index="0">The</span>
      <span id="k1" class="clip tok"        data-start="0.7" data-duration="5.3" data-track-index="1">capital</span>
      <span id="k2" class="clip tok"        data-start="1.4" data-duration="4.6" data-track-index="2">of</span>
      <span id="k3" class="clip tok"        data-start="2.1" data-duration="3.9" data-track-index="3">France</span>
      <span id="k4" class="clip tok"        data-start="2.8" data-duration="3.2" data-track-index="4">is</span>
      <span id="k5" class="clip tok final"  data-start="3.5" data-duration="2.5" data-track-index="5">Paris</span>
      <span id="cur" class="cursor">▋</span>
    </div>
    <div id="check" class="clip check" data-start="3.6" data-duration="2.4" data-track-index="6">✓</div>
  </div>

  <style>
    [data-composition-id="token-pred"] { width: 100%; height: 100%; }
    [data-composition-id="token-pred"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 40px; padding: 0 80px; background: var(--bg);
    }
    [data-composition-id="token-pred"] .sentence {
      display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 10px 18px; max-width: 920px;
    }
    [data-composition-id="token-pred"] .tok {
      font-family: "Outfit"; font-size: 84px; font-weight: 700; color: var(--ink);
    }
    [data-composition-id="token-pred"] .final { color: var(--accent-2); }
    [data-composition-id="token-pred"] .cursor { font-family: "Outfit"; font-size: 84px; color: var(--accent); }
    [data-composition-id="token-pred"] .check { font-size: 96px; color: var(--accent-2); font-weight: 900; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // each predicted token slides up + fades in at its step time
    [["#k0",0.0],["#k1",0.7],["#k2",1.4],["#k3",2.1],["#k4",2.8],["#k5",3.5]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, y: 14, scale: 0.8, duration: 0.32, ease: "back.out(1.5)" }, at);
    });
    // blinking cursor while incomplete, then hand off to the check
    const blinkEnd = 3.5, cyc = 0.5;
    tl.fromTo("#cur", { opacity: 1 }, { opacity: 0.15, duration: cyc, ease: "steps(1)",
      yoyo: true, repeat: Math.ceil(blinkEnd / cyc) - 1 }, 0.1);
    tl.to("#cur", { opacity: 0, duration: 0.2 }, blinkEnd);          // cursor leaves once solved
    tl.from("#check", { opacity: 0, scale: 0, duration: 0.4, ease: "back.out(2)" }, 3.6);
    window.__timelines["token-pred"] = tl;
  </script>
</div>
```

> For a transcript-driven version (real narration), use the [Word-by-Word Sentence Build](#word-by-word-sentence-build) caption pattern with the mandatory `tl.set` exit kill per group.

---

## Probability Bars

**Use when**: "Most likely next word" visualizations and simple statistics. Horizontal bars fill to different widths; each row has a label (left), an animated fill, and a percentage (right). The winning bar uses the accent color; the rest are muted gray. Stagger appearance.

```html
<div data-composition-id="prob-bars" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="r0" class="clip bar win"  style="--p:78%" data-start="0"   data-duration="4"   data-track-index="0">
      <span class="lbl">Paris</span><span class="track"><span class="fill"></span></span><span class="pct">78%</span>
    </div>
    <div id="r1" class="clip bar"       style="--p:12%" data-start="0.3" data-duration="3.7" data-track-index="1">
      <span class="lbl">Lyon</span><span class="track"><span class="fill"></span></span><span class="pct">12%</span>
    </div>
    <div id="r2" class="clip bar"       style="--p:7%"  data-start="0.6" data-duration="3.4" data-track-index="2">
      <span class="lbl">Nice</span><span class="track"><span class="fill"></span></span><span class="pct">7%</span>
    </div>
    <div id="r3" class="clip bar"       style="--p:3%"  data-start="0.9" data-duration="3.1" data-track-index="3">
      <span class="lbl">Metz</span><span class="track"><span class="fill"></span></span><span class="pct">3%</span>
    </div>
  </div>

  <style>
    [data-composition-id="prob-bars"] { width: 100%; height: 100%; }
    [data-composition-id="prob-bars"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: center; gap: 32px;
      padding: 0 80px; background: var(--bg);
    }
    [data-composition-id="prob-bars"] .bar { display: grid; grid-template-columns: 220px 1fr 120px; align-items: center; gap: 24px; }
    [data-composition-id="prob-bars"] .lbl { font-family: "Inter"; font-size: 44px; font-weight: 700; color: var(--ink); }
    [data-composition-id="prob-bars"] .track { height: 44px; border-radius: 22px; background: #E5E1D6; overflow: hidden; }
    [data-composition-id="prob-bars"] .fill { display: block; height: 100%; width: var(--p); background: #B8B2A4; border-radius: 22px; transform-origin: left; }
    [data-composition-id="prob-bars"] .win .fill { background: var(--accent); }
    [data-composition-id="prob-bars"] .pct { font-family: ui-monospace, monospace; font-size: 40px; font-weight: 800; color: var(--ink); text-align: right; font-variant-numeric: tabular-nums; }
    [data-composition-id="prob-bars"] .win .pct { color: var(--accent); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    [["#r0",0.0],["#r1",0.3],["#r2",0.6],["#r3",0.9]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, x: -30, duration: 0.4, ease: "power2.out" }, at);
      tl.from(sel + " .fill", { scaleX: 0, duration: 0.7, ease: "power3.out" }, at + 0.1);
    });
    window.__timelines["prob-bars"] = tl;
  </script>
</div>
```

> Need a polished chart instead? `npx hyperframes add data-chart` gives an NYT-style bar+line chart with value labels.

---

# IMPACT & TRANSITION

---

## Kinetic Flash

**Use when**: "HERE'S HOW" transitions and statement reveals. A big word scale-pops in and an accent rule draws underneath. Light canvas.

```html
<div data-composition-id="kinetic-flash" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="txt"  class="clip txt"  data-start="0" data-duration="1.5" data-track-index="0">HERE'S HOW</div>
    <div id="rule" class="clip rule" data-start="0" data-duration="1.5" data-track-index="1"></div>
  </div>

  <style>
    [data-composition-id="kinetic-flash"] { width: 100%; height: 100%; }
    [data-composition-id="kinetic-flash"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 20px; background: var(--bg);
    }
    [data-composition-id="kinetic-flash"] .txt {
      font-family: "Outfit"; font-size: 160px; font-weight: 900; color: var(--ink);
      letter-spacing: -3px; text-align: center; line-height: 1;
    }
    [data-composition-id="kinetic-flash"] .rule {
      width: 60%; height: 7px; background: var(--accent); border-radius: 4px; transform-origin: center;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#txt",  { opacity: 0, scale: 0.5, duration: 0.45, ease: "back.out(2)" }, 0.1);
    tl.from("#rule", { scaleX: 0, duration: 0.4, ease: "power3.out" }, 0.35);
    window.__timelines["kinetic-flash"] = tl;
  </script>
</div>
```

> **Removed:** the old "Dark Impact with Video Background" snippet (dark `#050818` + neon glow) is intentionally gone. For dramatic statements over footage, use [B-Roll Full Bleed](#b-roll-full-bleed) with the neutral scrim and large light type — same impact, no dark-tech aesthetic.

---

## Scene Transitions

**Use when**: Cutting between any two scenes. In HyperFrames, the transition IS the exit. Follow the non-negotiable rules:

1. **Always transition** between scenes — no jump cuts.
2. **Always entrance-animate** every element of every scene via `gsap.from()`.
3. **Never exit-animate before a transition** — the outgoing scene must be fully visible when the transition fires.
4. **Only the final scene** may fade out.

**CSS transitions** (simplest — animate the scene container's opacity / transform / clip-path). Scenes 2+ start at `opacity: 0` and GSAP reveals them; the previous scene stays put underneath until covered.

```js
// in the ROOT composition timeline — scene-2 wrapper starts opacity:0 in CSS
tl.from("#scene-1 *", { opacity: 0, y: 30, duration: 0.5, ease: "power3.out", stagger: 0.08 }, 0.2);
// ... scene 1 holds fully visible (no exit tweens) ...
// push-slide transition: scene 2 slides up over scene 1
tl.fromTo("#scene-2", { yPercent: 100, opacity: 1 }, { yPercent: 0, duration: 0.45, ease: "power3.inOut" }, 4.0);
// only the FINAL scene fades out
tl.to("#scene-final", { opacity: 0, duration: 0.6, ease: "power2.in" }, 10.0);
```

**Shader transitions** (warp / dissolve / morph beyond CSS) composite both scene textures per-pixel on WebGL via `@hyperframes/shader-transitions`. Install a single-effect block and place it as the cut between two scenes — don't hand-write GLSL, and don't mix CSS and shader transitions in one composition:

```bash
npx hyperframes add cross-warp-morph   # premium morph
npx hyperframes add whip-pan           # fast camera whip (medium energy)
npx hyperframes add light-leak         # warm crossfade
```

**Choosing one** (pick ONE primary for 60–70% of cuts + 1–2 accents):
- **Calm:** blur crossfade / cross-warp-morph (0.5–0.8s, `sine`).
- **Medium:** push-slide / whip-pan / cinematic-zoom (0.3–0.5s, `power2`/`power3`).
- **High:** zoom-through / ridged-burn (0.15–0.3s, `power4`/`expo`).

Shader-compatible CSS (html2canvas capture): give every scene an explicit `background-color`, avoid the `transparent` keyword in gradients (use rgba at 0 alpha), and mark uncapturable decor `data-no-capture`.

---

# REGISTRY / COMPONENT-BASED SCENES (Use Sparingly)

These embed pre-made HyperFrames registry blocks/components as sub-compositions. **Limit to 2-3 per video** — overuse makes the piece feel templated. Install with `npx hyperframes add <name>`, then load via `data-composition-src` from the root, e.g.:

```html
<div data-composition-id="logo-outro" data-composition-src="compositions/logo-outro.html"
     data-start="10" data-duration="4" data-track-index="0"></div>
```

Browse everything: `npx hyperframes catalog` · https://hyperframes.heygen.com/catalog

---

## Logo Outro

**Use when**: Closing brand reveal — "Follow for more", logo + URL pill. Replaces the old custom logo-overlay component.

```bash
npx hyperframes add logo-outro
```

```html
<div data-composition-id="outro" data-composition-src="compositions/logo-outro.html"
     data-start="0" data-duration="4" data-track-index="0"
     data-variable-values='{"brand":"Retrofit AI","tagline":"Follow for more","url":"retrofit.ai"}'></div>
```

> `logo-outro` does piece-by-piece assembly, a glow bloom, tagline fade-in, and a URL pill. Pass per-instance content via `data-variable-values`.

---

## Video Card

**Use when**: A video/image showcase framed on a neutral canvas (prefer full-bleed [B-Roll](#b-roll-full-bleed) when you can). Build it inline — a non-timed wrapper holds the video so you can animate the frame:

```html
<div data-composition-id="video-card" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="frame" class="clip frame" data-start="0" data-duration="4" data-track-index="0">
      <div class="vidwrap">
        <video data-start="0" data-duration="4" data-track-index="1"
               src="assets/hook.mp4" muted playsinline crossorigin="anonymous"></video>
      </div>
    </div>
    <div id="cap" class="clip cap" data-start="0" data-duration="4" data-track-index="2">
      <span class="t">Quantum Computers</span><span class="s">A New Kind of Computing</span>
    </div>
  </div>

  <style>
    [data-composition-id="video-card"] { width: 100%; height: 100%; }
    [data-composition-id="video-card"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 40px; padding: 120px 80px; background: var(--bg);
    }
    [data-composition-id="video-card"] .frame {
      width: 100%; border-radius: 28px; overflow: hidden;
      box-shadow: 0 24px 60px rgba(0,0,0,.12); background: #000;
    }
    [data-composition-id="video-card"] .vidwrap { aspect-ratio: 4 / 3; }
    [data-composition-id="video-card"] .vidwrap video { width: 100%; height: 100%; object-fit: cover; }
    [data-composition-id="video-card"] .cap { display: flex; flex-direction: column; align-items: center; gap: 10px; text-align: center; }
    [data-composition-id="video-card"] .t { font-family: "Outfit"; font-size: 72px; font-weight: 800; color: var(--ink); }
    [data-composition-id="video-card"] .s { font-family: "Inter"; font-size: 40px; color: var(--ink-soft); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#frame", { opacity: 0, scale: 0.92, y: 30, duration: 0.55, ease: "power3.out" }, 0.1);
    tl.from("#cap",   { opacity: 0, y: 20, duration: 0.5, ease: "power2.out" }, 0.35);
    window.__timelines["video-card"] = tl;
  </script>
</div>
```

---

## Headline + Video Combo

**Use when**: Headline text with a video card below. Same idea as [Video Card](#video-card) with a headline block on top — entrance-stagger headline, then sub-headline, then the framed video. Keep the `<video>` inside a non-timed `.vidwrap` so the frame animates, not the video element:

```html
<div data-composition-id="head-video" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="h"  class="clip h"  data-start="0" data-duration="4" data-track-index="0">Revolutionary Tech</div>
    <div id="sh" class="clip sh" data-start="0" data-duration="4" data-track-index="1">See it in action</div>
    <div id="frame" class="clip frame" data-start="0" data-duration="4" data-track-index="2">
      <div class="vidwrap">
        <video data-start="0" data-duration="4" data-track-index="3"
               src="assets/demo.mp4" muted playsinline crossorigin="anonymous"></video>
      </div>
    </div>
  </div>

  <style>
    [data-composition-id="head-video"] { width: 100%; height: 100%; }
    [data-composition-id="head-video"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 24px; padding: 120px 80px 200px; background: var(--bg);
    }
    [data-composition-id="head-video"] .h  { font-family: "Outfit"; font-size: 88px; font-weight: 900; color: var(--ink); text-align: center; }
    [data-composition-id="head-video"] .sh { font-family: "Inter"; font-size: 44px; color: var(--ink-soft); margin-bottom: 16px; }
    [data-composition-id="head-video"] .frame { width: 100%; border-radius: 24px; overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,.12); background: #000; }
    [data-composition-id="head-video"] .vidwrap { aspect-ratio: 16 / 10; }
    [data-composition-id="head-video"] .vidwrap video { width: 100%; height: 100%; object-fit: cover; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#h",     { opacity: 0, y: 26, duration: 0.55, ease: "power3.out" }, 0.1);
    tl.from("#sh",    { opacity: 0, y: 18, duration: 0.45, ease: "power2.out" }, 0.3);
    tl.from("#frame", { opacity: 0, scale: 0.94, duration: 0.55, ease: "power3.out" }, 0.5);
    window.__timelines["head-video"] = tl;
  </script>
</div>
```

---

## Checklist Card

**Use when**: Good/bad practices or step-by-step reveals synced to audio. Rows reveal one by one, each with a status mark.

```html
<div data-composition-id="checklist" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="title" class="clip title" data-start="0" data-duration="5" data-track-index="0">Security Mistakes</div>
    <ul class="list">
      <li id="c0" class="clip row" data-start="0.3" data-duration="4.7" data-track-index="1"><span class="mk bad">✕</span>Using simple passwords</li>
      <li id="c1" class="clip row" data-start="0.9" data-duration="4.1" data-track-index="2"><span class="mk bad">✕</span>Clicking unknown links</li>
      <li id="c2" class="clip row" data-start="1.5" data-duration="3.5" data-track-index="3"><span class="mk bad">✕</span>Ignoring updates</li>
    </ul>
  </div>

  <style>
    [data-composition-id="checklist"] { width: 100%; height: 100%; }
    [data-composition-id="checklist"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: flex-start; justify-content: center;
      gap: 28px; padding: 0 100px; background: var(--bg);
    }
    [data-composition-id="checklist"] .title { font-family: "Outfit"; font-size: 80px; font-weight: 900; color: var(--ink); margin-bottom: 12px; }
    [data-composition-id="checklist"] .list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 28px; }
    [data-composition-id="checklist"] .row { display: flex; align-items: center; gap: 24px; font-family: "Inter"; font-size: 48px; font-weight: 600; color: var(--ink); }
    [data-composition-id="checklist"] .mk { width: 64px; height: 64px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; flex-shrink: 0; }
    [data-composition-id="checklist"] .bad { background: #FDE8E8; color: #DC2626; }
    [data-composition-id="checklist"] .good { background: #E6F6EC; color: #16A34A; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 20, duration: 0.5, ease: "power3.out" }, 0.1);
    [["#c0",0.3],["#c1",0.9],["#c2",1.5]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, x: -40, duration: 0.45, ease: "back.out(1.4)" }, at);
    });
    window.__timelines["checklist"] = tl;
  </script>
</div>
```

---

## Impact Word (Caption Component)

**Use when**: Dramatic full-screen text over footage. Instead of a dark-tinted component, layer a ready-made caption sub-composition over a [B-Roll Full Bleed](#b-roll-full-bleed) scene, or build the word inline. For a single full-screen word driven by transcript:

```bash
npx hyperframes add caption-kinetic-slam   # full-screen single word, alternating entrance directions
```

```html
<!-- in root: footage underneath, neutral scrim between, caption slam on top -->
<div data-composition-id="bg-bleed" data-composition-src="compositions/broll-bleed.html"
     data-start="8" data-duration="2.5" data-track-index="0"></div>
<div class="cap-scrim" data-start="8" data-duration="2.5" data-track-index="1"></div>
<div data-composition-id="slam" data-composition-src="compositions/caption-kinetic-slam.html"
     data-start="8" data-duration="2.5" data-track-index="2"></div>
```

If you'd rather keep it light-only (no footage), reuse the [Single Word Flash](#single-word-flash) at 180px on the neutral canvas. The caption component ships transparent — add the `.cap-scrim` (a semi-transparent neutral div) in the host only if the footage is bright.

---

## CTA (Headline Card)

**Use when**: Follow prompt, brand name, closing card. Light canvas with a soft dot-grid texture and a headline card. Build inline:

```html
<div data-composition-id="cta-card" data-width="1080" data-height="1920">
  <div class="dots" data-no-capture></div>
  <div class="scene-content">
    <div id="card" class="clip card" data-start="0" data-duration="4" data-track-index="0">
      <div class="l1">Retrofit AI</div>
      <div class="l2">Follow for More</div>
    </div>
  </div>

  <style>
    [data-composition-id="cta-card"] { width: 100%; height: 100%; position: relative; background: var(--bg); }
    [data-composition-id="cta-card"] .dots {
      position: absolute; inset: 0;
      background-image: radial-gradient(rgba(0,0,0,.06) 2px, transparent 2px);
      background-size: 48px 48px;
    }
    [data-composition-id="cta-card"] .scene-content {
      position: absolute; inset: 0; box-sizing: border-box;
      display: flex; align-items: center; justify-content: center;
    }
    [data-composition-id="cta-card"] .card {
      background: var(--bg-alt); border-radius: 36px; padding: 80px 100px;
      box-shadow: 0 30px 80px rgba(0,0,0,.12); text-align: center;
      display: flex; flex-direction: column; gap: 18px;
    }
    [data-composition-id="cta-card"] .l1 { font-family: "Outfit"; font-size: 96px; font-weight: 900; color: var(--accent); }
    [data-composition-id="cta-card"] .l2 { font-family: "Inter"; font-size: 52px; font-weight: 700; color: var(--ink); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#card",     { opacity: 0, scale: 0.85, duration: 0.5, ease: "back.out(1.5)" }, 0.1);
    tl.from("#card .l1", { opacity: 0, y: 16, duration: 0.4, ease: "power2.out" }, 0.3);
    tl.from("#card .l2", { opacity: 0, y: 12, duration: 0.4, ease: "power2.out" }, 0.45);
    window.__timelines["cta-card"] = tl;
  </script>
</div>
```

---

## CTA with Video Background

**Use when**: A CTA over moving footage. Keep it light: footage at full strength behind a soft neutral scrim, a white pill button that pops and pulses. No dark tint, no neon glow.

```html
<div data-composition-id="cta-video" data-width="1080" data-height="1920">
  <div class="ken">
    <video id="bg" data-start="0" data-duration="4" data-track-index="0"
           src="assets/cta-bg.mp4" muted playsinline crossorigin="anonymous"></video>
  </div>
  <div class="scrim"></div>
  <div class="scene-content">
    <div id="title" class="clip title" data-start="0" data-duration="4" data-track-index="1">Build it in HTML</div>
    <div id="btn"   class="clip btn"   data-start="0" data-duration="4" data-track-index="2">Get Started →</div>
  </div>

  <style>
    [data-composition-id="cta-video"] { width: 100%; height: 100%; position: relative; background: #000; }
    [data-composition-id="cta-video"] .ken { position: absolute; inset: 0; }
    [data-composition-id="cta-video"] .ken video { width: 100%; height: 100%; object-fit: cover; }
    [data-composition-id="cta-video"] .scrim {
      position: absolute; inset: 0; pointer-events: none;
      background: linear-gradient(to bottom, rgba(0,0,0,.25), rgba(0,0,0,.45));
    }
    [data-composition-id="cta-video"] .scene-content {
      position: absolute; inset: 0; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 40px;
    }
    [data-composition-id="cta-video"] .title { font-family: "Outfit"; font-size: 88px; font-weight: 800; color: #fff; text-shadow: 0 4px 24px rgba(0,0,0,.5); text-align: center; }
    [data-composition-id="cta-video"] .btn {
      font-family: "Inter"; font-size: 48px; font-weight: 700; color: var(--ink);
      background: #fff; padding: 28px 56px; border-radius: 999px; box-shadow: 0 16px 40px rgba(0,0,0,.3);
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.fromTo(".ken", { scale: 1.05 }, { scale: 1.12, duration: 4, ease: "none" }, 0);
    tl.from("#title", { opacity: 0, y: 24, duration: 0.5, ease: "power3.out" }, 0.2);
    tl.from("#btn",   { opacity: 0, scale: 0.8, duration: 0.45, ease: "back.out(1.7)" }, 0.5);
    // gentle pulse, finite
    const cyc = 0.8, dur = 4;
    tl.to("#btn", { scale: 1.04, duration: cyc, ease: "sine.inOut", yoyo: true,
                    repeat: Math.ceil((dur - 1) / cyc) - 1 }, 1.0);
    window.__timelines["cta-video"] = tl;
  </script>
</div>
```

---

## Grid Reveal Card

**Use when**: Binary bits or a data grid lighting up cell-by-cell with a progress counter. Build the grid deterministically (no `Math.random()`) and stagger the reveal.

```html
<div data-composition-id="grid-reveal" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div class="grid"></div>
    <div class="counter">0 / 64</div>
  </div>

  <style>
    [data-composition-id="grid-reveal"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="grid-reveal"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 48px;
    }
    [data-composition-id="grid-reveal"] .grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 14px; }
    [data-composition-id="grid-reveal"] .cell { width: 96px; height: 96px; border-radius: 14px; background: #E5E1D6; }
    [data-composition-id="grid-reveal"] .counter { font-family: ui-monospace, monospace; font-size: 56px; font-weight: 800; color: var(--ink); font-variant-numeric: tabular-nums; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const grid = document.querySelector("[data-composition-id='grid-reveal'] .grid");
    const N = 64, cells = [];
    for (let i = 0; i < N; i++) {
      const c = document.createElement("div");
      c.className = "cell";
      grid.appendChild(c); cells.push(c);
    }
    const counter = document.querySelector("[data-composition-id='grid-reveal'] .counter");

    const tl = gsap.timeline({ paused: true });
    cells.forEach((c, i) => {
      const at = 0.2 + i * 0.04;
      tl.to(c, { backgroundColor: "#2563EB", duration: 0.15, ease: "power1.out" }, at);
      tl.call(() => { counter.textContent = (i + 1) + " / " + N; }, [], at);
    });
    window.__timelines["grid-reveal"] = tl;
  </script>
</div>
```

---

## Hero Sphere Card

**Use when**: An orb / hero-object focal scene with title and label. Light canvas; a soft radial-gradient sphere pulses gently (radial gradients are H.264-safe).

```html
<div data-composition-id="hero-sphere" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="title" class="clip title" data-start="0" data-duration="4" data-track-index="0">The Core</div>
    <div id="orb"   class="clip orb"   data-start="0" data-duration="4" data-track-index="1"></div>
    <div id="label" class="clip label" data-start="0" data-duration="4" data-track-index="2">Always on</div>
  </div>

  <style>
    [data-composition-id="hero-sphere"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="hero-sphere"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 56px;
    }
    [data-composition-id="hero-sphere"] .title { font-family: "Outfit"; font-size: 84px; font-weight: 900; color: var(--ink); }
    [data-composition-id="hero-sphere"] .orb {
      width: 460px; height: 460px; border-radius: 50%;
      background: radial-gradient(circle at 38% 32%, #93B4FF 0%, var(--accent) 55%, #1E40AF 100%);
      box-shadow: 0 30px 90px rgba(37,99,235,.30);
    }
    [data-composition-id="hero-sphere"] .label { font-family: "Inter"; font-size: 44px; font-weight: 600; color: var(--ink-soft); letter-spacing: 2px; text-transform: uppercase; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 20, duration: 0.5, ease: "power3.out" }, 0.1);
    tl.from("#orb",   { opacity: 0, scale: 0.6, duration: 0.6, ease: "back.out(1.5)" }, 0.3);
    tl.from("#label", { opacity: 0, duration: 0.5, ease: "power1.out" }, 0.6);
    const cyc = 1.2, dur = 4;
    tl.to("#orb", { scale: 1.05, duration: cyc, ease: "sine.inOut", yoyo: true,
                    repeat: Math.ceil((dur - 1) / cyc) - 1 }, 1.0);
    window.__timelines["hero-sphere"] = tl;
  </script>
</div>
```

---

## Comparison Grid Card

**Use when**: Before/after or A-vs-B comparison. Two stacked panels: the top reveals cells sequentially, the bottom flashes all at once. Light canvas, labeled panels.

```html
<div data-composition-id="compare-grid" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div class="panel">
      <div class="plabel">Sequential</div>
      <div class="g top"></div>
    </div>
    <div class="panel">
      <div class="plabel">All at once</div>
      <div class="g bot"></div>
    </div>
  </div>

  <style>
    [data-composition-id="compare-grid"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="compare-grid"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: center; gap: 64px; padding: 0 80px;
    }
    [data-composition-id="compare-grid"] .panel { display: flex; flex-direction: column; gap: 24px; }
    [data-composition-id="compare-grid"] .plabel { font-family: "Inter"; font-size: 40px; font-weight: 700; color: var(--ink-soft); letter-spacing: 2px; text-transform: uppercase; }
    [data-composition-id="compare-grid"] .g { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; }
    [data-composition-id="compare-grid"] .cell { aspect-ratio: 1; border-radius: 12px; background: #E5E1D6; }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const mk = (sel, n) => {
      const g = document.querySelector("[data-composition-id='compare-grid'] " + sel);
      const out = [];
      for (let i = 0; i < n; i++) { const c = document.createElement("div"); c.className = "cell"; g.appendChild(c); out.push(c); }
      return out;
    };
    const top = mk(".g.top", 18), bot = mk(".g.bot", 18);
    const tl = gsap.timeline({ paused: true });
    top.forEach((c, i) => tl.to(c, { backgroundColor: "#2563EB", duration: 0.18, ease: "power1.out" }, 0.3 + i * 0.12));
    tl.to(bot, { backgroundColor: "#16A34A", duration: 0.25, ease: "power2.out" }, 2.6); // flash together
    window.__timelines["compare-grid"] = tl;
  </script>
</div>
```

---

## Icon Pyramid

**Use when**: Applications/features in a 2-top + 1-bottom pyramid. Each card: an icon tile in a gradient circle plus a label. Audio-synced staggered reveals.

```html
<div data-composition-id="icon-pyramid" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div class="row">
      <div id="p0" class="clip card" style="--c:#2563EB" data-start="0"   data-duration="4"   data-track-index="0"><span class="ic">⚡</span><span class="lbl">Fast</span></div>
      <div id="p1" class="clip card" style="--c:#16A34A" data-start="0.4" data-duration="3.6" data-track-index="1"><span class="ic">🔒</span><span class="lbl">Secure</span></div>
    </div>
    <div id="p2" class="clip card" style="--c:#D97706" data-start="0.8" data-duration="3.2" data-track-index="2"><span class="ic">📈</span><span class="lbl">Scalable</span></div>
  </div>

  <style>
    [data-composition-id="icon-pyramid"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="icon-pyramid"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 56px;
    }
    [data-composition-id="icon-pyramid"] .row { display: flex; gap: 56px; }
    [data-composition-id="icon-pyramid"] .card { display: flex; flex-direction: column; align-items: center; gap: 24px; }
    [data-composition-id="icon-pyramid"] .ic {
      width: 200px; height: 200px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 84px;
      background: linear-gradient(135deg, var(--c), color-mix(in srgb, var(--c) 60%, white));
      box-shadow: 0 18px 44px color-mix(in srgb, var(--c) 30%, transparent);
    }
    [data-composition-id="icon-pyramid"] .lbl { font-family: "Outfit"; font-size: 52px; font-weight: 800; color: var(--ink); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    [["#p0",0.0],["#p1",0.4],["#p2",0.8]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, scale: 0.6, y: 30, duration: 0.5, ease: "back.out(1.6)" }, at);
    });
    window.__timelines["icon-pyramid"] = tl;
  </script>
</div>
```

---

## Data Sources Vertical Stack

**Use when**: Listing data sources with icon + label + subtitle and a per-card accent. Horizontal cards stacked vertically with a subtle float. Light canvas.

```html
<div data-composition-id="sources" data-width="1080" data-height="1920">
  <div class="scene-content">
    <div id="s0" class="clip card" style="--c:#2563EB" data-start="0"   data-duration="4"   data-track-index="0"><span class="ic">🌐</span><span class="meta"><b>Web Crawl</b><i>2.1B pages</i></span></div>
    <div id="s1" class="clip card" style="--c:#16A34A" data-start="0.4" data-duration="3.6" data-track-index="1"><span class="ic">📚</span><span class="meta"><b>Books</b><i>40M volumes</i></span></div>
    <div id="s2" class="clip card" style="--c:#D97706" data-start="0.8" data-duration="3.2" data-track-index="2"><span class="ic">💬</span><span class="meta"><b>Dialogue</b><i>900M turns</i></span></div>
  </div>

  <style>
    [data-composition-id="sources"] { width: 100%; height: 100%; background: var(--bg); }
    [data-composition-id="sources"] .scene-content {
      width: 100%; height: 100%; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: center; gap: 32px; padding: 0 80px;
    }
    [data-composition-id="sources"] .card {
      display: flex; align-items: center; gap: 32px; padding: 32px 40px;
      background: var(--bg-alt); border-radius: 24px; border-left: 8px solid var(--c);
      box-shadow: 0 12px 32px rgba(0,0,0,.08);
    }
    [data-composition-id="sources"] .ic { font-size: 64px; }
    [data-composition-id="sources"] .meta { display: flex; flex-direction: column; gap: 6px; }
    [data-composition-id="sources"] .meta b { font-family: "Outfit"; font-size: 56px; font-weight: 800; color: var(--ink); }
    [data-composition-id="sources"] .meta i { font-family: "Inter"; font-size: 38px; font-style: normal; color: var(--ink-soft); }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    const dur = 4, cyc = 2;
    [["#s0",0.0],["#s1",0.4],["#s2",0.8]].forEach(([sel, at]) => {
      tl.from(sel, { opacity: 0, x: -50, duration: 0.5, ease: "back.out(1.3)" }, at);
      // subtle float, finite repeat (no repeat:-1)
      tl.to(sel, { y: -10, duration: cyc, ease: "sine.inOut", yoyo: true,
                   repeat: Math.ceil((dur - 1) / cyc) - 1 }, at + 0.6);
    });
    window.__timelines["sources"] = tl;
  </script>
</div>
```

---

# AUDIO

---

## SFX Layer Template

Add sound effects on their own audio tracks in the **root** composition. Each is a separate `<audio>` element with `data-volume` — never piggyback sound on a (muted) video. Place them at absolute second positions; trim into a source with `data-media-start` if needed.

```html
<!-- in the root composition, on dedicated high track indices -->
<audio id="sfx-whoosh" src="assets/sfx/whoosh.wav" data-volume="0.25"
       data-start="15.0" data-duration="0.8" data-track-index="20"></audio>
<audio id="sfx-pop"    src="assets/sfx/pop.wav"    data-volume="0.20"
       data-start="2.45" data-duration="0.5" data-track-index="21"></audio>
<audio id="sfx-impact" src="assets/sfx/impact.wav" data-volume="0.30"
       data-start="58.0" data-duration="2.0" data-track-index="22"></audio>
```

**Notes:**
- Audio clips need no `class="clip"` and no GSAP — they're driven entirely by their `data-*` timing.
- `data-volume` is `0–1`. The framework owns playback; don't call `audio.play()`.
- For a music bed, add one long `<audio>` on its own track. For voiceover, generate it with `npx hyperframes tts script.txt -o narration.wav`, then transcribe for captions with `npx hyperframes transcribe narration.wav`.

---

## Quick Reference (Remotion → HyperFrames)

| Remotion concept | HyperFrames equivalent |
| --- | --- |
| `useCurrentFrame()` + frame math | a GSAP tween at an absolute time position (seconds) |
| `spring()` | `ease: "back.out(n)"` / `elastic.out` overshoot |
| `<Sequence from durationInFrames>` | `data-start` / `data-duration` (seconds) on the element |
| frame `N` @30fps | `N / 30` seconds |
| `<Img src={staticFile('x')}>` | `<img src="assets/x">` |
| `<Video>` / `<OffthreadVideo>` | `<video muted playsinline>` (+ separate `<audio data-volume>`) |
| `<Audio volume>` | `<audio data-volume>` on its own track |
| `<AbsoluteFill>` | `.scene-content` flex container (padding to inset) |
| `isDarkBackground()` flag | not needed — light/neutral palette throughout |
| exit animations before a cut | banned — the transition IS the exit |
| `Math.random()` | seeded mulberry32 (determinism is non-negotiable) |

```js
// mulberry32 — the only sanctioned source of pseudo-randomness
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(1234);   // fixed seed → identical every render
```
