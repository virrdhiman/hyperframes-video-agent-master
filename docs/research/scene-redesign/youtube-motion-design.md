# Motion-Design Principles for the Scene Redesign

Distilled from YouTube teaching videos (see `playlist-motion-design.txt` for URLs).
Each principle cites the source + timestamp and ends with **→ HyperFrames** = how we
encode it. Evidence grids are in `grids/`.

**The core diagnosis.** Our generated scenes are flat vector shapes in a navy
void. The videos below converge on one root cause: *a shape only looks expensive
once it lives in a world* — it needs depth cues (shadow, blur, grain, gradient),
a contrast-driven hierarchy, and intentional negative space instead of empty
space. The two most useful pieces of evidence:

- `grids/lighting_overview.jpg` — a flat orange cartoon chicken on pure black
  (27s, *this is exactly our problem*) getting progressively desaturated,
  color-matched, shadowed and grained until it sits inside a real photo plate.
  This grid IS the fix, frame by frame.
- `grids/dune_poster_compare.jpg` — bottom-left = the cold teal "floating heads"
  cast poster the critics call cheap/generic; bottom-right = the warm
  orange-gradient "IT BEGINS" poster (single silhouette, huge negative space)
  they call the most expensive. Same franchise, opposite read.

---

## A. DEPTH — the fix for "flat shape in a void"

### 1. Desaturate + color-match a shape to its background before anything else
Advanced Lighting, **00:35–02:50**. The very first move to integrate a flat
graphic is to *pull it toward the scene*, not push the scene toward it:
desaturate ~12%, drop lightness ~10%, then use curves to bias the highlights
toward the background's color cast ("take blue out of the highlights so the
whites match the greenish background"). The flat element is too bright/too
saturated — that loudness is the tell.
**→ HyperFrames:** stop using pure saturated fills on dark backgrounds. Tint every
foreground shape a few percent toward the scene's dominant hue, and knock 8–12%
saturation off. Add a per-scene `tintTowardBackground` token.

### 2. A 2px Gaussian blur kills the "too crisp, too digital" vector edge
Advanced Lighting, **02:50–03:16**. Vector/shape layers are "so crisp and sharp"
they read as pasted-on. A barely-perceptible 2px blur on the edge softens that.
**→ HyperFrames:** apply `filter: blur(1–2px)` to flat SVG/shape layers (or a soft
1–2px inner feather), especially when composited over photographic B-roll.

### 3. Grain/noise on flat fills is mandatory, not decorative
Advanced Lighting, **03:16–04:55**. Real footage always carries sensor noise; a
flat one-color fill never does, and that mismatch screams "graphic." Add grain
to *lightness* (and a touch to hue/saturation) at ~4–5%, grain type not uniform,
animated ~24fps so it shimmers like film.
**→ HyperFrames:** add a reusable `<GrainOverlay opacity={0.04}>` (animated noise PNG
or SVG `feTurbulence`) on top of every flat-fill scene and the background itself.
Our configs currently have almost no noise/texture tokens (4 hits across the
whole repo) — this is the single biggest cheap-look gap.

### 4. Soft, offset, semi-transparent shadows = contact with the ground
Advanced Lighting, **04:55–08:00**. Build a shadow by duplicating the layer,
filling it a dark *scene-sampled* color (not black), feathering the mask ~500px
so it fades with distance, blurring it heavily (soft light = soft shadow), and
dropping opacity to ~50%. "It doesn't need to be accurate, it just needs to feel
real."
**→ HyperFrames:** offer two shadow recipes: (a) the house "hard sticker shadow"
`4px 4px 0 <color>` for the beige/collage aesthetic, and (b) a soft
depth-shadow for richer plates — large blur radius, ~40–50% opacity, color sampled
from the background, offset down. Never pure-black drop shadows; sample the ground color.

### 5. Depth = layered planes + gradient, not a single flat plane
DUNE Dissect, **21:20–22:11**. The 50th-anniversary poster is called the worst
precisely because "there's so little depth… it feels so flat… the textures don't
feel inspired," even though it technically has dunes + a moon + a worm
silhouette. The winners stack foreground/midground/background planes and use a
*color gradient* across the frame (the German poster's "red to orangey-yellow
gradient," 06:02–06:23; the warm "IT BEGINS" poster).
**→ HyperFrames:** backgrounds should be a 2–3 stop gradient (warm or scene-keyed),
never a flat `#0A1428` navy. Compose scenes in ≥3 depth planes (bg gradient →
midground shapes at reduced contrast → hero element) with subtle parallax.

---

## B. HIERARCHY & CONTRAST — the fix for "everything is the same, nothing pops"

### 6. The eye goes to the highest contrast + highest saturation first — design that on purpose
10 Underrated, **11:48–12:16**. Walking through a student frame: "Immediately with
the most saturated shapes and the highest contrast we are drawn here
[strawberries], then led down to the jam… the background character has much lower
contrast so it is less important. Clear hierarchy: 1 strawberries, 2 jam, 3
background." Hierarchy is built by *deliberately lowering* contrast on secondary
elements.
**→ HyperFrames:** enforce a 3-tier contrast ladder per scene — hero element at full
saturation/contrast, supporting at ~60%, background at ~30%. Right now we tend to
render every chip at full saturation, which flattens the read. Tie this to a
`tier: 1|2|3` prop on scene elements.

### 7. Know the single most important thing in every shot
10 Underrated, **11:16–11:48**. "In every shot you should know the most important
thing you want the audience to see. If there's too much going on they miss it
while chasing something unimportant in the corner." Same point in Floaty Movements
(**05:51–06:20**): constant motion everywhere becomes "visual white noise" so
"nothing stands out."
**→ HyperFrames:** one focal element per scene. Demote or remove competing animated
chips. Don't animate three things at the same energy at once (already in CLAUDE.md
as the pacing rule — extend it to *visual* energy, not just cut rate).

### 8. Eye-trace — choreograph where the viewer looks across the shot
10 Underrated, **10:52–11:16**. A falling blood drop is added specifically to pull
the eye from the top action down to the next beat — "eye tracing is how animators
direct the path of the viewer's eyes." A moving element becomes the baton handed
between focal points.
**→ HyperFrames:** sequence reveals so each new element appears *along the path* the
previous motion was traveling, not scattered. Use a single moving accent (a dot,
an underline, the caption word) to lead the eye between cards.

---

## C. NEGATIVE SPACE — the fix for "empty void vs intentional space"

### 9. Distinguish macro vs micro and passive vs active white space
DesignCourse Space, **00:11–03:13**. *Macro* white space = large empty expanses;
*micro* = gaps between lines, paragraphs, packed objects. Separately, *passive*
white space aids legibility/aesthetics, while *active* white space "controls the
order and movement of the reading experience… breaks things into digestible
chunks." Crucially: **"more macro white space suggests minimalism, modernity and
luxury"** (01:56–02:14) — emptiness is only premium when it's *framing a focal
point*, not when it's an unstructured void.
**→ HyperFrames:** our navy void fails because the space is passive and unframed.
Give every scene a margin grid (e.g. 8% safe margin), group related elements with
*tight* micro-spacing and separate groups with *generous* macro-spacing so the
emptiness reads as deliberate. One confident focal element in a large calm field
beats a half-full frame of scattered chips.

### 10. Negative space is not white space — it should carry meaning/form
DesignCourse Space, **04:09–11:03** and **14:32–14:46**. Negative space "creates
subject, form or even meaning when two or more objects interact" (FedEx arrow).
The empty area between things should be *shaped*, not leftover.
**→ HyperFrames:** let backgrounds/shapes interlock so the gaps form silhouettes or
lead lines; align elements to a grid so the channels between them are clean and
intentional. Proximity rule (12:50–13:33): elements that belong together must be
visibly closer than elements that don't.

---

## D. MOTION CHOREOGRAPHY — concrete values to paste in

### 11. Gate weave: wiggle(12, 3) on an adjustment layer for analog life
10 Underrated, **04:50–06:46**. A whole-comp `wiggle(frequency 12, amplitude 3px)`
on an adjustment layer mimics film-projector instability — "adds subtle complexity
and richness that makes it seem less clean and digital." To avoid edge gaps,
scale the layer 100→101. Apply a *second*, independent weave to the title for "the
smallest amount of parallax possible" and doubled life.
**→ HyperFrames:** add a `useGateWeave()` hook returning a tiny per-frame
`translate` from a seeded noise (freq ~12/s, amp ~2–3px), applied to the whole
scene, plus an independent one on the hero so foreground and background drift
apart slightly. This single change removes the "dead, perfectly-static" feel.

### 12. Posterize/step the framerate to ~12fps for a handmade feel
10 Underrated, **04:28–04:39**. Dropping the effective framerate (posterize time to
12fps) on an animation layer "really helps make it feel a bit more like
hand-drawn frame-by-frame animation" and hides over-smooth motion-tweening.
**→ HyperFrames:** for accent/illustrative motion, quantize interpolation to ~12fps
(`Math.floor(frame/2.5)`-style stepping) rather than buttery 30fps. Reserve smooth
30fps for camera/Ken-Burns moves.

### 13. Show the *result* of an action (impact splash) to sell weight
10 Underrated, **02:55–03:24**. Adding small splashes when fangs puncture: "Seeing
the result of an action makes you feel the impact much more… now we have something
to linger on." Without the after-effect the same motion feels weightless.
**→ HyperFrames:** every entrance/impact gets a reaction — a small particle pop, dust,
ring, or shake on the thing it lands near. Pair with anticipation→action→reaction
(Floaty Movements, **08:24–09:08**): wind-up, move, follow-through/overshoot.

### 14. Slow-in/slow-out and overshoot — never constant-velocity moves
Floaty Movements, **03:04–03:29**. Floaty = "constant velocity throughout… they
don't accelerate or decelerate." Fixing the spacing (ease) "goes a long way."
Also: real movement is *fast* once it starts, after a brief anticipation
(03:42–04:12) — slow moves read as "defective robots whose batteries are dying."
**→ HyperFrames:** keep using springs (`damping 12–14`) for overshoot, but audit for
linear `interpolate` moves and replace with eased ones. Bias durations *shorter* —
snappy entrances (8–14 frames) with a settle, not long glides.

### 15. Less is more — over-animation and too many keyframes both read cheap
Floaty Movements, **09:22–11:38**. Over-animating fine details nobody notices, and
piling on keyframes, makes motion "stilted and less fluid." "Less is more… use the
graph editor to control acceleration, not more keyframes."
**→ HyperFrames:** prefer 2–3 keyframe spring/ease moves over hand-tuned multi-step
animations. Don't animate properties that don't need to move.

---

## E. WHAT MAKES IT LOOK EXPENSIVE vs CHEAP (art-direction signals)

### 16. "Re-blanding" — a generic sans with no character is the cheap default
Rebrands Dissect, **08:35–10:08**. The Johnson & Johnson rebrand is "the skim milk
of the logo… 5% of the flavor, the rest is re-blanding water." The recurring 2023
failure is stripping all personality down to a flavorless sans serif.
**→ HyperFrames:** avoid defaulting every label to plain Inter/Helvetica centered and
upright. Commit to a typeface with character per aesthetic, keep our uppercase +
letter-spacing rule, and vary weight for hierarchy (DUNE Dissect 19:08–19:34
faults a cover for using "the same typeface, same weight, just different sizes —
change a weight if you set it so they don't all look the same").

### 17. Sparseness reads as grand *only* with scale and a strong focal point
DUNE Dissect, **04:09–04:22** and **05:25–06:23**. "What I love most is how sparse
it is — it makes it feel grand." But the sparse-but-flat 50th-anniversary cover
fails. The difference is *scale contrast*: a tiny silhouette against a vast field
(the lone figure on the orange dune) creates grandeur; evenly-sized flat elements
do not.
**→ HyperFrames:** when going minimal, exaggerate scale contrast — one large or one
tiny hero against a large calm gradient field. Don't fill the frame with
medium-sized equal elements.

### 18. One accent color per item in a series; warm gradient palettes feel premium
DUNE Dissect, **16:49–17:05** and **06:02–06:23**. Praise for covers that "choose
one accent color for each one of the series," and for the "red to orangey-yellow
gradient." Cold/desaturated palettes are repeatedly called cheap/wrong for a
warm-toned subject (08:19–08:46: the cold-blue poster "does no justice… screams
cheap").
**→ HyperFrames:** give each card/data point its own accent (already a stated
preference in memory — enforce it), and key the *background gradient* to the
scene's emotional temperature instead of a fixed navy. Warm gradients for
energy/impact scenes.

### 19. The "floating heads" composite is the canonical cheap cliché — earn the real footage instead
DUNE Dissect, **13:40–14:16**. The cast poster with floating heads blended into
dust is "muddy… the floating-head style doesn't work… too much Marvel
influence." A real, single, well-composed image beats a busy composite.
**→ HyperFrames:** don't stack cut-out heads/logos into a murky collage. Per
CLAUDE.md's media ladder, a single piece of real footage or one iconic clip earns
its place; reserve composites for when each element is clearly readable.

### 20. Repeated-system thinking looks intentional; ad-hoc decoration looks lazy
DUNE Dissect, **23:05–23:53**; Rebrands Dissect, **01:01–02:20**. The Galaxy
hardback's "one shape repeated for all the letters" reads as a confident *system*.
Conversely the Pepsi deck's "loads of circles drawn on top of one another, rotated
at the whim of the designer and justified afterwards" with fake golden-ratio
construction grids is mocked as pseudo-rigor.
**→ HyperFrames:** derive scene layouts from a real grid/module system and reuse a
small shape vocabulary across a video, rather than sprinkling unrelated decorative
shapes. Consistency of a constrained system > variety of one-offs.

---

## Top-priority changes for the pipeline (ranked)

1. **Kill the flat navy void:** replace flat background fills with 2–3-stop
   gradients keyed to scene temperature, in ≥3 depth planes. (#5, #18)
2. **Add a global grain/texture overlay** (~4% animated noise) on every scene and
   background — biggest single cheap-look fix. (#3)
3. **Add a soft depth-shadow recipe** (large blur, scene-colored, ~45% opacity)
   for richer plates, alongside the existing hard sticker shadow. (#4)
4. **Enforce a 3-tier contrast/saturation ladder** so one focal element pops and
   secondaries recede. (#6, #7)
5. **Integrate foreground shapes:** desaturate ~10% + tint toward bg + 1–2px edge
   blur so they stop looking pasted-on. (#1, #2)
6. **Add `useGateWeave()` + 12fps posterized accent motion** to remove the
   dead-static digital feel. (#11, #12)
7. **Treat space intentionally:** margin grid, tight micro-spacing within groups,
   generous macro-spacing between, one focal element in a calm field. (#9, #10)
