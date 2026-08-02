# Full style — Postiz promo ("Retrofit AI" violet short)

Our open-source-scheduler promo. Centered talking head over dark violet backdrops with
browser-chrome b-roll panels, signature orbit + calendar-fill beats. Source project:
`hf-agent/projects/postiz/`. Delivered 1080×1920, 41.1s, **60fps** (v3). QA grids in `out/`.

## Palette → [elements/palettes/postiz.md](../elements/palettes/postiz.md)
Violet `--vio #a855f7` / `--vio-lt #c084fc` / `--vio-dk #7c3aed`, ink `#0b0a12`,
panel `#100d1a`/`#1a1626`, white. Brand glyphs keep native colors.

## Composition (1080×1920)
- Talking head CENTERED; b-roll panels + graphics sit over the dark cutaway backdrops,
  never over the face. Subtle animated dot-grid behind (opacity breathes 0.32↔0.55).
- B-roll lives in a clipped window at left62 top526 956×642 (see ken-burns).

## Scene-by-scene (verified timings on the rendered 60fps file)
| t (s) | Beat | On screen | Elements used |
|---|---|---|---|
| ~0.8 | "FIRED" strike | red strikethrough auto-fits the word (scaleX 0→1) | strikethrough (in this file) |
| 6.4 | Postiz brand | "FREE" exits ~5.8s, Postiz wordmark enters on the spoken word — never co-present | brand hand-off |
| 7.28 | Channels b-roll | panel bounces in, Ken Burns pan **L→R**, zoom 1.16→1.24 | [ken-burns-broll](../elements/animations/ken-burns-broll.md) |
| 11.94 | Composer b-roll | Ken Burns pan **R→L**, 1.16→1.24 | ken-burns-broll |
| 17.64 | Calendar b-roll | Ken Burns **zoom-in + pan DOWN**, 1.16→1.27 | ken-burns-broll |
| 22–23.4 | Orbit ring | 5 social icons sweep to equidistant slots, settle pulse, slow spin | [postiz-orbit-icons](../elements/animations/postiz-orbit-icons.md) |
| 28.5 | "NO AGENCY FEES" strike | auto-fit red strikethrough | strikethrough |
| 29.16 | Docker b-roll | Ken Burns pan **L→R** up-drift, 1.16→1.22 | ken-burns-broll |
| 33.6–37.1 | Calendar fill | "ONE EVENING → A WHOLE MONTH" card, ~24 dots fill progressively | [postiz-calendar-fill](../elements/animations/postiz-calendar-fill.md) |
| 37.8 | CTA / close | white CTA card pops, follow pulse | [comment-cta-card](../elements/subtitles/comment-cta-card.md) |

## Strikethrough (auto-fit) — reusable note
Bar animates `scaleX 0→1` (transformOrigin centered) so it crosses the word edge-to-edge at
any width — never a fixed pixel length that over/undershoots. Centered on the letter middle,
slight balanced tilt. Fires on the spoken negative word.

## Brand hand-off rule
Two hero blocks never co-exist: ensure the exiting word fully clears (~0.3s gap) before the
next wordmark enters on its spoken cue. Verify frame-by-frame either side of the swap.

## Rules carried from this build
- Re-encode b-roll sources with DENSE keyframes before render (sparse → black-frame crash).
- 60fps render = buttery orbit spin + Ken Burns pan (source video stays native fps).
- Nothing over the speaker's face; panels stay on dark cutaway backdrops.
