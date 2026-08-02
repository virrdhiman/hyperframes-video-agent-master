---
name: silence-detection
description: Detecting and trimming silence from audio/video before bringing it into HyperFrames
---

# Silence detection

Dead air at the head/tail of a recording (and long mid-clip gaps) makes a piece drag. Detect and trim silence as a **pre-processing step on the source file**, before placing the clip — then bring the trimmed result into the composition.

## Adaptive detection

Two passes give a clip-appropriate threshold instead of a fixed guess:

1. **Measure loudness** — get the recording's integrated loudness and its gating threshold (EBU R128). The gating threshold is the level below which audio is "too quiet to count."
2. **Detect silences** using that gating threshold as the noise floor, with a minimum silence duration (~0.5s is a good default). You get pairs of `silence_start` / `silence_end` timestamps.

(Any standard audio tool that exposes loudnorm-style measurement and a silencedetect-style pass works; the adaptive-threshold idea is what matters.)

## Interpreting

- **Leading silence:** a silence segment at/near 0. If the first `silence_start` is > ~0.5s, there's no real leading silence.
- **Trailing silence:** the last segment that runs to (or near) the file's end.
- Treat near-contiguous silences (gap < 0.2s) at the head or tail as one block.

## Applying the trim in HyperFrames

Once you know the first non-silent second and the last non-silent second, trim with clip attributes:

- `data-media-start="<leadingEnd seconds>"` — skip the leading silence.
- `data-duration="<trailingStart − leadingEnd seconds>"` — drop the trailing silence.

This keeps narration tight without re-encoding the source. For mid-clip gaps, either split into multiple clips around the gap or accept a short breath — don't over-cut, which makes speech feel unnatural.
