# Parallax world motion — living background + grid/texture drift (Cars24)

Decoded 2026-06-22 from the Cars24 motion sequences (`style_study/_motion/cars24_seq_18.jpg`,
`fire_seq_30.jpg`). **The background is NEVER a static fill.** In every ref the world is alive: the
grid floor drifts, the editorial-text/world layer scrolls, b-roll runs full-frame with its own motion,
and the whole thing reads as DEPTH because the layers move at different speeds (parallax). This is the
piece the owner called out — pair it with `host-positioning-choreography.md` (the host is its own fastest layer).

## The layer stack (back → front), with relative motion speed
1. **BACK SCREEN / horizon text** (slowest, ~2–6px/s) — e.g. "INDIA GOES…" on a showroom wall, or a
   faint far texture. Drifts slowly, large blur/low contrast = far away.
2. **WORLD / GRID floor** (slow, the signature motion) — a perspective grid receding to a vanishing
   point that CONTINUOUSLY scrolls toward/under the viewer (synthwave-floor feel), OR a big editorial-
   TEXT sheet that pans. ~8–20px/s. This is the "grid/texture motion" that makes the studio feel alive.
3. **B-ROLL / product** (mid) — full-frame footage with ken-burns (slow 1.0→1.08 zoom + a few % pan)
   ON TOP OF the footage's OWN motion (rotating car turntable, assembly line, lighting cycle). When
   b-roll owns the frame, host shrinks to a corner (see choreography corner-BL/BR).
4. **GRAPHIC ZONE cards** (front-mid) — label plates / arrows / numbers slide+settle (never hard-pop),
   drift ~3–8px while held so they breathe.
5. **HOST cutout** (front, fastest/independent) — its own entrance/anchor/scale per beat.
6. **GRAIN / texture overlay** (very front, ~3–5% opacity) — subtle constant shimmer over everything.

**Parallax rule:** when the host moves one way, nudge the world layer slightly the OTHER way (or slower
same-way) so depth reads. Different speeds per layer = the parallax. Don't move everything in lockstep.

## Seek-safe implementation (GSAP `tl`, NO rAF/Date — render-safe)
Drive every drift off the SAME timeline so `hyperframes` seek-render is deterministic. Use long linear
tweens (the "continuous" feel) + `ease:"none"`.
```js
// GRID FLOOR drift (perspective grid as a tall bg image / CSS background-position)
tl.to("#worldGrid", { backgroundPositionY: "+=480", duration: 10, ease: "none" }, 0);
// or move a transform on an oversized grid div:
tl.fromTo("#worldGrid", {yPercent:-6}, {yPercent:6, duration:12, ease:"none"}, 0);

// EDITORIAL-TEXT world pan (oversized text sheet behind host)
tl.fromTo("#worldText", {xPercent:0, yPercent:-4}, {xPercent:-8, yPercent:4, duration:12, ease:"none"}, 0);

// BACK SCREEN (slowest)
tl.fromTo("#bgScreen", {xPercent:0}, {xPercent:-3, duration:14, ease:"none"}, 0);

// B-ROLL ken-burns on top of native footage motion
tl.fromTo("#broll", {scale:1.0, xPercent:0}, {scale:1.08, xPercent:-3, duration:5, ease:"none"}, BEAT);

// PARALLAX coupling: when host steps right, drift the world left a touch (different magnitude)
tl.to("#host",      {xPercent:22, duration:0.6}, BEAT);
tl.to("#worldGrid", {xPercent:-4, duration:0.6}, BEAT);   // opposite, smaller = depth
```
Oversize every moving bg layer by ~10–15% (e.g. width:115%, offset -7%) so the drift never exposes an edge.

## Per-world flavour
- **Grid worlds (green / purple / charcoal):** the grid is a perspective floor → vertical scroll toward
  camera is the hero motion; add a faint vignette + a slow hue/light sweep.
- **Sky / nostalgia world:** clouds drift slowly sideways; subtle.
- **Fire / combustion world:** flame layer flickers (seek-safe = a pre-rendered flame VIDEO drifting +
  scaling, NOT JS particles).
- **Location-composite (showroom/factory/pump):** the B-ROLL itself is the world motion; add ken-burns
  + keep the back wall text/screen as the slow parallax layer.

## Gotchas
- ALL drift on the timeline, `ease:"none"`, no infinite CSS loops that desync from seek (a CSS
  `@keyframes` drift is OK only via the css-animations adapter that HyperFrames can seek).
- Keep magnitudes SMALL on the far layers (a few %); big motion only on b-roll/host — else it reads seasick.
- Never let a moving layer expose its edge → oversize + offset.
- BLANK-SCENE GUARD: drift via `to`/`fromTo(immediateRender:false)`, never `fOut` a scene container.
- Performance: prefer ONE drifting background image/video per beat + transforms over many animated DOM nodes.
