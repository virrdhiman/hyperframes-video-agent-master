# GSAP_DEMOS_CATALOG.md — curated official GSAP demos usable in our renders

Source: https://demos.gsap.com (sitemap audited 2026-06-11; 77 demos total). Each demo
page embeds its CodePen — fetch source with `python3 tools/stock_fetcher/codepen.py <pen-url>`.
**All GSAP plugins are FREE since 3.13** (MorphSVG, DrawSVG, ScrambleText, SplitText,
MotionPath, Physics2D) — load from the gsap CDN like the core.

**The filter that produced this list:** our renders seek a paused timeline frame-by-frame —
no scroll, cursor, or drag exists at render time. Anything ScrollTrigger/mouse/Draggable-driven
is useless to us regardless of how good it looks on the web. ~45 of the 77 demos failed that
filter and are intentionally absent. Time/timeline-driven techniques below get re-wired onto
our beat timeline (`window.__timelines`).

## ★ High value — adapt these first
| Demo | URL slug | Use in our videos |
|---|---|---|
| Text scrambling (ScrambleText) | `text-scrambling` | decode/glitch-in a word or number — AI/tech reveals, "95%" scrambling into place |
| Rolling text (odometer digits) | `rolling-text` | stat slams: counts, prices, benchmark scores rolling to final value |
| Morph between SVG shapes (MorphSVG) | `morph-between-svg-shapes` | logo↔icon↔shape morphs; shape-morph scene transitions — fresh fingerprint |
| Smooth / dynamic morphing | `smooth-morph` · `dynamic-morphing` | same family; pick whichever variant fits the beat |
| Text masking | `text-masking` | masked headline reveal — strong hook-text treatment |
| Draw a path (DrawSVG) | `draw-a-path` | stroke draw-on: underlines, a circle scribbled around a key word, routes, signatures |
| Animate along a path (MotionPath) | `animate-along-a-path` · `motionpath-waypoints` | icon/plane travels a route — pair with the travel-map SVG for "going global" beats |
| Staggering | `staggering` | staggered element reveals (HUMAN_EDIT_GUIDE motion rule) — canonical reference |

## ◐ Situational — for specific beats
| Demo | URL slug | When |
|---|---|---|
| Text replacement | `animate-text-replacement` | "not X → Y" word swap |
| Card stack | `card-stack` | a stack of options/models fanning out |
| Radial menu | `radial-menu` | radial fan-out of icons — "the ecosystem / what it can do" |
| Image sequence | `image-sequence` | frame-sequence playback (product 360° spin) — drive frame index from the timeline, NOT scroll |
| Directional marquee / horizontal text | `directional-marquee` · `horizontal-text` | looping ticker/banner — seamless-loop variant only |
| Keyframes / complex timeline | `keyframes` · `complex-timeline` | reference for multi-step choreography on one element |

## ✗ Skipped on purpose (do not fetch)
- All `*scroll*`, `cursor-*`, `*-slider`, `*-carousel`, `*-gallery`, `flip-*`, `draggable`,
  `magnetic-button`, `macos-dock-effect`, `proximity-scale-grid`, `pinned-panels`,
  `velocity-skew` — interaction-driven; no scroll/cursor/drag exists in a render.
- `canvas-particles`, `create-physics-based-effects`, `generating-randomness` — rAF +
  randomness; would need a deterministic rebuild (like `text-shatter.html`) to be usable.

## Adaptation rules (same as every motion ref)
1. Lift the tween/technique, not the page: drive it from the composition's paused
   `window.__timelines["<id>"]` timeline — no rAF, no `Date.now`, no `Math.random`.
2. Re-tint to the video's accent; LIGHT palette (no dark/neon).
3. When an adapted demo ships in a delivered video, save the measured spec to
   `styles/elements/` and add a row in `styles/INDEX.md` (or componentize into
   `compositions/components/` if paste-in reusable).
