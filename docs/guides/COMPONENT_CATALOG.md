# HyperFrames Component Catalog

Patterns and ready-made building blocks for "brand-autopsy" style explainer videos in **HyperFrames** (HTML + CSS + paused GSAP timeline).

There are no React components to import here. A HyperFrames composition is:

- an **HTML file** whose root is a `<div data-composition-id="..." data-width data-height>`,
- timed elements carrying `data-start` / `data-duration` / `data-track-index` (all in **seconds**),
- a single **paused** GSAP timeline registered on `window.__timelines["<id>"]`,
- plain CSS for appearance and `z-index` for stacking.

Two ways to reuse a "component":

1. **Registry component/block** — installed with `npx hyperframes add <name>` and embedded via `data-composition-src`. See [Registry Catalog](#registry-catalog).
2. **Inline pattern** — a small HTML+CSS+GSAP snippet you paste into your composition. Each entry below gives one or both.

> Timing conversion from the old library: **seconds = frame / 30**. A `delayFrames={30}` becomes `0.5` seconds; `framesPerCell={5}` becomes `5/30 ≈ 0.167` seconds per cell. Work in seconds directly — there is no `secToFrame`/`inScene` anymore.

---

## Table of Contents

1. [Registry Catalog](#registry-catalog)
2. [Background Components](#background-components)
3. [Card Components](#card-components)
4. [Advanced Scene Components](#advanced-scene-components)
5. [Overlay Components](#overlay-components)
6. [Utility Components](#utility-components)
7. [Theme Constants](#theme-constants)
8. [Helpers](#helpers)

---

## Registry Catalog

Before building from scratch, check the registry — many "components" already exist as ready-made blocks.

```bash
npx hyperframes catalog                 # list all ~111 blocks & components
npx hyperframes catalog --tag caption-style
npx hyperframes catalog --tag data
npx hyperframes catalog --json
npx hyperframes add <name>              # install into the project
```

Mapping the old library to ready-made registry items:

| Need (old component) | Registry item | Install |
|---|---|---|
| Film texture / warmth over a scene | `grain-overlay` | `npx hyperframes add grain-overlay` |
| Edge darkening / focus pull | `vignette` | `npx hyperframes add vignette` |
| Premium light sweep on a reveal | `shimmer-sweep` | `npx hyperframes add shimmer-sweep` |
| Texture through letterforms | `texture-mask-text` | `npx hyperframes add texture-mask-text` |
| Word-by-word kinetic impact (old `KineticTypography`) | `caption-kinetic-slam` | `npx hyperframes add caption-kinetic-slam` |
| Karaoke / per-word captions | `caption-pill-karaoke`, `caption-highlight` | `npx hyperframes add caption-highlight` |
| Particle burst on impact word | `caption-particle-burst` | `npx hyperframes add caption-particle-burst` |
| News / social card (old `NewsArticleCard`) | `x-post`, `reddit-post`, `macos-notification` | `npx hyperframes add x-post` |
| Data grid / stats (old `GridRevealCard` stats) | `data-chart`, `us-map*`, `world-map` | `npx hyperframes add data-chart` |
| Decision tree / flow | `flowchart`, `flowchart-vertical` (portrait) | `npx hyperframes add flowchart` |
| Logo outro | `logo-outro` | `npx hyperframes add logo-outro` |
| Scene-to-scene cut (replaces hard cuts) | a single shader transition, e.g. `light-leak`, `cross-warp-morph`, `glitch` | `npx hyperframes add light-leak` |
| Grid dissolve between scenes | `grid-pixelate-wipe` | `npx hyperframes add grid-pixelate-wipe` |

Everything below is for the cases the registry does not cover — your own brand cards and overlays.

---

## Background Components

Backgrounds are CSS + GSAP layers placed at low `z-index` behind a `.scene-content` container. Keep a **light/neutral** palette (see [Theme Constants](#theme-constants)). Avoid full-screen linear gradients (H.264 banding) — prefer radial or solid + localized glow.

### BeigeCanvas

Warm beige base with a soft radial wash. Pure CSS, no animation needed.

**When to use:** the default backdrop for any brand-autopsy scene.

```html
<div id="bg" class="beige-canvas"></div>
<style>
  .beige-canvas {
    position: absolute; inset: 0; z-index: 0;
    background:
      radial-gradient(circle at 50% 38%, #F2ECDD 0%, #E8E0D0 55%, #DED4C0 100%);
  }
</style>
```

This is a static, untimed decorative layer — no timeline registration needed. If you want a slow life to it, animate a wrapper, not the page:

```js
tl.fromTo("#bg", { scale: 1.06 }, { scale: 1, duration: 6, ease: "sine.inOut" }, 0);
```

---

### DotGrid

Drifting dot pattern for subtle texture. Built from a repeating radial-gradient so it stays deterministic.

**When to use:** behind cards to add depth without busyness.

```html
<div id="dots" class="dot-grid"></div>
<style>
  .dot-grid {
    position: absolute; inset: -40px; z-index: 1;
    opacity: 0.05;
    background-image: radial-gradient(rgba(47,36,20,1) 2px, transparent 2px);
    background-size: 30px 30px;   /* spacing */
  }
</style>
<script>
  // drift the pattern slowly (finite, deterministic)
  tl.to("#dots", { backgroundPositionX: 30, backgroundPositionY: 30,
                   duration: 8, ease: "none" }, 0);
</script>
```

Tunables: dot size = the `2px` radius, `spacing` = `background-size`, `opacity` on the element.

---

### FloatingShapes

Soft circles that drift on sine/cosine paths. Use a small fixed set of shapes (no `Math.random`) so renders are reproducible.

**When to use:** ambient motion behind headline or icon scenes.

```html
<div class="floaters" aria-hidden="true">
  <span class="floater f1"></span>
  <span class="floater f2"></span>
  <span class="floater f3"></span>
</div>
<style>
  .floaters { position: absolute; inset: 0; z-index: 1; pointer-events: none; }
  .floater { position: absolute; border-radius: 50%;
             background: radial-gradient(circle, rgba(108,92,231,0.18), transparent 70%); }
  .f1 { width: 360px; height: 360px; top: 12%; left: 8%; }
  .f2 { width: 280px; height: 280px; top: 58%; left: 70%; }
  .f3 { width: 200px; height: 200px; top: 70%; left: 18%; }
</style>
<script>
  // gentle, finite drift — different phase per shape (scene is 10s)
  tl.to(".f1", { x: 40, y: -30, duration: 7, ease: "sine.inOut", yoyo: true,
                 repeat: Math.ceil(10/7) - 1 }, 0);
  tl.to(".f2", { x: -50, y: 25, duration: 8, ease: "sine.inOut", yoyo: true,
                 repeat: Math.ceil(10/8) - 1 }, 0);
  tl.to(".f3", { x: 30, y: 40, duration: 6, ease: "sine.inOut", yoyo: true,
                 repeat: Math.ceil(10/6) - 1 }, 0);
</script>
```

Never use `repeat: -1` — compute a finite repeat count from the scene duration.

---

### SubtleGradientShift

Slow color-temperature shift for depth. Animate a radial overlay's opacity, not a full-screen linear gradient.

**When to use:** long holds where a perfectly static frame would feel dead.

```html
<div id="shift" class="grad-shift"></div>
<style>
  .grad-shift {
    position: absolute; inset: 0; z-index: 1; mix-blend-mode: multiply;
    background: radial-gradient(circle at 40% 40%, rgba(91,143,185,0.10), transparent 60%);
  }
</style>
<script>
  tl.to("#shift", { opacity: 0.6, duration: 6, ease: "sine.inOut",
                    yoyo: true, repeat: 1 }, 0);
</script>
```

---

## Card Components

A "card" is a `.scene-content` flex column (it fills the scene via `width:100%;height:100%;padding`) holding a centered card surface. Build the hero frame in CSS first, then add `gsap.from()` entrances.

### HeadlineCard

Two-line floating headline.

**When to use:** intros, section dividers, "follow for more" outros.

```html
<div data-composition-id="headline" data-width="1920" data-height="1080">
  <div class="beige-canvas"></div>
  <div class="scene-content">
    <div class="headline-card">
      <h1 id="line1">Retrofit AI</h1>
      <h2 id="line2">Follow for More</h2>
    </div>
  </div>
  <style>
    [data-composition-id="headline"] .scene-content{
      display:flex; align-items:center; justify-content:center;
      width:100%; height:100%; padding:160px; box-sizing:border-box;
    }
    .headline-card{
      background:#FFFFFF; border-radius:28px; padding:80px 100px;
      box-shadow:0 16px 44px rgba(47,36,20,0.2); text-align:center;
    }
    #line1{ font-family:Inter,sans-serif; font-weight:800; font-size:120px;
            color:#2F2414; margin:0; }
    #line2{ font-family:Inter,sans-serif; font-weight:600; font-size:48px;
            color:#5B8FB9; margin:16px 0 0; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from(".headline-card", { scale: 0.9, opacity: 0, duration: 0.6, ease: "back.out(1.5)" }, 0.2);
    tl.from("#line1", { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.35);
    tl.from("#line2", { y: 30, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.55);
    window.__timelines["headline"] = tl;
  </script>
</div>
```

To swap the old `tone` choice, change the card surface / accent colors — keep them inside the light palette. For a background image, add an `<img class="clip">` behind the card (see VideoCard).

---

### VideoCard

Centered media card on the beige base. Image uses `<img class="clip">`; video uses a `<video muted playsinline>` (no `class="clip"`) wrapped in an untimed div so you can animate the wrapper.

**When to use:** product demo / B-roll framed inside a brand card.

```html
<div class="scene-content">
  <div class="media-card">
    <!-- IMAGE variant -->
    <img id="shot" class="clip" src="assets/product.jpg"
         data-start="0" data-duration="5" data-track-index="0" />
    <!-- VIDEO variant: video is NOT a clip; wrap to animate -->
    <div class="video-wrap">
      <video id="demo" src="assets/demo.mp4" muted playsinline
             data-start="0" data-duration="5" data-track-index="0"></video>
    </div>
    <div class="caption">
      <div class="title">Product Demo</div>
      <div class="subtitle">See it in action</div>
    </div>
  </div>
</div>
<style>
  .media-card{ background:#FFF; border-radius:24px; padding:24px;
               box-shadow:0 16px 44px rgba(47,36,20,0.2); }
  .media-card img, .video-wrap video{ width:1200px; height:675px;
               object-fit:cover; border-radius:16px; display:block; }
  .caption .title{ font:700 40px Inter; color:#2F2414; margin-top:20px; }
  .caption .subtitle{ font:500 26px Inter; color:#6B5E4A; }
</style>
<script>
  tl.from(".media-card", { y: 50, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
  // animate the WRAPPER for video, never the <video> dimensions
  tl.from(".video-wrap", { scale: 0.94, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.3);
</script>
```

If the source clip carries audio you want, add a **separate** `<audio>` element (the video stays muted):

```html
<audio id="demo-audio" src="assets/demo.mp4" data-start="0" data-duration="5"
       data-track-index="3" data-volume="1"></audio>
```

---

### ChecklistCard

Checklist with staggered reveals; each row marked good / bad / neutral.

**When to use:** "do this, not that" segments, audits, security checklists.

```html
<div class="scene-content">
  <div class="checklist-card">
    <h2 id="cl-title">Security Checklist</h2>
    <ul class="check-list">
      <li class="row good"><span class="mark">✓</span>Strong passwords</li>
      <li class="row bad"><span class="mark">✕</span>Weak passwords</li>
      <li class="row good"><span class="mark">✓</span>2FA enabled</li>
    </ul>
  </div>
</div>
<style>
  .checklist-card{ background:#FFF; border-radius:24px; padding:64px 72px;
                   box-shadow:0 16px 44px rgba(47,36,20,0.2); min-width:760px; }
  #cl-title{ font:800 56px Inter; color:#2F2414; margin:0 0 32px; }
  .row{ display:flex; align-items:center; gap:20px; font:600 38px Inter;
        color:#2F2414; list-style:none; padding:14px 0; }
  .mark{ width:48px; height:48px; border-radius:50%; display:grid;
         place-items:center; color:#FFF; font-size:28px; }
  .good .mark{ background:#1A9E55; }      /* GREEN_CHECK */
  .bad  .mark{ background:#D93025; }      /* RED_X */
</style>
<script>
  tl.from("#cl-title", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.2);
  // stagger rows — old delayFrames (0,30,60) ÷ 30 = 0, 1.0, 2.0s; tightened here
  tl.from(".row", { x: -40, opacity: 0, duration: 0.5, ease: "power2.out",
                    stagger: 0.5 }, 0.5);
</script>
```

Background dot grid / floaters: add the [DotGrid](#dotgrid) and [FloatingShapes](#floatingshapes) layers behind `.scene-content`.

---

### NewsArticleCard

Publication card with logo, headline, body, and a highlighted callout.

**When to use:** citing a news beat. For an authentic social look, prefer the registry blocks `x-post` / `reddit-post` instead.

```html
<div class="scene-content">
  <article class="news-card">
    <img id="pub-logo" class="clip" src="assets/techcrunch.png"
         data-start="0" data-duration="5" data-track-index="0" />
    <h2 id="news-headline">Breaking: New AI Breakthrough</h2>
    <p id="news-body">Scientists discover a faster path to drug candidates…</p>
    <span id="news-highlight">70% improvement</span>
  </article>
</div>
<style>
  .news-card{ background:#FFF; border-radius:20px; padding:56px 64px;
              box-shadow:0 8px 30px rgba(0,0,0,0.15); max-width:1100px; }
  #pub-logo{ height:56px; width:auto; }
  #news-headline{ font:800 64px Inter; color:#2F2414; margin:28px 0 18px; }
  #news-body{ font:400 30px Inter; color:#5A5042; line-height:1.4; max-width:900px; }
  #news-highlight{ display:inline-block; margin-top:24px; padding:8px 18px;
                   background:#FCE36B; color:#2F2414; font:700 30px Inter;
                   border-radius:8px; }
</style>
<script>
  tl.from("#pub-logo", { opacity: 0, y: -20, duration: 0.4, ease: "power2.out" }, 0.2);
  tl.from("#news-headline", { y: 36, opacity: 0, duration: 0.55, ease: "power3.out" }, 0.4);
  tl.from("#news-body", { y: 24, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.6);
  tl.fromTo("#news-highlight", { scaleX: 0, transformOrigin: "left center" },
            { scaleX: 1, duration: 0.4, ease: "power2.out" }, 0.85);
</script>
```

---

### IconCard

Single icon with a label. Use an inline `<svg>` or an `<img class="clip">` icon — no icon React library.

**When to use:** one concept per card (e.g. "Drug Discovery").

```html
<div class="scene-content">
  <div class="icon-card">
    <div class="icon-ring">
      <svg viewBox="0 0 24 24" width="60" height="60" fill="none"
           stroke="#FFF" stroke-width="2">
        <path d="M4 4c8 4 8 12 16 16M20 4C12 8 12 16 4 20"/>
      </svg>
    </div>
    <div class="icon-label">Drug Discovery</div>
  </div>
</div>
<style>
  .icon-card{ display:flex; flex-direction:column; align-items:center; gap:28px; }
  .icon-ring{ width:160px; height:160px; border-radius:50%;
              background:linear-gradient(135deg,#6C5CE7,#5B8FB9);
              display:grid; place-items:center;
              box-shadow:0 12px 30px rgba(108,92,231,0.35); }
  .icon-label{ font:700 40px Inter; color:#2F2414; }
</style>
<script>
  // old delayFrames={30} → 1.0s; tightened to 0.4s here
  tl.from(".icon-ring", { scale: 0, opacity: 0, duration: 0.5, ease: "back.out(1.7)" }, 0.4);
  tl.from(".icon-label", { y: 24, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.65);
</script>
```

---

## Advanced Scene Components

These were the heaviest old components. In HyperFrames you build the grid/structure as static HTML, then drive reveals with a GSAP **stagger** on the timeline.

### GridRevealCard

Sequential cell reveal (binary bits, data grids). Generate cells deterministically; reveal with a per-cell stagger (old `framesPerCell` ÷ 30 = seconds between cells).

**When to use:** "one at a time" demonstrations, classical-bit grids, loading metaphors.

```html
<div class="scene-content">
  <h2 id="gr-title">Classical Bits</h2>
  <div id="gr-sub">ONE AT A TIME</div>
  <div id="grid" class="bit-grid"></div>
  <div id="gr-counter" class="counter">0 / 24</div>
</div>
<style>
  .bit-grid{ display:grid; grid-template-columns:repeat(6, 80px);
             gap:10px; justify-content:center; margin-top:28px; }
  .cell{ width:80px; height:80px; border-radius:12px; background:#FFF;
         box-shadow:0 8px 30px rgba(0,0,0,0.15);
         display:grid; place-items:center; font:800 40px Inter; color:#2F2414; }
  #gr-title{ font:800 64px Inter; color:#2F2414; text-align:center; margin:0; }
  #gr-sub{ font:600 26px Inter; color:#6C5CE7; text-align:center; letter-spacing:3px; }
  .counter{ font:700 30px Inter; font-variant-numeric:tabular-nums;
            color:#2F2414; text-align:center; margin-top:20px; }
</style>
<script>
  const perCell = 5 / 30; // framesPerCell=5 → seconds per cell
  const values = [1,0,1,1,0,0, 1,0,1,0,1,1, 0,1,0,1,1,0, 1,1,0,0,1,0];
  const grid = document.getElementById("grid");
  values.forEach(v => {
    const c = document.createElement("div");
    c.className = "cell"; c.textContent = v; grid.appendChild(c);
  });
  tl.from("#gr-title", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.2);
  tl.from("#gr-sub",   { y: 20, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.4);
  tl.from(".cell", { scale: 0, opacity: 0, duration: 0.25, ease: "back.out(1.7)",
                     stagger: perCell }, 0.6);
  // counter ticks up in lockstep with the stagger
  const total = values.length, counter = document.getElementById("gr-counter");
  for (let i = 1; i <= total; i++){
    tl.call(() => { counter.textContent = `${i} / ${total}`; }, [], 0.6 + i * perCell);
  }
</script>
```

For a real animated chart instead of a hand-rolled grid, use the registry block: `npx hyperframes add data-chart`.

---

### HeroSphereCard

Light-theme hero scene with a glowing orb. The original dark+neon variant is **dropped** — this keeps the neutral palette with a localized glow (avoids dark-bg banding).

**When to use:** a single conceptual "hero" beat (e.g. superposition, a core idea).

```html
<div class="scene-content sphere-scene">
  <h1 id="sp-title">QUANTUM QUBITS</h1>
  <div id="sp-sub">0 AND 1 AT THE SAME TIME</div>
  <div class="sphere"><span class="orb-label">0</span><span class="orb-label">1</span></div>
  <div id="sp-bottom">SUPERPOSITION</div>
</div>
<style>
  .sphere-scene{ display:flex; flex-direction:column; align-items:center;
                 justify-content:center; gap:28px; }
  .sphere{ width:300px; height:300px; border-radius:50%;
           background:radial-gradient(circle at 38% 32%, #FFFFFF, #BFD3E6 60%, #8FB4D6 100%);
           box-shadow:0 0 80px rgba(91,143,185,0.45);
           display:flex; align-items:center; justify-content:center; gap:40px;
           font:800 64px Inter; color:#2F2414; }
  #sp-title{ font:800 88px Inter; color:#2F2414; margin:0; }
  #sp-sub{ font:600 30px Inter; color:#5B8FB9; letter-spacing:3px; }
  #sp-bottom{ font:800 40px Inter; color:#6C5CE7; letter-spacing:4px; }
</style>
<script>
  tl.from("#sp-title", { y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
  tl.from("#sp-sub",   { y: 24, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.45);
  tl.from(".sphere",   { scale: 0.6, opacity: 0, duration: 0.7, ease: "back.out(1.4)" }, 0.6);
  // pulse (finite repeat over a 6s scene)
  tl.to(".sphere", { scale: 1.04, duration: 1.2, ease: "sine.inOut",
                     yoyo: true, repeat: Math.ceil(6/1.2) - 1 }, 1.4);
  // old bottomLabelDelayFrames={50} → ~1.67s
  tl.from("#sp-bottom", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, 1.7);
</script>
```

---

### ComparisonGridCard

Side-by-side "one by one vs all at once" comparison. Top grid reveals with a stagger; bottom grid flashes on all at once at a fixed time (old `flashFrame` ÷ 30).

**When to use:** classical-vs-parallel, slow-vs-fast, before-vs-after.

```html
<div class="scene-content">
  <h2 id="cmp-title">Classical vs Quantum</h2>
  <div class="panel"><div class="panel-label">CLASSICAL — ONE BY ONE</div>
       <div id="top-grid" class="mini-grid"></div></div>
  <div class="panel"><div class="panel-label">QUANTUM</div>
       <div id="bot-grid" class="mini-grid"></div>
       <div id="cmp-emphasis" class="emphasis">⚡ ALL AT ONCE ⚡</div></div>
</div>
<style>
  .panel{ margin:18px 0; }
  .panel-label{ font:700 28px Inter; color:#2F2414; margin-bottom:12px; }
  .mini-grid{ display:grid; grid-template-columns:repeat(6, 50px); gap:6px; }
  .mini-grid .cell{ width:50px; height:50px; border-radius:8px; background:#6C5CE7; }
  .emphasis{ font:800 44px Inter; color:#6C5CE7; margin-top:14px; }
</style>
<script>
  const N = 6, perCell = 4 / 30, flashAt = 100 / 30; // framesPerCell, flashFrame
  const mk = (id) => { const g = document.getElementById(id);
    for (let i = 0; i < N*N; i++){ const c = document.createElement("div");
      c.className = "cell"; g.appendChild(c); } };
  mk("top-grid"); mk("bot-grid");
  tl.from("#cmp-title", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.2);
  // top: slow one-by-one
  tl.from("#top-grid .cell", { scale: 0, opacity: 0, duration: 0.2,
                               ease: "back.out(1.7)", stagger: perCell }, 0.5);
  // bottom: hidden until the flash, then all at once
  tl.set("#bot-grid .cell", { scale: 0, opacity: 0 }, 0);
  tl.to("#bot-grid .cell", { scale: 1, opacity: 1, duration: 0.3, ease: "power2.out" }, flashAt);
  tl.from("#cmp-emphasis", { scale: 0.7, opacity: 0, duration: 0.4,
                             ease: "back.out(2)" }, flashAt);
</script>
```

---

### IconGridCard

Grid / pyramid of icon cards revealed in sequence.

**When to use:** "applications" or "features" beats with 3–6 items.

```html
<div class="scene-content">
  <h2 id="ig-title">Applications</h2>
  <div class="icon-grid pyramid">
    <div class="ig-item"><div class="ig-icon">🧬</div><div class="ig-label">Drug Discovery</div></div>
    <div class="ig-item"><div class="ig-icon">🌍</div><div class="ig-label">Climate Modeling</div></div>
    <div class="ig-item"><div class="ig-icon">📈</div><div class="ig-label">Predictions</div></div>
  </div>
</div>
<style>
  #ig-title{ font:800 64px Inter; color:#2F2414; text-align:center; margin:0 0 40px; }
  .icon-grid{ display:flex; gap:24px; justify-content:center; flex-wrap:wrap; }
  .ig-item{ width:420px; background:#FFF; border-radius:20px; padding:40px;
            box-shadow:0 8px 30px rgba(0,0,0,0.15); text-align:center; }
  .ig-icon{ font-size:96px; line-height:1; }
  .ig-label{ font:700 34px Inter; color:#2F2414; margin-top:18px; }
  /* layout="pyramid": let flex-wrap balance the last row */
</style>
<script>
  tl.from("#ig-title", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.2);
  // old per-item delayFrames 30/60/90 → 1.0/2.0/3.0s; here a tighter 0.4s stagger
  tl.from(".ig-item", { y: 50, opacity: 0, scale: 0.9, duration: 0.5,
                        ease: "back.out(1.4)", stagger: 0.4 }, 0.5);
</script>
```

For inline SVG icons instead of emoji, drop an `<svg>` into `.ig-icon` (see [IconCard](#iconcard)).

---

## Overlay Components

Overlays sit above a talking-head or B-roll `<video>` at a higher `z-index`. The video stays `muted playsinline`; the overlay is HTML+GSAP. There is no `speed` prop — author timing against the clip's real seconds (trim with `data-media-start` if needed).

### ImpactWord

Full-screen dramatic word over tinted media.

**When to use:** a single hard-hitting word punctuating narration.

```html
<div data-composition-id="impact" data-width="1920" data-height="1080">
  <video id="impact-bg" src="assets/impact_bg.mp4" muted playsinline
         data-start="0" data-duration="3" data-track-index="0"></video>
  <div id="impact-tint" class="tint"></div>
  <div class="scene-content impact-stage">
    <h1 id="impact-word">THE FUTURE</h1>
  </div>
  <style>
    [data-composition-id="impact"] .tint{ position:absolute; inset:0; z-index:1;
       background:rgba(91,143,185,0.45); }   /* light-palette tint, was dark navy */
    [data-composition-id="impact"] .impact-stage{ position:relative; z-index:2;
       display:grid; place-items:center; }
    #impact-word{ font:900 140px "Inter",sans-serif; color:#FFF;
       letter-spacing:2px; text-shadow:0 6px 30px rgba(0,0,0,0.35); }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from("#impact-word", { scale: 1.4, opacity: 0, duration: 0.4, ease: "power4.out" }, 0.1);
    tl.to("#impact-word", { opacity: 0, scale: 0.95, duration: 0.3, ease: "power2.in" }, 2.6);
    window.__timelines["impact"] = tl;
  </script>
</div>
```

For an automated version, use the registry caption block `caption-kinetic-slam` or `caption-particle-burst`.

---

### CompanyLogoOverlay

Logos appear over a talking head, then fade out together. Each logo is an `<img class="clip">` whose `data-start` is its appear time in seconds.

**When to use:** "trusted by" / "as seen in" beats over narration.

```html
<div class="logo-strip">
  <img id="logo-google" class="clip" src="assets/logos/google.png"
       data-start="2.5" data-duration="2.5" data-track-index="1" />
  <img id="logo-microsoft" class="clip" src="assets/logos/microsoft.png"
       data-start="3.3" data-duration="1.7" data-track-index="2" />
</div>
<style>
  .logo-strip{ position:absolute; top:6%; left:0; right:0; z-index:3;
               display:flex; gap:48px; justify-content:center; align-items:center; }
  .logo-strip img{ height:150px; width:auto;
               filter:drop-shadow(0 6px 18px rgba(0,0,0,0.25)); }
</style>
<script>
  // entrances at each logo's appear time
  tl.from("#logo-google",    { y: -30, opacity: 0, duration: 0.4, ease: "power2.out" }, 2.5);
  tl.from("#logo-microsoft", { y: -30, opacity: 0, duration: 0.4, ease: "power2.out" }, 3.3);
  // fade ALL out together (old fadeOutAt=5.0, fadeOutDuration=0.5)
  tl.to(".logo-strip img", { opacity: 0, duration: 0.5, ease: "power2.in" }, 5.0);
</script>
```

A label can sit under each logo — add a `<div class="logo-label">` and animate it alongside.

---

### MiniImpact

Small impact word over a talking head, with an optional pulse ring.

**When to use:** lightweight emphasis that doesn't take over the frame.

```html
<div id="mini" class="mini-impact">
  <div id="mini-ring" class="pulse-ring"></div>
  <span id="mini-word">THE FUTURE</span>
</div>
<style>
  .mini-impact{ position:absolute; top:22%; left:0; right:0; z-index:3;
                display:grid; place-items:center; }
  #mini-word{ font:900 80px Inter; color:#2F2414;
              background:#FCE36B; padding:8px 24px; border-radius:12px; }
  .pulse-ring{ position:absolute; width:120px; height:120px; border-radius:50%;
               border:4px solid #6C5CE7; opacity:0; }
</style>
<script>
  // old startSec=5.9, durationSec=1.4
  const start = 5.9, dur = 1.4;
  tl.from("#mini-word", { scale: 0.6, opacity: 0, duration: 0.3, ease: "back.out(2)" }, start);
  tl.fromTo("#mini-ring", { scale: 0.4, opacity: 0.7 },
            { scale: 1.8, opacity: 0, duration: 0.8, ease: "power2.out" }, start);
  tl.to("#mini-word", { opacity: 0, duration: 0.25, ease: "power2.in" }, start + dur - 0.25);
</script>
```

Drop the `.pulse-ring` element to disable the ring (the old `showPulseRing={false}`).

---

### HeadlineVideoCombo

Headline text above a video card. Reserve bottom space so captions don't collide.

**When to use:** a titled demo — headline + subheadline + media in one scene.

```html
<div class="scene-content combo">
  <h1 id="combo-headline">Revolutionary Tech</h1>
  <div id="combo-sub">See it in action</div>
  <div class="video-wrap combo-media">
    <video id="combo-video" src="assets/demo.mp4" muted playsinline
           data-start="0" data-duration="6" data-track-index="0"></video>
  </div>
</div>
<style>
  .combo{ display:flex; flex-direction:column; align-items:center;
          justify-content:flex-start; gap:18px;
          padding:120px 160px 200px; box-sizing:border-box; } /* bottomPadding=200 */
  #combo-headline{ font:800 88px Inter; color:#2F2414; margin:0; text-align:center; }
  #combo-sub{ font:600 34px Inter; color:#5B8FB9; }
  .combo-media video{ width:1100px; height:620px; object-fit:cover;
                      border-radius:20px; box-shadow:0 16px 44px rgba(47,36,20,0.2); }
</style>
<script>
  tl.from("#combo-headline", { y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.2);
  tl.from("#combo-sub", { y: 24, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.4);
  tl.from(".combo-media", { y: 60, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.6);
</script>
```

---

### KineticTypography

Word-by-word kinetic text synced to a transcript over background media. This is the core narration technique — for the full pipeline (transcribe → group → animate → guaranteed exit) see `hyperframes-captions` and the registry caption styles.

**When to use:** energetic narration where each word punches in.

**Fastest path — registry:**

```bash
npx hyperframes add caption-kinetic-slam   # full-screen single-word slam
npx hyperframes add caption-highlight      # TikTok per-word red sweep
```

Install, then port its animation into a host comp driven by your real transcript JSON (the component hardcodes its own WORDS array).

**Inline pattern** (one group visible at a time, with the mandatory hard exit):

```html
<div id="kt" class="kinetic"></div>
<style>
  .kinetic{ position:absolute; bottom:120px; left:0; right:0; z-index:3;
            text-align:center; overflow:visible; }
  .kt-group{ font:900 96px Inter; color:#FFF; opacity:0;
             text-shadow:0 4px 20px rgba(0,0,0,0.4); }
</style>
<script>
  // groups derived from a transcript: [{text, start, end}, ...] (seconds)
  const groups = [
    { text: "THE", start: 0.2, end: 0.7 },
    { text: "FUTURE", start: 0.7, end: 1.4 },
    { text: "IS HERE", start: 1.4, end: 2.3 },
  ];
  const host = document.getElementById("kt");
  groups.forEach((g, i) => {
    const el = document.createElement("div");
    el.className = "kt-group"; el.id = `kt-${i}`; el.textContent = g.text;
    host.appendChild(el);
    tl.fromTo(el, { y: 60, opacity: 0, scale: 1.2 },
              { y: 0, opacity: 1, scale: 1, duration: 0.25, ease: "power3.out" }, g.start);
    // mandatory deterministic kill at the end of each group
    tl.to(el, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, g.end - 0.12);
    tl.set(el, { opacity: 0, visibility: "hidden" }, g.end);
  });
</script>
```

The old `fallbackWord` is just the first group; the old `fps` is gone (you work in seconds).

---

## Utility Components

### FadeOut

Final-scene fade to black. **Only the last scene may exit-animate** — never fade scenes mid-composition (the transition is the exit).

**When to use:** the very end of a composition.

```html
<div id="fade" class="fade-out"></div>
<style>
  .fade-out{ position:absolute; inset:0; z-index:99; background:#000; opacity:0;
             pointer-events:none; }
</style>
<script>
  // old startFrame/endFrame at 68f/70f → 2.267s / 2.333s on a short comp.
  // Here: from full visible to black over the last 0.4s of a 10s comp.
  tl.to("#fade", { opacity: 1, duration: 0.4, ease: "power2.in" }, 9.6);
</script>
```

### Registry finishing layers

Prefer these ready-made overlay components over hand-rolling:

```bash
npx hyperframes add grain-overlay     # film grain / analog warmth
npx hyperframes add vignette          # edge darkening, focus pull
npx hyperframes add shimmer-sweep     # premium light sweep on a reveal
```

Each installs as a transparent overlay sub-comp you embed via `data-composition-src` at a high `z-index`.

---

## Theme Constants

Light / neutral palette only. Define once as CSS custom properties at the composition root and reference everywhere — this is the HyperFrames equivalent of the old exported constants. (Dark-theme and dark+neon / glassmorphism palettes are intentionally **removed**.)

```html
<style>
  [data-composition-id="root"]{
    /* Surfaces & background */
    --beige:        #E8E0D0;   /* warm background */
    --beige-radial: radial-gradient(circle at 50% 38%, #F2ECDD 0%, #E8E0D0 55%, #DED4C0 100%);
    --card:         #FFFFFF;   /* card surface */
    --minimal-bg:   #FFFFFF;   /* clean/corporate surface */

    /* Text */
    --ink:          #2F2414;   /* primary text on light */
    --ink-soft:     #5A5042;   /* secondary text */

    /* Accents */
    --purple-pill:  #6C5CE7;   /* accent purple */
    --steel-blue:   #5B8FB9;   /* secondary accent */
    --green-check:  #1A9E55;   /* success */
    --red-x:        #D93025;   /* error */
    --highlight:    #FCE36B;   /* yellow callout */

    /* Depth (subtle, light-theme) */
    --card-shadow:  0 8px 30px rgba(0,0,0,0.15);
    --heavy-shadow: 0 16px 44px rgba(47,36,20,0.2);

    /* Type */
    --font:         "Inter", Arial, sans-serif;
    --impact-font:  "Inter", "Arial Black", sans-serif;
  }
</style>
```

**Tone reference (light only).** The old `tone` choice becomes a pick of surface + accent within this palette:

| Tone | Surface | Accent | Best for |
|---|---|---|---|
| `warm` | `--beige` / `--beige-radial` | `--purple-pill` | Default brand autopsy |
| `minimal` | `--minimal-bg` (white) | `--steel-blue` | Clean, corporate |

> Fonts: write the `font-family` directly in CSS — the HyperFrames compiler embeds supported fonts (Inter is built-in). No font imports needed; assets live alongside `index.html` and are referenced with relative paths like `assets/logo.png`.

---

## Helpers

You work in **seconds** in HyperFrames, so the old frame-math helpers are gone. Keep these small utilities for deterministic, readable timing.

### Frame → seconds (only if porting old values)

If you are migrating old frame numbers, divide by the fps once. There is no runtime helper — just inline the math:

```js
const FPS = 30;
const sec = (frame) => frame / FPS;   // 30 frames → 1.0s
tl.from("#title", { opacity: 0, duration: 0.5 }, sec(15)); // was frame 15 → 0.5s
```

### Scene-window check (in seconds)

Replaces the old `inScene`. With a paused timeline you schedule by absolute time, but for conditional logic inside a `tl.call`, a plain range check works:

```js
const S = { s1: [0, 5.0], s2: [5.0, 9.0] };
const inScene = (t, [a, b]) => t >= a && t < b;
// inside a tl.call(() => { ... }, [], time) you can branch on inScene(t, S.s1)
```

### Seeded randomness (mulberry32)

`Math.random()` / `Date.now()` are **banned** (non-deterministic renders). When you need pseudo-random values (jitter, scatter, particle offsets), seed a PRNG:

```js
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(1234);
const jitter = (rand() - 0.5) * 20; // stable across every render
```

### Dynamic text fit

For copy that may overflow a fixed container, size it at build time instead of guessing:

```js
const fontSize = window.__hyperframes.fitTextFontSize(
  longHeadline, { maxWidth: 1600, fontFamily: "Inter", fontWeight: 800 }
);
```

---

## Rendering

```bash
npx hyperframes lint          # structural + determinism checks
npx hyperframes validate      # WCAG contrast audit
npx hyperframes inspect       # headless layout/overflow check
npx hyperframes preview       # dev preview server
npx hyperframes render --output out.mp4
npx hyperframes render --docker --output out.mp4   # pinned Chrome/fonts/FFmpeg
```

Determinism rules are the same as before: no `Math.random()` unseeded, no `Date.now()`, no timers or render-time fetches, finite durations only. Build the timeline **synchronously** and register it on `window.__timelines["<id>"]`.
