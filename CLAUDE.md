# HyperFrames Composition Project

## Skills — USE THESE FIRST

**Always invoke the relevant skill before writing or modifying compositions.** Skills encode framework-specific patterns (e.g., `window.__timelines` registration, `data-*` attribute semantics, shader-compatible CSS rules) that are NOT in generic web docs. Skipping them produces broken compositions.

| Skill                      | Command                   | When to use                                                                                       |
| -------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------- |
| **hyperframes**            | `/hyperframes`            | Creating or editing HTML compositions, captions, TTS, audio-reactive animation, marker highlights |
| **hyperframes-cli**        | `/hyperframes-cli`        | Dev-loop CLI: init, lint, inspect, preview, render, doctor                                        |
| **hyperframes-media**      | `/hyperframes-media`      | Asset preprocessing: tts (Kokoro), transcribe (Whisper), remove-background (u2net)                |
| **hyperframes-registry**   | `/hyperframes-registry`   | Installing blocks and components via `hyperframes add`                                            |
| **website-to-hyperframes** | `/website-to-hyperframes` | Capturing a URL and turning it into a video — full website-to-video pipeline                      |
| **tailwind**               | `/tailwind`               | Tailwind v4 browser-runtime styles for projects created with `hyperframes init --tailwind`        |
| **gsap**                   | `/gsap`                   | GSAP animations for HyperFrames — tweens, timelines, easing, performance                          |
| **animejs**                | `/animejs`                | Anime.js animations registered on `window.__hfAnime`                                              |
| **css-animations**         | `/css-animations`         | CSS keyframes that HyperFrames can pause and seek                                                 |
| **lottie**                 | `/lottie`                 | `lottie-web` and dotLottie players registered on `window.__hfLottie`                              |
| **three**                  | `/three`                  | Three.js scenes rendered from HyperFrames `hf-seek` events                                        |
| **waapi**                  | `/waapi`                  | Web Animations API motion driven through `document.getAnimations()`                               |

> **Skills not available?** Ask the user to run `npx hyperframes skills` and restart their
> agent session, or install manually: `npx skills add heygen-com/hyperframes`.

## Commands

```bash
npm run dev          # start the preview server (long-running — keep it alive in background)
npm run check        # lint + validate + inspect
npm run render       # render to MP4
npm run publish      # publish and get a shareable link
npx hyperframes lint --verbose  # include info-level findings
npx hyperframes lint --json     # machine-readable output for CI
npx hyperframes docs <topic> # reference docs in terminal
```

> **`npm run dev` is a long-running server, not a one-shot command.** It blocks until stopped.
> In Claude Code, always run it with `run_in_background: true`. Never run it as a foreground
> command — it will time out and the server will die, breaking the browser preview.

## Documentation

**For quick reference**, use the local CLI docs command (no network required):

```bash
npx hyperframes docs <topic>
```

Topics: `data-attributes`, `gsap`, `compositions`, `rendering`, `examples`, `troubleshooting`

**For full documentation**, discover pages via the machine-readable index — do NOT guess URLs:

```
https://hyperframes.heygen.com/llms.txt
```

## Project Structure

- `index.html` — main composition (root timeline)
- `compositions/` — sub-compositions referenced via `data-composition-src`
- `meta.json` — project metadata (id, name)
- `transcript.json` — whisper word-level transcript (if generated)
- `docs/guides/` — production guides (see below) · `docs/motion-ref/` — motion-design memory
- `editing-styles/` — named editorial styles · `tools/` — Python asset/audio/caption/stock pipelines
- `raw/` — source footage to edit

## Style Library — CHECK BEFORE EDITING (mandatory)

**Before starting ANY video edit, skim `styles/INDEX.md` and open the relevant style files.**
It holds proven, MEASURED looks (palettes, layouts, animations, transitions, subtitles) decoded
from real references and our own delivered shorts. Reuse the specs; never re-invent a solved look
and never clone a frame-for-frame — each edit must still be visually UNIQUE.
- **Full styles** (`styles/full/`): complete video breakdowns, scene-by-scene, linking elements.
- **Element styles** (`styles/elements/`): reusable pieces by category — `transitions/`,
  `animations/`, `subtitles/`, `palettes/`. Mix & match.
- Added something new (a transition, animation, palette, etc.)? Save it back into the right
  `styles/` file and add a row to `styles/INDEX.md`. Keep MEASURED values (hex, px, timing, easing).

## Production Workspace & Guides

This project doubles as a short-form (9:16) video-production workspace, migrated from a prior Remotion setup. Editorial/workflow guidance (complementary to the framework skills above):

- `docs/guides/AGENT_GUIDE.md` — editor mindset, pacing/energy model, visual hierarchy. **Start here for any editing task.**
- `docs/guides/MOTION_LIBRARY.md` — **PRIMARY JOB**: THE master index of every premade motion asset — the COMPLETE HyperFrames registry (all 113 blocks/components installed in `compositions/`), CodePen-derived components, GSAP demo techniques, Noto Lotties, overlays. The Director cites pieces per beat in the BRIEF; Bella executes them THEMED (accent CSS vars, LIGHT palette, timed to the word — never demo styling). Read it before designing or building any beat.
- `docs/guides/HUMAN_EDIT_GUIDE.md` — **mandatory**: human-feel rules (motion on everything, avatar punch-ins, CSS-beat limits, texture) + AI-asset recipes (`tools/ai_assets/replicate_gen.py` — Nano Banana 2 + Wan i2v).
- `docs/guides/QUICK_COMPOSITION_GUIDE.md` — composition structure + component tiers.
- `docs/guides/SCENE_SNIPPETS.md` — copy-paste HyperFrames scene patterns (HTML+GSAP).
- `docs/guides/COMPONENT_CATALOG.md` — reusable component patterns + registry mappings.
- `docs/guides/BROLL_GUIDE.md`, `COMMON_ASSETS.md`, `CHROMAKEY_TRANSPARENT_VIDEO.md` (green-screen → `hyperframes remove-background`), `RENDER_FIX.md`, `STIMULUS_VIDEO_COMPLETE.md`.
- `.agents/skills/video-production-rules/` — general editorial rules (captions, transitions, audio, timing, pacing) for HyperFrames.

**Authority order (important):** HyperFrames' own house-style and the `/hyperframes` skill are **authoritative**. `docs/legacy-preferences.md` holds editorial preferences migrated from the old Remotion project and is **INACTIVE by default** — do not apply them as defaults until the user explicitly says to activate them. Dark-theme / dark-tech / neon styling has been intentionally removed from this workspace — do not reintroduce it.

## Linting — ALWAYS RUN AFTER CHANGES

After creating or editing any `.html` composition, **always** run the full check before considering the task complete:

```bash
npm run check
```

Fix all errors before presenting the result. Inspect warnings should be reviewed before rendering.

## Key Rules

1. Every timed element needs `data-start`, `data-duration`, and `data-track-index`
2. Elements with timing **MUST** have `class="clip"` — the framework uses this for visibility control
3. Timelines must be paused and registered on `window.__timelines`:
   ```js
   window.__timelines = window.__timelines || {};
   window.__timelines["composition-id"] = gsap.timeline({ paused: true });
   ```
4. Videos use `muted` with a separate `<audio>` element for the audio track
5. Sub-compositions use `data-composition-src="compositions/file.html"` to reference other HTML files
6. Only deterministic logic — no `Date.now()`, no `Math.random()`, no network fetches

## Pull request workflow

All changes go through a pull request: create a branch, open a PR, never push directly to the default branch.
