---
name: transitions
description: Scene transitions in HyperFrames — CSS vs shader, the entrance-only / transition-is-the-exit discipline
---

# Scene transitions

Every multi-scene composition uses transitions. The hard rules:

1. **Always transition between scenes — no jump cuts.**
2. **Every scene entrance-animates** — every element animates in via `gsap.from()`. No element appears fully-formed.
3. **Never exit-animate before a transition.** The transition **is** the exit; the outgoing scene must be fully visible at the moment the transition fires. (Banned: `gsap.to(..., { opacity: 0 })` on a scene's elements before its cut.)
4. **Only the final scene may fade out.**

## CSS vs shader

- **CSS transitions** animate the scene container (opacity / transform / clip-path / filter). Simpler, no GPU. Scenes 2+ start at `opacity: 0` and GSAP reveals them. For page-burn / zoom-out the outgoing scene needs a higher `z-index`.
- **Shader transitions** (`@hyperframes/shader-transitions`) composite both scene textures per pixel on WebGL — warp / dissolve / morph beyond what CSS can do. Don't hand-write GLSL; use the package. Don't mix CSS and shader in one composition. Shader capture (html2canvas) needs: no `transparent` keyword in gradients (use `rgba(...,0)`), an explicit `background-color` on every `.scene` (also passed as `bgColor`), and uncapturable decor marked `data-no-capture`.

The registry ships ready-made single shader effects (`npx hyperframes catalog --tag shader`: glitch, light-leak, whip-pan, ripple-waves, cinematic-zoom, domain-warp-dissolve, ridged-burn, swirl-vortex, cross-warp-morph, chromatic-radial-split, …) and transition showcase reels.

## Choosing transitions (editorial)

Pick ONE primary transition for 60–70% of cuts plus 1–2 accents. Match energy and mood:

- **Energy:** calm = blur crossfade / cross-warp-morph (0.5–0.8s, sine) · medium = push slide / whip-pan / cinematic-zoom (0.3–0.5s, power2/3) · high = zoom-through / ridged-burn / glitch / chromatic-split (0.15–0.3s, power4/expo).
- **Mood → type:** warm = light-leak; tech = grid-dissolve / glitch; premium = focus-pull / cross-warp; playful = elastic / 3D-flip / swirl.
- **Position:** opening cut most distinctive; outro the slowest crossfade.
- Avoid visibly repeating geometric patterns — prefer organic noise.

Because transitions overlap the two scenes, plan timing so the outgoing scene is still fully built when the cut begins. See [light-leaks](./light-leaks.md) for overlay-style effects that play over a cut without consuming scene time.
