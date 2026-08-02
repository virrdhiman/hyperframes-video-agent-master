# PREFLIGHT_CHECKLIST.md — read before EVERY video, verify before EVERY delivery 🎬

This is the non-negotiable checklist. Skipping it is how we shipped a video whose
headline feature (the kinetic text impacts) was 100% absent while the delivery note
claimed "✅ impacts." Evidence over intent. Every. Single. Time.

---

## A. PRE-FLIGHT (before you build anything)

- [ ] Read `SOUL.md`, `CLAUDE.md`, `AGENTS.md`, `docs/guides/CREATIVE_SPEC.md`, `docs/guides/AGENT_GUIDE.md`, latest `memory/*.md`.
- [ ] Invoke the **`/hyperframes`** skill for framework mechanics (authoritative).
- [ ] **CHECK THE HEYGEN/HYPERFRAMES COMPONENT CATALOG BEFORE EDITING.** Run `npx hyperframes catalog` (and skim `docs/guides/COMPONENT_CATALOG.md` + `docs/guides/SCENE_SNIPPETS.md`). For each beat that needs a caption / lower-third / transition / VFX / scene, pick the registry block or in-repo reusable scene that suits best **before** hand-rolling one. Don't reinvent a caption sweep or kinetic headline that already exists — reuse, then customize. List which catalog items you chose in the ledger.
- [ ] **PROACTIVE UPDATES — the owner should never have to ask "update?".** Send him a short status message at every real milestone on your OWN initiative: (a) plan/ledger locked, (b) build applied + lint clean, (c) QA grid read (with verdict), (d) render launched (detached), (e) render done + link. During a long detached render, ping a one-line progress note every ~5–7 min off the logfile until it finishes. A milestone reached silently is a milestone half-done.
- [ ] **Write the EXPLICIT-ASK LEDGER.** Copy every concrete thing the user asked for into a literal checkbox list, e.g.:
  - [ ] global 1.15× speed-up
  - [ ] remove the **second** India clip
  - [ ] bigger top chips, in the headroom
  - [ ] kinetic text impacts over the head
  You will tick each one OFF AT DELIVERY, with a frame that proves it. An ask with no proving frame is NOT done.
- [ ] Transcript word-timestamps loaded; plan every reveal to land ON its spoken word.
- [ ] Canvas is **1080×1920**. Size every element per the **Proportional Sizing** table below — never eyeball raw px.

## B. BUILD INVARIANTS (HyperFrames determinism — break one and frames silently vanish)

- [ ] Single **paused** GSAP timeline registered on `window.__timelines["root"]`.
- [ ] **NO function-callbacks.** `tl.add(function(){...}, t)` is suppressed during seek-render → invisible. Build every tween as `tl.fromTo/to` at an **absolute** time. No relative `"+=x"` (resolves against timeline end). `tl.args` is not a real property.
- [ ] Never animate `opacity`/`visibility` on a `.clip` element — animate inner content; let the clip boundary hard-cut.
- [ ] Every timed element: `class="clip"` + `data-start` + `data-duration` + `data-track-index`.
- [ ] `data-track-index` is pure z-order; **no two overlapping clips on the same track**.
- [ ] Every b-roll `<video>` has a **unique `id`**; pre-trimmed clips use `data-media-start="0"`.
- [ ] Deterministic only: no `Date.now()`, no `Math.random()` (use seeded mulberry32), no network.
- [ ] Two top-band graphics at once = clutter. **Sequence** an impact and a chip — impact punches solo, chip slides in after it exits.
- [ ] **Host anchoring (`styles/elements/animations/robust-anchoring.md` — MANDATORY):** measure the avatar face once; place every beat with the face-anchored `hX/hY` helpers. Host is **DEFAULT-ON at every beat, side-docked with a fun lean toward the content (±6–16° rotateZ) — never mid-frame, never a shrunken floating PiP** (scale ≥0.85 so the chest-cut stays off-frame). **≥50% of the visible avatar on screen at ANY edge (`face_x ∈ ~[170,910]`) and the head ALWAYS fully in frame** — re-check on punch-ins. Host-off only for hero/AI beats or a ≤1.5s cutaway. Annotations (circles/arrows on text) via element-anchored `circleEl`, never fixed svg coords. Pinned overlays (ticker, finish layers) live OUTSIDE the `#camera` zoom wrapper.
- [ ] **Video-not-website (`HUMAN_EDIT_GUIDE.md` §2b):** every data beat gets a full-bleed plate/footage behind it; poster type over footage instead of cards-on-flat-bg; editor-texture pass on all containers (`styles/elements/finishing/editor-texture-pass.md`); topic-native SFX identity + trendy hits in `audio.json`.

## C. PROPORTIONAL SIZING (size = % of the 1080×1920 canvas, not a guess)

Reference: **1% of width = 10.8px**, **1% of height = 19.2px**. Use WIDTH (1080) for type/logos.
Short-form is watched on a phone at thumbnail size — **when unsure, go BIGGER.**

| Element | % of width | px (1080w) | Notes |
|---|---|---|---|
| Hero / kinetic impact headline | 13–20% | **140–216px** | the slam words; 1–2 words only |
| Big stat number ("5×") | 18–24% | **200–260px** | the punch |
| Caption words | 6–8% | **64–86px** | one group at a time |
| Chip / lower-third title | ~3% | **30–36px** | + kicker ~2% (22px) |
| Logo in polaroid chip | ≥11% | **≥120px** | brief minimum |
| Hero logo | ~18–22% | **200–240px** | |
| CTA name / handle | 2.5–3.5% | **28–38px** | |
| **Hard floor** | ~2% | **~22px** | nothing meaningful smaller |

Layout: a primary graphic should **fill ≥40%** of the frame (QA rubric). Safe zones —
top ~220px, bottom ~440px, sides ~60–130px; caption band ~y1280–1500. Face is sacred:
when a top graphic is up, push the A-roll DOWN (~330–420px) so nothing covers the face.

## D. PRE-DELIVERY QA — BLOCK ON THIS. No ✅ without a frame.

- [ ] `npm run check` (lint + validate + inspect + template-text) → **0 errors**.
- [ ] `npx hyperframes snapshot --at <10–14 timestamps across the whole video>` → **READ every panel.**
- [ ] **Walk the EXPLICIT-ASK LEDGER (section A). For each item, name the exact frame/timestamp that proves it.** If you cannot point to a frame, it is NOT done — go fix it. This is the step that was skipped.
- [ ] **For every headline feature, name the frame it appears in.** "I wrote the code" is not proof. "Visible at 7.7s" is.
- [ ] Rubric on each panel: FILL ≥40% · NOT-FLAT · nothing on the face · no caption/CTA collision · MOTION every 2–4s · single accent · LIGHT palette · CTA off the face · no template text.
- [ ] **HOST GRID (separate pass): snapshot every host beat into one labeled grid** — each host side-docked + angled (never mid-frame), grounded (no visible bottom cut), face fully visible, drawings wrapping their exact text. This grid caught every malposition the rubric missed.
- [ ] Render, then **re-QA a grid sampled from the actual MP4** (not just the composition snapshots) + confirm width/height/fps/duration with ffprobe.
- [ ] Deliver with the QA grid and a one-line accent/mood note. The ✅ list you send must be the ledger you just verified frame-by-frame.

> The difference between a good editor and a bad one here is a single habit:
> **claim nothing you have not seen in a frame.**
