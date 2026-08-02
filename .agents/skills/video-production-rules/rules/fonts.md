---
name: fonts
description: Fonts in HyperFrames — compiler-embedded built-ins and local .woff2 files
---

# Fonts

HyperFrames embeds fonts at compile time, so font loading is simple — no runtime font-load step, no blocking on web-font fetches.

- **Built-in fonts:** just write the `font-family` you want in CSS. The compiler embeds supported fonts automatically, and they're available immediately when the timeline builds (no async wait).
- **Custom fonts:** drop `.woff2` files in a `fonts/` directory and add `@font-face` declarations pointing at the local files. If a `design.md` names a font that isn't built-in and there are no font files, warn the user before writing HTML and offer a built-in fallback.

Because fonts are embedded, you can size text with the helper `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })` synchronously — useful for captions and any dynamic copy that must fit a box.

Editorial defaults:

- Prefer one or two families with clear weight contrast over many fonts.
- Headlines 60px+, body 20px+, data labels 16px+ at render scale.
- `font-variant-numeric: tabular-nums` on numbers and counters so columns don't jitter.
- Variable fonts can be animated on their axis (`font-variation-settings`) for an elegant weight-shift — load the `.woff2` locally.
