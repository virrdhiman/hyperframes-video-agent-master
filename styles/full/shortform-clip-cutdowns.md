# Short-form clip-cutdown system (3 proven formats)

Reusable system for turning fetched footage (YouTube via `tools/stock_fetcher/youtube.py`)
into 9:16 shorts. Three delivered variants below share ONE generator pattern. Each project
has a `build_composition.py` that emits `index.html` deterministically (HTML is gitignored —
run the script to regenerate; media is re-fetchable).

## Shared generator pattern (`projects/*/build_composition.py`)
Python tables → HTML + GSAP timeline. Three decoupled tracks:
- **AUDIO spine** — VO (ElevenLabs) and/or original-dialogue snippets, interleaved with ~0.1–0.35s gaps.
- **PICTURE cuts** — fast hard cuts (`tl.set(opacity)` + white flash), each a `<video muted data-volume="0">`
  seeked via `data-media-start`, with a gentle ken-burns (`scale z0→z1`) and optional focal `fx` pan.
- **CAPTIONS** — phrase-level pops built in JS from a table; group set `visibility:visible`+`opacity:1` on show.
Timeline is `paused`, registered on `window.__timelines[id]`. Pick scenes by the **grid method**:
`ffmpeg fps=1/N … tile=` contact sheet → read it → pin exact `media_start`s. Always QA with a
real **draft render** (`hyperframes render -q draft`) + frame grab — offline mocks lie.

## Variant A — Viral reaction cutdown  → `projects/dodo-grandma-cat`
- **Look:** 3:4 video card (840×1120 @ top 300, centered, 26px radius, white hairline + shadow) on black.
  Static yellow ALL-CAPS hook up top (#ffd21e, 58px, stroke), captions directly under the card, follow handle bottom.
- **Audio trick:** our VO narrates, then PAUSES so the **original clip audio** plays the punchlines
  (interleaved VO mp3s + pre-trimmed dialogue mp3s with gaps). White caption = narration, italic-yellow = quoted line.
- **Source prep:** crop burnt-in captions off the source bottom (`crop=W:H-70`); per-scene `fx` to keep faces framed.

## Variant B — How-it's-made explainer  → `projects/baseball-bat-howmade`
- **Look:** same 3:4 card, but cooler bg; each caption carries a blue **stage kicker** (① THE WOOD … ⑨ PLAY BALL)
  + a yellow **progress bar** under the card. Multi-source footage (How It's Made + a factory tour).
- **Audio:** VO-only (Eric, documentary); source clips muted. Fast ~2.2s cuts across the real process stages.

## Variant C — Fullscreen nature-glow  → `projects/bioluminescence` (card) + `-v2` (fullscreen)
- **Look:** cyan-glow palette on deep navy; glowing card border, drifting orbs, slow ~3s mesmerizing holds.
- **v2 = no frame:** footage fills the whole 1080×1920, NO card/hook/handle — captions only over a bottom scrim.
  ⚠ Fullscreen `object-fit:cover` upscales ~3×/frame and **times out the renderer** → pre-bake each scene to a
  vertical 1080×1920 clip (`crop=ih*9/16:ih,scale=1080:1920`, `-g 15`, `+faststart`), one file per scene (media-start 0).

## Key gotchas (see also the agent's media-gotchas memory)
- HD downloads: `pip install -U yt-dlp yt-dlp-ejs` (local signature solver) → 720p/1080p instead of 360p.
- Same `src` + multiple `data-media-start` collides for **audio** → pre-trim to separate files.
- `class="clip"` on `<audio>` silences it (visibility controller hides it). Every media needs a unique `id`.
- Caption parent group must be set `opacity:1` on show, not just `visibility`.
- Voices used: Jessica `cgSgspJ2msm6clMCkdW9` (playful), Eric `cjVigY5qzO86Huf0OWal` (explainer), Brian `nPczCjzI2devNBz1zQrb` (nature).
