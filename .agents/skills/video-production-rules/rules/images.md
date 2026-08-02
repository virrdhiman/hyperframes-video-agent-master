---
name: images
description: Embedding images in HyperFrames
---

# Images

Embed a timed image as an `<img class="clip">` with `data-start`/`data-duration`/`data-track-index`:

```html
<img id="logo" class="clip" data-start="0" data-duration="3" data-track-index="1" src="assets/logo.png" />
```

- **Local files** live in `assets/` and are referenced by relative path (sub-compositions reach the project root with `../`). Remote URLs work directly; add `crossorigin="anonymous"` to external media.
- **Sizing/position** via CSS — `width`/`height`/`object-fit`. Use padding and flex to place images inside `.scene-content` rather than absolute-positioning content containers. Reserve `position:absolute` for decoratives.
- **Animated images** (GIF/APNG/WebP) — see [gifs](./gifs.md).

## Motion treatment

A static photo with no motion reads as dead air in video. Give images a gentle move — a slow Ken-Burns scale/pan (`gsap.to` on a wrapper), a soft parallax, or a subtle entrance. **Animate a wrapper div, not constraints on the `<img>` itself**, and keep the move slow and continuous (don't snap). For dynamic image swaps (sequences, per-prop avatars, state-based icons) build the `src` from a variable/seeded value, never from `Date.now()`/`Math.random()`.

Legibility: if text sits over an image, add a scrim or gradient behind the text so it clears contrast.
