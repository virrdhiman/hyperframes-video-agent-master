# Comparison node-graph VS (two brand clusters, drawn-on edges)

The "A vs B" beat as two small node-graphs facing off — e.g. Apple (dark red) on one side, Google
(blue) on the other — each a hub icon with a few satellite nodes, connector edges drawing on, labels
in SF Pro. States the rivalry/handoff visually without a wall of text.

## Look
- Two clusters, left and right (or top/bottom), separated by a thin divider or a small "VS" mark.
- Each cluster: a central hub (brand logo/glyph) + 2–4 satellite dots, thin connector lines.
- **Brand-native tints** (real brand cues): Apple = dark red `#8D2B24`-family; Google = blue.
  Labels neutral (`#1A1A1A` on light, `#F9F6FA` on dark), SF Pro, ~30–40px.
- Sits in the upper content zone over the light-top gradient; lower module/PiP untouched below.
- Single accent discipline holds: lime is NOT used here — clusters use their own brand colors only.

## Motion (seek-safe on `tl`)
```js
// hubs pop, satellites stagger out, edges "draw" via strokeDashoffset on the SAME tl
tl.fromTo("#hub-a", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }, t0);
tl.fromTo("#hub-b", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }, t0 + 0.08);
tl.fromTo(".sat", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.06 }, t0 + 0.3);
// edges: set pathLength/strokeDasharray = L, animate strokeDashoffset L -> 0
tl.fromTo(".edge", { strokeDashoffset: (i, el) => el.getTotalLength?.() ?? 200 },
                   { strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut", stagger: 0.05 }, t0 + 0.4);
tl.fromTo("#vs-mark", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }, t0 + 0.7);
```

## Key ideas
- Edge "draw-on" is `strokeDashoffset` tweened on `tl` (set dasharray = path length first) — fully
  seek-safe, no rAF. Use inline SVG `<path>`/`<line>` so `getTotalLength()` works.
- Keep each cluster small and legible; this is a GLANCE beat (~2–3s), not a readable chart.
- Brand colors do the storytelling — don't add extra accent colors. One hub icon per side, max.
- Good "rivalry / handoff / migration" beat; follow it with a stat or a list to pay off the claim.
