# CARS24-LAB — canonical reference for the Cars24 cutout house style

**Reference handle:** `cars24-lab` (a.k.a. "the Cars24 v3 demo / position study").
When the owner says **cars24-lab**, it means everything in this card.

## The learning-sample video (v3)
- `style_study/_pos/cars24_demo_v3.mp4` — 25s, 12 beats. The full house-style showcase.
- Earlier iterations: `cars24_demo_v2.mp4` (same-side entrances + SFX#2 + Ken-Burns face fix).
- Demonstrates: all 11 host anchors, same-side push-in entrances, viral whoosh SFX (#2),
  Ken-Burns face zoom (centre full-bleed only), parallax world drift, per-beat world-color shifts.

## Where the decoded learnings live
- **Full style spec:** `styles/full/cars24-cutout-explainer.md` (the complete look + "what we learned" set).
- **Host positions/choreography:** `styles/elements/animations/host-positioning-choreography.md`
  - 11 anchors: centre-fullbleed · centre-punch/face-punch (Ken-Burns only) · left-third · right-third ·
    corner-BL · corner-BR · corner-TL · corner-TR · edge-L-mid · edge-R-mid · off-stage.
  - Rule: entry-edge = rest-edge (enter from the side you anchor on, never cross frame).
- **Parallax/background motion:** `styles/elements/animations/parallax-world-motion.md` + `parallax-grid-zoom.md`.
- **Position boards (visual):** `style_study/_pos/position_board.jpg`, `corner_top.jpg`,
  `elements/animations/cars24_host_positions_board.png` / `cars24_host_positions_real.png`.
- **Entrance SFX options:** `style_study/_pos/entrance_sfx_options.mp3` (the owner picked #2, viral whoosh).
- **Reference frame grabs:** `style_study/_pos/ov_cars24.jpg`, `ov_e85.jpg`, `ov_90s.jpg`, `ov_wagonr.jpg`.
- **Palette:** `styles/elements/palettes/cars24-green.md`.

## 🔒 STANDING DEFAULT FOR ALL CUTOUT VIDEOS (the owner, 2026-06-24)
"Just like cars24. This is what I want for all of our cutout videos. Save this exact guide." →
`cars24_demo_v3.mp4` is the LOCKED reference. The EXACT per-anchor lean angles + entrance values are
baked into `styles/elements/animations/host-positioning-choreography.md` → the "🔒 LOCKED — v3
canonical lean angles + entrance" section. Match those numbers on EVERY cutout video; don't ask again.
- LEAN = constant rotateZ rest pose per anchor (2D in-plane ONLY, NEVER rotateY/skew); magnitude grows
  with edge distance: centre ±1–2° · thirds ±10° · bottom corners ±22° · edge-mid floats ±24° · top peeks ±30°.
- Lean is HELD through the same-side push-in entrance (does NOT spin to upright); points toward content.

## Locked decisions (from the build sessions)
- Entrance = same-side push-in + SFX #2 (viral whoosh).
- Face punch-in is ONLY the Ken-Burns zoom on the centre full-bleed position (no extreme head-crop).
- Cutout host docks to a position with NO element overlap; face always clear; full-bleed only on hook + CTA.
- Background must be alive (grid drift + parallax world); dead static grid = FAIL.
- Rotate WORLD-COLOR + accent per day for freshness WITHIN the house style (don't abandon the skeleton).
