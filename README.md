# HyperFrames video

A video knowledge base built on **HyperFrames** — HTML + GSAP rendered to deterministic,
frame-by-frame video. A composition is an HTML document whose elements carry `data-*` timing
attributes, animated by a paused GSAP timeline registered on `window.__timelines`. Each frame
is seeked in headless Chrome and encoded with FFmpeg, so the same input renders to identical
output.

## Repository layout

| Path | Purpose |
|------|---------|
| `index.html` | Main composition (root timeline; carries `data-composition-id`) |
| `compositions/` | Sub-compositions referenced via `data-composition-src` |
| `assets/` | Served media — `assets/<topic>/` per video; `assets/common/` for shared SFX/music/backgrounds |
| `raw/` | Source footage not yet cut into `assets/` |
| `docs/guides/` | Workflow + reference guides (start with **AGENT_GUIDE.md**) |
| `tools/` | Pipelines: stock fetcher, transcription, asset generation, etc. |
| `projects/` | Per-video config: `script.txt`, scene briefs, subtitles |

**Docs:** [docs/guides/README.md](docs/guides/README.md) — start with
[docs/guides/AGENT_GUIDE.md](docs/guides/AGENT_GUIDE.md).

## Commands

```bash
# Preview — long-running Studio server on port 3002 (keep it alive in the background)
npx hyperframes preview

# Check — lint + validate + inspect (run before every render)
npm run check

# Render — to MP4
npx hyperframes render -c index.html -o out/video.mp4
```

> **`npx hyperframes preview` is a long-running server, not a one-shot command.** It blocks
> until stopped. In Claude Code, always run it in the background. Visual output matches the
> render exactly (though preview can stutter — the render is always frame-perfect).

Other useful commands:

```bash
npx hyperframes doctor                 # verify Node / FFmpeg / Chrome environment
npx hyperframes render -c x.html -o out/x.mp4 --docker   # deterministic, reproducible render
npx hyperframes docs <topic>           # inline terminal docs
```

## Key rules

1. Every timed element needs `data-start`, `data-duration`, and `data-track-index`.
2. Timed elements **must** have `class="clip"` — the framework uses it for visibility control.
3. Timelines are paused and registered on `window.__timelines["<composition-id>"]`.
4. Videos use `muted` with a separate `<audio>` element for the audio track.
5. All media lives **under the project root** (`assets/...`), referenced by relative path —
   external CDN URLs break renders.
6. Deterministic logic only — no `Date.now()`, no `Math.random()`, no network fetches.

## Docs

Discover pages via the machine-readable index (don't guess URLs):
`https://hyperframes.heygen.com/llms.txt`. Human docs at
`https://hyperframes.heygen.com`.

---

## Server setup (hf-agent)

This repo is the **HyperFrames video-agent setup** (generator, tooling, docs, skills,
components). Media/secrets/build outputs are gitignored — fetched/generated per video.

```bash
# 1. prerequisites: Node 22+, FFmpeg, ImageMagick, Python 3, (yt-dlp auto-used by youtube.py)
node --version && ffmpeg -version | head -1 && magick --version | head -1

# 2. secrets — copy the template and fill in real keys
cp .env.example tools/.env && $EDITOR tools/.env
ln -sf tools/.env .env          # the fetchers read ./.env

# 3. HyperFrames CLI + skills (no install needed; npx pulls them)
npx hyperframes doctor          # verify env
npx skills add heygen-com/hyperframes   # (skills are also vendored in .agents/skills/)

# 4. workflow (see docs/guides/AGENT_GUIDE.md + CREATIVE_SPEC.md):
#    transcript.json (word-level) -> fetch assets (tools/stock_fetcher/*) ->
#    python3 build_composition.py -> npm run check -> npx hyperframes snapshot (QA every frame) ->
#    npx hyperframes render --output out/<slug>.mp4
```

**Key docs:** `docs/guides/CREATIVE_SPEC.md` (the contract), `AGENT_GUIDE.md`, `QA_GRID_GUIDE.md`,
`SPLITSCREEN_GUIDE.md`, `docs/reference/` (avatar looks, bedrock-v3 blueprint). Every video is
sped **1.10×** and graphics are **word-synced** to the transcript.
