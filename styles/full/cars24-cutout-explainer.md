# Cars24 "Cutout Explainer" — keyed cutout host on composited worlds (v2, complete)

Decoded from TWO Cars24-style references:
1. Long-form Short "Car Names Are Sad Now" (IIwuoek6ghg, 2026-06-20) — host on a green graph-paper grid.
2. EV "5 fuels" vertical Short (O35szDnG_-k, 2026-06-21) — host **composited onto real locations**.
Reference frames: `styles/fb_ref/cars24/` + `style_study/ytshort2/` (grid.jpg, dense1.jpg, cuts.jpg).

**The look in one line:** a real presenter, **chroma-keyed to a clean cutout**, is composited
into a series of worlds — either a deep-green graph-paper studio grid OR real location B-roll
(petrol pump, showroom, highway, factory) — holding a branded mic, while bold literal evidence
photos, minimal red stamp-label cards, big yellow arrows and a red rubber stamp pop in beside him.
He is **always moving**: a fresh entrance + anchor + scale every beat, stepping aside and shrinking
when the world/product must own the frame. Fast, casual, honest "video-essay" energy. Face ALWAYS clear.

## What we LEARNED (the full set — don't ship a Cars24 cut missing any of these)
1. **It's green-screen, not on-location.** The presenter is keyed (you can catch the studio grid /
   alpha-checker behind him on cuts, plus green spill on his arm). He is composited ONTO the
   locations — never actually there. So we replicate it the same way: keyed cutout + swap the world.
2. **DYNAMIC HOST POSITIONING** (was missing in all our cuts) — per beat he enters from L/R/T/B,
   anchors centre/side/corner, and zooms in/out; he steps aside + shrinks so B-roll/product fills the
   frame, then returns. → full spec in `elements/animations/host-positioning-choreography.md`. NON-NEGOTIABLE.
3. **Heavy REAL B-roll** behind/around him (cars, pumps, factory, highway, product close-ups) — the
   world is the background, cutaways keep it moving. Pull genuine official/stock footage, never 100% CSS.
4. **Minimal text overlays** — sparse stamp-style label cards (red distressed text on a white rounded
   plate, e.g. PETROL / CNG / DIESEL), a corner category stamp ("FUTURE"), the occasional list with
   strikethroughs. Text supports; it does NOT stack into dense card walls. The host + edit carry it.
5. **Punch accents:** big yellow draw-on UP arrows ("this → became → that"), a red rubber STAMP slam
   on the payoff, optional scribble circles. Homemade/honest vibe.
6. **Two world modes** — pick per video for a fresh fingerprint: (A) **green-grid studio** (clean,
   whiteboard-coded) or (B) **location-composite** (host dropped into real B-roll scenes). Don't repeat
   the same mode 3 days running (STYLE cooldown).

## ELEMENT CATALOG + FONTS + SIZES (decoded from 4 more Cars24-style Shorts, 2026-06-21)
Refs: `style_study/c24/` — 7UGMmzQ3yV8 (90s kaali-peeli cars), qDXuPTGve-8 (E85 petrol price),
N877IDASYxo (Wagon R Flex Fuel / 100% ethanol), yhIQysLbQvA (ethanol E20→E100). These are the
"faster cuts + a ton of elements" benchmark. Key additions to the v1 understanding:

**WORLD / BACKGROUND IS A COLORED VARIANT — not always green.** The graph-paper/grid texture
persists but its COLOR is chosen per topic/mood: deep-green grid (default explainer), **blue
sky+clouds** (nostalgia / "90s" / past), **solid purple grid** (tech / future / hype), **orange
fire/flames** (combustion / heat / energy), dark charcoal grid (mystery/serious). Pick the world
color to match the beat; switch worlds between sections for variety. Keep the same yellow + red-stamp
+ white-plate accent language across whatever world color you pick.

**FAST CUTS + DENSE ELEMENTS.** At 2fps the host's pose/expression changes almost every frame →
real cuts every ~0.5–1.5s. Every beat carries 2–4 on-screen elements (label + photo + arrow + badge).
Never hold a static frame; if the host talks >1.5s, a new element/cut must land. This is the energy.

**EMPHASIS-HOLD repeat:** a key stat plate (e.g. `₹82.12`, `100% Ethanol`) is REPEATED unchanged
across several rapid cuts while the host keeps talking — hammering the number in. Hold the same card
3–5 cuts for the punch stat.

**Recurring elements (with measured treatment):**
- **Price / stat plate** — rounded rect (radius ~18px), RED fill `#C0392B` + white bold text, OR white
  `#FBFAF6` + red text; top-third or beside host. Big bold price (`₹82.12`, `PETROL PRICE`). Sizes ~64–96px.
- **Circular product badge** — car/product photo masked in a YELLOW `#F5C518` ring/disc, centred;
  Hindi/Eng label under it. Used for "exhibit" framing of a product.
- **Escalating sequence labels** — a number series built one at a time: `E20 → E27 → E30 → E85 → E100`
  (or `MY→MYS→MYSTERY` letter-build). Huge bold (~140–200px), green/white fill, each new value pops in.
- **Brand-name label = ITALIC serif/script** (e.g. *Wagon R Flex Fuel*, *Flex Fuel Prototype*) — a
  DISTINCT font from the body. Product names italic-serif; everything else heavy sans. ~70–100px, white
  with a green accent word.
- **Big stat number** — `41%`, `100%`, `1%` huge condensed sans beside host, often two-tone (white +
  green/yellow keyword). ~120–200px.
- **Date / calendar badge** — small pill top-right (e.g. "JUNE 5th"), white on accent.
- **Float accents** — `???` question marks for rhetorical beats; emoji/icons (🛑 STOP, 💡 bulb, 🌳/🌍
  tree-earth for eco). Used sparingly as punctuation.
- **Topical B-roll close-ups** — engine bay, twin exhaust pipe, sugarcane field, fuel pump, a news clip
  of the relevant official (e.g. minister) — literal evidence, ken-burns, behind/around the host.
- **B&W footage** for past/"mystery" beats (desaturate the B-roll).

**FONTS (replicate with):** big labels/numbers = heavy condensed sans (Anton / Archivo Black /
Bebas-style), often UPPERCASE, white with a green `#1F9E5A`-ish or yellow `#F5C518` keyword. Body/captions
= bold grotesk. **Brand/product names = italic serif** (e.g. a Playfair/Times italic). Hindi labels =
bold Devanagari (Noto Sans Devanagari Bold). Always embed @font-face locally (office-box render).

**SIZES (9:16 1080×1920):** hero number/blend label 140–220px; price/stat plate text 64–96px; brand
italic 70–100px; date pill ~36–44px; label-plate caption 40–56px. Keep ~40px head-gap clear.

## VARIATION STUDY — how the 4 refs differ (revisited 2026-06-22, the owner asked)
The 4 Cars24-style Shorts run the SAME skeleton but swap a small set of dials by topic/mood. THIS is
our daily-freshness mechanism (vary the dials, keep the skeleton):
- **WORLD COLOR is topic-driven, not random:** blue-sky+clouds = nostalgia/90s/past · charcoal/dark =
  serious "now"/price · solid-purple grid = tech/future · orange FIRE/flames = combustion/heat/energy ·
  green-grid = default explainer · B&W desaturate = mystery/past beat. Pick the world to MATCH the beat;
  switch worlds between sections for momentum. Keep the yellow + red-stamp + white-plate accents constant
  across whatever world you pick.
- **EMPHASIS-HOLD (every ref):** one key stat plate (`₹82.12`, `100% Ethanol`, `E85`) is repeated
  UNCHANGED across 3-5 rapid cuts while the host keeps talking — hammers the number. Use on the punch stat.
- **ESCALATING NUMBER SEQUENCE (signature device):** a series built one value at a time —
  `E20→E27→E30→E85→E100`, `MY→MYS→MYSTERY` — huge condensed green/white numerals, each new value pops,
  often over the fire or purple world. Strong for "it keeps getting bigger" beats.
- **GREEN-DUOTONE PORTRAIT CARD:** the host's own face duplicated as a green duotone "exhibit" card (the
  "E85" cards) — a cheap, on-brand way to make a label feel like a topic poster.
- **CIRCULAR YELLOW PRODUCT BADGE:** car/product photo masked in a yellow ring, centred, label under it —
  "exhibit" framing.
- **ITALIC-SERIF brand/product names** (*Wagon R Flex Fuel*, *Flex Fuel Prototype*) — distinct from the
  heavy-sans body type. Product names italic-serif, everything else heavy condensed sans.
- **REAL OFFICIAL NEWS-CLIP b-roll** (e.g. minister Gadkari) for authority — matches our official-source-
  first rule; pull the 1-2 most iconic seconds.
- **TOPICAL CLOSE-UP b-roll as literal evidence:** engine bay, twin exhaust, sugarcane field, fuel pump,
  ceiling fan — always concrete, never generic.
- **Rhetorical punctuation:** `???` question marks, a red STOP sign, eco tree+earth 🌳🌍, date pill
  (top-right "JUNE 5th"). Sparse — punctuation, not walls.
- **Host WARDROBE varies per ref** (white polo / dark tee / orange tee) and even the presenter changes —
  in the refs the world+wardrobe pairing IS the fingerprint. OUR host is always the owner, so the WORLD-COLOR
  + accent + device-set rotation carries the per-day fingerprint instead of wardrobe.

### HeyGen-gesture gap (production note)
The Cars24 "alive" feel comes hugely from the presenter's CONSTANT hand gestures + expression change
every ~0.5s (the 2fps cut cadence). Our HeyGen cutout is comparatively static-torso with limited hands.
COMPENSATE by leaning HARDER on: (1) the dynamic host positioning/zoom choreography (more frequent
enter/anchor/step-aside/return moves), (2) denser element cuts (a new plate/arrow/badge lands every
~1-1.5s so the FRAME keeps changing even when the host doesn't), (3) emphasis-hold + escalating-number
devices that animate around him, and (4) avatar punch-ins on emphasis words. Don't expect the avatar's
body to carry the energy — the EDIT must.

## Why it works
- Keyed host reads as a real person teaching you → high trust + watch-through (not a stock VO).
- Constant repositioning + B-roll = momentum; nothing sits still long enough to scroll past.
- Graphics are LITERAL evidence placed in their own zone → never covers the face.
- Hand-drawn arrows / rubber stamp = energy + a homemade, believable feel.

## Palette (MEASURED) — green-grid mode
- BG base square **#143E30** (deep pine); grid line **#2E6149** (~1px on ~80px lattice).
- Accent yellow (UP arrows/highlights) **#F5C518**; stamp red **#C0392B** (~12° rotate, distressed).
- Panel white **#FBFAF6** (soft shadow, 16–24px radius); plate ink **#1A1A1A** bold condensed.
- Location-composite mode: world = the B-roll itself; keep the SAME yellow + red-stamp accents +
  white plates so the brand language stays consistent across both modes.
- Vars in `elements/palettes/cars24-green.md`.

## Layout zones (9:16, 1080×1920)
- **HOST ZONE:** the moving cutout (see choreography element). Feet near bottom; mic near chin;
  ~40px breathing gap around the head — nothing crosses it, EVER (full-bleed or corner alike).
- **GRAPHIC ZONE:** wherever the host ISN'T this beat — 1–2 evidence photos in white rounded panels
  (±3° tilt) + label plate, OR full-frame B-roll, OR a stamp card. Yellow UP arrows stack to show
  progression. Red stamp slams diagonally on the reveal.
- The host slides to clear the zone the graphic needs (left card → host right-third / corner-BL).

## Scene-by-scene skeleton (adapt; ~45–60s) — note the ENTRY/ANCHOR/SCALE column
| # | beat | host entry → anchor → scale | world / graphic zone | motion |
|---|------|------|--------------|--------|
| 1 | HOOK | zoom-in → centre → 1.0 | studio grid OR establishing B-roll, one teaser card | host pop-in, card slide+settle |
| 2 | SET-UP | from left → left-third → 0.92 | evidence photo #1 + label plate on the RIGHT | panel scale 0.9→1, tilt |
| 3 | BUILD | from bottom → right-third → 0.92 | photo #2 on LEFT + yellow UP arrow draws between | arrow stroke draw-on |
| 4 | PROOF | step aside → corner-BR → 0.62 | full-frame product/B-roll fills behind him | ken-burns B-roll, host shrinks |
| 5 | PUNCH | return + zoom → centre → 1.12 | red rubber STAMP slams the reveal | stamp scale 1.4→1 + shake |
| 6 | CTA | from top → centre → 1.0 | world clears, CTA plate lower-third | plate rise, host settle, face clear |

## BACKGROUND MOTION & PARALLAX (the owner, 2026-06-22 — re-checked the Cars24 video)
The background is NEVER a static fill. The world is alive and reads as DEPTH because layers move at
different speeds (parallax): back screen/horizon text drifts slowest → the GRID floor scrolls toward
the viewer (the signature "grid motion") OR an editorial-text sheet pans → b-roll runs full-frame with
ken-burns ON TOP of its own footage motion (rotating car, assembly line, lighting cycle) → graphic
cards slide+breathe → the host cutout is the fastest, independent foreground layer → a faint grain
overlay shimmers over all. **Parallax coupling:** when the host shifts one way, nudge the world the
OTHER way (smaller magnitude) so depth pops. FULL recipe + seek-safe GSAP code:
`elements/animations/parallax-world-motion.md`. This is mandatory now — a dead static grid behind the
host is a FAIL.

## Linked elements
- **Host motion:** `elements/animations/host-positioning-choreography.md` (entrances, anchors, scales). ← core piece
- **Background/world motion:** `elements/animations/parallax-world-motion.md` (grid drift, text pan, b-roll ken-burns, parallax coupling). ← core piece
- BG (grid mode): `elements/animations/green-grid-bg.md`.
- Stamp: `elements/animations/rubber-stamp-slam.md`. Arrows: `elements/animations/progression-up-arrow.md`.
- B-roll motion: `elements/animations/ken-burns-broll.md`. Palette: `elements/palettes/cars24-green.md`.

## REPLICATION RECIPE (how to actually build + replicate this)
1. **Host plate:** render the HeyGen avatar with `tools/heygen_playwright.py --background remove`
   (transparent alpha; magenta `--background magenta` #FF00FF is the chroma fallback — green clashes
   with the owner's mic LED, blue with his polo). Dense-keyframe re-encode the result.
2. **Build the host wrapper** `#host` (cutout `<img>`/`<video>` + soft contact shadow div). Place feet
   near the bottom edge.
3. **Pick the world per beat:** grid mode → drop the `green-grid-bg` layer; location mode → full-frame
   B-roll `<video>`/photo BEHIND `#host`. Source REAL official/stock footage (PIPELINE step 4b), never 100% CSS.
4. **Apply the choreography:** for each beat set ENTRY + ANCHOR + SCALE from the choreography element;
   alternate entry directions; shrink to a corner over full-frame B-roll/product, return + zoom for the punch.
5. **Add evidence + accents in the GRAPHIC ZONE** the host cleared: white tilt panels + label plates,
   yellow draw-on UP arrows for progression, red rubber-stamp slam on the payoff, sparse stamp cards.
6. **Keep text minimal** — let host + B-roll carry it; lower-third CTA plate at the end.
7. **Render** office box 60fps `--workers 1`; **audio_finish** music + on-beat SFX (~1/beat, -14 LUFS);
   **pipeline_check** (loudness + blank-scene gate) before delivery.

## Build notes / gotchas
- Soft contact shadow MUST be attached to `#host` so it moves/scales with him (else he looks pasted on).
- `transform-origin: <side> bottom` so zoom keeps his feet planted.
- One motion per beat; vary entry direction beat-to-beat; never block the evidence; never static >1 beat.
- All motion seek-safe on GSAP `tl` (no rAF/Date) — arrow via stroke-dashoffset, stamp via scale,
  host via `fromTo(immediateRender:false)` + `to` repositions.
- BLANK-SCENE GUARD: fade the host/inner content, never the scene container (rules/animations.md).
- Captions optional — in the refs the host carries it; if used keep lower-third, off the face.
