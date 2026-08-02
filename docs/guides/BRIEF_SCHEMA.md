# BRIEF_SCHEMA.md — the Director's locked brief for Bella

Write to `projects/<slug>/BRIEF.md`. Fill EVERY field; Bella builds exactly to this.

## Header
- **slug / date / topic / one-line hook**
- **accent**: hex + source (brand → accent; AWS=orange, OpenAI=teal, Azure=blue, else fitting)
- **avatar**: look name + `character_id` (from `docs/reference/heygen-avatar-looks.md`) + why this mood
- **caption style**: default = word-by-word appear+rise; OR a `caption-*` for a specific vibe — say which + why
- **duration target**: 40-60s · **palette**: LIGHT/warm (never dark) · **finishing grade**: warm finish layer ON (per `FINISHING_GRADE.md`); note any per-video warmth/grain tuning
- **VARIATION NOTE**: how this video's structure/look deliberately differs from the last (cite DIRECTOR_MEMORY)

## HOOK ENGINEERING (the first ~1.5s decides retention — spec 2-3 variants)
Give Bella **2–3 distinct hook treatments** for the opening beat; she builds all, you pick the
strongest from the grid at QA. Vary the *mechanism*, not just the words. **For EVENT/RELEASE
topics, variants from the first two rows are the DEFAULT starting point (the owner, 2026-06-11) —
deviate only with a stated reason:**
| variant | mechanism | visual | on-screen hook text |
|---|---|---|---|
| A | official event/keynote footage cold-open | the 1-2 most iconic seconds of the YT clip (ts-range) | … |
| B | founder/figure-led open ("‹founder› just cooked") | B&W press-photo cutout on bold accent bg (webveda `dream-intro-hero` is one option — restyle freely, not a template) | … |
| C | bold claim over FAST b-roll | which clip / query | … |
| D | number/stat slam | the number + accent | … |
| E | pattern-interrupt (question / contradiction) | … | … |
State which you EXPECT to win and why; the QA grid confirms or overrules it.

## Per-beat plan (one row per cut; aim 1.5-2.5s avg, hook <1.5s — a beat container may run
up to ~4.5s ONLY if 2–4 internal on-word reveals keep the on-screen change every ≤1.5s;
sub-cut inside the beat, never hold a static card: see `styles/full/morning-edition-editorial.md`
"Pace & rhythm" for the measured spec from the approved 07-11 cut)
**The `library piece` column is MANDATORY (the owner, 2026-06-11)** — cite the
`MOTION_LIBRARY.md` piece by name (caption style, transition, text effect, card/block,
lottie, overlay) or write `bespoke: <why>`. Un-shopped briefs get bounced at QA.
**The `host` column is MANDATORY (the owner, 2026-07-12)** — per `robust-anchoring.md`: host is
DEFAULT-ON every beat; write the face-target as `side face_x,face_y @scale lean°` (e.g.
`R 895,720 @0.90 -12°`), side-docked with a fun lean toward the content (never mid-frame,
never a floating PiP, scale ≥0.85, **≥50% of the avatar visible at any edge — `face_x` within
~[170,910] — and the head always fully in frame**), or `OFF: <why>` (hero/Omni beat, or one
≤1.5s cutaway max).
| # | time | spoken line | host (side x,y @scale lean / OFF:why) | visual: full-bleed plate/b-roll + poster type / clipping / component | library piece | on-word reveal | impact/caption note | SFX cue |
|---|------|-------------|----------------------------------------|-----------------------------------------------------------|---------------|----------------|---------------------|---------|
Every data/stat beat needs a full-bleed plate or footage behind poster type — a stat on the
flat world bg is a website, not a video (`HUMAN_EDIT_GUIDE.md` §2b).

## AI ASSET PLAN (per `HUMAN_EDIT_GUIDE.md` §5 — budget ≤4 images + ≤2 motion clips)
Spec each AI-generated asset like any other asset (they go in the owner's 4b approval shortlist,
likeness edits labeled "AI edit of your likeness"):
| # | recipe (A logo-scene / B the owner-scenario / C concept) | prompt sketch | still or +i2v motion | which beat |
|---|---|---|---|---|
Also state the **motion plan** per HUMAN_EDIT_GUIDE §1: which 2-3 emphasis words get avatar
punch-ins, and confirm no run of >2 consecutive pure-CSS beats.

## AUDIO PLAN (per `AUDIO_GUIDE.md` — Bella renders the cue times into `audio.json`)
- **music bed**: mood → which `assets/common/music/<bed>.mp3` + resting `music_gain_db` (default -18)
- **SFX map**: riser into the hook · whoosh on hard cuts · pop on reveals · impact/sub-boom on stat slams · swell on the outro. List the *type* per beat (the `SFX cue` column above); moderate, one per beat, not every frame. **Levels + lengths per AUDIO_GUIDE §2a: every one-shot gets a `dur` trim, gains respect the -4dB `sfx_cap_db`.**
- **master**: final mix to **-14 LUFS** (the tool does this) — the deliverable is `<slug>_final.mp4`.

## Explicit-ask ledger
- [ ] one checkbox per concrete ask (from the owner or this brief); ticked at QA only WITH a proving frame.

## Non-negotiables (reminder to Bella)
LIGHT palette · 1.10× speed · captions synced on-word · CTA off the face · no template text · BIG elements · push-down so graphics never cover the face · hard cuts as the base grammar (a BRIEF-specced registry transition allowed 1–2× max on the biggest beat change — HUMAN_EDIT_GUIDE §5b) · **warm finishing layer on · b-roll color-matched warm · audio: ducked music + motivated SFX + -14 LUFS master · HUMAN_EDIT_GUIDE rules: no static hold >1.5s, avatar punch-ins, reveals cut ON the word, premade motion library checked before building**.
