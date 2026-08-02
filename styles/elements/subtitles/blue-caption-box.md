# Blue solid caption box (webveda)

The lower-third caption highlight: white bold text on a solid electric-blue rounded box, one
short line per beat. The signature subtitle look of the webveda "Rule of 100" style.

## Spec (MEASURED, 1080×1920)
- **Position:** lower-third, box TOP at **y≈1408**, height ~100px, centered, ~105px side margins
  (box width ~870px). Vertical center ~y1459 (~76% down). Always above any bottom edge.
- **Style:** white bold **~46–52px** on a SOLID `#1D31FA` box, corner-radius ~14–18px,
  padding ~26–30px.
- **Behaviour:** ONE short line per beat. Swap the WHOLE line on each new beat (not word-by-word
  scroll). If a line wraps, shorten it.

## Motion (seek-safe on `tl`)
```js
tl.fromTo("#cap",{scale:0.9,opacity:0},{scale:1,opacity:1,duration:0.18,ease:"back.out(2)"},T);
// swap line text per beat; pop each new line
```

## Rules
- Stays in the lower-third — never in the face zone (y600–1300).
- Solid box (not semi-transparent) — that's the intended highlight.
- No watermark beneath it; keep the bottom clean.
