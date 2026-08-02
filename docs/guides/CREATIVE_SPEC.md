# Retrofit AI — Creative Spec (standing context)

The creative + operating contract for the "Retrofit AI" short-form vertical feed
(9:16, 1080×1920, 30fps). Follow it unless the user overrides. Adapted for this
**HyperFrames** project; the original was written for a Remotion/server pipeline —
server-only bits (HeyGen A-roll automation, `--gl` render flags, SOCKS proxy, `Root.tsx`)
are noted as **[Remotion/server — N/A here]** and don't apply to local HyperFrames editing.

> ✅ **DIRECTION RESOLVED — LIGHT wins (standing rule).** This feed is **LIGHT + warm +
> physical/editorial**: warm off-white / paper grounds + ONE brand accent + ink text. The old
> §2 "dark near-black" wording and the `OpenAIBedrockMain_v3` "dark cinematic" build
> ([BEDROCK_V3_BLUEPRINT](../reference/bedrock-v3-blueprint.md)) are **SUPERSEDED** — kept only
> as historical/structural reference, never a palette reference. Do NOT restyle dark.

## 0) Scope & mission
Niche = AI & tech, practically useful. Pillars: (1) AI news/launches, (2) genuinely useful
AI tools ("tools to help" — favor actionable), (3) tech-business (AI's impact on companies,
funding, markets), (4) broader tech with an AI angle. Pick stories with a strong hook + a
concrete payoff. **Always be fact-correct** — verify claims from real sources; never invent
numbers, dates, or quotes. (Topic research can use Claude/me directly — "what's the latest
news" — plus HN/Reddit/RSS/SERPER.)

## 1) Script & tone
- **Voice:** energetic, punchy, fast-paced, confident, human. Short active sentences,
  conversational creator tone. Not snarky, not dry.
- **Length:** target **40–60s**; hard floor 30s, hard ceiling 70s. Trim script to fit.
- **Hook:** first ~2s = a bold hook line (claim or stat) over a FAST b-roll shot. Lead visual
  is b-roll/real footage, NOT the avatar. Hook spoken immediately.
- **Cold open:** NO bumper/intro. Straight into the hook from frame 1.
- **Outro:** "Follow Retrofit AI for more such <topic-fitting adjective> videos." Accent CTA
  card in a clear zone (top band, OFF the face), last ~2–3s. (HyperFrames: `tiktok-follow`
  block or a custom CTA.)

## 2) Visual system
- **Backgrounds for graphic scenes:** NEVER hand-code grids/particles. Priority: (a) subtle
  abstract Pexels motion loop (dots/grid/particles/gradient-mesh), muted + looped behind a
  scrim; else (b) CSS gradient/solid in the topic accent. Spec intent: a **warm off-white /
  paper** ground (LIGHT) with enough contrast that foreground ink text stays crisp — NOT dark.
  (See the RESOLVED note above.)
- **B-roll sourcing — STRICT order:** real person/event → real YouTube footage of that event;
  general concept → Pexels/Pixabay stock loop; explainer/no real footage → generate
  (nano-banana image via Replicate → animate with wan-2.2 i2v). **All b-roll: muted, looped,
  always moving (Ken Burns/zoom). Never frozen.** Keys in `tools/.env` (PEXELS, PIXABAY,
  REPLICATE, SERPER). Cost-check generation with `tools/scenes_dryrun.py` first.
- **Avatar framing — per beat, default full-bleed:** full-bleed (hook, opinions, direct
  lines) · split/contained window (face + content coexist) · floating-circle PiP over a
  b-roll/motion bg (keep presence during a cutaway) · full cutaway to b-roll/graphics (pure
  data/proof beats). **Rule: never hide the face >~5s straight; return to the avatar.** See
  [SPLITSCREEN_GUIDE](SPLITSCREEN_GUIDE.md) for the layouts (incl. the broadcast band).
- **Color:** **ONE accent per video**, from the subject's brand (Microsoft→Azure blue,
  NVIDIA→green, OpenAI→teal, AWS→orange, etc.); no obvious brand → pick a fitting accent.
  Base + that one accent + white/gray text, consistent across the whole video.

## 2b) Safe areas & bleed margins — HARD RULE (IG Reels + YouTube Shorts)
This video ships to **both Instagram Reels and YouTube Shorts**, so the editor must design to
the **intersection** of both platforms' UI-safe areas. Each platform paints its own chrome
(action rail, caption, title, channel, Subscribe, progress bar) over the bottom + right edges.
Anything that **must be seen or read** — captions, titles, numbers/stats, logos, CTAs, key
graphics, the number badge — MUST sit fully inside the combined SAFE rectangle. Only decorative
full-bleed backgrounds, b-roll, and the avatar may bleed to the frame edges.

**Measured unsafe bands @ 1080×1920 (px):**

| edge | Instagram Reels | YouTube Shorts | USE (stricter of the two) |
|------|-----------------|----------------|---------------------------|
| top    | 0–250    | 0–150    | **0–250** |
| bottom | 1500–1920 (420) | 1380–1920 (540) | **1380–1920** (YT eats more: title 2 lines + channel + Subscribe + buttons + progress) |
| left   | 0–60     | 0–60     | **0–60** |
| right  | 890–1080 (190) | 880–1080 (200) | **880–1080** (like/comment/share/sound rail) |

**→ COMBINED SAFE RECTANGLE (design to this): `x ∈ [60, 880]`, `y ∈ [250, 1380]` (820×1130).**
- Nothing readable may touch or cross those four boundaries. "Near the margin but legible" = a
  BLOCKER (QA hard-fail), same standing rule as the 06-08 "1,000,000+" miss.
- **Bottom is the tight one:** the YT-Shorts bottom chrome reaches up to **y1380**, so the old
  "locked lower-third caption band ~y1280–1490" now runs INTO it. Captions/CTAs must move UP to
  sit **≤ y1380** (recommended caption band **~y1120–1360**, still clear of the face). See §5.
- Avatar/PiP/b-roll may extend past these edges (decorative), but never put a caption, badge,
  logo, stat, or CTA in a red band.

## 3) Avatar looks (mood-matched)
Classify each script into a dominant mood → pick the matching HeyGen look. Full
mood→look→`character_id` map (stable IDs): [HEYGEN_AVATAR_LOOKS](../reference/heygen-avatar-looks.md).
**[Remotion/server — generating HeyGen A-roll is human-assisted (needs home-IP tunnel);
locally you edit A-roll already in the project.]**

## 4) Editorial principles ("make it feel hand-cut")
- **Motivated edits:** every cut/graphic appears ON a spoken word (drive reveals off the
  word-level transcript `transcript.json`), never at a fixed timecode.
- **Placement intelligence:** graphics go in the frame's negative space relative to the
  b-roll subject / the speaker — never bury the face or hero object. Read a clip frame first.
- **No dead air:** every frame earns its place. No empty/half-black frames or empty stages.
- **Compose, don't sequence-with-gaps:** establish a full layout fast, then animate WITHIN it
  (highlight items on their word) — don't pop items onto an empty stage one by one.
- **Imperfection = human:** ±2–3° rotations, springy overshoot, subtle constant wobble/float.
- **Continuous life:** Ken Burns on A-roll; b-roll always pans/zooms; nothing frozen.
- **Hard cuts only** — no crossfades/slides between scenes.

## 5) Pacing, captions, music, SFX
- **Cut cadence (fast but motivated):** avg **1.5–2.5s**, hooks <1.5s, **never static >2.5s**,
  cut on spoken phrases. If a beat runs long, change something WITHIN it every 2–4s. The user
  likes **fast-cut videos with lots of relevant b-roll.**
- **Captions:** word-by-word **appear+rise** default (white words + multi-direction shadow
  outline, NOT the red-sweep pill — the owner's default); line-by-line for calm beats; one style per
  video; **overridable per brief** when the vibe demands a different caption style.
  Caption band sits inside the combined safe area, **above the YT-Shorts bottom chrome (y≤1380)**
  — recommended **~y1120–1360** (clear of the face); move only to dodge a key graphic, to
  predefined slots. (The old ~y1280–1490 band runs into YT Shorts' bottom UI — see §2b.)
- **Annotations:** sparse, purposeful, hand-drawn/springy, ~1 per beat, never clutter.
- **Music:** ducked 0.10–0.15 under VO, up to 0.4 in gaps, 0.3s ramps, mood per topic; VO
  dominant. `tools/audio_generator/` (ElevenLabs) / Pixabay; always re-encode (`libmp3lame`,
  never `-c copy`).
- **SFX:** moderate — whoosh on cuts, pop on reveals, impact on stats; not every beat.
- **Logo/watermark:** none for now.

## 6) Pipeline (HyperFrames)
script → `transcript.json` (word-level) → fetch/generate assets (`tools/`) → build composition
(`build_composition.py` → `index.html`) → **QA** ([QA_GRID_GUIDE](QA_GRID_GUIDE.md): snapshot →
read every contact-sheet frame → fix → repeat) → render only when approved. **[Remotion/server
bits — `--gl=swangle`, detached long renders, tag-leak guard, SOCKS proxy for yt-dlp/HeyGen,
`src/Root.tsx` — do not apply to this local HyperFrames project.]**

## 7) Definition of done
A composition that previews at 1080×1920/30fps, 30–70s, passing the QA grid (no caption
overlap, no frozen b-roll, no off-style/empty frames, captions synced to the word, single
accent color, CTA off the face, mood-matched look). Report the result + the QA grid + a
one-line note on the look/mood/color chosen.
