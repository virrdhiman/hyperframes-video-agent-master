# Reimagining the Editing System — Master Plan

**Goal:** stop shipping "another programmatic video." Move from hand-coded flat SVG-on-navy-void to a system where (a) the editor composes from real, depth-rich generated assets, (b) a fresh house design language is enforced by construction + lint, and (c) pacing/caption/meme craft is codified. Synthesized from 5 research passes (Replicate model matrix, internal design audit, pipeline architecture, YouTube motion-design + short-form editing). Artifacts in this folder.

**Locked direction (user):** Fresh house design language · Hybrid asset model (shared library + per-video heroes) · $2–6 generation/video · Memes sparingly.

---

## 1. Diagnosis — why it currently looks cheap (one sentence)

A shape only looks expensive once it lives in a *world*. Today every "graphic" scene is a flat single-color `<div>` (tilt + one drop-shadow + spring) floating on a flat `#0D1117` void — no depth planes, no grain, no texture, no temperature, no grid, one centered element. The scenes that already look good are the *asset-backed* ones (full-bleed AI images, 3D). So the cheapness is specific and fixable: **port asset density + depth into the flat archetypes, and never render a flat fill again.**

The two reference grids that prove it: `grids/lighting_overview.jpg` (flat orange shape on black → integrated into a real plate) and `grids/dune_poster_compare.jpg` (cold teal floating-heads = cheap; warm gradient + single silhouette + depth = expensive).

---

## 2. The fresh house design language — "SIGNAL"

A new system, distinctive, premium, achievable in HyperFrames, and consistent across every video so the channel reads as one brand.

### 2.1 Foundation — every frame, no exceptions
Every scene is built from **≥3 depth planes + grain**, never a flat fill:
1. **Background plane** — a 2–3-stop gradient *keyed to scene temperature* (see palette), generated (flux-1.1-pro) or CSS-gradient, with a faint mesh/texture. Never one flat color.
2. **Mid plane** — the shape/asset system (cards, cutouts, icons) with real contact + ambient shadows, slight blur on anything not in focus.
3. **Foreground plane** — the single hero focal element at full saturation/contrast.
4. **Grain overlay** — ~4% animated film grain over the *entire* comp (the #1 single fix: it's the sensor-noise tell that makes flat fills read as pasted stickers).
Plus a global **gate-weave** (`wiggle ~12f, 3px`) on the comp and an independent one on the hero — kills the dead-static digital feel.

### 2.2 Palette — temperature as meaning (this is the one creative call I want your sign-off on)
Move off teal/orange. Proposed **SIGNAL** palette:
- **Base ink:** warm near-black `#16120E` (not cold navy) → gradients, never flat.
- **Paper:** warm bone `#EDE6D6` for light/editorial scenes (we alternate dark↔light scenes for rhythm).
- **Hero accent — "Signal":** electric coral-red `#FF4A2E` (used for the single most important thing on screen, sparingly).
- **Cool tension:** cobalt `#2B59FF` (used *against* coral to create tension on comparison/conflict beats — temperature = story, warm = payoff, cool = problem).
- **Metal:** soft chrome/`#C9CBD1` gradient for premium accents and data chrome.
3-tier contrast hierarchy is mandatory: **hero 100% saturation+contrast, support ~60%, background ~30%.** The eye goes to highest contrast first — build it on purpose.

### 2.3 Type system (fresh, editorial)
- **Display / caption pops:** a heavy grotesk — Archivo Black / Inter Tight Black (uppercase, letter-spacing 2–6).
- **Editorial insight moments:** a high-contrast serif — Fraunces — for "the real story" quote beats (gives an editorial, non-template feel).
- **Data / mono:** JetBrains Mono.
- One type scale (e.g. 1.25 ratio) that *doubles as a lint threshold* — no off-scale sizes.

### 2.4 Grid & space
6×8 safe grid with fixed margins (reuse the safe-zone pixels already in `still_grid.py` so spec, grid component, and QA rubric share one source of truth). **Negative space frames a focal point — it is never an empty void.** Tight micro-spacing within a group, generous macro-spacing between groups.

### 2.5 Motion language
Spring-based, house default `damping 12–14`; slow-in/slow-out + overshoot + a **reaction beat** (pop/dust/shake) on every impact; **posterize accent motion to ~12fps** for a handmade feel (reserve buttery 30fps for camera moves); one focal element moving at a time (equal-energy motion everywhere = visual white noise).

### 2.6 A repeated shape *system* (brand glue)
One consistent "plate/card" motif (paper texture, fixed corner radius, fixed tilt range ±3°, contact shadow recipe), one icon family (Recraft `line_circuit`/`line_art` style-locked), one transition grammar (hard cuts + the seam-cut we already use). Repetition of *system* across videos = brand; repetition of *framing within a video* = the boredom we're killing.

---

## 3. The asset system (hybrid: shared library + per-video heroes)

### 3.1 Model starter kit (live-verified IDs, from `replicate-model-matrix.md`)
| Need | Model | Output | ~Cost |
|---|---|---|---|
| Hero vector illustration / logo | `recraft-ai/recraft-v4-svg` | SVG | $0.08 |
| Icons / glyphs / decorative accents (style-locked) | `recraft-ai/recraft-v3-svg` | SVG | $0.08 |
| Textured/grainy backgrounds (kills the void) | `black-forest-labs/flux-1.1-pro` (explore via `flux-schnell` $0.003) | PNG | $0.04 |
| Hero raster art + consistent subjects across scenes | `google/nano-banana-2` | PNG | ~$0.067 |
| Alpha cutouts | `recraft-ai/recraft-remove-background` | PNG | $0.006 |
| Ambient B-roll loops behind text | `bytedance/seedance-1-lite` (fallback `wan-video/wan-2.2-i2v-a14b` for on-brand line-art) | MP4 | ~$0.09/5s |

**~$1.10 generation per ~12-scene video** at full quality (under $0.50 with flux-schnell backgrounds) → comfortably inside $2–6. One-time shared-library generation budget ~$15–30.

### 3.2 Hybrid split
- **Shared library** (`public/common/elements/`): backgrounds, the SIGNAL icon family, accents, textures, chrome — generated once, cached, reused across all videos. This is what makes videos look like one brand and keeps per-video cost near-zero.
- **Per-video heroes** (`public/<slug>/elements/`): 2–4 bespoke hero illustrations / cutouts / loops that carry that specific story.

### 3.3 `scenes.json` element-request schema (additive, backward-compatible)
Each scene declares **capabilities, not model IDs**:
```jsonc
{ "type": "graphic",
  "elements": [
    { "id": "bg",   "type": "background",       "prompt": "warm coral dune gradient, grain, 3 depth planes", "reuse": "shared" },
    { "id": "hero", "type": "hero-illustration", "prompt": "lone silhouette cresting a dune", "style_ref": "signal" },
    { "id": "ico1", "type": "svg-icon",          "prompt": "GPU chip", "style_ref": "signal", "recolor": "#FF4A2E" }
  ] }
```
Plus top-level `style_refs` (named style anchors: prompt suffix + optional ref image + palette) so an icon set stays coherent.

### 3.4 `tools/asset_studio/` (dispatched from `generate_assets.py` as "Phase 0.5: ELEMENTS")
Model registry · capability→model dispatch · prompt-hash cache/dedup (a hit anywhere is free everywhere) · style-ref composition · recolor · manifest per folder · cost preview wired into `scenes_dryrun.py`. Reuses the existing parallel/retry/`--force` machinery — no new concurrency model. **No per-project Python** (honors CLAUDE.md).

### 3.5 HyperFrames consumption — `components/asset-system/`
Good design becomes *structural*: `BackgroundLayer` (has **no** solid-color prop — you physically cannot render a flat fill), `SceneGrid` (6×8, built-in safe margins), `DepthLayer`, `GrainOverlay`, `SvgAsset` (inlines generated SVG so it animates/recolors in TSX), `AssetCard`. Flat/sparse/hand-SVG scenes become awkward to build and then fail the gate.

---

## 4. Editing & pacing layer (codified, from short-form research)

- **Energy field per scene** — hot 0.8–1.5s / mid 2–3.5s / cool 4–6s; never 3 same-energy scenes in a row; frame must visibly change every 2–4s (internal change if a scene runs long).
- **Pattern interrupt at the 50% mark** + every 30–60s — distinct bg + SFX gear-change (midpoint is the 2nd-biggest drop-off).
- **Hook scene** — motion + 4–7 word top-safe text, lands sound-off, snap cut not fade (50–60% of drop-off is the first 3s).
- **Captions** — bold grotesk, word-by-word, highlighted active word, scale-pop-and-hold w/ motion blur, **5-variant reveal library** (scale-pop / scroll / typewriter-mask / 3D-extrude / box jump-out + staggered "echo") so it's not the identical pop every video.
- **Text-layout rule (fixes overlap)** — one text block per safe zone at a time; phrase N fully exits before N+1 enters; center third (face) kept clear.
- **Memes/iconic clips — sparingly** — ~1 per 45–60s max, never back-to-back, on a punchline beat, re-captioned with a comic bubble if used, hard-cut straight back to the through-line. Fetch clip to `public/<slug>/` first.

---

## 5. Teaching mechanism + QA gate (the durable part)

**Prose the editor reads:**
- `DESIGN_LANGUAGE.md` — the SIGNAL spec above; every numeric doubles as a lint threshold.
- `ELEMENT_CATALOG.md` — auto-generated from asset manifests, with copy-paste TSX snippets.
- `SCENE_EXEMPLARS.md` — worked scene JSON + TSX + a passing grid.

**Enforceable gate (not just prose):**
- `tools/asset_studio/design_lint.py` wired into `npm run check`: LINT001 no hand-rolled `<svg>` paths, LINT002 no flat-color background, LINT003 local-asset-path-only, LINT004 element-exists, LINT005 type-scale, LINT006 safe-area.
- `grid_review.py --rubric` (rendered): RUBRIC-FILL ≥40% non-empty · NO-OVERLAP · NOT-FLAT · MOTION · DENSITY-RUN → emits `pass:true/false`.
- **New stop condition in CLAUDE.md:** a render isn't "done" until static lint exits 0 **and** the rubric reports pass. Turns "eyeball the grid" into a self-scoring loop the editor agent must clear. (Also fix the `grid_review.py --scenes` quirk the short-form agent found: it still samples the whole video; isolate a window with `--interval 9999`.)

---

## 6. How one scene gets made (new workflow)

1. Editor writes the beat in `scenes.json` with a `type:"graphic"` scene + `elements[]` (capabilities + prompts + style_ref).
2. `scenes_dryrun.py` previews prompts + cost (cache-aware).
3. `generate_assets.py` Phase 0.5 generates/caches elements → `public/.../elements/` + manifest.
4. Editor composes the scene in TSX using `asset-system` components (BackgroundLayer + SceneGrid + DepthLayer + SvgAsset + GrainOverlay) — flat fills impossible by construction.
5. Render → `grid_review.py --rubric` + `design_lint` → fix until `pass:true`.

---

## 7. Phased rollout

- **P0 — Foundations (no AI assets yet):** design tokens (spacing/type/radius/shadow/grain), `SceneGrid`, `DESIGN_LANGUAGE.md` (SIGNAL), lock palette. *Biggest immediate visual win is here: grain overlay + gradient backgrounds + 3-tier contrast can be retrofitted to existing comps before any model spend.*
- **P1 — asset-system components:** BackgroundLayer/DepthLayer/GrainOverlay/SvgAsset/AssetCard.
- **P2 — asset_studio + `elements[]` schema + model registry + cache + dryrun cost.**
- **P3 — generate the shared SIGNAL library** (backgrounds, icon family, accents) — one-time ~$15–30.
- **P4 — teaching + QA gate** (DESIGN_LANGUAGE/ELEMENT_CATALOG/EXEMPLARS + design_lint + --rubric + CLAUDE.md stop condition).
- **P5 — editing layer** (energy-field helper, 5-variant caption library, pattern-interrupt + meme module).
- **P6 — Pilot:** rebuild the OpenAI→AWS Bedrock short end-to-end as the reference exemplar; iterate to a clean rubric pass; lock it as the template.
- **P7 — Wire into openclaw** (update CLAUDE.md + the editor agent's instructions + the QA stop condition) — closes pending task #6.

---

## 8. Cost summary
Per video ~$1.10 generation (within $2–6). One-time shared library ~$15–30. Plus the build effort for tooling/components above (no recurring cost).

## 9. Open decisions for you
1. **Sign off / tune the SIGNAL palette + type** (§2.2–2.3) — the one creative call before P0.
2. **Build order** — recommend starting P0+P1 now (pure quality win, zero model spend) and demoing a retrofit of one existing scene before committing to P2–P7.
3. **Pilot target** — confirm the OAI→Bedrock short as the pilot rebuild (it's our most-recent reference).
