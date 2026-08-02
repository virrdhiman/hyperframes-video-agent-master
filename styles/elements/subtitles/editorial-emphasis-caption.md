# Editorial-emphasis captions (9:16 retune) — the owner's preferred BODY system

**RECOMMENDED (the owner, 2026-07-12).** One of the two caption styles the owner picked for the
approved "Morning Edition" cut — the body workhorse (~90% of runtime). Pairs with
`parallax-statement-wall.md` (the other pick) for the 2 statement beats. Rotate vs
`redbox-sweep-caption.md` per the 3-day style cooldown.

Source: registry `caption-editorial-emphasis` (`npx hyperframes add caption-editorial-emphasis`)
— but the demo is 1920×1080 with a hardcoded transcript. **Port the mechanics into the host
comp driven by `words.js`** with this measured 9:16 retune (shipped in
`retrofit-2026-07-11-fable/retrofit-2026-07-11/index.html`):

## Measured spec (1080×1920)
- Band: `#capwrap` at `left:90, width:900, top:1190` (face-safe under the host's chin zone);
  blocks CENTERED (`justify-content:center`), one block at a time.
- Word chips: each word on its own paper chip — bg `rgba(251,247,236,.92)`, radius 6,
  `padding:6px 14px 9px`, soft stacked shadow, tilt jitter ±0.3–0.6° alternating.
  Normal words: Outfit 700 **54px** ink `#14120F`. **Emphasis words: Playfair italic 800
  92px, red `#D8232A`** (the money words: billion/largest/sixty/feeds/198/trillion/seven/
  149/170/2027/pricier/rich/winner — 1 emphasis max per block).
- Grouping: 2–4 words per block; break on punctuation, gaps >0.45s, or right after an
  emphasis word (when block ≥2). Canvas-measure each block; scale down if >900px.
- Motion: per-word pop at the word's start (opacity 0 + scale 1.12, origin bottom-left,
  0.1s power2.out); block fade-in 0.1s; block exit 0.12s power2.in + **mandatory hard-kill
  `tl.set(...{opacity:0,visibility:hidden})`** at hide-time (seek-safe).
- SKIP ranges: captions OFF during statement walls and any beat whose graphic carries the
  same words (e.g. a kicker card) — never duplicate text on screen.
- Re-fit after `document.fonts.ready` (canvas measure needs loaded fonts).

Why it reads premium: ink-on-paper chips survive any background (light world or dark plate),
and the serif-italic red slams give every stat a typographic hit without a new component.
