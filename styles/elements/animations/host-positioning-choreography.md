# Host positioning choreography — the moving cutout host

Decoded from the Cars24-style EV Short (`O35szDnG_-k`, 2026-06-21) + the long-form ref.
**This is the #1 thing we kept missing:** the keyed cutout host is NEVER parked dead-centre,
static, full-bleed for the whole video. Every beat gives him a fresh **entrance + anchor +
scale**, and he physically **steps aside / shrinks** when the B-roll or product must own the
frame, then comes back. That motion is what makes it feel alive and "in the world".

## The rule (apply to EVERY beat)
Each beat picks three things for the host cutout:
1. **ENTRY** — he ALWAYS slides in from the SAME SIDE he's about to anchor on (the owner, 2026-06-22):
   right-anchor → enter from the right edge; left-anchor → from the left; corner-TL → drop in from
   top-left; centre/bottom → rise from the bottom. He never crosses the frame to land on the opposite
   edge — the entry edge = the rest edge. (This OVERRIDES the old "vary the entry direction" note.)
2. **ANCHOR** — where he rests: centre / left-third / right-third / a bottom corner.
3. **SCALE** — zoom IN for emphasis/punchline; zoom OUT + shove to a corner when B-roll/product
   carries the frame. Never block the evidence; never leave him static or same-scale >1 beat.

Default cadence (≈45–60s short): hook = centre medium → each content beat alternates a NEW
entry direction + anchor, shrinking to a corner over B-roll/product → punch = zoom-in centre →
CTA = settle centre, face clear.

## DEFAULT = LARGE full-bleed bottom-center (the owner, 2026-06-22, re-checked the video)
The narrator is NOT a small contained figure — in the refs he's a BIG full-bleed cutout filling the
lower ~2/3 of the frame, bottom-anchored, mic (RØDE + brand flag) at his chin, eyes upper-center. He
stays prominent for talking beats and only SHRINKS to a corner (0.55–0.65) when full-frame b-roll/
product takes the world. Read `scale 1.00` below as that LARGE full-bleed size, not a medium shot.
The background behind him is always moving — pair every position with `parallax-world-motion.md`
(when the host shifts one way, drift the world slightly the other way for depth).

## Presenter ANGLE (the owner, 2026-06-22 — "I want the same angles, they look really nice")
The cutout host is NEVER flat straight-on. He's shot/keyed at a **dynamic 3/4 turn, leaning/angled
toward the content** — body twisted ~15–30° toward the b-roll/card, head tilted, shoulder forward,
mic up at the chin. Two locked refs:
- **corner-TL peek** — head & shoulders leaning IN from the top-left edge, looking down toward the
  scene, 3/4 from above (his petrol-station ref).
- **edge-R-mid float** — torso turned ~3/4 toward frame-centre, mic up, head tilted, cut by the right
  edge (his factory ref).
Rule: pick the cutout/pose whose lean points TOWARD whatever it's clearing space for; mirror the pose
for the opposite-side position. Real-frame board: `cars24_host_positions_real.png`.

## 🔒 LOCKED — v3 canonical lean angles + entrance (the owner, 2026-06-24: "Just like cars24. This is what I want for ALL our cutout videos.")
The reference is `style_study/_pos/cars24_demo_v3.mp4`, source `projects/cars24-position-demo/index.html`.
These are the EXACT measured values — use them as the standing default for every cutout video.

**LEAN = a CONSTANT rest pose per anchor** — `rotation` (rotateZ, 2D in-plane ONLY; NEVER `rotateY`/
`transformPerspective` = that skews the flat cutout). The lean is HELD: start rotation == end rotation
through the whole entrance — it does NOT spin to upright. Magnitude GROWS with edge distance, and the
lean points TOWARD the content / into the frame (left-side host leans +°, right-side leans −°; mirror).

| beat | anchor | rest x,y px (1080×1920) | scale | LEAN ° | entrance (same-side push-in) |
|---|---|---|---|---|---|
| HOOK | centre full-bleed | 0, 0 | 1.00 | **+1** | rise from bottom (y 2880→0), 0.55s power3.out |
| FACE | centre Ken-Burns | 0, 0 | 1.00→1.14 (origin 50% 14%) | **+3** | hold + slow zoom over the beat |
| — | left-third | −238, +77 | 0.92 | **+10** | from left (x −1534→−238) |
| — | right-third | +238, +77 | 0.92 | **−10** | from right (x +1534→+238) |
| — | corner bottom-R | +464, +442 | 0.62 | **−22** | from right (x +1210→+464) |
| — | corner bottom-L | −464, +442 | 0.62 | **+22** | from left (x −1210→−464) |
| — | corner top-L peek | −389, −461 | 0.56 | **+30** | drop from top (y −2035→−461) |
| — | corner top-R peek | +389, −461 | 0.56 | **−30** | drop from top |
| — | edge-R mid float | +508, −154 | 0.66 | **−24** | from right (x +1253→+508) |
| — | edge-L mid float | −508, −154 | 0.66 | **+24** | from left (x −1253→−508) |
| PUNCH | centre punch | 0, −125 | 0.92→1.13 | **+8** | rise + scale punch (origin 50% 100%, back.out(1.6)) |
| CTA | centre settle | 0, 0 | 1.00 | **+2** | rise from bottom |

Lean ladder (memorise): centre ≈ ±1–2° · thirds ≈ ±10° · bottom corners ≈ ±22° · edge-mid floats ≈ ±24° · top peeks ≈ ±30° · centre-punch +8°.

**Entrance mechanic (locked):** pure SAME-SIDE push-in — slide in from further out on the SAME side as
the rest anchor (entry edge = rest edge), TRANSLATE-ONLY, lean constant throughout, dur ~0.55s
power3.out. Top peeks drop from top; hook/CTA/punch rise from bottom. ~2.1s per beat.
**World/parallax (locked):** continuous grid bg-position drift the whole video + per-beat grid x-drift
~±26 OPPOSITE the host. World-color shifts per section: green→purple→blue→charcoal→orange→green (0.45s).
Ken-Burns ONLY on centre full-bleed (1.00→1.14, origin 50% 14%). Full-frame b-roll behind corner/edge
anchors (scale 1.06→1.14, x ±18 opposite the host) so the world owns the frame while the host shrinks.
Red rubber-stamp slam on the punch beat (scale 1.6→1, rotation −18→−12, 0.18s power4.out).
HONEST LIMIT: this lean is a flat-cutout approximation of cars24's real 3/4 body pose — for true
body-twisted 3/4 turns, render the HeyGen avatar at a few camera angles (the natural next upgrade).

## Measured anchors / scales (9:16, 1080×1920)
Cutout PNG/alpha host, feet near bottom edge, soft contact shadow under him.
| anchor | transform-origin | rest x/y (translate %) | scale | use |
|---|---|---|---|---|
| centre-fullbleed | 50% 100% | 0, 0 | 1.00 | DEFAULT — large bottom-center talk (lower ⅔ of frame) |
| centre-punch | 50% 100% | 0, 0 | 1.12 | punchline / emphasis (zoom in) |
| face-punch-in (KEN BURNS only) | 50% 88% | 0, 0 | 1.00 → ~1.14 | NOT a separate crop/anchor (the owner, 2026-06-22). It is ONLY a slow Ken-Burns push applied TO centre-fullbleed during a talking beat — host stays full-bleed bottom-center, scale eases 1.00→~1.14 over the beat with origin a touch above his face so the FINAL frame still keeps eyes upper-center & face fully in-frame (never an extreme 1.6–2.0 head crop, never jumps him off the default position) |
| left-third | 0% 100% | -22%, 0 | 0.92 | clear RIGHT for a card/B-roll |
| right-third | 100% 100% | +22%, 0 | 0.92 | clear LEFT for a card/B-roll |
| corner-BR (small) | 100% 100% | +28%, +6% | 0.62 | full-frame product/B-roll behind him |
| corner-BL (small) | 0% 100% | -28%, +6% | 0.62 | full-frame B-roll, host bottom-left |
| corner-TL (head/shoulders) | 0% 0% | -26%, -30% | 0.50–0.58 | host PEEKS from TOP-LEFT edge over full-frame b-roll (head & shoulders only, mic up). Use when the b-roll's foreground/bottom must stay clear |
| corner-TR (head/shoulders) | 100% 0% | +26%, -30% | 0.50–0.58 | same, top-RIGHT edge — mirror when the b-roll subject sits left |
| edge-R-mid (floating) | 100% 50% | +30%, -8% | 0.60–0.70 | host hugs the RIGHT edge at MID height — head & torso float at the side (NOT bottom-planted), cut by the frame edge, over full-frame b-roll. Use when b-roll fills the frame and the bottom is busy |
| edge-L-mid (floating) | 0% 50% | -30%, -8% | 0.60–0.70 | mirror — host hugs the LEFT edge at mid height over full-frame b-roll |
| off-stage (parked) | – | translate fully out | – | beat where ONLY B-roll/cards show |

## Entrances (seek-safe GSAP, ~0.5–0.8s, run on the timeline `tl` — NO rAF/Date)
`#host` wraps the cutout `<img>`/`<video>`; animate the wrapper. Use `fromTo` with
`immediateRender:false` so seek-render doesn't pre-apply the start state.
```js
// FROM LEFT (slide + slight rotate settle)
tl.fromTo("#host",{xPercent:-160,rotation:-8,autoAlpha:0},
  {xPercent:-22,rotation:0,autoAlpha:1,duration:0.7,ease:"power3.out"}, START);

// FROM BOTTOM (rise up)
tl.fromTo("#host",{yPercent:120,autoAlpha:0},
  {yPercent:0,autoAlpha:1,duration:0.6,ease:"power3.out"}, START);

// FROM TOP (drop in)
tl.fromTo("#host",{yPercent:-120,autoAlpha:0},
  {yPercent:0,autoAlpha:1,duration:0.6,ease:"power3.out"}, START);

// ZOOM-IN punch (push toward camera)
tl.fromTo("#host",{scale:0.86,autoAlpha:0},
  {scale:1.12,autoAlpha:1,duration:0.5,ease:"power2.out"}, START);

// STEP ASIDE + SHRINK to corner-BR (hand frame to B-roll/product)
tl.to("#host",{xPercent:28,yPercent:6,scale:0.62,duration:0.6,ease:"power2.inOut"}, START);

// RETURN to centre
tl.to("#host",{xPercent:0,yPercent:0,scale:1,duration:0.5,ease:"power2.inOut"}, START);
```
Reposition between beats with `tl.to(...)` (not a fresh `set`), so seeks tween smoothly.

## Cut cadence (decoded 2026-06-21)
Some Cars24 creators keep the host MORE centred but compensate with **very fast cuts (~0.5–1.5s)** +
**2–4 elements per beat** + emphasis-hold repeats of a key stat card. So either way the screen never
sits still: if the host isn't moving (entrance/anchor/scale change), then a CUT or a new ELEMENT must
land within ~1.5s. Combine both for max energy: reposition the host AND keep elements popping.

## Gotchas
- `transform-origin: <side> bottom` so scale changes keep his feet planted (no float).
- One motion per beat — don't entrance AND reposition AND zoom in the same 0.5s (reads jittery).
- Keep the soft contact shadow attached to `#host` so it moves/scales WITH him.
- ENTRY EDGE = REST EDGE (the owner, 2026-06-22): he enters from the same side he anchors on, never
  crosses the frame to land on the opposite edge. Get variety from the ANCHOR/SCALE/world-color, not
  from making him fly across the screen.
- BLANK-SCENE GUARD: never `fOut`/opacity:0 the host's SCENE CONTAINER; fade the inner host only
  (see rules/animations.md) or the whole beat renders empty on seek.

## Outro / CTA push-down sizing (the owner, 2026-06-26)
When a full-bleed host covers TEXT/elements that must be read (CTA headline, roster, copy stacked over
his head), push the host DOWN+back so those elements clear — but size it RIGHT:

- **Keep the host BIG.** Target `scale ~0.80–0.85`, never a 0.6x shrink. The avatar staying large reads
  as intentional staging; a tiny avatar reads as broken.
- **Small gap, not a void.** The host's FACE should sit JUST BELOW the elements above it with a SMALL
  visible gap (~40–90px on 1080×1920). No big empty dead band between the elements and the face.
- **Tune by the FACE, not the element top.** The HeyGen cutout has HEADROOM above the face, so the
  visible face lands well below the element's scaled top edge (`top = 1920*(1-scale) + y`, bottom origin).
  The face is ~roughly 30% further down inside the element than the top edge implies. So: render or
  `hyperframes snapshot` the resting frame, look at where the FACE actually is, then lower `y` until the
  face is just under the elements. Don't trust the top-edge math alone — it undershoots.
- Move `#host` + `#hostPool` + `#hostRim` + `#hostShadow` together (pool/rim a touch smaller scale).
- Spring back to full-bleed on the scene change (`back.out(1.4)`).

**Rejected vs approved (retrofit GTA6 CTA):**
- ✗ `y:150, scale:0.66` — avatar too small + huge empty gap above it.
- ✓ `y:80, scale:0.82` — for a top element band ending ~700px; face landed just below with a tidy small gap.

```js
// elements occupy the top band; host pushed down JUST below them, still large
tl.to("#host",{y:80,scale:0.82,rotation:0,duration:0.7,ease:"power2.out"}, T);
tl.to(["#hostPool","#hostRim","#hostShadow"],{y:80,duration:0.7,ease:"power2.out"}, T);
tl.to(["#hostPool","#hostRim"],{scale:0.76,duration:0.7,ease:"power2.out"}, T);
```

---

## v4 ADDENDUM — VISIBILITY FLOOR (the owner, 2026-07-12 — SUPERSEDES the v3 small-corner anchors)

The v3 table's shrunken corner/edge anchors (scale 0.56–0.66, top-peeks) are **retired**: at
chest-up-cutout scales below ~0.85 the bottom cut shows mid-frame and the host reads as a
floating PiP ("pasted sticker"). The locked v4 rules — full spec + measured face-target
cheat sheet in **`robust-anchoring.md`** (the authority for anchor math):

1. **≥50% of the visible avatar stays on screen at ANY edge** — never dock so far that more
   than half the body bleeds off (`face_x ∈ [~170, ~910]` with the standard face measure).
2. **The head is ALWAYS fully in frame** — hair to chin, both sides, top included; re-check
   on every punch-in.
3. **Scale ≥ 0.85, grounded** — the chest-cut bottom edge stays below the frame, always.
4. **FUN rotateZ leans, always toward the video content**: thirds ±6–8°, edge-docks ±10–14°,
   lower-corner peeks up to ±16°. Never 0°, never away from content, never rotateY.
5. Host is **default-ON every beat**, side-committed (never mid-frame); make room by
   edge-docking or going LOW under poster text — never by shrinking.

Entrances, same-side push-in, held leans, CTA push-down and full-bleed moments from v3 all
still apply — v4 only replaces the small anchors and adds the visibility floor.
