---
name: subtitles
description: Subtitle data and routing for HyperFrames captions
---

# Subtitles

Subtitles in HyperFrames are the same pipeline as captions — word-synced text driven from a transcript on the paused GSAP timeline. The transcript is a flat JSON array of `{ id, text, start, end }` (times in seconds, not milliseconds). Phrase-level SRT/VTT can be imported but only gives phrase timing; word-level JSON unlocks per-word animation.

Routing:

- **Generate from audio/video** → see [captions](./captions.md) (`npx hyperframes transcribe`, including the `.en`-translates-non-English gotcha and the mandatory quality check).
- **Display / style** → see [display-captions](./display-captions.md) (grouping into pages, active-word highlighting, exit kill).
- **Import an existing `.srt`/`.vtt`** → see [import-srt-captions](./import-srt-captions.md).

Editorial notes that apply regardless of style:

- Keep groups short enough to read at the clip's pace (high energy 2–3 words, calm 4–6).
- One group on screen at a time; never let two overlap.
- Position so subtitles never cover a speaker's face; bottom band for landscape, lower-middle for portrait.
- Every group needs the mandatory hard exit kill so it can't linger past its `end`.
