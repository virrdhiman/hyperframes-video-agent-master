# Common Assets Catalog

Reusable assets for all video projects. Located in `assets/common/`.

In HyperFrames, assets are referenced with **relative paths** from the composition HTML
(e.g. `assets/common/sfx/filename.wav`) — there is no `staticFile()` helper. All media
must live **under the project root** so the renderer can resolve it deterministically.

---

## Sound Effects (`assets/common/sfx/`)

Reference with a relative path: `src="assets/common/sfx/filename.wav"`.

### Whoosh / Transitions
| File | Use Case |
|------|----------|
| `air-woosh.wav` | Light transition, slide-in |
| `el_soft_whoosh.mp3` | Soft airy transition (ElevenLabs; default "quick cut" whoosh) |
| `cinematic-whoosh-fast.wav` | Dramatic fast transition |
| `cinematic-whoosh-stutter.wav` | Stuttered/glitchy transition |
| `fast-rocket-whoosh.wav` | Intense/powerful transition |
| `metal-hit-woosh.wav` | Impact + whoosh combo |
| `epic-movie-whoosh-impact.wav` | Cinematic title reveal |
| `explainer-pops-whoosh.wav` | Explainer video style |
| `whoosh-1.wav` | Generic whoosh |

### Pop / UI Sounds
| File | Use Case |
|------|----------|
| `long-pop.wav` | Element appear |
| `hard-pop-click.wav` | Button press |
| `bubble-pop-alert.wav` | Soft notification |
| `dry-pop-notification.wav` | Subtle alert |
| `select-click.wav` | Selection/toggle |
| `modern-tech-select.wav` | Modern UI select |
| `sci-fi-click.wav` | Tech/futuristic UI |
| `camera-shutter-click.wav` | Photo/screenshot |

### Impact / Hits
| File | Use Case |
|------|----------|
| `cinematic-glass-hit.wav` | Dramatic reveal |
| `hard-horror-hit-drum.wav` | Tension/suspense beat |

### Notifications / Success
| File | Use Case |
|------|----------|
| `success-bell.wav` | Completion/success |
| `positive-notification.wav` | Good news alert |
| `game-level-up.wav` | Achievement/milestone |

### Typing
| File | Use Case |
|------|----------|
| `typing-fast.wav` | Keyboard typing sequence |

---

## Music (`assets/common/music/`)

| File | Use Case |
|------|----------|
| `bgm_ambient_loop.mp3` | Minimal ambient bed under VO (ElevenLabs; loop with `data-duration` + `data-media-start`) |

---

## Background Videos (`assets/common/backgrounds/`)

Drop in as a muted `<video>` clip with timing attributes, behind a content layer.

### 9:16 (Vertical/Mobile)
| File | Description |
|------|-------------|
| `abstract-blue-particles-9x16.mp4` | Blue floating particles |
| `abstract-colorful-9x16.mp4` | Colorful gradient flow |

### 16:9 (Horizontal/Desktop)
| File | Description |
|------|-------------|
| `abstract-gradient-flow-16x9.mp4` | Smooth gradient flow |
| `abstract-liquid-16x9.mp4` | Liquid/fluid motion |
| `blue-gradient-waves-16x9.mp4` | Blue wave gradients |
| `bokeh-lights-16x9.mp4` | Soft bokeh lights |
| `warm-gradient-16x9.mp4` | Warm orange/red gradient |

> This is a **light/neutral** project. Prefer the warm, soft, light-toned backgrounds
> above; build on warm white, light grey, or beige grounds with bright accents.

---

## Animated Backgrounds (CSS + GSAP)

Animated backgrounds in HyperFrames are plain HTML/CSS layers driven by the paused GSAP
timeline — there is no React component to import. Build them inline, or pull a ready-made
block from the registry:

```bash
npx hyperframes catalog --type block --tag background   # browse
npx hyperframes add <block-name>                         # copy HTML + assets in
```

Common patterns you can author by hand:

| Pattern | Description | How |
|---------|-------------|-----|
| Dot grid | Drifting dot pattern | `background-image` radial-gradient dots + GSAP `backgroundPosition` tween |
| Floating shapes | Soft circles that drift | a few absolutely-positioned divs with finite-repeat `yoyo` `y` tweens |
| Gradient shift | Moving radial gradient | animate `--x`/`--y` CSS vars or `background-position` |
| Floating particles | Rising/floating particles | staggered divs animated upward; keep repeats finite (never `repeat: -1`) |
| Looping video bg | Looping clip with overlay | muted `<video>` clip + a tinted overlay div on top |

---

## Usage Examples

### SFX (timed one-shot)
```html
<!-- Plays a whoosh at 2.0s; data-volume scales the level (0-1) -->
<audio src="assets/common/sfx/cinematic-whoosh-fast.wav"
       data-start="2.0" data-volume="0.8"></audio>
```

### Music bed (looping under VO)
```html
<!-- Background music ducked under speech; start the clip 4s into the track -->
<audio src="assets/common/music/bgm_ambient_loop.mp3"
       data-start="0" data-duration="60" data-media-start="4" data-volume="0.18"></audio>
```

### Video background
```html
<!-- Muted background video behind the content; dim with an overlay div -->
<video src="assets/common/backgrounds/warm-gradient-16x9.mp4"
       muted playsinline
       class="clip" data-start="0" data-duration="10" data-track-index="0"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:0.3"></video>
<div class="clip" data-start="0" data-duration="10" data-track-index="1"
     style="position:absolute; inset:0; background:rgba(255,255,255,0.35)"></div>
```

### Recommended SFX / music levels
Style-agnostic levels that read well under narration:

| Element | `data-volume` | Notes |
|---------|---------------|-------|
| Whoosh / transition | 0.6 - 0.8 | Punchy but not startling |
| UI pop / click | 0.4 - 0.6 | Subtle accent |
| Impact / hit | 0.7 - 0.9 | Reserve for big reveals |
| Music bed under VO | 0.12 - 0.20 | Duck well below speech |
| Music with no VO | 0.35 - 0.5 | Can come forward |

---

## License

- **SFX**: Mixkit License (free for commercial use)
- **Videos**: Pexels License (free for commercial use, no attribution required)

---

## Fetched audio library (Freesound — premade, royalty-free) — added 2026-06

Populated by `python3 tools/stock_fetcher/freesound.py --pack all` (default `--license commercial`
= CC0 + CC-BY; CC-BY credits logged to `assets/common/CREDITS.md`). Re-run any time to refresh.

**SFX (`assets/common/sfx/`)** — filename prefix = category, e.g. `whoosh_<id>_<name>.mp3`:
`whoosh` · `swipe` · `pop` · `click` · `impact` · `subdrop` · `riser` · `swell` · `glitch` ·
`notification` · `typewriter` · `viral_swoosh` · `trap_impact` · `woosh_reverse`.

**Music beds (`assets/common/music/`)** — prefix = mood:
`lofi_chill` · `upbeat_corporate` · `cinematic_inspire` · `tech_ambient` · `energetic_pop` · `warm_acoustic`.

Map them to beats in the BRIEF's AUDIO plan and Bella renders the cue times into
`projects/<slug>/audio.json` for `tools/audio_finish.py` (ducked music + SFX + -14 LUFS master).
Ad-hoc top-ups: `freesound.py -q "<query>" --type sfx|music -n N`.

### Meme / soundboard pack (`assets/common/memes/`) — fair-use commentary accents
Popular meme SFX fetched from myinstants via `python3 tools/stock_fetcher/myinstants.py --pack`
(ad-hoc: `myinstants.py -q "vine boom"`): iphone_notification · roblox_oof · vine_boom · bruh ·
airhorn · sad_violin · rimshot · emotional_damage · anime_wow · among_us · windows_error ·
heavenly · aww · faaah · crickets · taco_bell · discord_ping · nope, etc. Usable as SFX cues in
`audio.json` exactly like any other clip. **These are copyrighted/trademarked, NOT royalty-free**
— the owner treats them as fair-use commentary accents (provenance logged in `memes/SOURCE.md`).
Use with intent (one or two per video) to match the moment; Freesound remains the bulk library.

### Reaction-meme video cutaways (`assets/stock/memes_video/`) — by emotion
Short reaction shorts fetched from YouTube via `python3 tools/stock_fetcher/reaction_memes.py
-e <emotion>` (or `--pack`): funny · sad · excited · shocked · mindblown · awkward · facepalm ·
thinking · clapping · scared. Default pulls **green-screen** clips (chroma-key before compositing
— `CHROMAKEY_TRANSPARENT_VIDEO.md`); `--no-green` for full-frame cutaways. Trimmed ~3s; scale/crop
to 1080×1920, keep to ~1–2s on screen. Downloads route through the home-IP SOCKS proxy (needs the
tunnel up, like HeyGen) + deno. Fair-use commentary accents — drop between A-roll beats to
punctuate a punchline/stat/turn; one or two per video, matched to the moment.

---

## Premade Lottie pack (`assets/common/lottie/`) — Noto Animated Emoji
Fetched 2026-06-11 via `tools/stock_fetcher/noto_lottie.py` (Google, **CC BY 4.0** — credit in
post.md when used). 60fps, 1024px, transparent. Embed per the lottie skill (`autoplay:false,
loop:false`, register on `window.__hfLottie`).

In the pack: `confetti` `confetti-ball` `boom` `fire` `rocket` `zap` `eyes` `hundred`
`mind-blown` `star-struck` `thinking` `partying-face` `clap` `money-wings` `chart-up`
`check` `warning` `siren` `light-bulb` `lock` `robot` `brain`.
**On demand** (~600 more): `python3 tools/stock_fetcher/noto_lottie.py --emoji "🫠" --name melt`
— browse https://googlefonts.github.io/noto-emoji-animation/

## Texture overlays (`assets/common/overlays/`)
`grain_*` `lightleak_*` `dust_*` (Pixabay, fetched 2026-06-11). Black-background clips
composite with `mix-blend-mode: screen` at 4–8% opacity (HUMAN_EDIT_GUIDE §4). Preview
before first use; refetch more with `tools/stock_fetcher/pixabay.py`.

## HyperFrames registry — ALL 113 blocks/components INSTALLED (the owner, 2026-06-11)
The complete registry is on disk: blocks in `compositions/`, components in
`compositions/components/` (+ `texture-mask-text/` with its texture pack).
**The categorized index with use-cases, restrictions (dark/neon pieces are RESTRICTED),
and the Director⇄Bella usage contract lives in `MOTION_LIBRARY.md` — that is the file to
read; this section just records the inventory.** Browse for NEW additions:
`npx hyperframes catalog` → `npx hyperframes add <name>` (re-audit when the count grows
past 113).

## GSAP official demos — curated catalog
`docs/motion-ref/GSAP_DEMOS_CATALOG.md` — the render-usable subset of demos.gsap.com
(time/timeline-driven only; scroll/cursor/drag demos excluded). Top picks: text-scrambling,
rolling-text odometer, MorphSVG shape morphs, text-masking, DrawSVG path draw-on,
MotionPath travel. All GSAP plugins are free since 3.13. Fetch each demo's embedded pen
via `tools/stock_fetcher/codepen.py`.

## CodePen motion references (`docs/motion-ref/codepen/`)
Fetch any public pen (MIT) with `python3 tools/stock_fetcher/codepen.py <pen-url>` — works
via CodePen's embed CDN (`cdpn.io/<user>/fullpage/<slug>`), which bypasses the Cloudflare
403 that blocks the normal page from any of our IPs. References to ADAPT (seek-safe rules
in HUMAN_EDIT_GUIDE §5b), not drop-ins. Saved so far:
| File | What it is |
|------|------------|
| `svg-stroke-text-drawon.html` | "SVG Text Animation Using Stroke Offset Method" (Ayachem) — handwriting-style stroke-dashoffset letter draw-on; CSS keyframes, ports near-verbatim |
