# MOTION_LIBRARY.md — THE master index of every premade motion asset (2026-06-11)

**Using this library well is a PRIMARY JOB of the Director and Bella (the owner, 2026-06-11).**
The Director SHOPS here first — every BRIEF must cite which library pieces each beat uses
(or state why a beat is bespoke). Bella EXECUTES them well — tinted to the video's accent,
timed to the word, never default-styled. A video that ignores this library and hand-rolls
generic CSS is doing it wrong; a video that pastes pieces unthemed is doing it wrong too.
**Use them wisely: pick the 3–6 pieces the story needs, not 20 because they exist.**

The full HyperFrames registry (113 items) is INSTALLED locally — blocks in `compositions/`,
components in `compositions/components/`. Browse: `npx hyperframes catalog`. Each file has
a usage header (CSS vars, include snippet). Sub-compositions embed via
`data-composition-src="compositions/<name>.html"`; components paste inline.

---

## 1) Caption styles (components) — pick ONE per video, log it in the STYLE/LOOK fingerprint
| Component | Vibe | Notes |
|---|---|---|
| caption-pill-karaoke | per-word karaoke highlight in a pill | social default |
| caption-kinetic-slam | full-screen single-word slams | high energy hooks |
| caption-emoji-pop | emoji + squeeze entrance | playful |
| caption-highlight | TikTok-style bg sweep per word | punchy |
| **caption-editorial-emphasis ★ RECOMMENDED BODY (the owner 2026-07-12)** | dual-font size contrast; measured 9:16 port in `styles/elements/subtitles/editorial-emphasis-caption.md` | premium/editorial — the approved 07-11 pairing |
| caption-weight-shift | font-weight transitions | minimal/elegant |
| caption-clip-wipe | per-word clip-path wipe | clean |
| caption-gradient-fill | gradient text + elastic bounce | colorful |
| caption-texture | flowing texture mask in big type | statement words |
| **caption-parallax-layers ★ RECOMMENDED STATEMENT (the owner 2026-07-12)** | behind-subject 3D layering; max 2 walls/video; measured 9:16 port in `styles/elements/subtitles/parallax-statement-wall.md` | statement beats — pairs with editorial-emphasis (one voice: same serif + accent) |
| ⚠ caption-neon-accent / neon-glow / glitch-rgb / matrix-decode / particle-burst / blend-difference | neon/glitch/dark | **RESTRICTED: dark/neon is banned house-wide — only when the TOPIC itself demands it (e.g. a gaming/cyber story) AND the Director justifies it in the BRIEF** |

## 2) Transitions (blocks: shader) + (components)
Hard cuts stay the base grammar — **max 1–2 BRIEF-specced transitions per video, on the
single biggest beat change**. Installed: whip-pan · flash-through-white · light-leak ·
cinematic-zoom · sdf-iris · ripple-waves · swirl-vortex · thermal-distortion ·
chromatic-radial-split · domain-warp-dissolve · ridged-burn · gravitational-lens ·
cross-warp-morph · glitch (⚠ dark-leaning) + components grid-pixelate-wipe,
parallax-zoom / parallax-unzoom (eBay-hero style card↔grid zoom — great beat opener) +
our light-streaks. The `transitions-*` showcase blocks are demo reels — open them to
PREVIEW a family, then use the individual block.

## 3) Text effects (components)
morph-text (gooey word morph) · texture-mask-text (66 texture masks through letterforms) ·
shimmer-sweep (light pass) · our text-gradient-fill · our text-shatter (deterministic
shatter — myth-busting) · our wave-underline · cutaway-kinetic-headline.

## 4) Citation / social cards (blocks) — USE for real posts instead of screenshots
x-post · reddit-post · instagram-follow · tiktok-follow · yt-lower-third · spotify-card.

## 5) Data, maps, showcase (blocks)
data-chart (NYT-style bar+line) · world-map · us-map / us-map-bubble / us-map-hex /
us-map-flow · spain-map · flowchart / flowchart-vertical · apple-money-count ($ counter +
money burst — pricing beats) · nyc-paris-flight (map flight) · north-korea-locked-down
(news-style map zoom + annotation — relabel for any locked-down/banned story) ·
ui-3d-reveal · app-showcase (floating phones) · vpn-youtube-spot · blue-sweater-intro-video
(creator intro → X follow card — restyle for Retrofit) · logo-outro.

## 6) Code/dev visuals (blocks)
code-snippet-light-modern / light-plus / light-2026 / solarized-light / visual-studio-light /
apple-terminal-basic / -novel / -man-page / -clear-light (LIGHT themes — preferred) ·
⚠ dark themes (dark-modern, monokai, homebrew, ocean…) installed but RESTRICTED same as §1.

## 7) Heavy VFX (blocks — WebGL/WebGPU; render on the office GPU box only)
vfx-iphone-device (real GLTF iPhone/MacBook with live screen content — USE for phone/product
videos) · vfx-text-cursor · vfx-liquid-background · vfx-magnetic · vfx-portal · vfx-shatter ·
liquid-glass-* (notification/context-menu/media-controls/widgets) · ios26-liquid-glass ·
macos-tahoe-liquid-glass (made for Apple-OS stories). Budget ONE heavy VFX beat per video max;
preview locally before committing the render.

## 8) CodePen-derived components (ours, seek-safe, warm-tinted)
glow-border · light-streaks · wave-underline · text-gradient-fill · orbit-system ·
text-shatter — see `styles/INDEX.md` "Ready-made components" table for what each does.
Raw pens to adapt: `docs/motion-ref/codepen/` (incl. 824-path travel-map SVG — extract
elements). Fetch more: `python3 tools/stock_fetcher/codepen.py <pen-url>` (works despite
Cloudflare via the cdpn.io embed CDN; MIT, auto-credited).

## 9) GSAP official demos (techniques to re-wire onto our timeline)
`docs/motion-ref/GSAP_DEMOS_CATALOG.md` — curated render-usable subset of demos.gsap.com:
text-scrambling, rolling-number odometer, MorphSVG shape morphs, text-masking, DrawSVG
draw-ons, MotionPath travel, staggering. All GSAP plugins free since 3.13.

## 10) Lottie + overlays + SFX (assets)
`assets/common/lottie/` — 22 Noto Animated Emoji (confetti, boom, fire, eyes, 100,
mind-blown, chart-up, siren…); ~600 more on demand: `tools/stock_fetcher/noto_lottie.py
--emoji "X"` (CC BY 4.0 — credit Google in post.md). `assets/common/overlays/` — grain /
light-leak / dust (screen-blend at 4–8%). SFX/music per `AUDIO_GUIDE.md` (cap -4dB, `dur`
trims). Bespoke Lottie: text-to-lottie skill, last resort.

---

## The contract (Director ⇄ Bella)
1. **Director (BRIEF):** per-beat plan cites the library piece by name per beat (caption
   style, any transition, text effect, card/block, lottie, overlay) — or says "bespoke:
   <why>". No un-shopped briefs.
2. **Bella (build):** use the cited pieces; theme EVERY one (CSS vars → video accent,
   LIGHT palette, fonts); time reveals to the word; verify each embedded piece renders
   (one preview frame) before the full render. Never ship a piece in its demo styling.
3. **QA:** Director checks pieces were used as specced + themed + no dark/neon leakage;
   library usage goes in the QA-REPORT and the STYLE/LOOK fingerprint row.
4. **Variation:** the library is wide so cuts stay FRESH — rotate pieces per the 3-day
   cooldown; never repeat last video's combination.
5. **Growth:** new adapted pen/demo that ships → componentize into
   `compositions/components/` + row in `styles/INDEX.md` + (if external) credit in
   `assets/common/CREDITS.md`.
