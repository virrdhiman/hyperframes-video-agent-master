# Flint chart draw-on (beautiful animated data charts)

Turn real data into a premium, themed chart that reveals itself on the timeline — line/bar/pie
etc. — WITHOUT dropping a live-animating chart lib into the render (that flickers on seek).

## Pipeline (two steps)
1. **Compile a static, themed SVG** with our helper (Flint → ECharts SSR → SVG, animation OFF):
   ```bash
   node tools/flint_svg.cjs <spec.json> <out.svg> [width] [height]
   ```
   - `spec.json` = a compact Flint `ChartAssemblyInput` (`data.values`, `semantic_types`,
     `chart_spec.chartType` = "Line Chart" | "Bar Chart" | "Pie Chart" | …, `encodings`, `baseSize`).
     Sample: `tools/_flint_sample.json`.
   - Extra house keys on the spec root: `"style":"dark"|"light"`, `"accent":"#6EA8FF"`,
     `"palette":["#..",…]`, `"area":true|false`.
   - House theme baked in: transparent bg, Inter, thin faint axes, subtle grid, thick (5px) rounded
     line + gradient area fill, rounded-top bars, our accent/palette forced to WIN over Flint defaults.
2. **Inline that SVG** into the composition (paste it inside a glass card `<div>`) and animate the
   REVEAL with GSAP off the paused `window.__timelines["root"]` timeline. Never `chart.setOption`
   in the browser; never animate ECharts itself.

The helper TAGS the data marks so GSAP can target them regardless of ECharts' class numbering:
- `[data-flint-line]` → the data line (`fill:none`, `stroke-width:5`)
- `[data-flint-area]` → the gradient area fill under a line
- grid/axes = `.zr0-cls-0`, markers = `.zr0-cls-4`, bars = `.zr0-cls-1` (per-series)

## Reveal A — LINE draw-on (premium, for line charts)
```js
var line = document.querySelector("#chart [data-flint-line]");
var area = document.querySelector("#chart [data-flint-area]");
var frame= document.querySelectorAll("#chart .zr0-cls-0, #chart text"); // grid+axes+labels
var dots = document.querySelectorAll("#chart .zr0-cls-4");              // point markers

gsap.set(frame,{opacity:0}); gsap.set(area,{autoAlpha:0});
gsap.set(dots,{transformOrigin:"50% 50%",scale:0,autoAlpha:0});
tl.to(frame,{opacity:1,duration:0.5,stagger:0.01},0.6);               // grid fades in first
var L=line.getTotalLength(); gsap.set(line,{strokeDasharray:L});      // measure ONCE at load
tl.fromTo(line,{strokeDashoffset:L},{strokeDashoffset:0,duration:1.5,ease:"power2.inOut",immediateRender:false},1.0);
tl.to(area,{autoAlpha:1,duration:1.0},1.3);                           // area follows the line
tl.to(dots,{scale:1,autoAlpha:1,duration:0.35,stagger:0.18,ease:"back.out(2.2)"},1.15);
```
- `getTotalLength()` runs in Chromium at build/load — deterministic, seek-safe.
- Keep area fade STARTING slightly after the line so it trails the draw (don't front-load it).

## Reveal B — universal WIPE (any chart type: bar / pie / mixed)
Bars/pie slices have no clean per-element selector, so wipe the whole SVG wrapper — deterministic,
works for everything:
```js
gsap.set("#chart",{clipPath:"inset(0% 0% 100% 0%)"});                 // hidden from the bottom
tl.to("#chart",{clipPath:"inset(0% 0% 0% 0%)",duration:1.4,ease:"power3.out"},t);   // grow up
```
- Bars → wipe bottom→up (bars grow out of the axis). Pie → swap to a radial: animate a conic/`clip-path
  circle()` or just fade+scale from centre.

## Key ideas
- ONE static SVG per chart, animation off → zero flicker across distributed render workers.
- Give the chart its own zone (glass card in the top/free band) — never over the host's face.
- Draw-on = line charts; wipe = everything else. Both drive off `tl`, never `tl.play()`.
- Demo project proving both: `projects/_flint-demo/` (line draw-on + bar wipe), snapshots in
  `out/_flint_test/snaps/`.
```
