---
name: lottie
description: Embedding Lottie vector animations in HyperFrames
---

# Lottie animations

HyperFrames plays Lottie vector animations through its Lottie integration (`window.__hfLottie`) — see the dedicated `/lottie` skill for the authoritative API. The pattern:

- Place the Lottie JSON in `assets/` (or alongside the composition). Load it **synchronously** as the timeline builds — do not fetch it inside `async`/`setTimeout`/`Promise`; the capture engine reads `window.__timelines` synchronously after load. (No render-time network fetch.)
- Drive the animation's progress from the **paused GSAP timeline** so it's deterministic and seekable, rather than letting Lottie autoplay on its own clock.
- Size and position with CSS (`width`/`height`); place it inside `.scene-content` with flex/padding, not absolute-positioned content containers.

Editorial:

- Lottie suits premium / explainer / icon-accent moments — a small vector flourish, an animated icon, a logo build. Don't let it fight the main content.
- Keep its timing in step with the scene's other entrances; a Lottie that finishes long after everything else has settled reads as dead air.
- Use it as one of 2–3 techniques in a composition, not the whole show.
