# Full style — webveda "Rule of 100"

Punchy, number-driven, blue-accented talking-head reel. Decoded from the reference reel
(facebook.com/reel/959298476937167 · 1080×1920 · 30fps · ~27s). Reproduce the SPEC — never
clone a frame-for-frame. Reference frames/grids: `~/workspace/workspace/fb_ref/`
(fbref_grid.jpg, study/t_*.png, morph/morph_intro.jpg, morph/morph_circle.jpg).

## When to use
Tech / creator / "how-to" talking-head shorts that want a strong repeated NUMBER motif,
bold blue branding, sticker-style platform icons, fast kinetic beats.

## Palette → [elements/palettes/webveda.md](../elements/palettes/webveda.md)
Electric blue `#1D31FA` (caption boxes + wipes), number blue `#3B82F6`, accent yellow `#FFD400`,
hero red `#FF0000`, white, near-black `#0A0A0A`.

## Typography
Heavy geometric sans. Numbers → **Anton** (black weight, tight tracking). Hero/words →
**Montserrat Black / Poppins Black**. Captions → bold sans, one short line.

## Composition (1080×1920)
- Talking head CENTERED, head upper-center, soft-blurred real-room bokeh background.
- FACE ZONE = center column **y600–1300** — keep clear of ALL graphics/text. Hard rule.
- Kinetic text + intro hero live in the TOP HEADROOM BAND (~y60–620).
- Captions in the lower-third box. **NO watermark anywhere.**

## Scene-by-scene skeleton (a NEW beat every ~1–1.5s)
| # | Beat | What's on screen | Elements used |
|---|---|---|---|
| 1 | ~0–2s intro hero | Yellow circle + B&W cutout + black "crushed" over distressed red "DREAM"; clears by 2s | [dream-intro-hero](../elements/animations/dream-intro-hero.md) |
| 2 | Hook | Giant number "100" (~330px) pops into top band, breathing scale | (number motif, below) |
| 3 | List build | Word-stack "TRY / LOSE / LEARN" staggers in inside the circle | [numbered-badge-drawon](../elements/animations/numbered-badge-drawon.md) |
| 4 | B-roll cut | Fast cutaway (grids, thumbnails, gameplay), badge pop "100 VIDEOS" | circle-wipe hand-off |
| 5 | Scene morph | Circle-grow wipe carries to next backdrop | [circle-grow-wipe](../elements/transitions/circle-grow-wipe.md) |
| … | Repeat | Alternate talking-head ↔ b-roll, number motif recurs | — |
| last | CTA/close | Final caption line, clean talking head | [blue-caption-box](../elements/subtitles/blue-caption-box.md) |

## The number motif (signature)
Giant number cap-height ~330px (~17% of frame), parked y210–560. Animate scale 0.5→1 with
back/overshoot, then a tiny breathing scale. Supporting words ~56–72px around it.

## Overlap rules
MAY: top text over blurred b-roll · number over its circle · stickers clipping number edge ·
caption text on its blue box · intro hero collage (red word + cutout + circle).
MUST NOT: anything over the face zone · two hero blocks (number + wordmark) on one frame ·
elements bleeding to the extreme edge (keep ~80–105px margins).

## Subtitles → [elements/subtitles/blue-caption-box.md](../elements/subtitles/blue-caption-box.md)
Lower-third, box top y1408, ~870×100px, white bold ~46–52px on solid `#1D31FA`, one line per beat.

## Reproduce-it checklist
1. 9:16 1080×1920, 30fps (60 only for motion-graphics smoothness).
2. Centered talking head, blurred bg, NO watermark.
3. Open with intro hero (~2s), clear by 2s.
4. Pick ONE repeated number/word motif, ~330px, top band.
5. Top-band kinetic text only; face zone clear.
6. Blue caption box ~870×100 @ y1408, one short line.
7. ≥1 circle-grow wipe + sticker icons + numbered draw-on if a list fits.
8. Keep every section visually UNIQUE — house mindset, not a clone.
