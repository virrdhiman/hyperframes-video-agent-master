# Legacy Editorial Preferences (migrated)

> ⚠️ **MIGRATED FROM THE REMOTION PROJECT — INACTIVE BY DEFAULT.** These are the user's prior editorial preferences. HyperFrames' own house-style and the `/hyperframes` skill remain authoritative. Do NOT apply these as defaults until the user explicitly says to activate them.

This is a reference archive of the editorial/house-style preferences carried over from the previous Remotion video workspace (`CLAUDE.md` and editor rule files). Techniques have been translated from Remotion (frames / `interpolate` / `spring`) to GSAP / HyperFrames (seconds / timeline tweens / eases). Dark-theme / neon / dark-tech material has been dropped — this is a light/neutral project.

---

## Visual aesthetic — prior defaults

- **Bouncy, settling motion.** Remotion springs at `damping: 12–14` → GSAP overshoot eases such as `back.out(1.7)` (snappy land) or `elastic.out(1, 0.5)` (looser bounce). Not robotic linear motion. (HyperFrames already asks for ≥3 different eases per scene.)
- **Imperfect alignment.** Chips/cards rotate `-3deg` to `3deg`. Perfectly upright = lazy template.
- **Thick directional drop shadows.** `box-shadow: 4px 4px 0 <color>` over soft blur. *Caution:* hard offset shadows and large flat fills can show H.264 banding on render — keep grounds non-flat (radial/solid+glow rather than a full-screen linear gradient on a dark bg) and test a render before committing to a heavy shadow style.
- **Continuous imperfect motion.** Elements needn't freeze after entering — add a subtle finite `yoyo` float on `y` and a slight rotational wobble. Keep repeats finite (`Math.ceil(duration/cycle)-1`), never `repeat: -1`.
- **Media hierarchy (try in this order):** real footage > talking head > split screen > editorial list > custom SVG > brand cards. **Brand cards (HeadlineCard / ChecklistCard equivalents) max 2 per video.**
- **NO glassmorphism.** (This is the user's prior rule — kept as-is.) Build on warm white / light grey / beige grounds with bright accents.
- **Letter-spacing 2–6** on every uppercase line, even small amounts. Pair heavy weight + tracking so type reads as "designed."

## Asset generation rules (prior)

- **No text/labels/numbers baked into generated images** — typography is added by the compositing layer (HyperFrames HTML + CSS). End every line-art image prompt with "White background."
- **Video prompts (wan-2.2):** always preface with the line-art style instruction; never use "cinematic" or "warm" (triggers photorealism).
- `characters: []` in scenes.json = text-only nano-banana run (no ref image).
- **Audio:** split scripts on `[PAUSE]` markers, generate per-segment, **always re-encode when stitching** (`-c:a libmp3lame`, never `-c copy`).
- **Background removal:** use `rembg`, never PIL flood-fill.
- **Cost-check before generating:** dry-run the scenes config to preview prompts + estimated cost.

## SFX / music levels (prior)

- VO: full volume (1.0).
- Music: `0.12` during narration, `0.45` in pause windows, ~0.3s ramp.
- Whooshes 0.7 / impacts 0.55–0.6 / ambient 0.45 / page-turns 0.5.
- Anything below 0.25 is inaudible when mixed.
- (HyperFrames note: audio is always a separate `<audio data-volume>` element; bound each SFX with its own `data-start`/`data-duration` so a clip doesn't play to its full source length.)

## Pacing (prior)

- Change the visual every **2–5s**; hooks faster (2–3s), context scenes breathe more.
- **Never run 3+ same-energy scenes in a row.**
- Hard cuts are the house style — no slow crossfades or decorative wipes/zooms between scenes. (In HyperFrames, a "hard cut" is a 1–2 frame flash transition, since multi-scene comps still require a transition between scenes; the transition is the exit.)

## Render guardrails (prior)

- Keep render concurrency modest (the old rule was `--concurrency=4`; check memory headroom before going higher). HyperFrames equivalent: `--workers` (1–8/auto).
- Bound every SFX/audio clip to its intended window so it doesn't bleed to the full source length.
- For chromakey'd talking heads, composite a **pre-keyed alpha** clip (transparent WebM) rather than chromakeying at render time. In HyperFrames, video must be `muted playsinline`, and you never animate its dimensions (wrap it and animate the wrapper).

## Things to avoid (prior)

- ❌ Editing the shared asset-generation tool for project-specific behavior — put it in `scenes.json`.
- ❌ Reinventing a component/scene pattern that already exists — check the catalog/snippets first.
- ❌ Adding images/video from external CDNs — fetch to local `assets/` first (external URLs break deterministic render).
- ❌ Committing render output, raw footage, temp, or `node_modules`.
- ❌ Mocking the database/network/filesystem in tests when an integration test would catch the same bug.
- ❌ "Fancy transitions" (crossfades, slides between scenes) — prior house style is hard cuts.
