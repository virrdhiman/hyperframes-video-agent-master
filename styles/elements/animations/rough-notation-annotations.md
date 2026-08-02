# rough-notation — annotate-on highlights (circle / underline / box / highlight, seek-safe)

**Use for ANY "annotate a word / circle a UI element / underline / highlight / strike" effect**
(the owner, 2026-06-25 — "I love rough notation, add it and wire it in for upcoming videos").
Built ON TOP of RoughJS, so it inherits the same hand-drawn marker feel but gives a clean
high-level API for the 7 classic annotation types. This is the device the viral reels use to
circle the exact button/word in a screen-recording.

When to reach for this vs raw RoughJS:
- **rough-notation** → you want to annotate an EXISTING DOM element (a caption word, a stat, a
  region of a screenshot): circle it, underline it, box it, highlight it, strike it. It
  auto-measures the target's bounding box and lays the mark over it.
- **raw RoughJS** (`roughjs-handdrawn-shapes.md`) → you want a free-floating arrow / shape at
  explicit coordinates that points BETWEEN things.

## Types (config `type:`)
`circle` · `underline` · `box` · `highlight` (marker fill) · `strike-through` · `crossed-off` · `bracket`

## Vendor
- Canonical copy: `styles/assets/vendor/rough-notation.min.js` (v0.5.1 IIFE, global `RoughNotation`).
  `curl -fsSL https://unpkg.com/rough-notation@0.5.1/lib/rough-notation.iife.js`
- COPY it into each project's `assets/vendor/` alongside `rough.min.js`. Include AFTER gsap AND
  rough.min.js, BEFORE the timeline script:
  ```html
  <script src="assets/vendor/gsap.min.js"></script>
  <script src="assets/vendor/rough.min.js"></script>
  <script src="assets/vendor/rough-notation.min.js"></script>
  ```

## 🔒 DETERMINISM RULE (non-negotiable for render) — VALIDATED 2026-06-25
rough-notation's own `show()` animation uses `requestAnimationFrame` → on distributed seek-render
workers it flickers/freezes. NEVER use its built-in animation. The proven seek-safe pattern:
1. Create with **`{animate:false, seed:<fixed>}`** and call **`show()` ONCE at load** → it draws the
   FULL annotation instantly as `<svg class="rough-annotation">` `<path>` elements appended to the DOM.
2. Grab those paths, prime `strokeDasharray`/`strokeDashoffset = pathLength`, then GSAP-drive the
   draw-on with `tl.fromTo(..., immediateRender:false)` — exactly like RoughJS.
The fixed `seed` keeps the squiggle identical on every worker/frame (no flicker).

## Proven pattern (validated by snapshot — staggered circle→underline→box all drew clean)
```js
// helper: build an annotation, instant full draw, return it
function rn(el, cfg){
  var a = RoughNotation.annotate(el, Object.assign({animate:false, seed:7}, cfg));
  a.show();
  return a;
}
rn(document.getElementById('w1'), {type:'circle',    color:'#FF2D2D', strokeWidth:4, padding:18});
rn(document.getElementById('w2'), {type:'underline', color:'#36F08A', strokeWidth:6});
rn(document.getElementById('w3'), {type:'box',       color:'#FFD23F', strokeWidth:5, padding:14});

// each annotation appends one <svg class="rough-annotation"> in call order — tag + draw-on:
var svgs = document.querySelectorAll('svg.rough-annotation');
svgs[0].id='rn0'; svgs[1].id='rn1'; svgs[2].id='rn2';
function prime(svgSel, at){
  var paths = document.querySelectorAll(svgSel + ' path');
  paths.forEach(function(p){ var L=p.getTotalLength()||400; p.__L=L;
    p.style.strokeDasharray=L; p.style.strokeDashoffset=L; });
  tl.fromTo(paths,{strokeDashoffset:function(i,t){return t.__L;}},
    {strokeDashoffset:0,duration:0.5,ease:'power1.inOut',stagger:0.04,immediateRender:false}, at);
}
prime('#rn0', 0.3);   // circle draws on at 0.3s
prime('#rn1', 0.9);   // underline at 0.9s
prime('#rn2', 1.5);   // box at 1.5s
```

## Gotchas
- **Annotate STATIC targets only.** The mark is positioned from the target's bounding box at
  `show()` time and does NOT follow a moving element. Annotate words/UI regions that hold still
  while marked. If the target must move, wrap target + its `svg.rough-annotation` in one parent
  and move the parent.
- `highlight` is a translucent marker fill (good behind a word); `box`/`circle`/`underline` are
  strokes. `padding` (px, can be `[t,r,b,l]`) controls how loose the mark sits around the target.
- rough-notation makes ONE `<svg>` per annotation; with many on screen, tag them by index in
  creation order (as above) rather than relying on a shared selector.
- Keep the color on-palette per video. Red `#FF2D2D` circle = "look HERE" on a screenshot;
  green underline = key term; yellow box = the payoff value.
- For a SEQUENCE reveal use a GSAP `stagger` across one annotation's paths, and stagger the
  `prime(... at)` start times across annotations (as above).
