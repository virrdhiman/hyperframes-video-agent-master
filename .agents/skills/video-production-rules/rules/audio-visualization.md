---
name: audio-visualization
description: Audio-reactive visuals in HyperFrames — pre-extracted band data, per-frame timeline calls, deterministic mapping
---

# Audio visualization (audio-reactive)

Audio-reactive motion in HyperFrames is **deterministic**: you analyze the audio **ahead of render** into a band-data file, then drive GSAP from that data on the timeline. There is **no Web Audio at render time** — that would be non-deterministic and is banned.

## 1. Pre-extract band data

Produce a JSON of per-frame frequency bands, e.g.:

```json
{ "fps": 30, "totalFrames": 900, "frames": [ { "bands": [0.0, 0.4, ...] }, ... ] }
```

Bands are 0–1; index 0 is bass, higher indices are treble. (Generate with the audio-extract script in the `/gsap` skill, e.g. `extract-audio-data.py audio.wav --fps 30 --bands 16 -o audio-data.json`.)

## 2. Drive visuals per frame

Sample the data on the timeline with `tl.call`, one call per frame, at second-position `frame / fps`:

```js
data.frames.forEach((f, i) => {
  tl.call(() => applyBands(f.bands), [], i / data.fps);
});
```

A single tween won't "react" — you need the per-frame calls (or, for captions, bake the peak band intensity into each word's entrance tween).

## 3. Map bands → GSAP props (subtle)

- **bass → scale** (pulse) — keep it small, ≤5–6%.
- **treble → text-shadow / box-shadow** (glow) — apply to active words only.
- **amplitude → opacity / y.**
- **mid → border-radius.**

Mandatory for music-driven captions; skip for calm tutorials/voiceover.

## Never

Equalizer bars, waveforms, spectrum analyzers, music-note clipart, or strobing. Keep reactions tasteful — the audio drives *emphasis*, it isn't the subject.
