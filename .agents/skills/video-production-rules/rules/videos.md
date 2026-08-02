---
name: videos
description: Embedding videos in HyperFrames — muted+playsinline, trimming, audio separation, wrapper animation
---

# Videos

Embed video as `<video muted playsinline>`. The element is **muted** — its sound, if any, comes from a **separate `<audio>` element** (see [audio](./audio.md)).

```html
<video id="clip" data-start="0" data-track-index="0" src="assets/clip.mp4" muted playsinline></video>
<audio id="clip-a" data-start="0" data-track-index="2" src="assets/clip.mp4" data-volume="1"></audio>
```

Rules:

- **Duration** defaults to the source length; `data-duration` caps it.
- **Trim** into the source with `data-media-start="<seconds>"`. Start later on the timeline by setting `data-start`.
- **Never animate the video element's width/height/top/left** — wrap it in a non-timed `<div>` and animate the wrapper (scale, position, opacity). The framework forces `opacity:1` on any element carrying `data-start`/`data-duration`, so any opacity move also belongs on the wrapper.
- **Never** call `play`/`pause`/`seek` — the framework owns playback.
- **Never nest a video inside a *timed* div** — use a non-timed wrapper.
- Don't loop with `repeat: -1`; to extend, lay repeated clips or compute a finite count.

Sizing/position via CSS (`object-fit: cover` to fill). For a transparent-subject overlay, see [transparent-videos](./transparent-videos.md).
