# OpenAIBedrockMain_v3 — treatment blueprint (the reference build of THIS video)

> ⛔ **SUPERSEDED / HISTORICAL — DARK build. Do NOT use as a style/palette reference.**
> This documents the old `OpenAIBedrockMain_v3` *dark cinematic* treatment. The Retrofit AI
> feed is now **LIGHT + warm + physical/editorial** (see `docs/guides/CREATIVE_SPEC.md` —
> "DIRECTION RESOLVED: LIGHT wins"). Read this ONLY for structural ideas (broadcast band,
> alternating avatar modes, motivated cuts) — never for palette. Its "kinetic pill default"
> caption note is also superseded by the word-by-word **appear+rise** default.

The prior Remotion build of this exact "OpenAI on AWS Bedrock vs Azure" video, in the
**SIGNAL** design language. This is the closest reference to what the user wants. Capture
the *treatment* (dark cinematic, hero images, broadcast band, alternating avatar modes,
fast motivated cuts) and rebuild it in HyperFrames. Same VO/timing as the current
`transcript.json`. Source: `/Users/face/Movies/my-video/src/components/openai-bedrock-v3/`.

## Look & feel
- **DARK cinematic.** Near-black base (`ink` / `inkDeep`), built from **generated assets**
  composed in depth planes with grain — "never flat divs on a void."
- **ONE accent = coral** (`SIGNAL.coral`), plus `cobalt` and AWS orange as secondary.
- Per-beat **tone temperature** carries the story: `cold` (cobalt) → `ember` (coral/warm) →
  `grid` (dark `#241D14`) → `steel` (`#2A2F38`). cold gated-past → warm freedom → cool tension → warm payoff.
- Grain (~0.06) + vignette (~0.6) + a tone-grade soft-light layer (~0.16) on top.

## Layout geometry (1080×1920)
- `STAGE` = the hero/graphic stage: `top:150, bottom:1130, left:70, right:70, cx:540`.
- `SEAM_Y = 1150` — a hard **coral seam line** (4px, glowing) between the hero stage and the
  avatar band, with a 70px ink scrim below it to blend the crop.
- `AVATAR_BAND` = `{ top:1150, h:770 }` — the speaker lives here in "broadcast" beats.
- Corner-avatar PiP (CTA): ~300×400 bottom-right, coral border.

## Avatar modes (alternate them — never hide the face >~5s)
`full` = full-bleed reaction (graded) · `broadcast` = hero stage on top + avatar cropped into
the lower band behind the coral seam (crop the full-frame video UP via translateY so the face
lands in the band) · `hidden` = full cutaway to hero/graphics (pure data/proof beats) ·
`corner` = PiP over an ambient loop (CTA).

## Generated assets per beat
- Backgrounds: `bg_cold.png`, `bg_ember.png`, `bg_grid.png` (flux).
- Cinematic heroes: `hero_street.png`, `hero_multicloud.png`.
- Ambient loop: `loop_embers.mp4`.
- Recraft icons (SVG): chip, cloud, lock, dollar, code, dev.
- Logos: openai, microsoft, amazon.
(In HyperFrames: fetch real footage first per the b-roll order; generate hero stills via
`tools/image_generator` (nano-banana/Replicate) → animate with Ken Burns or wan-2.2.)

## Beat treatment timeline (16 beats, synced to the locked VO; `until` = raw second)
| until | scene | avatar | tone | caption |
|------:|-------|--------|------|---------|
| 4.60  | hookOld     | full      | cold  | kinetic |
| 6.36  | hookFlip    | full      | ember | kinetic |
| 11.00 | models      | broadcast | grid  | kinetic |
| 15.00 | bedrock     | broadcast | grid  | kinetic |
| 19.30 | vsAzure     | broadcast | cold  | kinetic |
| 20.30 | thinkPause  | full      | ember | kinetic |
| 25.20 | money       | hidden    | ember | kinetic |
| 28.60 | street      | hidden    | ember | kinetic |
| 30.10 | devPause    | full      | grid  | kinetic |
| 35.20 | plugIn      | broadcast | grid  | kinetic |
| 40.86 | benefits    | broadcast | grid  | kinetic |
| 42.90 | codexPause  | full      | ember | kinetic |
| 47.84 | codexStat   | hidden    | grid  | kinetic |
| 48.90 | realStory   | full      | ember | editorial |
| 56.14 | multicloud  | hidden    | ember | editorial |
| 999   | cta         | corner    | ember | kinetic |

Deliberately **alternates full-bleed reaction beats with hero/broadcast graphic beats** — that
rhythm is the "fast cut" feel. Captions: kinetic pill default, editorial (calmer line) for the
closing realStory/multicloud beats.

## How this maps to the current HyperFrames build
The current `build_composition.py` already does the face-clear principle via PUSH-DOWN (springs
the talking head down so graphics use the headspace) — that's the light-mode cousin of the
"broadcast band + coral seam." To match v3: go dark cinematic, add per-beat hero images/b-roll,
formalize the broadcast band (hero top / avatar band / seam), alternate avatar modes, and tighten
cuts. See [CREATIVE_SPEC](../guides/CREATIVE_SPEC.md) and [SPLITSCREEN_GUIDE](../guides/SPLITSCREEN_GUIDE.md).
