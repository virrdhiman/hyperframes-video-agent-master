# AGENTS.md — Start Here

You are an AI agent working in a **HyperFrames** video repository: HTML + GSAP rendered
frame-by-frame to deterministic MP4. This file is your entry point. Read it first, then index
the repo using the map below before taking any action.

## FIRST RUN — onboard the user (do this before anything else)

If this is a fresh clone and you have not yet greeted the user this session, run this short
onboarding **before** touching any files:

1. **Welcome them warmly** and introduce the repo in one line:
   *"Welcome to the HyperFrames Video Agent — a system that turns a topic into a finished,
   word-synced 9:16 short. I'll get you set up in under a minute."*
2. **Ask their name** and what they want to make first ("What should I call you? And what's the
   first video you'd like to build?"). Use their name from then on.
3. **Explain the API keys.** The repo reads fine with zero keys, but to actually *run* the
   pipelines they'll need a few free/paid API keys in `tools/.env` (copy from `.env.example`).
   Walk them through it in tiers — don't dump all of them at once:
   - **Core (start here):** `SERPER_API_KEY` (serper.dev — topic research + b-roll search),
     `PEXELS_API_KEY` (pexels.com — free stock video/photo), `PIXABAY_API_KEY` (pixabay.com),
     `FREESOUND_API_KEY` (freesound.org — SFX). These get the basic stock-driven pipeline running.
   - **Voice/captions (optional):** `ELEVENLABS_API_KEY` (elevenlabs.io) for premium TTS +
     transcription — **skippable**, since HyperFrames ships a *local* Kokoro TTS + Whisper.
   - **AI asset generation (optional):** `REPLICATE_API_TOKEN` (replicate.com — image/video +
     thumbnails), `FAL_KEY` (fal.ai), `GOOGLE_API_KEY` (Google AI — Veo video / Imagen image).
     Only needed if they want AI-generated visuals instead of stock.
   - **Publishing (optional):** `PUBLER_API_KEY` + `PUBLER_WORKSPACE_ID` (publer.com) for auto-posting.
4. **Show them the two setup commands** and offer to help fill the keys:
   ```bash
   cp .env.example tools/.env && ln -sf tools/.env .env   # create your key file
   npx hyperframes doctor                                  # verify Node 22+ / FFmpeg / Chrome
   ```
   Tell them: *"Paste any keys you have and I'll drop them in; leave the rest blank — the
   pipeline degrades gracefully and only uses what's configured."*
5. Once they're set, point them at the **dev loop** below and ask what to build first.

Keep onboarding friendly and brief. Never ask for a key in plain chat if you can have them paste
it into `tools/.env` directly, and never commit `tools/.env` (it is gitignored).

## Read order (do this before editing)

1. **`CLAUDE.md`** — the technical contract: the timeline model, `data-*` attribute semantics,
   the skills you must invoke, and the hard rules. **Authoritative on anything technical.**
2. **`docs/guides/AGENT_GUIDE.md`** — the editorial master guide (editor mindset, pacing,
   visual hierarchy). Editorial guidance, not a technical override.
3. **`docs/guides/README.md`** — index of every workflow + reference guide.
4. **`styles/INDEX.md`** — the style library: proven, measured looks (palettes, layouts,
   animations, transitions, captions). Skim before designing any beat; reuse, never re-invent.

## Use the skills first

This repo ships HyperFrames skills (vendored in `.agents/skills/`). **Always invoke the
relevant skill before writing or modifying a composition** — they encode framework patterns
(`window.__timelines` registration, `data-*` semantics, seek-safe CSS) that generic web docs
lack. See the skills table in `CLAUDE.md`. If skills are unavailable, run
`npx hyperframes skills` (or `npx skills add heygen-com/hyperframes`) and restart the session.

## Repository map (for indexing)

| Path | What it is |
|------|-----------|
| `index.html` | Main composition — the root timeline (`data-composition-id`) |
| `compositions/` | Sub-compositions referenced via `data-composition-src`; the installed registry blocks/components live here |
| `lib/` | Framework runtime + shared helpers |
| `build_composition.py` | Assembles a composition from project config + transcript |
| `styles/` | Style library — `full/` (whole-video breakdowns) + `elements/` (transitions, animations, subtitles, palettes). Index: `styles/INDEX.md` |
| `editing-styles/` | Named editorial styles |
| `docs/guides/` | Workflow + reference guides (start with `AGENT_GUIDE.md`) |
| `docs/reference/`, `docs/research/` | Avatar looks, blueprints, background research |
| `tools/` | Python pipelines — stock fetch, transcription, TTS, asset/thumbnail generation, publishing |
| `meta.json` | Project metadata (id, name) |
| `transcript.json` | Word-level Whisper transcript (drives word-synced graphics) |
| `hyperframes.json` | Installed registry blocks/components manifest |
| `.env.example` | Template — copy to `tools/.env` and fill real keys (nothing secret is committed) |

Note: media, renders, and secrets are **gitignored** — they are fetched/generated per video and
are intentionally absent from this public repo.

## The dev loop

```bash
npx hyperframes doctor                       # verify Node 22+ / FFmpeg / Chrome
npx hyperframes preview                      # long-running Studio server on :3002 (run in background)
npm run check                                # lint + validate + inspect — run before every render
npx hyperframes render -c index.html -o out/video.mp4
```

## Hard rules (see `CLAUDE.md` for the full list)

1. Every timed element needs `data-start`, `data-duration`, `data-track-index`, and `class="clip"`.
2. Timelines are **paused** and registered on `window.__timelines["<composition-id>"]`.
3. Deterministic logic only — no `Date.now()`, no `Math.random()`, no network fetches at render.
4. All media lives under the project root (`assets/...`), referenced by relative path — external
   CDN URLs break renders.
5. Run `npm run check` and fix all errors before considering any change complete.

## Pull request workflow

All changes go through a pull request: create a branch, open a PR, never push directly to the default branch.
