---
name: transparent-videos
description: Rendering and using videos with transparency (alpha) in HyperFrames
---

# Transparent videos

Two situations:

## Rendering a composition WITH transparency

When the *output* needs an alpha channel (e.g. an overlay to drop onto other footage), render to an alpha-capable container/codec:

```bash
# WebM (VP9 + alpha) — plays in a browser / composition <video>
npx hyperframes render --format webm ...

# ProRes 4444 (.mov) — for import into editing software (larger files)
npx hyperframes render --format mov ...
```

WebM/VP9-alpha is ideal for playing back inside another HyperFrames composition (Chrome decodes VP9 alpha natively); ProRes `.mov` is ideal for handing to an external editor.

## Making a subject transparent (background removal)

To turn a clip of a person/object into a transparent overlay, pre-process it:

```bash
npx hyperframes remove-background subject.mp4 -o transparent.webm
```

Outputs: `.webm` (VP9 + alpha, default — plays in a composition `<video>`), `.mov` (ProRes 4444, for editing), or `.png` (still cutout). `--quality fast|balanced|best` trades file size for cleanliness; use `best` for masters.

## Using the transparent clip

- Embed it as a normal `<video muted playsinline>` clip; the alpha shows through whatever is behind it in `z-index` order.
- **Text-behind-subject** compositing: base video (back) → headline → cutout `.webm` on top, with the cutout wrapped in a **non-timed** div whose opacity you animate (the framework forces `opacity:1` on any element with `data-start`/`data-duration`, so animate the wrapper, never the video). Give both videos `data-start="0"` + `data-media-start="0"` so they decode in sync.
- Putting a cutout over its **own** source doubles the subject's RGB — only do it over a clean plate or a different background.
