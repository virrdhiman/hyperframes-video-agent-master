---
name: sfx
description: Sound effects in HyperFrames — placement and levels
---

# Sound effects

Add a sound effect as its own `<audio>` element on an SFX track, starting at the second the on-screen event happens:

```html
<audio id="whoosh" data-start="2.3" data-track-index="3" src="assets/whoosh.wav" data-volume="0.7"></audio>
```

SFX land on transitions, impacts, reveals, and emphasis beats. Sync the `data-start` to the visual moment, not loosely "around" it.

**Levels (style-agnostic defaults):**

- **Whoosh / swish** (transitions, fast moves): ~**0.7**
- **Impact / thud / boom** (slams, hits): ~**0.55–0.6**
- **Music bed:** ~**0.12** under voiceover, ~**0.45** in pauses (see [audio](./audio.md))

Keep SFX from masking voiceover — duck or lower them when narration is speaking. Use them sparingly; a well-placed whoosh on a key cut beats a sound on every motion. Place SFX files in `assets/`. Don't loop an effect with `repeat: -1`; one-shots are one clip.
