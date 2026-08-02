# "Morning Edition" — editorial print-special (retrofit-2026-07-11 recut, APPROVED 2026-07-12)

the owner's verdict: *"this is really good"* — after two rejected passes. This file records what
the approved cut actually does, so future runs reuse the THINKING (not clone the look).
Source comp: `retrofit-2026-07-11-fable/retrofit-2026-07-11/index.html`. Final:
`render_recut_final.mp4` (65.5s @60fps native; 1.10× at delivery).

## Concept discipline
One metaphor carried everywhere: "Wall Street **history** → front pages". World, captions,
SFX, hero, CTA all speak print. Pick ONE such literalized metaphor per video and let it set
palette + surfaces + foley (gold-rush=coins, print=paper, courtroom=gavels…).

## Measured fingerprint
- Palette: paper `#F4EFE6` · card `#FBF7EC` · ink `#14120F` · editorial red `#D8232A`
  (stamps/emphasis/walls) · green `#0F8A46` ONLY on the up-tick. LIGHT world, never dark.
- Type: Playfair 800 (+italic) serif for editorial/emphasis · Anton for poster numerals ·
  Outfit body. Captions: editorial-emphasis chips (ink on paper, red Playfair-italic
  emphasis words) + parallax red serif walls on exactly 2 statement beats.
- World: living paper — drifting newsprint columns (opacity ~.05), hairlines, pinned top
  ticker strip (OUTSIDE the camera transform), warm finish + grain.
- Containers: editor-texture pass (`styles/elements/finishing/editor-texture-pass.md`) —
  tape, grain, hard offset shadows, highlighter kickers, worn-ink stamps.

## The beat grammar that made it "a video, not a website"
Every beat = **full-bleed image layer + poster type + docked host**, from these molds:
1. **Plate beat** (stat/date): AI/stock full-bleed plate graded `brightness(.72–.8)` →
   poster numeral 200–430px cream/red ON the footage → kicker + one sub-line. No card.
2. **Clipping beat** (evidence): taped paper card (logo/photo/front-page mock/tickets) +
   rough red annotation (arrow/circle/X, element-anchored) + host docked opposite.
3. **Statement wall** (×2 max): giant condensed red serif BEHIND the host, front line in
   front (caption systems swap off during walls).
4. **Stamp payoff**: red rubber stamp slams OVER host + frame (z above host), worn ink.
Hero = Kling motion from an identity still (Nano Banana + `face` Element); one Gemini Omni
camera-swap on the record line (see `docs/OMNI-HOOK-CAMERA-ANGLES.md`).

## Host choreography (the approved pattern)
Default-ON every beat, side-docked + leaned, face-anchored, grounded, ≥0.85 — full rules +
cheat sheet in `styles/elements/animations/robust-anchoring.md`. 3–4 face-anchored punch-ins
on emphasis words ("feeds", "198%", "$170"). Off ONLY for hero + Omni beats.

## Pace & rhythm — the measured fast-cut spec (what made it feel edited)
- **Beat containers avg ~2.8s (21 beats / 65.5s native), but EVERY beat carries 2–4 internal
  reveals, so something changes on screen every ~1–1.5s.** That's the trick: don't shrink
  beats below what the VO sentence needs — sub-cut INSIDE them. A 4.5s sentence beat =
  3 sub-beats (B14: route arc draws 1.4s → 7 stubs machine-gun in at 0.16s stagger → 7×
  slams → price tag), never one static card held 4.5s.
- **Every reveal lands ON its word's start** (`findW()` from words.js — never ~0.2s late):
  odometers start counting on the number's first syllable ("$26.5B" at 10.06), stamps slam on
  the stressed word ("ever" 14.46 · "shortage." 29.10 · "seven" 39.36 · "pricier." 53.40),
  chips/tags pop per spoken item.
- **Number payoff cadence**: riser starts on the word → count runs 0.9–1.35s → deep impact
  lands exactly at count-end. Used on $26.5B, 60%, 198%, $1T, 7×, $170.
- **Hard cuts are the grammar: exactly 2 spec'd transitions in 65s** — one whip-pan (hero →
  world handoff at 4.94) + one 1–2-frame white flash (into the №01 kicker). Never back-to-back,
  never on ordinary cuts.
- **Punch-ins ×3–4** on emphasis words (face-anchored, no vertical jump) + hero micro-punch on
  "shovels" — the pseudo-cut that keeps a single shot alive.
- **Breathing before hits**: 0.3–0.5s where motion settles right before each statement wall and
  the thesis collage — the contrast is what makes the slams read fast.
- **Entrances 0.24–0.55s** (power3/power4.out, back.out only on emphasis); exits 0.22–0.3s
  power2.in; card float/drift for the whole hold (nothing static >1.5s); stagger multi-items
  0.06–0.16s.
- **Captions in 2–4 word groups**, one at a time, swapped per group; statement walls replace
  captions on their beats (never both).
- **~1 SFX cue per beat + risers** (34 cues / 65.5s), music bed −21dB with swells into the hits.
- **Global 1.10× speed at delivery** (house standard) — build native, speed in post.

## Audio identity
34 cues / 65s: topic foley (paper slap, stamp thunk, ticker, press rumble, cash register on
the price pop) + el_riser into every number payoff + el_deep_impact on landings + vine boom
on the 2 biggest words + generated news underscore bed at −21dB → `audio_finish.py` −14 LUFS.

## Cooldown note
Log in PRODUCED.md at delivery. The print-world + paper palette + red serif walls go on the
standard 3-day style cooldown; the beat grammar (plates/poster type/docked host/stamps-over)
is evergreen and should carry into every future cutout video.
