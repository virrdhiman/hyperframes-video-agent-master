# 🎨 Style Library — READ THIS BEFORE EDITING

**Mandatory pre-edit step (Chhotu + Bella):** before starting ANY video edit, skim this
index and open the relevant style files. Reuse proven looks; never re-invent or clone a
frame-for-frame. Each edit must still be visually UNIQUE — these are the house *mindset* +
exact specs, not a copy-paste template.

There are two kinds of style:
- **Full styles** (`full/`) — how a complete video was built, scene-by-scene, with timings;
  each scene links to the element files it uses.
- **Element styles** (`elements/`) — reusable individual pieces, categorised. Mix & match.

---

## Full styles (`full/`)
| Style | What it is | File |
|---|---|---|
| webveda "Rule of 100" | Punchy number-driven talking-head reel (decoded from reference) | [full/webveda-rule-of-100.md](full/webveda-rule-of-100.md) |
| Postiz promo | Our open-source-scheduler promo short (orbit + calendar + b-roll) | [full/postiz-promo.md](full/postiz-promo.md) |
| BrandBuddies "Glossy Pitch" | Warm-room talking-head pitch: glossy 3D-blue keywords + white blueprint slides + mockup cards + iMessage CTA | [full/brandbuddies-glossy-pitch.md](full/brandbuddies-glossy-pitch.md) |
| Vaibhav style | ~90s numbered countdown listicle (#01→#N): warm PiP lower-third + giant lime number + rotating Apple-clean content beats, single lime accent | [full/vaibhav-style.md](full/vaibhav-style.md) |
| Short-form clip cutdowns | Fetched-footage 9:16 system + 3 variants: viral reaction (3:4 card, VO pauses for source audio), how-it's-made explainer (stage kickers), fullscreen nature-glow | [full/shortform-clip-cutdowns.md](full/shortform-clip-cutdowns.md) |
| Cars24 cutout explainer (v2, complete) | Keyed cutout host composited into worlds — green graph-paper grid OR real location B-roll (pump/showroom/highway). **DYNAMIC host positioning** (enters L/R/T/B, anchors corner/side/centre, zooms in/out, steps aside for B-roll), heavy real B-roll, minimal red stamp-label cards, yellow progression arrows, red rubber stamp; face always clear. Includes a full replication recipe. | [full/cars24-cutout-explainer.md](full/cars24-cutout-explainer.md) |
| **"Morning Edition" editorial print (APPROVED 2026-07-12)** | The recut that flipped "great website, bad video" → "really good": ONE literalized metaphor everywhere (history=front pages), **beat grammar = full-bleed plate + poster type + docked host**, taped/grained containers, stamps slam OVER host, statement serif walls ×2, topic foley + trendy hits. Beat molds are EVERGREEN; palette/world on 3-day cooldown. | [full/morning-edition-editorial.md](full/morning-edition-editorial.md) |

## Element styles (`elements/`)

### Transitions (`elements/transitions/`)
| Element | File |
|---|---|
| Circle-grow wipe (signature morph) | [elements/transitions/circle-grow-wipe.md](elements/transitions/circle-grow-wipe.md) |

### Animations (`elements/animations/`)
| Element | File |
|---|---|
| **Host positioning choreography** (moving keyed cutout: per-beat entrance L/R/T/B + anchor + zoom in/out + step-aside for B-roll) | [elements/animations/host-positioning-choreography.md](elements/animations/host-positioning-choreography.md) |
| **Robust anchoring (v4, AUTHORITY for anchor math)** (MANDATORY for cutout videos: face-anchored host `hX`/`hY`; host DEFAULT-ON every beat, side-docked + fun leans toward content — never mid-frame, never floating PiP; **≥50% of the avatar visible at any edge, head always fully in frame**, scale ≥0.85 grounded; element-anchored `circleEl`; stamps slam OVER host; fixed overlays outside the camera transform) | [elements/animations/robust-anchoring.md](elements/animations/robust-anchoring.md) |
| **Parallax world motion** (living bg: grid-floor drift, editorial-text pan, b-roll ken-burns + native motion, layered parallax coupling — Cars24) | [elements/animations/parallax-world-motion.md](elements/animations/parallax-world-motion.md) |
| "crushed DREAM" intro hero (thumbnail open) | [elements/animations/dream-intro-hero.md](elements/animations/dream-intro-hero.md) |
| Postiz orbit ring (icons rotate to equidistant) | [elements/animations/postiz-orbit-icons.md](elements/animations/postiz-orbit-icons.md) |
| Ken Burns zoom+pan b-roll (mobile-friendly) | [elements/animations/ken-burns-broll.md](elements/animations/ken-burns-broll.md) |
| Postiz calendar-fill signature | [elements/animations/postiz-calendar-fill.md](elements/animations/postiz-calendar-fill.md) |
| Numbered-badge draw-on | [elements/animations/numbered-badge-drawon.md](elements/animations/numbered-badge-drawon.md) |
| Siri / Apple-Intelligence glow border (seek-safe conic ring) | [elements/animations/siri-intelligence-glow.md](elements/animations/siri-intelligence-glow.md) |
| Parallax grid zoom / unzoom (squares assemble + focal hero) | [elements/animations/parallax-grid-zoom.md](elements/animations/parallax-grid-zoom.md) |
| Scrolling highlight list (vertical pan, active line bold — also a tall-page pan reveal) | [elements/animations/scrolling-highlight-list.md](elements/animations/scrolling-highlight-list.md) |
| Percent stat card (big % count-up, full-screen) | [elements/animations/percent-stat-card.md](elements/animations/percent-stat-card.md) |
| Comparison node-graph VS (two brand clusters, drawn-on edges) | [elements/animations/comparison-nodegraph-vs.md](elements/animations/comparison-nodegraph-vs.md) |
| **Flint chart draw-on** (real-data line/bar/pie → themed static SVG via `tools/flint_svg.cjs`; GSAP line draw-on / universal wipe — seek-safe) | [elements/animations/flint-chart-drawon.md](elements/animations/flint-chart-drawon.md) |
| Phone-stack community CTA (tilted 3D stack, "Want to stay…") | [elements/animations/phone-stack-cta.md](elements/animations/phone-stack-cta.md) |
| Giant two-tone hash + number (silver #NN backing + lime number, signature mark) | [elements/animations/giant-hash-number.md](elements/animations/giant-hash-number.md) |
| **RoughJS hand-drawn shapes & arrows** (sketchy SVG, fixed-seed = no flicker, stroke-dashoffset draw-on — DEFAULT for all arrows/circles/underlines) | [elements/animations/roughjs-handdrawn-shapes.md](elements/animations/roughjs-handdrawn-shapes.md) |
| **rough-notation annotate-on** (circle/underline/box/highlight/strike a DOM element — built on RoughJS, `animate:false`+fixed seed, GSAP draw-on; DEFAULT for circling a UI element or marking a word) | [elements/animations/rough-notation-annotations.md](elements/animations/rough-notation-annotations.md) |
| **GSAP plugins — full seek-safe set** (SplitText·DrawSVG·MorphSVG·MotionPath·Flip·ScrambleText·TextPlugin·CustomEase/Bounce/Wiggle·Physics2D — all FREE+vendored+validated; per-char reveals, stroke draw-on, shape morphs, path travel, shared-element morph across a cut, decode/typewriter text, projectile bursts) | [elements/animations/gsap-plugins.md](elements/animations/gsap-plugins.md) |

### Subtitles / captions (`elements/subtitles/`)
| Element | File |
|---|---|
| Blue solid caption box (webveda) | [elements/subtitles/blue-caption-box.md](elements/subtitles/blue-caption-box.md) |
| End CTA "comment" card (DM-the-link outro) | [elements/subtitles/comment-cta-card.md](elements/subtitles/comment-cta-card.md) |
| Numbered PiP lower-third (#NN module: PiP-left + silver # + lime number + caption) | [elements/subtitles/numbered-pip-lowerthird.md](elements/subtitles/numbered-pip-lowerthird.md) |
| Serif-italic hook (cold-open headline over AI concept image) | [elements/subtitles/serif-italic-hook.md](elements/subtitles/serif-italic-hook.md) |
| **Red-box sweep caption** (TikTok highlight — phrase holds, red box sweeps active word, NO per-word blink; long-running house default — rotate vs the recommended pair below per cooldowns) | [elements/subtitles/redbox-sweep-caption.md](elements/subtitles/redbox-sweep-caption.md) |
| **Editorial-emphasis captions — RECOMMENDED BODY system (the owner 2026-07-12)** (paper word-chips, ink Outfit 54px + red Playfair-italic 92px emphasis words; measured 9:16 port of registry `caption-editorial-emphasis`) | [elements/subtitles/editorial-emphasis-caption.md](elements/subtitles/editorial-emphasis-caption.md) |
| **Parallax statement wall — RECOMMENDED STATEMENT device (the owner 2026-07-12)** (giant red serif wall BEHIND the cutout host + front phrase line above, max 2/video; measured 9:16 port of registry `caption-parallax-layers` incl. the mandatory scaleX-fit) | [elements/subtitles/parallax-statement-wall.md](elements/subtitles/parallax-statement-wall.md) |

### Backgrounds / world loops (`elements/backgrounds/`)
Moving abstract loops that sit BEHIND the keyed cutout host (Cars24 house style). Real Mixkit +
Pixabay stock (free commercial, no attribution), dense-keyframe re-encoded → render-ready in
`assets/backgrounds/`. the owner-approved set (2026-06-23). Crop 16:9 → 9:16 with `object-fit:cover`.
**DEFAULT to the MINIMAL set** — low-distraction worlds so host + topic stay the focus.
| Set | Looks (when to use) | File |
|---|---|---|
| **Minimal (DEFAULT)** (4) | Halftone matrix (best default, dark mono) · Polygon lines (purple) · Plexus particles (dark+amber) · Hexagon data (cyan-on-black) — sparse, low-motion, best host contrast | [elements/backgrounds/cutout-world-loops.md](elements/backgrounds/cutout-world-loops.md) |
| **Energy / Mixkit** (5) | Hex texture · Node network (plexus on grid floor) · Code matrix · Dust particles (neutral) · Waveform bars — busier, for beats that want motion | [elements/backgrounds/cutout-world-loops.md](elements/backgrounds/cutout-world-loops.md) |

### Palettes (`elements/palettes/`)
| Palette | File |
|---|---|
| webveda Rule-of-100 | [elements/palettes/webveda.md](elements/palettes/webveda.md) |
| Postiz (violet/dark) | [elements/palettes/postiz.md](elements/palettes/postiz.md) |
| Vaibhav lime (lime-on-shifting-gradient) | [elements/palettes/vaibhav-lime.md](elements/palettes/vaibhav-lime.md) |
| Cars24 green (deep-green grid + yellow/red accents) | [elements/palettes/cars24-green.md](elements/palettes/cars24-green.md) |

### Finishing (`elements/finishing/`)
| Element | File |
|---|---|
| Warm finishing layer + b-roll color-match (one unified grade) | [elements/finishing/warm-finish-layer.md](elements/finishing/warm-finish-layer.md) |
| **Editor texture pass** (MANDATORY on containers: tape + paper grain + hard offset shadows + highlighter kickers + worn-ink stamps — kills the "AI card" look) | [elements/finishing/editor-texture-pass.md](elements/finishing/editor-texture-pass.md) |

---

## Ready-made components (`compositions/components/`) — paste-in HTML, seek-safe
Unlike the spec files above, these are **drop-in HTML snippets** (CSS-var themable, no
rAF/Date/Math.random — HyperFrames seeks them frame-by-frame). Paste the `<style>`/markup
into a composition. CodePen-derived ones are adapted & re-tinted warm (MIT, credited in
`assets/common/CREDITS.md`); see the comment header in each file for usage + vars.
| Component | What it does | Adapted from | File |
|---|---|---|---|
| Glow border | Rotating conic-gradient glow ring to highlight a card/stat | CodePen "Magic Card" (gayane) | [glow-border.html](../compositions/components/glow-border.html) |
| Light streaks | Sweeping light bars — transition wipe / logo-outro accent (Netflix-free) | CodePen "Netflix Intro" (claudio_bonfati) | [light-streaks.html](../compositions/components/light-streaks.html) |
| Wave underline | Single animated SVG wave — caption underline or low-opacity bg ribbon | CodePen "SVG wave" (elwinvdhazel) | [wave-underline.html](../compositions/components/wave-underline.html) |
| Text gradient fill | Moving gradient/texture flows through letters (local, no PNG dep) | CodePen "Animated text fill" (zitrusfrisch) | [text-gradient-fill.html](../compositions/components/text-gradient-fill.html) |
| Orbit system | Concentric rings + planets, ambient bg for scale/reach beats | CodePen "Solar System" (kowlor) | [orbit-system.html](../compositions/components/orbit-system.html) |
| Text shatter | Letters fly apart / snap together — shock / "myth busted" beats (deterministic) | CodePen "Shattering Text" (ARS) | [text-shatter.html](../compositions/components/text-shatter.html) |
| Shimmer sweep | Light pass across text/elements | HyperFrames registry | [shimmer-sweep.html](../compositions/components/shimmer-sweep.html) |
| Grain / vignette | Texture overlays | HyperFrames registry | [grain-overlay.html](../compositions/components/grain-overlay.html) · [vignette.html](../compositions/components/vignette.html) |
| Parallax zoom / unzoom | Hero card scales to full-frame while siblings parallax out | HyperFrames registry | [parallax-zoom.html](../compositions/components/parallax-zoom.html) |
| **UI design-style pack (10 looks)** | 10 drop-in surface treatments for cards/panels/buttons — one class per look. Pick ONE per video for a fresh visual fingerprint. | IG reel decode (topic_fetch/ig_styles) | [ui-design-styles.html](../compositions/components/ui-design-styles.html) |

### UI design-style pack — pick one look per video (decoded from IG reel, 2026-06-15)
Drop-in, **fully static** (zero rAF/Date — seeks perfectly). Paste the `<style>` once,
add `.ds-card` + a look class to any card/panel/button. CSS-var themable
(`--ds-accent`, `--ds-surface`, per-style fill vars). Proof sheet:
`topic_fetch/ig_styles/ui_styles_sheet.png`. **Use these to vary the LOOK** (helps the
3-day STYLE cooldown — a different surface language = a different fingerprint).

| # | Style | Class | The look (when to use) |
|---|---|---|---|
| 1 | Skeuomorphism | `.ds-skeu` | Real materials: metal/leather, glossy bevel, deep drop shadow. Retro / tactile / "physical device" beats. |
| 2 | Neumorphism | `.ds-neu` | Soft UI: element == bg color, light+dark twin shadow. Calm minimal dashboards (needs matching bg; `.ds-neu--inset` for pressed). |
| 3 | Glassmorphism | `.ds-glass` | Frosted translucent panel over a colorful blurred backdrop. Layered cards, needs something vivid behind. |
| 4 | Minimalism | `.ds-min` | Linear/Vercel clean: white, hairline border, whitespace, one accent. Premium SaaS / "less is more". |
| 5 | Maximalism | `.ds-max` | Spotify-Wrapped: vivid gradient, huge type, black highlight blocks (`.ds-mark`). Loud hype reveals. |
| 6 | Brutalism | `.ds-brut` | Thick black border, hard offset shadow (no blur), zero radius, mono. Edgy / dev / "raw" energy. |
| 7 | Liquid Glass | `.ds-liquid` | Apple iOS-26: glass + specular refraction rim, pill buttons. Sleek Apple-flavored beats. |
| 8 | Bento Grid | `.ds-bento` + `.ds-bento-tile` (`--c`/`--r` span) | LAYOUT, not a card: tight grid of varied rounded tiles. Feature grids / spec dashboards. |
| 9 | Spatial UI | `.ds-spatial` | visionOS: floating panel w/ big grounded shadow + glass. Depth / "in the room" overlays. |
| 10 | Claymorphism | `.ds-clay` | Puffy 3D clay: chunky radius, pastel fill, twin inner shadow. Playful / friendly / kids-app vibe. |

> **ALL 113 registry blocks/components are installed** — the master index with use-cases,
> restrictions, and the Director⇄Bella usage contract is `docs/guides/MOTION_LIBRARY.md`
> (PRIMARY JOB to use it well — the owner, 2026-06-11). Reference-only CodePen pens to adapt
> live in `docs/motion-ref/codepen/`; curated GSAP official demos in
> `docs/motion-ref/GSAP_DEMOS_CATALOG.md`.

---

## How to add to this library
- New full video → add `full/<name>.md` (overview, palette, scene-by-scene table with
  start/dur, and a "links to elements" list). Then add a row to the Full-styles table above.
- New reusable piece → drop it in the right `elements/<category>/` file (transitions,
  animations, subtitles, palettes). Add a row above. Keep MEASURED/real values (hex, px,
  timings, easings) — no eyeballing.
- All HyperFrames motion must be SEEK-SAFE on the GSAP timeline `tl` (no rAF/Date).
- Keep reference frames/grids alongside: `~/workspace/workspace/fb_ref/` (webveda),
  project `out/` QA grids (postiz).
