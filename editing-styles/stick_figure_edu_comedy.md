# Stick-Figure Educational Comedy — Production Pipeline

> **Reference**: `assets/inspo/diogenes-ref.mp4` (Sam O'Nella Academy)
> **Grid**: `assets/inspo/diogenes-ref-grid.jpg` (5x5 contact sheet)
> **Character**: `replicate-prediction-g6863j6nh9rmy0cxjnfta3n3b4.webp`
> **Diogenes character**: `assets/diogenes_character.png`
> **Productions**: "Bottled Water" (`BottledWater-v2`), "Diogenes Comedy" (`DiogenesComedy-v1`), "Marcus Aurelius 7 Lessons" (`MarcusAurelius-7Lessons`)

---

## 1. Visual Style Rules

| Rule | Detail |
|------|--------|
| **Art style** | Clean black-and-white line art, vector feel, black outlines on white bg |
| **Character consistency** | Use character image(s) as `image_input` references in nano-banana. Supports multiple refs via `characters` array |
| **NO text in images** | All text, numbers, labels come from the HyperFrames caption pipeline / on-canvas HTML — never bake text into generated images |
| **Backgrounds** | Pure white (`#FFFFFF`) or off-white. No gradients, no textures |
| **Color** | Monochrome by default. Occasional accent color only for key props (green bottle, gold pedestal) |
| **Composition** | Character/objects centered, generous white space around them |

---

## 2. Universal Asset Pipeline

All asset generation runs through a **single reusable tool** + a **per-project JSON file**:

```
tools/generate_assets.py          ← universal pipeline (never edit per project)
projects/<topic>/scenes.json      ← per-project scene definitions (edit this)
```

### Quick Start

```bash
# 1. Write your script
#    → projects/<topic>/script.txt

# 2. Define scenes in JSON
#    → projects/<topic>/scenes.json  (see schema below)

# 3. Generate voiceover
python3 tools/generate_assets.py projects/<topic>/scenes.json --voiceover

# 4. Transcribe for captions
python3 tools/transcription/transcribe.py public/<topic>/voiceover.mp3 \
  --out projects/<topic>/subtitles.json

# 5. Generate all images + videos (parallel, with retries)
python3 tools/generate_assets.py projects/<topic>/scenes.json

# 6. Stitch a quick preview
python3 tools/generate_assets.py projects/<topic>/scenes.json --stitch

# 7. (Optional) Generate background music via ElevenLabs Music API
#    POST https://api.elevenlabs.io/v1/music/detailed
#    prompt + music_length_ms + force_instrumental: true

# 8. Build HyperFrames composition for final render
#    → index.html  (or compositions/<topic>.html for a sub-composition)
```

### CLI Reference

```bash
# Full generation (images in parallel → videos after → retries on failure)
python3 tools/generate_assets.py projects/<topic>/scenes.json

# Generate only specific scenes
python3 tools/generate_assets.py scenes.json --only s01_hook s05_rain

# Images only / videos only
python3 tools/generate_assets.py scenes.json --images-only
python3 tools/generate_assets.py scenes.json --videos-only

# Override parallel workers (default: 4)
python3 tools/generate_assets.py scenes.json --workers 6

# Force regenerate (ignore existing files)
python3 tools/generate_assets.py scenes.json --force

# Dry run (see what would be generated without running)
python3 tools/generate_assets.py scenes.json --dry-run

# Generate voiceover from script
python3 tools/generate_assets.py scenes.json --voiceover

# Stitch slideshow from images + voiceover
python3 tools/generate_assets.py scenes.json --stitch
```

---

## 3. scenes.json Schema

```jsonc
{
  // ── Project metadata ──────────────────────────────────────
  "project": "bottled_water",           // project name
  "output_dir": "public/bottled-water", // where assets go
  "character": "character.webp",        // single style ref (legacy)
  "characters": [                      // multi-ref: send multiple images
    "main_character.webp",             //   to nano-banana for consistency
    "secondary_character.png"          //   across multiple characters
  ],

  // ── Model config ──────────────────────────────────────────
  "style_prefix": "Minimalist black-and-white line art...",
  "image_model": "google/nano-banana",
  "video_model": "wan-video/wan-2.2-i2v-fast",
  "image_defaults": {
    "aspect_ratio": "16:9",
    "output_format": "jpg"
  },
  "video_defaults": {
    "resolution": "720p"              // 720p (832x480 → 1264x720)
  },

  // ── Processing config ─────────────────────────────────────
  "parallel_workers": 4,     // concurrent Replicate API calls
  "max_retries": 3,          // auto-retry failed generations
  "retry_delay_sec": 10,     // wait between retry rounds

  // ── Voiceover config ──────────────────────────────────────
  "voiceover": {
    "script": "projects/<topic>/script.txt",
    "output": "public/<topic>/voiceover.mp3",
    "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
    "model": "eleven_multilingual_v2",
    "stability": 0.4,
    "similarity_boost": 0.75,
    "style": 0.3,
    "speed": 1.05
  },

  // ── Scene definitions ─────────────────────────────────────
  "scenes": [
    {
      "id": "s01_hook",             // unique filename stem
      "type": "image",              // "image" or "video"
      "prompt": "Description..."    // NO text instructions!
    },
    {
      "id": "anim_money",
      "type": "video",              // generates .mp4
      "source": "s17_money",        // source image ID (must exist)
      "prompt": "Camera zooms..."   // motion description
    }
  ]
}
```

### Scene types

| Type | Output | Required fields | Notes |
|------|--------|----------------|-------|
| `image` | `{id}.jpg` | `id`, `type`, `prompt` | Uses character(s) as style ref via nano-banana. Optional per-scene `characters` override |
| `video` | `{id}.mp4` | `id`, `type`, `source`, `prompt` | Animates a source image via wan-2.2 at 720p. Source image must be generated first |

### Prompt rules
- Describe the scene visually, never mention text/labels
- End every prompt with "White background."
- Include character description when the main character appears
- For split-screen pairs, generate two separate images
- The `style_prefix` is auto-prepended — don't repeat it in scene prompts

---

## 4. Pipeline Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    scenes.json                          │
│  (project config + scene definitions)                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              tools/generate_assets.py                   │
│                                                         │
│  Phase 0: Voiceover (--voiceover flag)                  │
│    └→ ElevenLabs TTS → public/<topic>/voiceover.mp3     │
│                                                         │
│  Phase 1: Images (parallel with ThreadPoolExecutor)     │
│    ├→ Worker 1: s01 → nano-banana → s01.jpg             │
│    ├→ Worker 2: s02 → nano-banana → s02.jpg             │
│    ├→ Worker 3: s03 → nano-banana → s03.jpg             │
│    └→ Worker 4: s04 → nano-banana → s04.jpg             │
│    ... (continues until all images done)                │
│    └→ Auto-retry failed images up to N times            │
│                                                         │
│  Phase 2: Videos (parallel, after ALL images complete)  │
│    ├→ Worker 1: anim_X → wan-2.2(source_img) → .mp4    │
│    └→ Worker 2: anim_Y → wan-2.2(source_img) → .mp4    │
│    └→ Auto-retry failed videos up to N times            │
│    └→ Skips videos whose source images failed           │
│                                                         │
│  Phase 3: Stitch (--stitch flag)                        │
│    └→ ffmpeg concat → <project>_stitched.mp4            │
│                                                         │
│  ✓ Only proceeds when all assets are generated          │
│  ✓ Corrupt files (<1KB) auto-deleted and retried        │
│  ✓ Existing files skipped unless --force                │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  HyperFrames Composition (index.html / compositions/*)  │
│    - References generated assets from assets/           │
│    - Adds text overlays, captions, transitions          │
│    - Full/split/video layouts                           │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Script Structure

Write a ~250-300 word educational comedy script (~1:40-2:00 at conversational pace).

```
HOOK (0-10s)      — Shocking statement, question, or bold claim
CONTEXT (10-20s)  — Historical background, "how we got here"
MIDDLE (20-65s)   — Key facts, comparisons, data points
TWIST (65-82s)    — Surprising reveal that reframes everything
KICKER (82-96s)   — Additional shocking fact that seals the argument
OUTRO (96-101s)   — Sarcastic/funny wrap-up
```

---

## 6. HyperFrames Composition Pattern

**Format**: 1920x1080, horizontal. Set `data-composition-id` + `data-width`/`data-height` on the root.

**Scene definition** (data-driven): each scene maps to a timed clip — an `<img class="clip">` / `<div class="clip">` (full/split layouts) or a `<video muted playsinline>` (video layout), timed via `data-start` (seconds), `data-duration`, and `data-track-index`. A small JS array of scene descriptors drives building the paused GSAP timeline registered on `window.__timelines["<id>"]`:
```javascript
// scene descriptor (drives DOM + timeline build)
const scene = {
  start: 0,         // seconds → data-start
  duration: 3,      // seconds → data-duration
  assets: [],       // 1 = full, 2 = split-screen
  layout: "full",   // "full" | "split" | "video"
  text: "",         // only key stats/prices
  textColor: "",
  textSize: 0,
  textPosition: "top", // "top" | "bottom" | "center"
};
```

| Layout | When to use | Assets |
|--------|------------|--------|
| `full` | Default — single image fills frame | 1 image |
| `split` | Comparisons (tap vs bottle, gas vs water) | 2 images side by side |
| `video` | Complex concepts that need motion | 1 video (falls back to image) |

**Text overlays**: Only for key stats (prices, percentages, multipliers). Animated with overshoot GSAP eases (`back.out(1.7)`/`elastic.out`), Impact font, color-coded (red=expensive, green=cheap). **Must have a semi-transparent white background** (`rgba(255,255,255,0.88)` with padding and rounded corners) so text doesn't overlap/clash with images and videos beneath it.

**Captions**: Handled by the HyperFrames caption pipeline — dark pill at bottom, Inter 30px, white, quick fade-in (~0.13s).

**Transitions**: Hard cuts only. No crossfades.

---

## 7. Pacing Guidelines

| Segment | Duration | Images | Cadence |
|---------|----------|--------|---------|
| Hook | 10s | 4-5 | Fast — new image every 2-3s |
| Context | 8s | 2-3 | Medium — let scene breathe |
| Middle facts | 30s | 8-10 | Steady — match voiceover beats |
| Comparisons | 12s | 4-6 | Split-screens + stats |
| Twist/Kicker | 20s | 5-6 | Mix of video + static |
| Outro | 5s | 2 | Slow — character signs off |

**Total**: 25-30 images + 2-3 animations for a 2-minute video. For longer videos (~4 min), scale to 33+ images and 5 animations.

---

## 8. Background Music & Pauses

### When to use
For longer-form content (3+ minutes) or topics with an epic/cinematic feel (philosophy, history, biographies). Short comedy videos (under 2 min) generally don't need music.

### Music generation (ElevenLabs)
```python
# POST https://api.elevenlabs.io/v1/music/detailed
requests.post(url, json={
    "prompt": "Cinematic ambient instrumental...",
    "music_length_ms": 270000,  # match VO duration
    "model_id": "music_v1",
    "force_instrumental": True,  # no vocals
})
# Response: multipart/mixed — extract audio from second part
```

### Script structure with pauses
Insert `[PAUSE]` markers in the script between major sections. Generate VO in separate segments, then stitch with ffmpeg adding 1.5s silence gaps:
```
Intro paragraph...
[PAUSE]
Lesson one...
[PAUSE]
Lesson two...
```

### Segment-based VO generation
```bash
# 1. Split script at [PAUSE] markers
# 2. Generate each segment via ElevenLabs TTS separately
# 3. Stitch with ffmpeg:
ffmpeg -f concat -safe 0 -i concat.txt -c copy voiceover.mp3
# concat.txt alternates segment files and 1.5s silence files
```

### Volume ducking in HyperFrames
Music plays from a separate `<audio data-volume="0.12">` element, and volume is tweened on the paused GSAP timeline. Adjust dynamically:
- **During VO**: low volume (`0.12`) — music sits behind narration
- **During pauses**: higher volume (`0.45`) — music swells, letting the lesson breathe
- **Ramp**: 0.3s smooth GSAP tween between levels

```javascript
// pause windows drive GSAP volume tweens on the audio element's media volume
const PAUSE_WINDOWS = [
  [19.41, 20.91],  // after intro
  [52.49, 53.99],  // after lesson 1
  // ...
];

// For each window, tween volume up at window[0] and back down at window[1]:
// tl.to(musicVol, { value: 0.45, duration: 0.3 }, start)
//   .to(musicVol, { value: 0.12, duration: 0.3 }, end)
// where the proxy updates the <audio> element's volume via onUpdate.
```

### Lesson title cards
For listicle videos (Top 7, 5 Things, etc.), use a `"lesson"` layout:
- Large gold number (Impact, 180px) with an overshoot GSAP entrance (`back.out(1.7)`)
- Lesson quote below in a white pill badge
- Background image at 30% opacity with blur

---

## 9. Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#FFFFFF` | All frames |
| Text | `#1A1A1A` | Captions, neutral text |
| Stat Red | `#DC2626` | Expensive prices, markups |
| Stat Green | `#16A34A` | Cheap prices, positive |
| Stat Blue | `#2563EB` | Neutral emphasis |
| Stat Gold | `#D97706` | Awards, premium |
| Subtitle BG | `rgba(0,0,0,0.78)` | Caption pill |
| Overlay Text BG | `rgba(255,255,255,0.88)` | Background pill behind stat text overlays |

---

## 10. File Structure

```
projects/<topic>/
  script.txt              # Voiceover script
  scenes.json             # Scene definitions (drives generate_assets.py)
  subtitles.json          # Word-level timestamps from transcription

public/<topic>/
  voiceover.mp3           # ElevenLabs TTS output (stitched with pauses)
  vo_segment_00.mp3       # Individual VO segments (when using pauses)
  vo_segment_01.mp3
  bg_music.mp3            # Background music (ElevenLabs Music API, optional)
  s01_<desc>.jpg          # Generated scene images (no text)
  s02_<desc>.jpg
  ...
  anim_<desc>.mp4         # wan-2.2 animated scenes (720p)
  sfx/                    # Sound effects directory
    whoosh.wav            # Local SFX in assets/ (no external SFX CDN)
    page-turn.wav         # Local SFX in assets/ (no external SFX CDN)
    deep_impact.mp3       # Custom ElevenLabs SFX
    quill_writing.mp3     # Custom ElevenLabs SFX
    stone_reveal.mp3      # Custom ElevenLabs SFX
  <project>_stitched.mp4  # ffmpeg preview (optional)

tools/
  generate_assets.py      # Universal pipeline (reads scenes.json)
  audio_generator/elevenlabs.py
  transcription/transcribe.py

./
  index.html              # HyperFrames composition (root)
  compositions/
    <topic>.html          # HyperFrames sub-composition (optional)
```

---

## 11. Learnings

### Pipeline & Generation
- **No text in generated images** — HyperFrames handles all typography via the caption pipeline (and on-canvas HTML text), with animation, sizing, and timing
- **Parallel generation** — 4 workers cuts generation time by ~75% vs sequential
- **Auto-retry with backoff** — Replicate has intermittent capacity limits; 3 retries with 10s delay handles it
- **Videos depend on images** — Pipeline ensures all images complete before video animation starts
- **One JSON, one tool** — never write per-project Python scripts; just write a new scenes.json
- **Multi-character refs** — send multiple character images to nano-banana via `characters` array for consistent multi-character scenes
- **720p videos** — set `video_defaults.resolution: "720p"` for wan-2.2; default 480p is too low quality
- **ElevenLabs STT for transcription** — use the `/v1/speech-to-text` endpoint with `scribe_v1` model for word-level timestamps
- **Each major character needs their own reference** — generate a dedicated character ref image (e.g. `assets/marcus_aurelius_character.png`) using nano-banana with the main character as style input, so the characters appear in the same art style

### Visual & Composition
- **Text overlays need backgrounds** — always put a semi-transparent white pill (`rgba(255,255,255,0.88)`) behind stat text like "$400", "$20/mo", etc. Without it, text overlaps images and becomes unreadable
- **Split-screens for comparisons** — side-by-side is clearer than sequential
- **Animate complexity** — use wan-2.2 for processes, flows, and actions (Alexander scene, lantern walk, chains breaking)
- **Hard cuts > transitions** for comedy
- **Faster pacing** — change the image every 2-5 seconds
- **White space is power** — emptiness around a character focuses attention
- **Smaller text uses FONT_FAMILY** — only use IMPACT_FONT for large stat numbers (>80px); quotes and phrases look better in Inter
- **NEVER repeat the same image in consecutive scenes** — if you have 33 images and 50 scene slots, interleave and alternate assets so no image appears back-to-back. Reusing an image 3+ times consecutively makes the video feel stuck/frozen
- **Lesson cards: centered vertical hierarchy** — follow the professional editorial pattern: LESSON label (18px, muted, `marginBottom: 16px`) → giant number (300px, gold, hero element) → gold divider line → quote (38px, italic, 75% max-width, centered). The LESSON label needs breathing room from the number — at least 16px gap. The gold divider line should be short and elegant (140px, not 280px) with generous top margin (28px) so it doesn't crowd the number. The number is the content — it must be the dominant focal point. A ghost watermark number (700px, 2.5% opacity) offset to the right adds depth without competing. Gold bottom bar anchors the frame. Never split number/quote into left-right columns — it creates dead space and breaks the Z-pattern reading flow

### Audio & Music
- **Background music for long videos** — use ElevenLabs Music API (`/v1/music/detailed`) with `force_instrumental: true` for cinematic ambient tracks
- **Segment-based VO** — for videos with deliberate pauses, generate VO segments separately then stitch with 1.5s silence gaps via ffmpeg
- **Volume ducking** — music stays at 0.12 during narration, ramps to 0.45 during pauses (0.3s ramp time). Lets music breathe between lessons
- **Pause windows** — track exact timestamps of silence gaps to drive the GSAP volume tweens on the `<audio data-volume>` element
- **Music length** — match `music_length_ms` to total VO duration so the single `<audio>` element covers the whole timeline (no looping needed; HyperFrames requires finite, deterministic durations)
- **Multipart response** — ElevenLabs Music API returns `multipart/mixed`; extract the audio part after the boundary separator
- **Stitch VO with re-encoding, never `-c copy`** — when concatenating MP3 segments + silence files, always re-encode through ffmpeg's `concat` filter with `-c:a libmp3lame`. Using `-c copy` causes MP3 frame alignment drift (silence files become 1.541s instead of 1.5s) which compounds across segments and desynchronizes captions/scenes

### Cinematic Title Card (Poster Style)
- **Poster-style layout** — split the frame into left/center/right columns: left has the stacked title name, center has the character cutout, right has a large number + subtitle. Full-width accent bar at the bottom
- **Background removal** — use `rembg` locally (`pip install "rembg[cpu]"`), which is an AI model that properly separates foreground from background, preserving internal whites (face, clothing folds). Simple flood-fill approaches break on line art because they can't distinguish background white from character white. Replicate `bria/remove-background` also works but may be intermittently unavailable
  ```python
  from rembg import remove
  from PIL import Image
  out = remove(Image.open("source.jpg"))
  out.save("cutout.png")
  ```
- **Invert line art for dark backgrounds** — use CSS `filter: brightness(0) invert(1)` on the cutout `<img>` to turn black lines white, making it pop on dark backgrounds
- **Ghost number** — place a giant (260px+) low-opacity number behind the main elements as a graphic design element (like "7" at `opacity: 0.06`), then overlay the actual visible number in gold
- **Gold bottom bar** — a full-width gold bar at the bottom (`height: 80px`) with dark text is the strongest visual anchor. Use a `y` GSAP tween with an overshoot ease (`back.out(1.4)`) to slide it up on entrance
- **Slow zoom applies to the content layer, not background** — wrap the entire content layer (a full-bleed `<div>`) in its own `transform: scale(zoom)` tween, separate from the base background div, so the zoom feels like a camera push

### Sound Effects (SFX)
- **ElevenLabs Sound Generation API** — `POST /v1/sound-generation` with `text` (description), `duration_seconds` (0.5-30s), and optional `prompt_influence` (0-1). Returns raw audio bytes
- **Local SFX files** — keep common cues (`whoosh.wav`, `page-turn.wav`, `switch.wav`, `ding.wav`) as local files in `assets/sfx/`. There is no built-in SFX CDN in HyperFrames — source/generate them once and reference them locally for deterministic offline renders
- **Keep SFX present but not dominant** — volumes between 0.45-0.7. Whooshes at 0.7, impacts at 0.55-0.6, ambient sounds (quill) at 0.45, page turns at 0.5. Below 0.25 they become inaudible when mixed with VO + music
- **Strategic placement only** — use SFX at: lesson card transitions (whoosh), journal/writing scenes (quill), dramatic reveals (impact), scene cuts (page turn). Don't add SFX to every scene
- **Render SFX as timed `<audio>` elements** — define an `SFX_CUES` array with `{time, src, volume}` and emit one `<audio data-start="<time>" data-volume="<volume>" src="assets/sfx/...">` per cue (audio defaults to its source length; no separate duration needed). The framework owns playback — never call play/seek
- **Custom SFX prompts** — be specific: "Deep cinematic bass impact hit, single powerful boom, short and punchy" works better than "boom sound"

### Title Card Design Principles (from professional editorial guides)
- **Rule of Thirds** — place key elements at grid intersections. For title cards: name at left-third, character at center, callout at right-third
- **Z-pattern reading** — eye scans top-left → top-right → diagonally → bottom-left → bottom-right. Place the primary text (name) top-left, secondary (number) top-right
- **Visual hierarchy through size** — the most important element should be 3-5x larger than supporting text. Title name at 140px, subtitle at 20px, label text at 13-14px
- **Proximity groups** — related items (label + number, or name + subtitle) must be close. Don't scatter related text across the frame
- **Ghost watermarks** — a huge low-opacity (2-4%) version of the hero element behind everything adds depth and fills empty space without competing
- **Subtitle text minimum 18-20px** — anything below 16px becomes unreadable on video. "FROM HIS PRIVATE JOURNAL" style labels should be 20px with letter-spacing 6+
- **Asymmetrical balance** — the character cutout on one side is balanced by text weight on the other. Both sides should feel equally "heavy" visually
- **Gold bottom bar** — a consistent design anchor across title cards and lesson cards. Slides up on entrance. Creates a strong visual endpoint

### wan-2.2 Animation Style
- **Always include style instructions in animation prompts** — wan-2.2 will drift to photorealism if the prompt only describes the scene. Always prepend: `"Minimalist black-and-white line art animation style, clean vector look with black outlines on white background."` and end with: `"Keep the illustration style consistent — simple line art, no photorealism, no color gradients."`
- **Don't say "cinematic" or "warm" in animation prompts** — these trigger photorealistic rendering. Use words like "simple", "clean", "minimal", "line art" instead
