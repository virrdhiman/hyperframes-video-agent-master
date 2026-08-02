# GSAP Plugins — the full seek-safe set (all FREE since GSAP 3.13)

Every GSAP plugin went 100% free post-Webflow. The whole seek-safe set is vendored at
`styles/assets/vendor/gsap-plugins/` (all `3.14.2`, version-matched to core `gsap.min.js`).
**Validated 2026-06-25**: snapshot contact sheet showed every plugin below seeking
deterministically frame-by-frame, zero flicker.

## How to use in a project
1. Copy the plugin file(s) you need from `styles/assets/vendor/gsap-plugins/` into the
   project's `assets/vendor/` (vendor per-project, like gsap/rough — never hot-link a CDN).
2. Load AFTER `gsap.min.js`, BEFORE your timeline script.
3. `gsap.registerPlugin(...)` once, then drive every effect from the paused `window.__timelines["<id>"]`
   timeline. **Never** `tl.play()` for render-critical motion.

```html
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/vendor/DrawSVGPlugin.min.js"></script>
<script src="assets/vendor/SplitText.min.js"></script>
<script>
  gsap.registerPlugin(DrawSVGPlugin, SplitText);
  const tl = gsap.timeline({ paused:true });
  // ...tweens...
  window.__timelines["root"] = tl;
</script>
```

## THE seek-safe rule (applies to every plugin)
HyperFrames renders by seeking a **paused** timeline frame-by-frame. A plugin is safe ONLY when its
visual is a pure function of timeline progress (or generated once at load). Anything driven by
`requestAnimationFrame`, real-time clocks, scroll, cursor, or drag will flicker/freeze on the render
workers. The plugins below are tween-driven → safe. The SKIP list at the bottom is interaction-driven → banned.

---

## ✅ Vendored & validated — pick per beat

| Plugin | File | What it does | Seek-safe usage |
|---|---|---|---|
| **SplitText** | `SplitText.min.js` | split a headline into chars/words/lines | `new SplitText(el,{type:"chars"})` ONCE at load, then `tl.from(split.chars,{y,opacity,stagger})`. The split happens at load = deterministic. Per-char/word/line reveals — our default hook-text treatment. |
| **DrawSVGPlugin** | `DrawSVGPlugin.min.js` | progressive stroke draw-on | `tl.fromTo(path,{drawSVG:"0%"},{drawSVG:"100%"})`. Underlines, a circle scribbled round a word, routes, signatures, connector lines. (RoughJS = sketchy look; DrawSVG = clean smooth stroke.) |
| **MorphSVGPlugin** | `MorphSVGPlugin.min.js` | morph one SVG path into another | `tl.to(path,{morphSVG:"M...new path..."})`. Logo↔icon↔shape morphs, shape-morph scene transitions — fresh visual fingerprint. Paths needn't share point counts. |
| **MotionPathPlugin** | `MotionPathPlugin.min.js` | move an element along an SVG path | `tl.to(el,{motionPath:{path:"#route",align:"#route",alignOrigin:[0.5,0.5]}})`. Icon/plane travels a route, "going global" map beats, orbiting elements. |
| **Flip** | `Flip.min.js` | record layout state, then animate the diff after a DOM/style change | `const s=Flip.getState(el)` → change layout/class → `Flip.from(s,{duration,ease})`. The barba-style **shared-element morph across a cut** — host/card continues into the next scene seamlessly. Capture state at build, NOT on an event. |
| **ScrambleTextPlugin** | `ScrambleTextPlugin.min.js` | scramble/decode text into final value | `tl.to(el,{scrambleText:{text:"95%",chars:"upperCase"}})`. Decode/glitch-in a word or stat — AI/tech reveals. |
| **TextPlugin** | `TextPlugin.min.js` | typewriter type-on / swap text | `tl.to(el,{text:"typed line",ease:"none"})`. Terminal/code typing, "not X → Y" swaps. |
| **CustomEase** | `CustomEase.min.js` | author any easing curve | `CustomEase.create("myEase","M0,0 C0.2,0 0.1,1 1,1")` then `ease:"myEase"`. Bespoke motion feel; also the dependency for CustomBounce/CustomWiggle. |
| **CustomBounce** | `CustomBounce.min.js` | realistic bounce ease (needs CustomEase) | `CustomBounce.create("bnc",{strength:0.6})` → `ease:"bnc"`. Object drops, squash-settle landings. |
| **CustomWiggle** | `CustomWiggle.min.js` | wiggle/oscillate ease (needs CustomEase) | `CustomWiggle.create("wig",{wiggles:6,type:"easeOut"})` → `ease:"wig"`. Shake/jiggle accents, attention nudges, error shakes. |
| **Physics2DPlugin** | `Physics2DPlugin.min.js` | velocity/angle/gravity projectile motion | `tl.to(el,{physics2D:{velocity:600,angle:-75,gravity:1200}})`. Confetti bursts, popped/launched objects, sparks. Deterministic — position is a pure function of timeline time (no rAF). |

Already wired via deterministic adapters (separate skills, not in this folder): **animejs, css-animations,
lottie, three.js**. Core GSAP (timelines, eases, stagger, transforms) is in the `gsap` skill SKILL.md.

## 🔴 SKIP — interaction-driven, NOT seek-safe (do not vendor for renders)
`ScrollTrigger`, `ScrollSmoother`, `Observer`, `Draggable`, `InertiaPlugin` — all react to scroll /
cursor / drag / throw, none of which exist at render time. `GSDevTools`, `MotionPathHelper` = dev-only
overlays. `EaselPlugin`/`PixiPlugin` need EaselJS/Pixi loaded (not in our stack). If a web demo's effect
depends on any of these, it cannot be lifted as-is — rebuild the motion on the beat timeline instead.

## Gotchas
- **immediateRender**: on a later `from()`/`fromTo()` targeting the same property+element, set
  `immediateRender:false` to avoid the start-state overwriting.
- **Flip**: capture `getState` at build time (synchronously in the setup script), never inside an event/timer.
- **SplitText**: split once; re-splitting on resize is a real-time op we don't need (fixed canvas).
- **No infinite repeat** (`repeat:-1`) anywhere — compute finite repeats from the visible duration.
- Re-tint plugin demos to the video's accent + keep the LIGHT palette default.
