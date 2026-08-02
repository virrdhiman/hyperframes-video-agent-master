# Short-Form Vertical Editing & Kinetic-Typography Rules

Research distilled from YouTube teaching videos + creator-craft articles, codified for our
HyperFrames 9:16 pipeline. Each rule cites a source + timestamp (where the source is a video) and
states **how we apply it in HyperFrames**.

Our current failure modes this is meant to fix:
- flat, even pacing (every scene the same length / same energy)
- text overlap & clutter (reveals colliding, captions over the subject)
- dark empty backgrounds (dead negative space, "programmatic video" feel)
- no tasteful meme / iconic-clip beats (no humor, no pattern interrupt)

---

## A. PACING — kill the flat, even rhythm

### A1. Establish a neutral shot length, then deviate on purpose
Pacing is varied, not constant. Pick a neutral average shot length and intentionally go shorter
for energy/urgency and longer to let a moment land. Monotone shot length = the "boring video"
signature.
- Source: Visla "Video Editing Pacing" guide; AIR Media-Tech retention-editing guide.
- **HyperFrames:** stop authoring scenes at a fixed ~4s cadence. Define each scene's `energy`
  (`hot` 0.8–1.5s, `mid` 2–3.5s, `cool` 4–6s) and **never place 3+ same-energy scenes in a row**
  (already a CLAUDE.md rule — now drive it from an explicit per-scene energy field in scenes.json).

### A2. Two-mode rhythm: micro-cut explanation vs. slow-focus hold
Alternate "fast explanation" (a visual change every 10–15s of talk, or every 1–3s of cuts) with
"slow focus" holds up to ~40s when a single visual deserves attention.
- Source: AIR Media-Tech "advanced retention editing"; Visla pacing guide.
- **HyperFrames:** within one video, mix bursts of 1–2s b-roll/word-pop scenes with one or two
  deliberately held hero shots (a Ken-Burns'd image or looping b-roll) — the hold *reads as
  intentional* only because the surrounding scenes are fast.

### A3. Frame must change every 2–4s minimum
High-performing shorts average one cut / visual change every 2–4s; each change "resets" attention.
- Source: OpusClip + vidIQ hook/retention articles; consistent across all retention sources.
- **HyperFrames:** if a scene exceeds ~4s with no new motion, add an *internal* change — a word-pop,
  a b-roll swap, a zoom-punch, an icon entrance — rather than holding a static frame.

### A4. Pattern interrupt at the midpoint (and every 30–60s)
The 50% mark is the second-biggest drop-off after the first 3s. Insert a deliberate mode switch
there: narration → graphic, new example, direct question, or a music/SFX shift.
- Source: OpusClip retention article; AIR Media-Tech (pattern interrupts every 30–60s).
- **HyperFrames:** for any video >40s, script a mid-video "gear change" scene with a distinct
  background/aesthetic + a punchy SFX so it visibly breaks the rhythm.

### A5. Contrast: follow hot with cool, silence with sound
Retention rises on contrast — a hard/fast cut followed by a soft beat, a silent moment broken by a
sudden sound. The brain uses the break to tag the moment emotionally.
- Source: Brandefy "Psychology of Video Editing"; AIR funny-video editing guide.
- **HyperFrames:** use the `[PAUSE]` windows we already cut for VO as *designed* beats — drop music to
  0.45 and let one strong visual sit there, then snap back to dense pacing.

---

## B. HOOK — first 3 seconds

### B1. 50–60% of drop-off happens in the first 3 seconds — engineer them
The 3-second hold is the threshold the algorithm uses to decide distribution. The opening frame
must be visually striking, the first words must promise payoff, pacing feels urgent.
- Source: OpusClip "Shorts Hook Formulas"; vidIQ viral-hooks article.
- **HyperFrames:** scene 0 is never a slow logo/title fade. Open on motion (real footage or a fast
  word-pop), 4–7 word on-screen hook in the top safe zone, land it **with sound off**.

### B2. Open with a pattern interrupt in the first second
Hard cut, whip-pan, snap-zoom, or a visual mismatch in second 1 to trigger curiosity. Start
mid-sentence if needed; hook = one sentence max.
- Source: OpusClip hook article; vidIQ.
- **HyperFrames:** allow a snap-zoom (GSAP scale with an overshoot ease, e.g. `back.out(2)`) or a
  hard cut between two framings on the first beat instead of easing in.

### B3. Write the hook and the payoff before anything else
Decide the first-3s hook and the final-3s payoff up front; loopability (end implies the start)
boosts replays.
- Source: OpusClip/UpMyViews shorts-strategy articles.
- **HyperFrames / pipeline:** add `hook` and `payoff` fields to the project brief; the last scene
  should visually rhyme with the first to invite a loop.

---

## C. CAPTIONS / KINETIC TYPOGRAPHY — make text pop, never clutter

### C1. Word-by-word reveal with a highlighted active word (Hormozi spec)
Each word pops on as spoken; the active word is highlighted (classic = yellow) while prior words
stay white. Font: Montserrat / Poppins / Anton / Bebas Neue **BOLD**. 2–3 fonts max.
- Source: Riverside + Submagic Hormozi-caption guides; CapCut caption-style guide.
- **HyperFrames:** our caption layer (per-word reveal from the transcript) should highlight the active word
  (scale-up + accent color), not just fade lines in. One bold sans, heavy weight, large.

### C2. The scale-pop-and-hold is the baseline reveal
Core kinetic move: word/line scales up fast with overshoot, then **holds** (hold-keyframes), with
motion blur on the pop. Bottom-up position + opacity is the clean default.
- Source: Kinetic-Type Techniques video (https://www.youtube.com/watch?v=sN2GQ5tTKI0) ~[1:00–3:00]
  scale/hold technique; Kinetic Typography #4 (https://www.youtube.com/watch?v=4vLwhXY0ZRw)
  [0:26–3:00] bottom-up opacity+position pop with comp-level motion blur.
- **HyperFrames:** GSAP scale 0.6→1.0 with an overshoot ease (`back.out(1.7)`), translateY +24→0, plus
  a brief motion-blur (CSS `filter: blur()` ramp or a duplicated-trail) on the pop frame. Then *hold* — don't keep animating idle text.

### C3. A small library of reusable text moves (don't reinvent per video)
Five patterns cover almost everything: (1) scale-pop hold, (2) horizontal scroll/marquee,
(3) typewriter / mask-wipe reveal, (4) 3D extrude pop for a single impact word, (5) shape-box
"jump-out" where a word leaps from a colored box.
- Source: Kinetic-Type Techniques video (https://www.youtube.com/watch?v=sN2GQ5tTKI0):
  scroll [~5:30], mask/typewriter reveal [~10:30], 3D extrude [~15:00], box jump-out [~21:00].
- **HyperFrames:** build these as 5 props/variants on one caption component; pick per scene for
  variety instead of one identical reveal every time (a major cause of "programmatic" feel).

### C3b. Staggered-tracking "echo" reveal for a single impact word/line
Observed in the grid: a line ("TECHNIQUE 01") is duplicated 6+ times stacked vertically; each copy
is offset in time and animates its **letter-spacing/tracking** open, so the word appears to echo/
ripple into place. Strong, cheap "designed" moment for a section title or one big keyword.
- Source: Top 5 Kinetic Type Techniques (https://www.youtube.com/watch?v=sN2GQ5tTKI0) intro card
  [~0:39 / grid kinetic-type-intro.jpg frame 39.0s] — vertical stack of the same line with
  progressively wider tracking, time-offset per copy.
- **HyperFrames:** render N copies of one impact line in a column, stagger each copy's start by
  ~2–3 frames, animate `letterSpacing` 0→wide with an overshoot ease; fade trailing copies. Use for the
  hook keyword or a section divider, **not** for body captions.

### C4. Keep idle text alive (subtle), don't freeze it
Even held text can have a micro-loop (turbulent displace / gentle drift) so the frame never feels
dead — but keep it subtle.
- Source: EASY Kinetic Typography (https://www.youtube.com/watch?v=l2868rcHXSw) [~2:00] turbulent
  displace loop; Fun Kinetic Typography (https://www.youtube.com/watch?v=1hcNQyyZzm8) progress-
  driven stroke reveals.
- **HyperFrames:** add a ±1px/±0.3° sine drift to held captions/cards (cheap, sells "alive").

### C5. Tracking/letter-spacing & weight do the design work
Uppercase impact lines need letter-spacing; bold weight + tracking is what makes type read as
"designed" vs default.
- Source: CapCut caption-style guide; matches our house rule (letter-spacing 2–6 on uppercase).
- **HyperFrames:** keep the existing 2–6 tracking rule; pair with heavy weight + thick drop shadow
  (`4px 4px 0` accent) for legibility on busy b-roll.

---

## D. TEXT LAYOUT — stop the overlap & clutter

### D1. One idea on screen at a time — sequence, don't stack
Word-by-word/line-by-line means only the words being spoken are present; old text clears before
the next phrase. Overlap happens when reveals run concurrently.
- Source: Hormozi-caption guides (word-by-word); video-essay editing (one point at a time).
- **HyperFrames:** caption phrase N must fully exit (or the prior card unmount) before phrase N+1
  enters. Don't mount two text blocks in the same safe zone simultaneously.

### D2. Reserve safe zones; never put captions over the subject's face
Captions/hooks live in top/bottom safe zones; keep overlays off the talking-head face. Big,
readable, high-contrast.
- Source: OpusClip hook article (top/bottom safe zones); our editor-mindset memo (overlays off face).
- **HyperFrames:** define top (≈12–22%) and bottom (≈70–88%) caption bands; auto-avoid the center
  third where the head sits. Our grid-review QA step exists exactly to catch face/text collisions.

### D3. Cap brand cards; prefer footage > head > split > list > card
Too many editorial cards/lists = template feel. Real footage and reaction beats carry attention.
- Source: our house style (CLAUDE.md) reinforced by retention sources (visual variety > static cards).
- **HyperFrames:** max 2 brand cards per video; lead with real/loop b-roll and motion, not stacked
  bullet cards on a dark background.

### D3b. Maximalist collage as the anti-"dark empty background"
The finished animation in the grid is a packed, bright collage: color-blocked panels, thick
outlined type, geometric shapes and stickers filling the frame ("SPEED UP YOUR WORKFLOW", "50%",
"PURE IMAGINATION"). Density + bold flat color is the opposite failure mode from our flat dark
frames — it always has something to look at, yet stays readable via strong figure/ground and big
type. (Matches our brand-autopsy physical-collage aesthetic.)
- Source: Fun Kinetic Typography (https://www.youtube.com/watch?v=1hcNQyyZzm8) grid frames
  99s / 176s / 220s / 253s / 297s.
- **HyperFrames:** for impact/title scenes, layer 3–6 rotated colored blocks/stickers behind the
  type (±3–4° per house rule), thick drop shadows, one dominant keyword huge. Beats a single
  centered word on black every time.

### D4. Kill dark empty backgrounds — fill negative space with motivated motion
Static dark frames read as "dead air" in the grid QA. Idle/empty = drop-off.
- Source: grid_review.py QA criteria (empty/half-black frames flagged); pacing sources (no static).
- **HyperFrames:** behind text use a looping animated bg (we already have
  `common/backgrounds/abstract-*-9x16.mp4`), a Ken-Burns image (base scale ≥1.08), or grain/drift —
  never a flat fill. Negative space should hold *motivated* motion, not nothing.

---

## E. B-ROLL & MEMES — motivated visuals + tasteful humor

### E1. B-roll must be motivated — it illustrates the exact word being said
Cut to footage/stills/animation that ties to the specific point at that moment; b-roll fills the
gaps you marked while watching, and directs the eye (circles/zooms to point at things).
- Source: How To Make A Video Essay: Editing (https://www.youtube.com/watch?v=Z2z514tcwpc)
  [~0:40–3:57] lay clips to VO, fill gaps with new footage, use circles/graphics to point.
- **HyperFrames:** every b-roll choice maps to a noun/verb in the VO line under it; loop short clips
  to fill; use an animated circle/arrow/zoom-punch to point at the thing being named.

### E2. Comedy timing: cut to the reaction/punchline as fast as possible
A well-timed cut makes the joke. Cut to the reaction immediately after the punchline; slow down a
beat to savor it; speed up mundane action to make it comically frantic; punch in with a fast zoom.
- Source: AIR "editing tricks for fast-paced funny videos"; video-essay editing.
- **HyperFrames:** for a punchline beat, hard-cut to the meme/reaction on the exact frame of the
  punch word; optionally `slow` (time-stretch) the held reaction, or snap-zoom for emphasis.

### E3. Memes / iconic clips = punctuation, not wallpaper — and keep them fresh
Memes punctuate commentary (Danny-Gonzalez style); fresh ones keep audiences entertained, stale
ones date the video. They are a pattern interrupt, used sparingly on a specific beat.
- Source: AIR funny-video guide (memes as references that punctuate; freshness matters).
- Concrete pattern (grid fun-kinetic-type.jpg): an instructional/explainer video drops short
  iconic film clips on punchline beats, sometimes with a comic speech bubble overlay re-captioning
  the clip — e.g. [187s] a movie still with bubble "The stroke needs to be thicker!", [275s] an
  office worker with "Because you didn't plan it!!". The clip itself is mundane footage; the
  overlaid bubble + timing is the joke. ~5–6 such inserts across a ~5min video = roughly 1 per
  45–60s, never two in a row, always cutting straight back to the through-line.
  Source: Fun Kinetic Typography (https://www.youtube.com/watch?v=1hcNQyyZzm8) grid frames
  44s / 187s / 209s / 231s / 275s.
- **HyperFrames:** insert a meme/iconic clip ONLY on a punchline or pattern-interrupt beat (≈1 per
  20–30s, not back-to-back), as a 0.8–2s hard-cut insert with its own SFX, then cut straight back
  to the through-line. Fetch the clip to `public/<slug>/` first (no external CDN at render time).

### E4. Speed-ramp & zoom for emphasis, not decoration
Speeding mundane action up or slowing a reaction down adds humor/emphasis; fast zoom-ins make a
beat "epic". Use as accents on specific moments.
- Source: AIR funny-video editing guide.
- **HyperFrames:** reserve snap-zoom / speed-ramp for the 1–2 biggest beats per video; overuse turns
  back into flat (everything emphasized = nothing emphasized).

---

## F. SOUND — pacing is half audio

### F1. Music is emotional architecture; match BPM to section energy
Music tells the viewer how to feel about the pacing. Slower 60–80 BPM for teaching/emotional;
100–120 BPM for builds/transitions. Edit cuts to land on the beat.
- Source: Brandefy psychology-of-editing; soundimages pacing guide; video-essay (cut to soundtrack).
- **HyperFrames:** pick bg music BPM per video energy; align hard cuts/word-pops to beat frames where
  possible. Keep our level rules (music 0.12 under VO, 0.45 in pauses, 0.3s ramp).

### F2. SFX punctuate the cut — whoosh on motion, impact on reveal
Sound effects (whoosh, pop, impact) reinforce cuts and reveals and lift "okay" moments.
- Source: AIR funny-video guide; our SFX-level rules.
- **HyperFrames:** keep whooshes 0.7 / impacts 0.55–0.6 / pops on word reveals; give each `<audio>`
  its own `data-start` / `data-duration` / `data-volume` so it doesn't bleed. Anything <0.25 is inaudible in the mix.

---

## Quick checklist for the redesign (paste into a brief)

- [ ] Per-scene `energy` field (hot/mid/cool); no 3 same-energy in a row.
- [ ] Frame changes ≥ every 2–4s; long holds only as deliberate contrast.
- [ ] Hook scene: motion + 4–7 word top-safe-zone text, lands sound-off, snap/cut not fade.
- [ ] Mid-video pattern-interrupt scene (>40s videos).
- [ ] Captions: word-by-word, highlighted active word, bold sans, 5-variant reveal library.
- [ ] One text block per safe zone at a time; phrase N exits before N+1; face stays clear.
- [ ] No flat dark backgrounds — looping bg / Ken-Burns / drift behind all text.
- [ ] Each b-roll motivated by the spoken word; point with circle/zoom.
- [ ] ≤1 meme/iconic clip per 20–30s, on a punchline beat, with SFX, hard-cut in and out.
- [ ] Music BPM matched to energy; cuts on beat; SFX on every reveal; levels per house rules.
- [ ] Run grid_review.py; fix dead frames, text/face collisions, frozen b-roll; re-grid.
