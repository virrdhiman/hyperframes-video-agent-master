---
name: gifs
description: Using animated images (GIF/APNG/WebP) in HyperFrames
---

# GIFs and animated images

Display an animated image (GIF, APNG, AVIF, WebP) as a normal `<img class="clip">` clip:

```html
<img id="anim" class="clip" data-start="0" data-duration="2.5" data-track-index="1"
     src="assets/animation.gif" style="width:500px;height:500px;object-fit:contain" />
```

- Place the file in `assets/`; remote URLs need CORS.
- **Fit** via CSS `object-fit` (`contain` keeps aspect, `cover` crops to fill).
- **Duration:** set `data-duration` to how long it should stay on screen. If you want the composition (or a clip) to match the GIF's natural length, measure it once ahead of time and set the seconds accordingly — don't guess.
- The animated image plays on its own internal clock while it's on the timeline.

Editorial caution: looping GIFs can feel cheap or distracting in a polished piece. Prefer a real video clip or a frame sequence when you need precise timeline-synced motion, and reserve GIFs for genuinely GIF-native content (reactions, stickers). If you need exact sync, a frame sequence driven as an image-swap (`src` built from a seeded/timed index, never `Math.random()`/`Date.now()`) gives deterministic control.
