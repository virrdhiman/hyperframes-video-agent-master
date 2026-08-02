# Motion graphics reference — [The Problem with Indian Venture Capital](https://www.youtube.com/watch?v=Guufmu3rIx4)

General motion-design reference, kept as knowledge for HyperFrames compositions. The animation principles here are framework-agnostic; encoding notes map to HyperFrames (HTML + GSAP timeline → deterministic video).

## Full documentation (read these instead of re-analysing)

| Doc | What it covers |
|-----|---------------|
| [`MOTION_PATTERNS.md`](MOTION_PATTERNS.md) | Every graphic pattern with visual specs, frame-by-frame animation sequences, and the HyperFrames translation |
| [`EDITOR_MINDSET.md`](EDITOR_MINDSET.md) | Pacing logic, graphic trigger rules, narrative structure, what NOT to do |

The docs above cover all 9 grids. Only re-run a contact-grid pass if you need a timestamp not already covered.

---

## Source files

| File | Description |
|------|-------------|
| `reference.mp4` | Full video (~13:46, 1920×1080, 30fps) |
| `reference.en.srt` | Auto subtitles |
| `reference.info.json` | yt-dlp metadata |

## Analysis workflow (contact grids)

Contact grids are still tiles of the reference video used to study *when* graphics appear and *how* a single animation moves. Build them with any ffmpeg-based tile script over the source `reference.mp4`. Each grid writes a `.json` manifest mapping cell index -> timestamp.

**Level 1 — Coarse (find *when* graphics appear)** — 4x4 grid over full video -> 16 frames, ~52s apart -> `grids/01_full_overview_4x4.jpg`.

**Level 2 — Medium (scan a chapter)** — 4x4 over a 60–120s window -> `grids/02_chapter_60-120_4x4.jpg`.

**Level 3 — Fine (study one animation)** — 4x4 over 2–4 seconds (~0.15–0.25s per frame) -> `grids/zoom_EXAMPLE_4x4.jpg`. This is the resolution you need to read the easing of a single move and translate it into GSAP timeline tweens.

## Key motion-graphic timestamps (from grid survey)

| Time | What happens | Grid to inspect |
|------|----------------|-----------------|
| **0:02–0:15** | Paper-stack news collage | `03_intro_45s_3x3.jpg` |
| **0:33** | India map "93+ UNICORNS" circles | `02_first_2min_4x4.jpg` |
| **1:02–1:08** | **Startups star -> Valuation -> Copycat Models** (fluid blue bridge) | `zoom_startups_anim_3x3.jpg` |
| **1:08–1:12** | Sentence build: "You will rarely see a startup…" | same zoom grid, cells 5–9 |
| **2:32** | Manufacturing circle ring | `02_first_2min_4x4.jpg` |
| **~4:44** | Pie / % split graphics (see coarse overview) | `01_full_overview_4x4.jpg` |

Your screenshot (`ref_user_startups-tech.png`) matches **~1:04** in `zoom_startups_anim_3x3.jpg` (cell 1–2).

### Animation readout — Startups wedge (~6s, 1:02–1:08)

From `zoom_startups_anim_3x3.jpg` (3x3 over 62–68s, ~0.67s per frame):

1. Black star + red **Startups** circle; **Valuation** + pink circle enter top wedge
2. Light-blue **fluid bridge** grows from star toward Valuation
3. Camera pans — **Copycat Models** + green circle in lower wedge
4. Hard cut to typography: **"You will rarely see a startup solving an Actual Problem"** (gray -> black stagger)

**Editor techniques to steal:** textured off-white bg, geometric containers, asymmetric wedges, morphing connector blob, pan instead of scale, phrase-by-phrase type (not all-at-once). In HyperFrames: pan by translating a non-timed wrapper `<div>` larger than the frame; grow the connector via SVG `stroke-dashoffset`; stagger phrase reveals on the GSAP timeline ~0.27s apart.

---

## Style notes (from reference + your screenshots)

- Off-white textured paper background, not pure white
- Bold geometric shapes (stars, wedges, circles) — Kurzgesagt / Polymatter-adjacent
- Flat color fills, thin black outlines, minimal gradients
- Typography inside shapes (labels like "Startups", "Tech") or large % numerals
- Asymmetric layouts; elements "connect" with fluid bridges between shapes

## Re-download

If you need to re-fetch the source reference video, use yt-dlp:

```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio" \
  --merge-output-format mp4 \
  -o "reference.%(ext)s" \
  "https://www.youtube.com/watch?v=Guufmu3rIx4"
```
