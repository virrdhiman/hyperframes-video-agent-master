# Parallax statement wall (9:16 retune) — the owner's preferred STATEMENT device

**RECOMMENDED (the owner, 2026-07-12).** The second of the owner's two picked caption styles — a
behind-the-host giant serif wall for 1–2 STATEMENT beats per video (never a running caption).
Pairs with `editorial-emphasis-caption.md` (the body system); body captions switch OFF while
a wall is up.

Source: registry `caption-parallax-layers` (`npx hyperframes add caption-parallax-layers`) —
1920×1080 demo, hardcoded words. **Port into the host comp** with this measured 9:16 retune
(shipped: "LARGEST EVER" + "WHO'S NEXT?" beats in retrofit-2026-07-11):

## Measured spec (1080×1920)
- Two layers sandwiching the cutout host: **behind** `z-index:35` (under host z40) and
  **front line** `z-index:60` (above host). The depth illusion NEEDS the keyed host between
  them — don't use on host-off beats.
- Behind words: Playfair 800 **225px**, red `#D8232A`, `-webkit-text-stroke:4px` same red,
  hard drop `text-shadow:3px 6px 0 rgba(168,27,33,.55)`, line at `top:210`, stretched
  `scaleY(2.1)`. **MANDATORY scaleX-fit**: measure `line.scrollWidth`, apply
  `translateX(-50%) scaleX(min(1, 1000/w)) scaleY(2.1)` after `document.fonts.ready` —
  unfitted walls overflow the frame (shipped bug, fixed).
- Behind words fade in ON their spoken word (opacity-only, 0.12s) — 1–2 words max
  ("LARGEST"+"EVER"), found via `findW()` from words.js.
- Front line: the full spoken phrase, Playfair italic 800 **66px** cream `#FBF7EC`, centered
  at `top:1430`, per-word instant-set on word timing (no tween — the restraint is the style).
- Whole wall lives in `clip` containers spanning exactly the beat window (hard in/out).
- Host on wall beats: full-bleed side-dock ~0.95 scale (per robust-anchoring v4) so the wall
  reads around the silhouette; red walls on the LIGHT paper world need no scrim.
- Budget: **max 2 walls per video** (statement device, not a caption system); unify serif +
  accent color with the body captions so the two systems read as one voice.
