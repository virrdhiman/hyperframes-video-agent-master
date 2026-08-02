---
name: video-production-rules
description: General editorial and video-production rules for HyperFrames compositions — captions/subtitles, scene transitions, audio and sound effects, fonts, timing, sequencing, images and videos, charts, maps, Lottie, light leaks, transparency, GIFs, audio-reactive visuals, and voiceover. These are style-agnostic craft notes that complement (not replace) the authoritative `/hyperframes` skill, which owns framework mechanics. Read a rule when working on that kind of element.
---

# Video Production Rules (HyperFrames)

These are the **editorial / general video-production practices** distilled from a broad video best-practices corpus and translated to HyperFrames. They capture *what makes video good* — pacing, caption hygiene, transition discipline, audio levels, legibility — not the framework plumbing.

**The `/hyperframes` skill is authoritative for framework mechanics.** When a rule here and the framework disagree on syntax (`data-*` attributes, the paused GSAP timeline on `window.__timelines`, media element rules), follow `/hyperframes`. These rules add craft on top.

## HyperFrames mental model (so the rules read correctly)

- **Timing is in SECONDS**, via `data-start` / `data-duration` / `data-track-index` on clips, plus a **paused** GSAP timeline registered on `window.__timelines["<composition-id>"]`. (Anything that referenced frames / `useCurrentFrame` / `interpolate` / `spring` / `<Sequence>` in a frame-based system maps to seconds here. A frame `N` at 30 fps is `N / 30` seconds.)
- **Media:** `<video muted playsinline>` for picture; a **separate** `<audio data-volume="...">` element for sound. Images use `<img class="clip">`. Project assets live in `assets/` (referenced by relative path). Never call `play`/`pause`/`seek`; never animate the video element directly — wrap it in a non-timed `<div>` and animate the wrapper.
- **Determinism is non-negotiable:** no `Math.random()` (unseeded), no `Date.now()`, no render-time fetch, no `repeat: -1`. Seed randomness with mulberry32. Build timelines synchronously.

## When to read which rule

- **Animations / timing / text-animations** — motion fundamentals and easing in seconds.
- **Captions / subtitles** — word-synced text from a transcript; the HyperFrames caption pipeline and `caption-*` registry components.
- **Transitions / light-leaks / transparent-videos** — scene cuts, overlay effects, alpha output.
- **Audio / sfx / voiceover / audio-visualization** — sound levels, TTS, audio-reactive visuals.
- **Images / videos / gifs / fonts** — media embedding and legibility.
- **Charts / maps / lottie** — data viz, map animation, vector animation via registry blocks and helpers.
- **Sequencing / trimming / timing / silence-detection** — laying clips on the timeline.

Each rule is a short guidance note. For exact syntax, the `/hyperframes`, `/lottie`, and shader-transition references are the source of truth.
