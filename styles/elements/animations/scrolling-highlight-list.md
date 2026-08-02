# Scrolling highlight list (vertical pan, active line bold)

A tall list of items scrolls vertically inside a fixed window; the line crossing the centerline
reads bold-black while neighbours dim to gray. The eye is pulled to the "current" item as the column
glides. (Vaibhav reel: "Faster window closing… / Faster AirDrop transfers / …".) Also the exact move
for a long product/design-page **pan reveal** (mount a tall screenshot, glide it past the frame).

## Look
- A masked window (`overflow:hidden`) ~720–900px tall inside the upper content zone.
- Inside it, a column taller than the window holding N rows (or one tall image).
- **Active row** (nearest the window center): `#1A1A1A`, bold, full opacity, slightly larger.
- **Neighbour rows:** `#8A8A8A`–`#B5B5B5`, regular weight, opacity ramped down by distance.
- For an IMAGE pan (design-page reveal) skip the per-row styling — just glide the tall PNG; add a
  soft top+bottom fade mask so content enters/exits gently, framed in a rounded browser/phone mock.

## Motion (seek-safe on `tl`)
```js
// glide the column up; total travel = columnHeight - windowHeight
tl.fromTo("#sl-col", { y: 0 }, { y: -travel, duration: dur, ease: "none" }, t0);

// per-row active emphasis driven by the SAME tl (no scroll listeners) —
// stagger each row's bold/dim around the moment it crosses the centerline
rows.forEach((r, i) => {
  const hit = t0 + (i / rows.length) * dur;        // when row i is centered
  tl.fromTo(r, { color:"#9A9A9A", fontWeight:400, opacity:0.55, scale:0.96 },
               { color:"#1A1A1A", fontWeight:800, opacity:1,    scale:1.00,
                 duration:0.30, ease:"power2.out" }, hit);
  tl.to(r, { color:"#9A9A9A", fontWeight:400, opacity:0.55, scale:0.96,
             duration:0.30, ease:"power2.in" }, hit + 0.55);  // fade back as it leaves
});
```
For a pure image pan: `tl.fromTo("#pan-img",{y:0},{y:-(imgH-frameH),duration:dur,ease:"power1.inOut"},t0)`
(slow-in/slow-out so components register; optional `scale:1.0→1.04` for life).

## Key ideas
- Everything driven off ONE `tl` tween — no `scroll`/rAF/IntersectionObserver, so it seeks frame-exact.
- Travel = `columnHeight − windowHeight`; let the active line dwell ~0.5s before handing off.
- Cheap, high-impact "I'm walking you down a list / page" beat. Pair with a count or a header label.
- Keep the moving panel OUT of the avatar/PiP zone; text/labels below or beside it, never on his face.
