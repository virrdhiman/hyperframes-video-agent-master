# "crushed DREAM" intro hero (thumbnail-style open)

A bold YouTube-thumbnail-style hook graphic that sits in the TOP band over the talking head
for the opening ~2s, then clears. NOT a logo/watermark — a hook. Decoded from
`fb_ref/study/t_1.4.png` + `fb_ref/morph/morph_intro.jpg`.

## Pieces (MEASURED, 1080×1920)
- **Yellow backdrop circle:** solid `#FFD400`, ~860px diameter, centered (~x540), vertical
  center ~y540 (top band). The visual anchor of the hook frame.
- **Cutout subject:** background-removed transparent-PNG B&W person/photo ON the circle, head
  upper-center. Optional collage props (cash/money) flanking. Make with
  `hyperframes-media remove-background`.
- **Headline stack (top-left, over circle):** small black bold lowercase line ("crushed") ABOVE
  a huge `#FF0000` ultra-bold uppercase word ("DREAM"), ~300–360px cap height, spanning most of
  the width, overlapping the cutout top. The big red word gets a **DISTRESSED / PNG look** —
  rough grungy edges, slight texture, faded stroke edges (not a clean vector fill).

## Animation (seek-safe on `tl`, all OUT by ~2s)
```js
tl.fromTo("#hcircle",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.4,ease:"back.out(2)"},0.0);
tl.fromTo("#hcutout",{y:60,scale:0.9,opacity:0},{y:0,scale:1,opacity:1,duration:0.45,ease:"power3.out"},0.15);
tl.fromTo("#hword",{scale:1.3,opacity:0},{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"},0.3); // + tiny shake
tl.to(["#hcircle","#hcutout","#hword"],{opacity:0,duration:0.25},1.9); // or hand to circle-grow-wipe
```

## Rules
- MAY overlap the cutout/circle (collage by design) but MUST clear the live face zone below.
- Exits (cut or circle-wipe) by ~2s so the talking head is clean.
- NO watermark — this is the only top-band graphic of the open.
