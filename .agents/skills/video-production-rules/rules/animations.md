---
name: animations
description: Animation fundamentals for HyperFrames compositions
---

# Animation fundamentals

All motion is driven by a **paused GSAP timeline** registered on `window.__timelines["<composition-id>"]`. Write times in **seconds** (positions and durations on tweens), not frames. The framework seeks the timeline; you never read a current-frame value. (In a frame-based system this was `useCurrentFrame()` + `interpolate`/`spring`; in HyperFrames it's GSAP tweens at second-positions.)

Core practice:

- **Layout before animation.** Build the hero frame (the moment most elements are visible) as static HTML+CSS first. Then add `gsap.from()` entrances toward those positions, and only-where-allowed `gsap.to()` exits.
- **Ease with intent.** Use ease-out for entrances (arrive with momentum, decelerate into place) and ease-in for exits (start slow, accelerate away). Vary eases — at least 3 different ones per scene; don't repeat one entrance pattern.
- **Offset the first animation** 0.1–0.3s rather than starting at t=0.
- **Only animate visual props** — `opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, transforms. Never animate `visibility`/`display`.
- **Never the same prop on the same element from two timelines.**
- **No infinite repeats.** `repeat: -1` breaks the capture engine — compute a finite count: `repeat: Math.ceil(duration / cycleDuration) - 1`.
- **NEVER fade-out a SCENE CONTAINER that was faded in with a `fromTo(... immediateRender:false)`.** This is the #1 "blank/empty scene" bug (it shipped retrofit-2026-06-19 — the video went empty after 33s). When you put BOTH a `fIn` (a `fromTo({opacity:0},{opacity:1}, immediateRender:false)`) AND a later `fOut` (a `.to({opacity:0})`) on the **same scene/container element**, the renderer SEEKS a paused timeline (it does not play it), and that seek corrupts the container's opacity baseline → the whole scene resolves to `opacity:0` for its ENTIRE span and renders blank. It looks fine in live preview (which plays) but is invisible in the render AND in `hyperframes snapshot` (snapshot uses the same seek path, so the snapshot is ALSO blank — QA can't see the bug). FIX: fade the scene's **inner content** in/out, and HARD-HIDE the empty scene with `tl.set("#sX",{autoAlpha:0}, endT)` (a `set`, not a tween) — never a `.to(opacity:0)` on the container that owns the `fromTo` entrance. A blank-frame gate in `tools/pipeline_check.py` now blocks delivery if any ≥3s stretch renders near-flat, but don't rely on the gate — author it correctly.

Bézier easing maps directly to CSS `cubic-bezier(x1,y1,x2,y2)` via GSAP's `CustomEase` (or a power/expo/sine ease), so timing can be shared with web specs and designer curves. A crisp UI entrance is roughly `cubic-bezier(0.16, 1, 0.3, 1)`; a playful overshoot has a control-point y > 1 (use sparingly for emphasis). See [timing](./timing.md).
