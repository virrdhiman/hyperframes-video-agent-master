---
name: timing
description: Easing, interpolation, and motion timing in HyperFrames (seconds-based GSAP)
---

# Timing and easing

HyperFrames timing is **seconds-based GSAP**. A tween's position and duration are seconds; the framework owns playback. (Anything that was frame-range `interpolate()` in a frame system becomes a GSAP tween from one value to another over a duration, at a second-position on the timeline.)

**Separate timing from mapping.** When several properties share the same motion, drive them off one normalized progress and derive each value, rather than re-specifying the curve per property. In GSAP, tween a single proxy `{ p: 0 }` to `{ p: 1 }` with the shared ease and read `p` in `onUpdate`, or reuse the same ease + position across tweens.

**Ease selection:**

- Default to ease-out for entrances, ease-in for exits.
- Custom curve from a designer? Use a `cubic-bezier`-equivalent ease (GSAP `CustomEase.create("x","M0,0 ... ")` or the matching power/expo/sine ease) — the four control points mean the same thing as CSS.
- Named-curve intuition (gentle → strong): `sine` < `power1`(quad) < `power2`(cubic) < `power3` < `power4`/`expo` < `circ`.
- Reach for overshoot (`back.out`) only for emphasis beats, not everywhere.

**Energy guide for transition/entrance speed:**

- Calm: 0.5–0.8s, sine/power1.
- Medium: 0.3–0.5s, power2/power3.
- High: 0.15–0.3s, power4/expo.

Clamp behavior is implicit in GSAP (a tween holds its end value), so you don't need explicit extrapolation flags — just don't read the timeline outside its built range.
