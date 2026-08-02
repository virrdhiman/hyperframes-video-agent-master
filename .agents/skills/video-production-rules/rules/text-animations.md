---
name: text-animations
description: Typography and text animation patterns in HyperFrames
---

# Text animations

**Typewriter effect.** Reveal text by **string slicing**, not per-character opacity. Drive it with `tl.call(() => el.textContent = full.slice(0, n), [], t)` at successive second-positions, or a GSAP tween with `ease: "steps(N)"` on a counter proxy. A blinking cursor and a pause after the first sentence read well. Never fade in characters individually — slicing keeps kerning correct and looks like real typing.

**Word highlighting** (highlighter-pen sweep). The canonical HyperFrames technique is the CSS marker emphasis family — a yellow marker sweep is a `scaleX: 0 → 1` on a behind-text bar with `transform-origin: left`. Other emphasis modes: hand-drawn circle (`back.out(1.7)` on an SVG ring), burst lines, scribble underline (animate `stroke-dashoffset`), sketch-out cross-hatch over struck text. Cycle modes every 2–5 emphasis beats by energy. See the `/hyperframes` CSS-patterns reference for the exact patterns; these are pure CSS+GSAP, deterministic, and fully seekable.

**Kinetic typography** synced to a transcript is the core narration technique — per-word entrance pops timed to word boundaries. See [captions](./captions.md).

General rules:

- Headlines 60px+, body 20px+, data labels 16px+ for rendered video.
- `font-variant-numeric: tabular-nums` on numbers and counters.
- Don't stack competing animations on one word; let emphasis words break the pattern (larger, accent color, slight overshoot).
- Avoid `<br>` for wrapping — set `max-width` and let text wrap naturally. Exception: deliberate display titles where each word is intentionally on its own line.
