# Internal Design-System Audit — Why the Output Reads "Programmatic," and a Generated-Asset Taxonomy to Fix It

> **Migration note:** this audit examined the *prior Remotion codebase* (`.tsx` compositions, the `dark-tech/`
> component library, etc.). Those files are historical evidence — they no longer exist in the HyperFrames project.
> The *diagnosis* (flat fills, navy void, weak shadows, no grid) and the *generated-asset taxonomy* are
> framework-agnostic and carry over directly: in HyperFrames the same fixes apply, with the consumption layer
> expressed as HTML + a paused GSAP timeline instead of React components. The dark/navy/glassmorphism material
> below is cited as the look being *escaped*, not endorsed.

Scope: audits the existing design system as actually implemented (not as the guides aspire to it), pinpoints the
patterns that make scenes look flat/cheap, catalogs the recurring scene archetypes, and proposes a reusable
generated-asset taxonomy to feed the AI-asset-generation reimagining (Recraft SVG, gpt-image, nano-banana, etc).

Primary evidence read:
- `docs/guides/AGENT_GUIDE.md`, `DARK_TECH_STYLE.md`, `DARK_TECH_COMPONENTS.md`, `COMPONENT_CATALOG.md`, `SCENE_SNIPPETS.md`
- `src/components/dark-tech/*` (all 10 components + `theme.ts`)
- `src/AIStylistMain_v1.tsx` (canonical dark-tech reference, 1100 lines)
- `src/NvidiaRTXSparkMain_v1.tsx` + `src/components/nvidia-rtx-spark/scenes.tsx` (multi-file scene module, incl. 3D)
- `public/common/*`, `assets/*`, the asset-generation rule

A blunt summary up front: **the system has a strong motion/timing layer and an excellent talking-head pipeline, but
its on-screen "graphics" are almost entirely CSS rectangles — solid-fill `<div>`s with rounded corners, a tilt, a
spring, and a drop-shadow — floating over a single dark `#0D1117` color or a radial-vignetted still.** There is no
texture, no depth beyond one shadow, no illustration, no iconography with weight, and no grid. The motion hides it in
isolated frames, but on a paused frame every "graphic" scene is a colored pill on a void. That is the cheap look.

---

## 1. DESIGN-DEBT LIST (file/line-grounded)

### D1 — The "navy void": a single flat background color is the default canvas
- `dark-tech/theme.ts:11` `bg: "#0D1117"`, used as the literal `backgroundColor` of the root `AbsoluteFill` in
  `AIStylistMain_v1.tsx:457` and `NvidiaRTXSparkMain_v1.tsx:140` (`background: NVIDIA_DARK`).
- `Vignette.tsx` (the canonical backdrop) is, when no `src` is supplied, **just a solid color + one radial gradient**
  (`Vignette.tsx:30,42-46`). No grain, no gradient banding control, no parallax layer, no texture.
- Why it reads cheap: a flat near-black fill with one centered element is the visual signature of a quick template.
  Real motion-design backplates have at least 3 of: gradient mesh, grain/noise, soft bokeh/particle depth, a vignette,
  and a subtle texture or grid. Here there is one (vignette) and it's optional.
- Several scenes don't even use the vignette — they paint pure black (`AIStylistMain_v1.tsx:472` `backgroundColor:"#000"`,
  `:795`, `:956`) so the element floats on a true void.

### D2 — Every "graphic" is a flat single-color CSS rectangle
- The chips/cards are all the same primitive: a `<div>` with `backgroundColor: <one solid color>`, `borderRadius`,
  one `boxShadow`, a `transform: scale/rotate`. Examples:
  - `ColorChip.tsx:54-68` (solid swatch + circle badge)
  - `TiltedChipStack.tsx:84-100` (solid pill)
  - `GlassRailCard.tsx:42-54` (one translucent panel)
  - `CounterPill.tsx:60-74`, the inline WARM TONE / MEDIUM-DEEP chips in `AIStylistMain_v1.tsx:682-704`,
    the LOOSE FIT / LOW CONTRAST chips `:825-852`, the NVIDIA `greenChip`/`outlineGreen` helpers
    `nvidia.../scenes.tsx:62-63`.
- There is **no fill variety**: no gradients-with-purpose, no inner highlight/lowlight, no border-light edge, no
  material (paper, glass-with-real-refraction, metal, sticker die-cut). Flat fill + one shadow = "PowerPoint shape."
- The guides even acknowledge two contradictory house styles and the code picks the cheaper read of both: AGENT_GUIDE
  bans glassmorphism and demands `4px 4px 0px` hard physical shadows (`AGENT_GUIDE.md:26-27`), while the dark-tech
  components use soft `0 12px 40px` glass shadows (`GlassRailCard.tsx:53`, `ColorChip.tsx:64`). Neither path adds
  texture; the result is "flat sticker" or "flat glass," never "designed object."

### D3 — Weak / single-layer shadows; no real depth stack
- Every shadow is one offset blur: `0 12px 40px rgba(0,0,0,0.5)` (`GlassRailCard.tsx:53`),
  `0 10px 30px rgba(0,0,0,0.35)` (`TiltedChipStack.tsx:96`), `0 20px 60px rgba(0,0,0,0.5)` (`LogoTile.tsx:55`).
- Premium depth needs layered shadows (contact + ambient + key) and/or an occlusion gradient under the element. One
  blurred drop shadow on a flat fill reads as "div with box-shadow," which is exactly the tell.
- The accent-tinted-shadow trick (`boxShadow: 0 12px 40px ${color}55`, `ColorChip.tsx:64`) is the only sophistication
  and it's applied uniformly, so it stops registering as intentional.

### D4 — No grid system; elements are absolutely-positioned by eyeballed pixel constants
- Layout is hardcoded magic numbers, not a grid: `paddingTop: 380` (`AIStylistMain_v1.tsx:676`), `paddingTop: 160`
  (`:773,:784`), `top: 220, left: 40` / `top: 380, right: 40` (`:828-846`), `paddingTop: 80` (`:863`),
  `paddingBottom: 650` (`nvidia.../scenes.tsx:91`), `top: 700` (`:248`).
- DARK_TECH_STYLE.md ships a "layout grid" table (`:116-131`) but it's prose zones, not an enforced column/baseline
  grid, and compositions don't reference it. Consequence: inconsistent margins between videos, single-element scenes
  that don't sit on any rhythm, and the constant collision-avoidance hacks below.
- The only "design system" depth is color tokens (`theme.ts`) — there are no spacing tokens, type-scale tokens, radius
  tokens, or shadow tokens. So every composition re-invents sizes and they drift.

### D5 — One element centered in space = the dominant composition
- Scene after scene is a single centered object on the void: scene 3 two chips centered (`:676`), scene 5a/5b three
  chips centered (`:773,:784`), scene 8 a bar + number centered (`:863`), NVIDIA hook one chip top-center
  (`scenes.tsx:69`), reveal one chip (`:91`), specs one chip swapped per word (`:109-128`), CTA one chip (`:260`).
- No foreground/midground/background separation, no supporting decorative elements, no asymmetry, no edge-bleed
  composition. "Big centered thing on dark" is the lowest-effort layout and it's the default here.

### D6 — Iconography is glyph/emoji strings, not designed marks
- "Icons" are literally unicode glyphs passed as strings: `icon="◉"`, `icon="☀"`, `icon="✓"`
  (`DARK_TECH_COMPONENTS.md:58-60`, `GlassRailCard.tsx:65`), `✓`/`✕` text in `ColorChip.tsx:84`,
  `⚠ THE CATCH` (`scenes.tsx:214`), `▲ +` / `▼` (`PhasedScoreBar.tsx:134`).
- These render in the system font, with no consistent weight, grid, or style — they look like keyboard characters, not
  iconography. The repo ships 75k+ animated icon libs (AGENT_GUIDE.md:203-215) but the actual graphic components don't
  use them; they fall back to glyphs.

### D7 — Text-overlap / collision risk is "solved" by manual pixel dodging, not layout
- The talking head is shoved around per-scene with hand-tuned springs to avoid overlapping graphics:
  `AIStylistMain_v1.tsx:421-445` (`dodgeSpring`, `tx = s2_shift*-220`, `ty = s3_shift*350 + s5_shift*400 + ...`),
  and NVIDIA pushes the avatar down `shiftY = push*360` (`NvidiaRTXSparkMain_v1.tsx:136-137`).
- Captions avoid the graphics by a fixed `paddingBottom: 150/180` and a "don't put UI in the center-bottom 220px" rule
  (`DARK_TECH_STYLE.md:131`). NVIDIA reveal hardcodes `paddingBottom: 650` to clear the face + subs (`scenes.tsx:91`).
- This is fragile: any change to VO length, chip count, or caption wrap re-introduces overlap because nothing is laid
  out relative to anything else — it's all absolute constants tuned by preview-and-nudge.

### D8 — Over-reliance on hand-coded flat SVG / CSS for "signature" visuals
- The "signature scene" guidance is to hand-build SVG with `<circle>/<rect>/<line>/<path>` and animate
  `stroke-dashoffset` (`SCENE_SNIPPETS.md:1001-1053`). That yields thin, flat, single-stroke vector diagrams — the
  literal definition of the look being escaped.
- The richest real visuals in the repo are NOT hand-coded: they're the AI-generated full-bleed images
  (`contrast_split.png`, `outfit_cards.png`, `style_analysis_report.jpg` in `AIStylistMain_v1.tsx`) and the 3D
  three.js objects (`Chip3D`, `ParticleCore`, `Logo3DCard` in `scenes.tsx:117-122,177-181,236-243`). The flat-feeling
  scenes are exactly the CSS-rectangle ones. This is the core insight for the redesign: **the depth already comes from
  generated/rendered assets; the cheapness comes from the CSS-primitive scenes.**

### D9 — Logos/object cutouts are ad-hoc, low-quality, and inconsistently framed
- Logos are dropped into a white frosted tile (`LogoTile.tsx`) or used raw (`scenes.tsx:239-242`). Sourcing is "Google
  Images PNG" (AGENT_GUIDE.md:178-181), which means inconsistent padding, resolution, and on-color (a transparent PNG
  with built-in white halo on a dark bg looks cheap). No normalized, color-matched, consistently-padded logo set.
- Object cutouts rely on `rembg` over stock/AI stills (`asset-generation.mdc` background-removal section) with no
  shared library — every video re-cuts its own, quality varies.

### D10 — Repeated identical framing across the library (templated feel)
- The dark-tech components encode ONE framing each (rail card always slides from right 600px, `GlassRailCard.tsx:51`;
  ColorChip always slides from left -200px, `ColorChip.tsx:51`; chips always tilt ±4° alternating,
  `TiltedChipStack.tsx:83`). Two different videos built from this kit look like the same video with different words —
  the opposite of the AGENT_GUIDE's "no two consecutive scenes the same" mandate (`AGENT_GUIDE.md:71`).
- The accent-color palette is also fixed (yellow/green/red, `theme.ts:13-16`; DARK_TECH_STYLE.md:148 forbids a third),
  so dark-tech videos are chromatically identical regardless of topic.

### D11 — Gradients used only as flat 2-stop fills, never as light
- The few gradients are 2-stop linear bar fills (`PhasedScoreBar.tsx:111-113`) or a flat scrim
  (`StripSlide.tsx:78`). No gradient mesh, no radial light source, no color temperature shift across the frame. This is
  why even the "glass" panels look like flat translucent boxes rather than lit surfaces.

### D12 — Glassmorphism is faked with `backdrop-filter: blur` over a dark void
- `GlassRailCard.tsx:47-48` (`backgroundColor: rgba(20,28,40,0.78)`, `blur(14px)`) and `StripSlide.tsx:100-105`
  (`blur(28px)`). Over a flat `#0D1117` there's nothing meaningful to refract, so the blur produces a uniform muddy
  panel, not glass. Glass only reads as glass over rich, high-frequency content behind it — which the void isn't.

---

## 2. RECURRING SCENE ARCHETYPES

These recur across compositions. For each: what it's for, and the visual primitives currently **hand-built every time**
(the targets for generated assets).

| # | Archetype | Where it shows up | Hand-built primitives today |
|---|-----------|-------------------|------------------------------|
| A1 | **Hook / title card** | `AIStylistMain_v1` s1 (`:470`), NVIDIA `HookScene` (`scenes.tsx:66`), every CTA | Big stroked Impact text + a pill + (optional) glitch jitter, over a dark scrim or a generated bg video. No designed lockup, no backplate art. |
| A2 | **Stat / counter** | `CounterPill`, money scene (`:953`), NVIDIA "128GB", "1 PETAFLOP" (`scenes.tsx:113,126`) | One solid pill, a counting number, a tilt. No data-viz frame, no unit chrome, no contextual illustration. |
| A3 | **Score / progress bar** | `PhasedScoreBar`, s8 rating (`:861`) | A rounded track `<div>` + a 2-stop gradient fill + a giant number + a `▲ +delta` glyph badge. Pure CSS. |
| A4 | **VS / comparison split** | `SplitContrast`, NVIDIA AI-flex split (`scenes.tsx:153`), chip-war "VS" (`:247`) | A pre-composited side-by-side image OR two stacked video panels + a glowing center divider `<div>` + 2 corner label chips. The "VS" is a text glyph. |
| A5 | **List / checklist / mistakes** | s5a/s5b ColorChip stacks (`:773,:784`), s7 mistakes (`:816`), NVIDIA catch chips (`scenes.tsx:215-217`) | N solid chips staggered, each with a `✓/✕` glyph. No bullet iconography, no row framing, no connective structure. |
| A6 | **Logo grid / brand row** | `LogoTile` row, NVIDIA chip-war 3D logos (`scenes.tsx:239-242`), `CompanyLogoOverlay` | Logos in white tiles (2D) or rotating 3D cards. Inconsistent logo sourcing/padding. |
| A7 | **Side-rail data panel** | `GlassRailCard` stack (DARK_TECH_COMPONENTS.md:52-61) | Glass `<div>` panels with a glyph icon + label + value. No real instrument/HUD chrome. |
| A8 | **Spec / property reveal** | s3 WARM TONE/MEDIUM-DEEP (`:676`), NVIDIA specs swapped per word (`scenes.tsx:109-128`) | One big chip per property, swapped on the spoken word. Flat. |
| A9 | **Custom SVG "signature" diagram** | Guide-prescribed (`SCENE_SNIPPETS.md:1001`), neural-net/GPS/quantum videos | Hand-coded thin-stroke `<circle>/<line>/<path>` with `stroke-dashoffset` draw-in. The flattest possible illustration. |
| A10 | **Full-bleed B-roll + type overlay** | s2/s4/s6/s9 (`AIStylistMain_v1`), all NVIDIA `BgVideo` scenes (`scenes.tsx:17-29`) | Generated/stock video or still, dark scrim, Ken Burns, text. **This is the archetype that already looks good** — depth comes from the asset. |
| A11 | **Talking head + floating accent** | base track in both files; MiniImpact/floating symbols (`SCENE_SNIPPETS.md:981`) | Keyed WebM + a floating chip/word, manually dodged to avoid the face. |
| A12 | **3D hero object / arena** | NVIDIA specs Chip3D, AI-flex ParticleCore, chip-war Logo3DCard (`scenes.tsx`) | three.js objects. Real depth — but bespoke per video and heavy. |
| A13 | **Map / journey** | GPS/GoogleMaps explainers (`src/components/google-maps/`, `GPSExplainedMain_*`) | Hand-built SVG routes/pins. (Same flat-SVG debt as A9.) |
| A14 | **Terminal / chat mockup / pipeline** | `MCPExplained` (AGENT_GUIDE.md:237), pipeline/orbit | Hand-built monospace `<div>` UI mockups. |

**Pattern:** A10 and A12 carry the visual quality; A1–A9, A13, A14 are the flat CSS/SVG-rectangle archetypes. The
redesign should push those archetypes from "CSS primitive" to "generated asset + thin animated overlay."

---

## 3. REUSABLE GENERATED-ASSET TAXONOMY

Goal: replace hand-coded flat primitives with art-directed generated assets, while keeping HyperFrames responsible for
timing, captions, and per-word reveals. Folder convention extends the existing `public/<slug>/` (per-video) +
`public/common/` (shared) split. Proposed shared root: **`public/common/gen/<category>/`**; per-video:
**`public/<slug>/gen/<category>/`**. Naming: `<category>_<concept>_<variant>_<WxH-or-ratio>.<ext>` (e.g.
`bg_mesh-charcoal-amber_01_1080x1920.png`, `icon_cpu_line_512.svg`, `cutout_sneaker_3q_2048.png`).

Each category below: what it's for → which archetypes it upgrades → folder → shared vs per-video → recommended model.

### T1 — `textured-background` (backplates)
- **For:** killing the navy void (D1, D5, D11, D12). Gradient-mesh / grain / bokeh-depth / abstract-tech plates that
  sit under everything, replacing flat `#0D1117`. Provide a matching darker "scrim variant" so type stays legible.
- **Upgrades:** A1, A2, A3, A5, A7, A8, A9 (any "graphic on void" scene). Makes glass (D12) actually refract.
- **Folder:** shared palettes in `public/common/gen/backgrounds/` (e.g. `bg_mesh-darktech-amber_*`), per-video tints
  in `public/<slug>/gen/backgrounds/`.
- **Shared vs per-video:** **Shared-first** (a set of 6–10 reusable plates per aesthetic), per-video override only when
  the topic needs a specific motif.
- **Model:** gpt-image / nano-banana for raster mesh+grain plates; ambient-loop variant via wan-2.2/Veo (see T7).

### T2 — `svg-icon` (designed icon set)
- **For:** replacing glyph/emoji "icons" (D6) and `✓/✕/⚠/◉/☀` strings with a consistent, weighted, on-brand icon
  system. Two-tone or duotone line icons with a uniform stroke and grid.
- **Upgrades:** A5 (list bullets/status), A7 (rail panel icons), A2 (unit/metric marks), A8 (property tags).
- **Folder:** `public/common/gen/icons/` (shared system, the default), `public/<slug>/gen/icons/` for topic-specific
  marks (e.g. a fingerprint sensor).
- **Shared vs per-video:** **Shared system** (the whole point is consistency), per-video extensions allowed.
- **Model:** **Recraft SVG** (vector, recolorable, crisp at any scale) — ideal because output is real SVG the existing
  components can tint with the accent tokens.

### T3 — `svg-logo` (normalized brand marks)
- **For:** fixing ad-hoc logo sourcing (D9). A curated, padding-normalized, on-dark/on-light variant set with
  consistent optical sizing, used by `LogoTile` and the 3D logo cards.
- **Upgrades:** A6 (logo grid), A11/A1 ("companies like X").
- **Folder:** `public/common/gen/logos/<brand>/` (shared — logos recur across videos).
- **Shared vs per-video:** **Shared** (Google/OpenAI/Apple/Intel/AMD/NVIDIA etc. appear repeatedly).
- **Model:** Recraft SVG vectorization / cleanup; manual curation. Store both `_on-dark` and `_on-light` variants.

### T4 — `hero-illustration` (signature-scene art)
- **For:** replacing the flat hand-coded `stroke-dashoffset` SVG diagrams (D8, A9, A13) with rich, depth-laden
  illustrations of the topic (a cross-section, a stylized device, a conceptual scene). Can be layered (fg/mg/bg PNGs)
  for parallax to add the missing midground (D5).
- **Upgrades:** A9 (signature diagram), A13 (map/journey art), A1 (hero hook art).
- **Folder:** `public/<slug>/gen/hero/` (these are topic-specific).
- **Shared vs per-video:** **Per-video** (bespoke to the story), but render in a shared style preset so videos still
  feel like one channel.
- **Model:** gpt-image / nano-banana (raster, photoreal or rich-illustration); Recraft SVG when a clean editorial
  vector diagram is wanted and you need to recolor/animate paths.

### T5 — `object-cutout` (transparent foreground objects)
- **For:** giving scenes a real foreground subject instead of a colored chip (D2, D5). Product shots, props, devices —
  alpha PNGs that drop onto a T1 backplate with a real contact shadow (T6).
- **Upgrades:** A2 (stat + the thing it's about), A5/A8 (a property shown as an object), A10/A11 (collage foreground).
- **Folder:** `public/common/gen/cutouts/` for recurring objects, `public/<slug>/gen/cutouts/` for topic objects.
- **Shared vs per-video:** **Mixed** — common props shared, topic props per-video.
- **Model:** nano-banana/gpt-image generation → `rembg` cutout (already the documented pipeline). Generate at 2k+,
  multiple angles (`_front`, `_3q`).

### T6 — `decorative-accent` (depth & material furniture)
- **For:** fixing weak shadows and flat fills (D2, D3, D11). A kit of reusable PNG/SVG accents: layered contact+ambient
  shadow plates to slide under cutouts/cards, light-leak/glow sprites, grain overlays, sticker/tape/paper edges,
  divider/HUD chrome, particle puffs. These give the "designed object" feel the CSS rectangles lack.
- **Upgrades:** A3 (real bar chrome), A4 (a designed divider instead of a `<div>` line), A6 (tile depth), all chip
  scenes (real shadows).
- **Folder:** `public/common/gen/accents/` (shared kit).
- **Shared vs per-video:** **Shared** (this is reusable furniture).
- **Model:** Recraft SVG for chrome/dividers/sticker edges; gpt-image for raster light-leaks/grain/shadow plates.

### T7 — `ambient-loop` (moving backplates & texture)
- **For:** turning the static void into living depth (D1) and giving glass something to refract (D12). Seamless looping
  abstract-tech motion plates, particle fields, slow gradient drifts — the moving counterpart to T1. The repo already
  leans on this for the scenes that look good (A10) and has a few in `public/common/backgrounds/`.
- **Upgrades:** A1 (hook bg), A7/A8 (rail/spec backplate), A4 (split-panel motion), any scene currently on `#000`.
- **Folder:** `public/common/gen/loops/` (shared), `public/<slug>/gen/loops/` for topic motion.
- **Shared vs per-video:** **Shared-first**, per-video for topic.
- **Model:** wan-2.2 / Veo 3.1 (already wired in `tools/`). Always provide a scrim/darkened variant for legibility.

### T8 — `data-frame` (instrument / chart chrome) — optional but high-leverage
- **For:** stat/score/comparison scenes (A2, A3, A4, A8) that today are bare pills/bars. A reusable set of designed
  frames: gauge faces, labeled meters, HUD readout panels, comparison brackets — generated as SVG so the composition animates
  the value but the *chrome* is art-directed, not a rounded `<div>`.
- **Upgrades:** A2, A3, A4, A7, A8.
- **Folder:** `public/common/gen/frames/` (shared).
- **Shared vs per-video:** **Shared.**
- **Model:** Recraft SVG (must stay vector so values/needles animate cleanly).

### Taxonomy at a glance

| Category | Fixes (debt) | Upgrades (archetypes) | Scope | Folder | Model |
|---|---|---|---|---|---|
| T1 textured-background | D1,D5,D11,D12 | A1,A2,A3,A5,A7,A8,A9 | shared-first | `common/gen/backgrounds/` | gpt-image / nano-banana |
| T2 svg-icon | D6 | A5,A7,A2,A8 | shared system | `common/gen/icons/` | Recraft SVG |
| T3 svg-logo | D9 | A6,A11,A1 | shared | `common/gen/logos/` | Recraft SVG |
| T4 hero-illustration | D8 | A9,A13,A1 | per-video | `<slug>/gen/hero/` | gpt-image / nano-banana / Recraft |
| T5 object-cutout | D2,D5 | A2,A5,A8,A10,A11 | mixed | `…/gen/cutouts/` | nano-banana + rembg |
| T6 decorative-accent | D2,D3,D11 | A3,A4,A6 + all chips | shared | `common/gen/accents/` | Recraft + gpt-image |
| T7 ambient-loop | D1,D12 | A1,A4,A7,A8 + voids | shared-first | `common/gen/loops/` | wan-2.2 / Veo |
| T8 data-frame | D2,D3 | A2,A3,A4,A7,A8 | shared | `common/gen/frames/` | Recraft SVG |

### Cross-cutting recommendations (beyond per-asset)
1. **Add real design tokens** alongside `theme.ts`: spacing scale, type scale, radius scale, and a layered-shadow
   token set. Most debt (D3,D4) is the absence of these. Generated assets won't fix an eyeballed `paddingTop: 380`.
2. **Introduce a layout grid** (column + baseline) that scenes anchor to, so single-element scenes sit on a rhythm and
   the manual head-dodging / caption-padding hacks (D7) can be derived instead of hand-tuned.
3. **Keep the winners:** A10 (full-bleed generated media) and A12 (3D) already deliver depth — the taxonomy mostly
   exports *that* quality into the flat archetypes via T1/T4/T5/T7.
4. **Style-preset every generator call** (one prompt prefix per aesthetic, like `style_prefix` in scenes.json) so
   shared assets stay channel-consistent across videos — countering the templated sameness (D10) without going flat.
