---
name: charts
description: Charts and data visualization in HyperFrames
---

# Charts and data viz

Two paths:

## Use a registry block (preferred for standard charts)

The catalog ships data-viz blocks (`npx hyperframes catalog --tag data`): `data-chart` (NYT-style bar + line) and map blocks (see [maps](./maps.md)). Install with `npx hyperframes add data-chart` and feed your numbers. Cheaper and more consistent than hand-rolling.

## Hand-build with HTML/SVG + GSAP

For custom charts, build with HTML, SVG, and plain JS, animated by the **paused GSAP timeline**. **Disable any third-party library's own animation** — those run on their own clock and cause flicker. Every motion must be a GSAP tween at a second-position.

Common patterns:

- **Bar chart:** lay out the bars statically, then `gsap.from()` each bar's height/scaleY with a stagger (e.g. 0.05–0.08s apart, ease-out).
- **Pie/donut:** animate `stroke-dashoffset` on an SVG circle from full to the segment length, starting at 12 o'clock (`transform: rotate(-90deg)`).
- **Line / stock graph:** build the SVG path from your points, then animate it drawing on via `stroke-dasharray`/`stroke-dashoffset` (the self-draw technique). A marker/arrow can ride the path end using SVG path-length math or GSAP MotionPath.

Editorial:

- Stagger reveals so the eye reads the data building up, rather than everything snapping in at once.
- `font-variant-numeric: tabular-nums` on axis/value labels.
- Label font size large enough to survive downscaling — at 1920×1080, keep value labels ≥24px.
- Animate counters up to their final value rather than popping the number in.
