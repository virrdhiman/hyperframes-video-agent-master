---
name: audio
description: Using audio in HyperFrames — separate audio element, volume, trimming, layering, levels
---

# Audio

Audio is **always a separate `<audio>` element** — never the audio track of a `<video>` (video clips are `muted playsinline`). Place audio on its own track index.

```html
<audio id="music" data-start="0" data-track-index="2" src="assets/music.mp3" data-volume="0.45"></audio>
```

Key behaviors:

- **Volume:** `data-volume="0..1"` (default 1). For a fade, don't animate the element directly — schedule it on the timeline by tweening a proxy and applying gain, or pre-bake the fade into the file. The framework owns playback; never call `play`/`pause`/`seek`.
- **Trim into the source:** `data-media-start="<seconds>"` skips into the file; `data-duration` caps how long it plays. The clip still starts at its `data-start` on the timeline.
- **Delay:** set `data-start` to the second you want it to begin.
- **Layering:** add multiple `<audio>` elements on different track indices (e.g. music, voiceover, SFX) — they mix.
- **Looping:** never `repeat: -1`. If you need a bed longer than the source, lay repeated clips or compute a finite repeat count from the composition duration.

**Levels (mixing discipline):** keep background music at ~0.12 under voiceover and ~0.45 in pauses; sit voiceover on top. See [sfx](./sfx.md) for effect levels and [voiceover](./voiceover.md) for narration.

Avoid pitch/speed tricks unless asked — they rarely improve a piece and can complicate deterministic rendering.
