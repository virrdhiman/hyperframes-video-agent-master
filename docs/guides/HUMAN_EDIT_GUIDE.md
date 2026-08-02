# HUMAN_EDIT_GUIDE.md — make the cut feel human-made (the owner, 2026-06-11)

**Mandatory read for the Director (when writing the BRIEF) and Bella (when building).**
Our cuts are clean but read "AI-deck-like": flat CSS cards, perfectly centered layouts,
static holds, no real-world texture. A human editor adds life by default. These rules close
that gap. The QA pass checks them (soft-fail: Director cites which rule and where).

---

## 1) NOTHING SITS STILL — motion on every element, always
A human editor never leaves a frame frozen. Agents do it constantly.
- **No static hold >1.5s.** Every card, still, or b-roll window gets continuous subtle
  motion for its whole lifetime: slow scale push (1.00→1.04 over the beat), Ken Burns
  pan on stills (see `styles/elements/animations/ken-burns-broll.md`), or a 2–4px drift.
- **Numbers count up, bars race, rings sweep** — never pop in at final value.
- **The avatar gets punch-ins**: on 2–3 emphasis words per video, scale the full-bleed
  avatar 1.00→1.06–1.10 with a snap ease (power3.out, ~0.25s). This is the single most
  human-feeling move in talking-head shorts and we currently never do it.
- **Micro-imperfection**: tilt cards ±0.5–1° instead of perfectly straight; stagger
  multi-element reveals by 0.06–0.12s instead of simultaneous; vary easings (back.out,
  power4.inOut) — never the same ease twice in a row, never linear.
- All motion must stay SEEK-SAFE on the GSAP timeline `tl` (no rAF / Date / random).

## 2) REAL IMAGERY BEATS DRAWN UI — every abstract claim gets a concrete picture
A human reaches for a *photo* of the thing; agents reach for a styled `<div>`.
- Pure-CSS beats are capped: **max 2 consecutive CSS-card beats** before a beat with real
  or AI-generated imagery (b-roll, screenshot, product UI, generated scene).
- Logos live in scenes, not flat: prefer "the logo as a physical object in a lit room"
  (AI-generated, §5) over a vector mark on a gradient.
- Screenshots of real artifacts (the actual leaderboard page, the actual pricing page,
  the actual tweet) are stronger than our re-drawn version — re-style only when the
  source is visually unusable.

## 2b) IT'S A VIDEO, NOT A WEBSITE (the owner, 2026-07-12 — from the Morning Edition recut)
The first build of retrofit-2026-07-11 was rejected as "great website, bad video". The
recut that got "this is really good" changed exactly these things — they are now RULES:
- **Full-bleed imagery behind data beats.** A number/stat/date beat never sits on the flat
  world bg — put a full-bleed plate behind it (AI-generated scene per §5, stock b-roll, or
  the topic's own footage, graded down `brightness(.72–.8)`) and set poster-scale type ON
  the footage. Cards on a flat background = website.
- **Poster type over footage beats cards.** Prefer 200–430px Anton/serif type composited
  on the plate (cream/red, deep text-shadow) over a rounded-corner card holding 100px text.
  Cards are for *clippings/evidence* (photos, logos, tickets), not for every stat.
- **Host presence is DEFAULT-ON, docked.** The host appears at (nearly) every beat, docked
  to a left/right edge, angled, grounded (see `styles/elements/animations/robust-anchoring.md`).
  Host-off is the exception (hero/AI beats), never the default. A video where the host
  vanishes for 8s stretches reads as a slideshow.
- **Stamps and key stats may slam OVER the host** (z above host). SOLD OUT / PRICIER / 7×
  landing across his chest is an editor move; politely tucking them beside him is a UI move.
- **Editor-texture pass on every container** — tape, grain, hard offset shadows, highlighter
  kickers, worn-ink stamps: measured CSS in `styles/elements/finishing/editor-texture-pass.md`.
  Clean vector cards with soft blur shadows read AI.
- **SFX identity per topic.** Pick a foley language that belongs to the story's world (print
  room = paper slaps, stamp thunks, ticker clicks) + 1–2 trendy hits (vine boom) on the two
  biggest emphasis words + risers into each number payoff. ~30+ cues per 60s. A dry VO over
  motion is the #1 "bot" tell after white balance.

## 3) PACING IS FELT — cut on words, breathe before twists
- Cut **on** the spoken word, not ~0.2s after it (agents consistently land late — read
  the word timestamps from `words.js` and align reveals to the word's *start*).
- **Breathing room before the twist/reveal**: 0.3–0.5s where motion settles and music
  swells — then hit. Constant density reads robotic; contrast creates the hit.
- Hard cuts remain the base grammar; AI motion lives *inside* shots, not as dissolves.

## 4) TEXTURE — the invisible 5% that makes it filmic
- The warm finishing grade (`FINISHING_GRADE.md`) is on; additionally use the common
  overlay pack `assets/common/overlays/` (fetched 2026-06-11: grain_*, lightleak_*,
  dust_* — black-background clips composite with `mix-blend-mode: screen`) at 4–8%
  opacity over b-roll and AI-generated clips. Preview each overlay before first use and
  catalogue the good ones in `COMMON_ASSETS.md`; refetch more with
  `python3 tools/stock_fetcher/pixabay.py -q "<kind> overlay" -o assets/common/overlays`.
- Color-match every external/AI clip warm (the existing rule) — mismatched white balance
  is the #1 "assembled by a bot" tell.

## 5) AI-GENERATED ASSETS — bespoke imagery nobody else has
Tool: `tools/ai_assets/replicate_gen.py` (Replicate; the Google-key tools
`imagen.py`/`veo.py` are DEAD — suspended key). Costs real money: budget **≤4 images +
≤2 motion clips per video**, and every generated asset goes through the owner's normal
asset-approval gate (step 4b) like any other asset.

### Recipe A — brand/logo → lifelike still → motion b-roll
For topic-brand beats (e.g. the Claude launch), don't show a flat logo — build a scene:
```bash
# 1) lifelike branded still grounded on the official logo
python3 tools/ai_assets/replicate_gen.py image \
  -p "the <brand> logo as a <material> object in <real-world scene>, photorealistic, \
      warm soft light, shallow depth of field" \
  --ref-image projects/<slug>/assets/<official-logo>.png -r 9:16 -o projects/<slug>/assets/ai
# 2) animate it into a 5s motion clip (this is the wow b-roll)
python3 tools/ai_assets/replicate_gen.py i2v \
  -p "slow cinematic push-in, <one motion idea: dust motes / flicker / parallax>" \
  --image projects/<slug>/assets/ai/nb2_01.png --duration 5 -o projects/<slug>/assets/ai
```
Material/scene ideas: clay sculpture on a desk · neon sign on brick · embroidered patch ·
carved wood · balloon in an office · etched glass. Match the video's palette in the prompt.

### Recipe B — the owner-in-a-scenario cutaway (quirky explainer beats)
Put the owner *into* the story for one beat (him at a 2am debugging desk, him holding a
giant "95%" trophy, him buried in API bills). Ground the identity on a REAL frame:
```bash
# 1) grab an identity reference from today's A-roll (he faces camera ~2s in)
ffmpeg -y -ss 2 -i projects/<slug>/avatar.mp4 -frames:v 1 projects/<slug>/assets/ai/face_ref.jpg
# 2) scenario edit — keep the face EXACTLY his
python3 tools/ai_assets/replicate_gen.py image \
  -p "this exact man, same face and glasses, <scenario>, cinematic warm light, photorealistic" \
  --ref-image projects/<slug>/assets/ai/face_ref.jpg -r 9:16 -o projects/<slug>/assets/ai
# 3) optional: 5s of motion (subtle — he reacts, light shifts; avoid mouth movement)
python3 tools/ai_assets/replicate_gen.py i2v -p "subtle natural motion, he <small action>, \
  camera slowly pushes in" --image projects/<slug>/assets/ai/<still>.png --duration 5 \
  -o projects/<slug>/assets/ai
```
**Likeness rules (hard):** only ever from a real captured frame/photo of the owner — never
invent his face from text. No mouth-flap motion (uncanny without audio). Scenario stills
of the owner ALWAYS go in the approval shortlist clearly labeled "AI edit of your likeness" —
he approves each one. (The old "never generate a fake face" rule still holds for the
*thumbnail* placeholder; grounded scenario cutaways approved via the gate are the
sanctioned exception — the owner, 2026-06-11.)

### Recipe B2 — founder/figure-led open (event & release videos)
When the story has a known face (Dario, Sam, Sundar, Jensen, Zuck, Tim…), humans lead with
the *person*, not the product card — "Dario just cooked" beats "95% SWE-bench" as a cold open.
- Source a REAL press/keynote photo (Serper image search / the official YT clip frame —
  fair-use editorial; never AI-invent a public figure's face).
- Classic treatment: cut out (`tools/image_generator/background_remover.py`), desaturate to
  B&W, drop on a bold accent background with a big claim word — the webveda
  `dream-intro-hero` element is the measured reference. **One proven option, NOT a strict
  rule** — equally valid: color cutout in a torn-paper frame, duotone in the video's accent,
  or the photo inside a "breaking"-style card. Vary it per the cooldown like any fingerprint.
- Optional: nano-banana edit to restage the photo (stylized poster look), or wan i2v for a
  subtle 3-5s parallax/zoom on the cutout — same approval-gate rules as every AI asset.

### Recipe C — concept b-roll when stock fails
When Pexels/Pixabay has nothing for an abstract beat ("a model thinking", "context
window"), generate the exact metaphor instead of settling for generic server-rack stock:
still via `image` (match palette), motion via `i2v`. Label source as "AI-generated" in
the shortlist + CREDITS.
- Generated video is NOT render-ready: dense-keyframe re-encode like any external clip
  (`BROLL_GUIDE.md`), then color-match warm (§4).

## 5b) PREMADE MOTION LIBRARY — PRIMARY JOB (the owner, 2026-06-11)
Humans reach for proven, polished motion pieces; agents rebuild everything from scratch.
**`MOTION_LIBRARY.md` is THE master index — Director shops it per beat, Bella executes
themed. That file's "contract" section is binding.** Sources in order — generate only
when nothing premade fits:
1. **HyperFrames registry — ALL 113 blocks/components installed locally** in
   `compositions/` + `compositions/components/` (categorized with use-cases and
   restrictions in MOTION_LIBRARY.md): caption styles, shader transitions, text effects,
   **x-post / reddit-post** (cite real posts as animated cards — far better than a
   screenshot), maps, apple-money-count, vfx-iphone-device, code-snippet themes,
   logo-outro, data-chart… `npx hyperframes catalog` to browse new additions.
2. **Premade Lottie pack** `assets/common/lottie/` (Noto Animated Emoji — confetti, boom,
   fire, eyes, 100, mind-blown, chart-up, siren…) + on-demand fetch of ~600 more:
   `python3 tools/stock_fetcher/noto_lottie.py --emoji "🎯" --name target`. CC BY 4.0 —
   credit Google in post.md when used.
3. **GSAP official demos** — `docs/motion-ref/GSAP_DEMOS_CATALOG.md` is the curated
   render-usable subset of demos.gsap.com (text-scrambling, rolling-number odometer,
   MorphSVG morphs, DrawSVG draw-ons, MotionPath travel…). All GSAP plugins free since
   3.13. Fetch each demo's embedded pen with the codepen tool below.
4. **CodePen motion references** — any public pen is fetchable despite Cloudflare via
   CodePen's embed CDN: `python3 tools/stock_fetcher/codepen.py <pen-url>` →
   `docs/motion-ref/codepen/<name>.html` (MIT-licensed, auto-credited). These are
   REFERENCES to adapt, not drop-ins: CSS-keyframe pens port near-verbatim (the
   css-animations skill makes them seekable); JS/rAF/random-driven pens must be rebuilt
   as paused GSAP timelines. Already saved: `svg-stroke-text-drawon.html` (handwriting
   stroke-dashoffset letter draw-on — great hook-text treatment). When an adapted pen
   works in a video, save the measured spec to `styles/elements/` like any element.
5. **text-to-lottie skill** — bespoke generation, LAST resort for accents (still first
   choice for brand-specific stings like the Retrofit logo).
**Transitions caveat:** hard cuts stay the BASE grammar. A registry shader transition is
allowed at most 1–2× per video, on the single biggest beat change, and only when specced
in the BRIEF (the owner, 2026-06-11 — softens the old hard-cuts-only absolute). Never
back-to-back transitions; never on ordinary cuts.

## 6) SOUND IS PART OF THE EDIT
Follow `AUDIO_GUIDE.md` §2a (level cap + per-cue `dur` trims — mechanical now). The
human layer on top: the music bed should *move* with the story — pick a bed with a
natural build for the reveal; never let a heavy SFX land on a word the viewer must hear.

## QA additions (Director checks at grid-QA)
- [ ] no static element >1.5s (spot-check 3 random mid-beat frame pairs 0.5s apart)
- [ ] ≥1 avatar punch-in on an emphasis word
- [ ] no run of >2 consecutive pure-CSS beats
- [ ] AI assets (if any) color-matched + textured, faces = real the owner only, approved in 4b
- [ ] every SFX cue has a `dur` (except riser/swell) and respects the -4dB cap
- [ ] **HOST GRID**: `npx hyperframes snapshot --at <every host beat>` → build a labeled grid;
      every host is side-docked + angled (never mid-frame), grounded (bottom cut off-frame,
      scale ≥0.85), face fully visible (no 40%-face edge slivers), face never covered
- [ ] **texture pass present**: tape/grain/hard-shadow on cards, ink speckle on stamps,
      highlighter on kickers (§2b) — a clean soft-shadow card is a FAIL
- [ ] every data beat has a full-bleed plate/footage behind it (no stat on flat world bg)
