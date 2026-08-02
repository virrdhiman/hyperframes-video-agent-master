---
name: trimming
description: Trimming clips and animations in HyperFrames
---

# Trimming

## Trimming media (video/audio)

Cut into a source with two attributes (seconds):

- `data-media-start="<seconds>"` — skip this far into the source before it plays (trims the beginning).
- `data-duration="<seconds>"` — stop after this long (trims the end).

The clip still begins at its `data-start` on the timeline; `data-media-start` only changes *which part of the source* plays. Combine the two to play an interior slice: e.g. `data-start="3" data-media-start="5" data-duration="4"` plays seconds 5–9 of the source, appearing at the 3-second mark of the composition.

## Trimming an animation

To start an entrance partway through, don't offset a wrapper — schedule the tween at a later second-position, or use `tl.from(sel, vars, position)` / `tl.fromTo(...)` and pick the position so the visible portion is the part you want. To end an element early, hard-kill it on the timeline at its cut: `tl.set(sel, { opacity: 0, visibility: "hidden" }, endTime)` (the framework already removes clips after `data-start + data-duration`, but a deterministic kill is the rule for anything that must not linger — e.g. captions).

Keep all of this seconds-based and on the paused timeline; never `seek()` media to trim.
