---
name: sequencing
description: Laying clips out in time in HyperFrames — start times, tracks, ordering, sub-compositions
---

# Sequencing

There is no wrapper-component sequencing in HyperFrames — you place clips on the timeline directly with attributes (the seconds-based equivalent of a frame-based `<Sequence>`):

- **Delay** a clip by setting `data-start="<seconds>"`.
- **Limit duration** with `data-duration="<seconds>"` (required on img/div clips; video/audio default to source length).
- **Tracks:** `data-track-index` groups clips. **Clips on the same track index cannot overlap in time** — put things that must run simultaneously on *different* tracks. Track index does **not** set visual stacking; use CSS `z-index` for layering.
- **Relative timing:** `data-start` can reference another clip, e.g. `"intro + 2"` (2 seconds after the clip with id `intro`) — handy for "right after this" chains so edits ripple.

## Sequential vs overlapping

- **One after another** (no overlap): place them on the same track index with consecutive start times, or compute `data-start` from the previous clip's end.
- **Overlap on purpose** (e.g. a transition where two scenes coexist, or B-roll under a held title): put them on different track indices and overlap their times.

## Sub-compositions

For a reusable scene, build it as a sub-composition and embed it via a host div with `data-composition-id` + `data-composition-src` + `data-start`/`data-duration`/`data-track-index`. The framework auto-nests its timeline — don't add it manually. Inside sub-comps prefer `gsap.fromTo()` over `gsap.from()`, and prefix ids to avoid collisions.

Build the whole timeline **synchronously**; no empty padding tweens just to set duration (duration comes from `data-duration`).
