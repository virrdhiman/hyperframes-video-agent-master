# RoughJS hand-drawn shapes & arrows (sketchy SVG, seek-safe)

**Use for ALL hand-drawn arrows, circles, underlines, boxes, highlights** from now on
(the owner, 2026-06-25 — "install and use rough js for the arrows and other shapes in this and
upcoming videos"). Replaces hand-coded SVG `<path>` arrows, which looked stiff/imperfect.
RoughJS gives an organic, marker-on-paper feel that reads as genuinely hand-drawn.

## Vendor (per project, offline)
- Drop the UMD bundle at `assets/vendor/rough.min.js` (RoughJS 4.6.6,
  `curl -fsSL https://unpkg.com/roughjs@4.6.6/bundled/rough.js`). Exposes global `rough`.
- Include AFTER gsap, BEFORE the timeline script:
  ```html
  <script src="assets/vendor/gsap.min.js"></script>
  <script src="assets/vendor/rough.min.js"></script>
  ```

## 🔒 DETERMINISM RULE (non-negotiable for render)
RoughJS randomises the sketch each call. Distributed render workers each re-run the page →
**every frame would get a different squiggle = flicker**. ALWAYS pass a FIXED `seed` so the
shape is identical on every worker/frame:
```js
var O={stroke:"#F5A623",strokeWidth:5,roughness:1.5,bowing:2.4,seed:7};
```
Generate the shape ONCE at load (outside the timeline), THEN animate it with GSAP.

## Markup
```html
<div class="arrow" id="ar1" style="left:560px; top:880px; width:300px; height:120px;">
  <svg id="ar1svg" viewBox="0 0 300 120"></svg>
</div>
```

## Build + draw-on (proven, retrofit-2026-06-25 arrow)
```js
(function(){
  var svg=document.getElementById("ar1svg");
  var rc=rough.svg(svg);
  var O={stroke:"#F5A623",strokeWidth:5,roughness:1.5,bowing:2.4,seed:7};
  var g=document.createElementNS("http://www.w3.org/2000/svg","g");
  g.appendChild(rc.path("M22,20 C150,4 250,44 268,96",O));   // curved shaft
  g.appendChild(rc.line(268,96,234,88,O));                    // arrowhead barb 1
  g.appendChild(rc.line(268,96,258,62,O));                    // arrowhead barb 2
  svg.appendChild(g);
  window.__ar1paths=g.querySelectorAll("path");
  window.__ar1paths.forEach(function(p){ var L=p.getTotalLength()||320; p.__L=L;
    p.style.strokeDasharray=L; p.style.strokeDashoffset=L; });
})();
// stroke-dashoffset draw-on (immediateRender:false = seek-safe; per-path L via function value)
fIn("#ar1",14.6,0.2);
tl.fromTo(window.__ar1paths,{strokeDashoffset:function(i,t){return t.__L;}},
  {strokeDashoffset:0,duration:0.6,ease:"power1.inOut",stagger:0.05,immediateRender:false},14.62);
```
Notes: RoughJS expands each requested shape into MULTIPLE `<path>`s (the sketch strokes) —
query them all and animate `strokeDashoffset` across the set with a small `stagger` so the
ink lays down naturally. `rc.line(...)` for the two arrowhead barbs.

## Tunable look
- `roughness` ~1.2–1.8 (higher = scratchier), `bowing` ~1.8–2.6 (curve wander),
  `strokeWidth` 4–6 for 1080-wide. For a hand-drawn CIRCLE use `rc.circle(cx,cy,d,O)`;
  underline = `rc.line`; highlight box = `rc.rectangle(x,y,w,h,{...,fill:'#...',fillStyle:'hachure'})`.
- Keep the accent on-palette per video (here amber `#F5A623`).
