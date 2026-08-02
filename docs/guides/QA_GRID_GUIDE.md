# QA_GRID_GUIDE — visual QA for every composition (handoff doc)

Self-contained guide to the contact-sheet QA pipeline for **HyperFrames** (9:16, 1080×1920).
Hand this to any agent/chat. QA is a **required, automatic step after every build** — a
composition is not "done" until its grid passes the rubric below.

The big difference from a traditional NLE/Remotion setup: **you do NOT need a full mp4
render to QA.** HyperFrames renders frames headlessly straight from `index.html`. The loop is:

> **regenerate `index.html` → `npx hyperframes snapshot` (dense set) → Read `snapshots/contact-sheet*.jpg` → fix → repeat**

(In the old Remotion project this was `render → grid → review → fix → re-render`, driven by
`tools/video_review/grid_review.py` + `still_grid.py`. Both are gone — the two HyperFrames
commands below replace them and skip the full render entirely.)

---

## The two commands (no full render needed)

### 1. `npx hyperframes snapshot` — frame stills + contact sheet (the standard QA)

Renders chosen frames straight from the composition and writes:
- `snapshots/frame-NN-at-<t>s.png` — one PNG per requested time
- `snapshots/contact-sheet-N.jpg` — the labeled grid(s) you **Read** and scan

```bash
# dense pass across the whole piece — one frame ~every 1s for a 58s comp:
npx hyperframes snapshot --at 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58

# densely sample specific windows (FINAL-time seconds), e.g. two beats at ~0.4s spacing:
npx hyperframes snapshot --at 14,14.4,14.8,15.2,15.6,16,...,28  --at 48,48.4,...,56

# a single sub-composition instead of the root:
npx hyperframes snapshot -c compositions/x-post.html --at 0.5,1.5,3
```

Then **Read each `snapshots/contact-sheet-N.jpg`** and scan it. The command does NOT judge
for you — you must actually open/Read the JPG. (`--frames N,N,N` selects by exact frame
number instead of seconds; useful when matching a 30fps timeline beat exactly.)

> A 1s-dense pass on a ~1-minute piece spills onto multiple contact sheets
> (`contact-sheet-1.jpg`, `contact-sheet-2.jpg`, …). **Read every one of them** — see the
> CRITICAL QA RULE below.

### 2. `npx hyperframes inspect` (alias `layout`) — headless layout audit

No grid, no eyeballing — a static check for **off-canvas / text overflow / element
collisions**, reported with timestamps, selectors, and fix hints.

```bash
npx hyperframes inspect --samples 15          # auto-sample 15 evenly-spaced frames
npx hyperframes inspect --at 1.5,4,7.25       # audit exact beats
npx hyperframes inspect --json                # machine-readable for CI
```

Suppress an intentional bleed with `data-layout-allow-overflow` on the element (e.g. a
full-bleed slam-word layer), or `data-layout-ignore` to skip it entirely. `inspect` is part
of `npm run check` (= **lint + validate + inspect**), so it runs on every check.

**Which to use:** `inspect` is the cheap automated gate (catches text off-screen / overflow
mechanically). `snapshot` + Read is the human-judgment gate (catches everything `inspect`
can't reason about: a logo on the face, frozen b-roll, dead air, a flat void). **Run both.**
You author against the live `npx hyperframes preview` server (port 3002); snapshot is for the
audit pass and for any agent that can't watch the preview.

---

## What to scan the grid for (review checklist)

- **Empty / half-black frames** — dead air, or a flat background "void."
- **Text or graphics colliding with the speaker's face / subject** — bad placement.
- **Frozen B-roll** — identical adjacent frames where the b-roll should be moving.
- **A single visual held too long** — static, not flashy (the frame should change every 2–4s).
- **Mistimed reveals** — text appearing before the spoken word, or a caption left on after its word.

## The pass rubric (the bar — a composition isn't done until all pass)

- **FILL** — every frame ≥ ~40% non-empty (no element floating in a void).
- **NOT-FLAT** — no scene background is a flat single color; use a gradient / image / texture + grain.
  (Note: prefer **radial** gradients or solid+glow on dark fills — full-screen linear gradients
  band under H.264. See authoring-rules.)
- **NO-OVERLAP** — no text block overlaps the face; only one text block per safe zone at a time.
- **MOTION** — something visibly changes every 2–4s (an internal change if a beat runs long).
- **DENSITY-RUN** — never 3 consecutive same-energy scenes; vary framing.
- **ON-SCREEN (HARD FAIL, the owner 2026-06-08)** — NO text/graphic may touch or cross the safe-zone
  margins. "Near the margin but still legible" is NOT acceptable — it is a BLOCKER. (The 06-08
  "1,000,000+" counter at the right margin was wrongly waved through.) Cross-check with `inspect`.
- **REAL-ASSETS (HARD FAIL)** — the video must show real internet-sourced assets (b-roll/photos/
  logos), NOT a 100% CSS/graphics build. A pure-CSS render fails QA (06-08 shipped pure CSS — flagged
  "not engaging").
- **AVATAR-FRAMING (HARD FAIL)** — the talking avatar must go FULL-BLEED at least once (hook/CTA);
  never a permanent tiny PiP for the whole video (06-08 PiP-only — disliked). Vary PiP↔full-bleed.
- **CENTERED (HARD FAIL, retrofit-2026-06-15)** — readable content must look centered on the TRUE
  frame center **x540** on the raw mp4, NOT left-shifted. Pixel-measure each row's center ≈ x540 (±15).
  Cap readable width ≤ ~660px so it's both centered AND clears the x880 rail (see corrected AUTHORING
  RULE below). Any "centered" row sitting noticeably left of center = BLOCKER.
- **NO-CAPTION-DOUBLING (HARD FAIL, retrofit-2026-06-15)** — at most ONE caption bar visible at any
  instant, and a per-scene card (lnote/CTA/hook) must not co-exist with a global caption of the same
  words. Snapshot the **±0.25s window around EVERY caption show/hide boundary** (the doubling only
  appears mid-crossfade — a 1s grid skips it). Two stacked/overlapping caption boxes = BLOCKER.
- **LAYERING / NO-OCCLUSION (HARD FAIL, retrofit-2026-06-15)** — no readable element may be hidden
  under a higher-z decoration: a phone **notch** must not cover the app-bar logo/title; a scrim/tint
  must not bury text. Check the z-order at each scene where a device frame, notch, or overlay sits over
  content (the ChatGPT logo was rendered UNDER the phone notch).
- **ELEMENT-SIZE / PADDING (retrofit-2026-06-15)** — primary brand logos inside cards ≥ ~120px tall;
  multi-card / multi-node rows have visible GAPS (never edge-to-edge crammed); cards have internal
  padding. Tiny logos + zero-gap cards read "cramped/unfinished."
- **PROOFREAD (HARD FAIL)** — read EVERY on-screen word for spelling, grammar, and bad line-wraps
  ("Your okay" → "You're OK"; "Charge-backs" wrapping to 2 lines). One typo on screen = BLOCKER.
- **NO-BLANK-SCENE (HARD FAIL, retrofit-2026-06-19)** — every beat MUST render content. Scan the grid
  for any EMPTY/blank panel (just the background, no text/cards/broll/face) and snapshot the MIDDLE of
  each beat, not only its transitions. A scene that renders fully invisible = BLOCKER. ROOT CAUSE =
  a GSAP `fOut()` / `.to(opacity:0)` applied to a SCENE CONTAINER that also has a `fIn`
  `fromTo(immediateRender:false)` entrance — on seek-render that whole scene resolves to opacity:0 and
  renders blank (it shipped "empty after 33s" on retrofit-2026-06-19). It looks fine in live preview
  (which PLAYS the timeline) but is dead in the render. **CRITICAL:** `snapshot` uses the same seek
  path, so a blank scene shows blank in the contact sheet too — you must actively LOOK for empty panels;
  "snapshots generated" does NOT mean the scenes are populated. Fix = fade inner content + hard-hide the
  empty scene with `tl.set(autoAlpha:0)`. `tools/pipeline_check.py` now also auto-blocks any ≥3s near-flat
  stretch, but the visual scan is still required. See `rules/animations.md`.
- **CUTOUT-HOST ZERO-OVERLAP (HARD FAIL, retrofit-2026-06-23)** — when content cards are on screen the
  cutout host must occupy a DEDICATED empty zone with ZERO element overlap: its HEAD must sit clearly
  BELOW (or fully clear of) every card/chip/title/panel on screen — never crowding a card or sitting
  under text. Mechanism that works: while any card shows, dock the host to a BOTTOM corner (alternate
  L/R per beat) small enough that the head lands below the lowest content element (06-23: scale ~0.42,
  feet anchored at frame bottom → head ~y1178, below the lowest card ~y1070). Full-bleed host only at the
  brief enter-hook and the outro (and at full-bleed, keep ALL cards in the lower third clear of the face,
  per rule #6). PITFALL: a host element that is full-height with `object-position:50% 8%` (face near top)
  scaled from `transform-origin:50% 100%` keeps the face HIGH even when "stepped aside" — it rose into
  the b-roll/chips on 06-23. Lower the scale (and/or add a small +y) until the head clears content; verify
  on the grid at EVERY content beat that no card touches the host head.
- **MEDIA-SPANS-CARD-LIFE (HARD FAIL, retrofit-2026-06-23)** — a b-roll `<video>` clip's playable
  duration MUST be ≥ the on-screen life of the card it fills, or it freezes/blacks out for the remainder
  (06-23: a 3.2s `evan_stage.mp4` wired `data-duration="5.9"` on a ~5.3s card → the EVAN card went black).
  CHECK: for every panel video, `clip_duration ≥ (fOut_time − fIn_time)`. If no clip that long+relevant
  exists, use a STATIC PHOTO (can't go black) or shorten the card. Snapshot the LAST 0.5s of every video
  panel and confirm it still shows real footage, not a frozen/black frame.
- **CAPTION-RELEVANT B-ROLL (HARD FAIL, retrofit-2026-06-23)** — every b-roll clip / photo must MATCH its
  on-card label and the spoken line. No generic/mismatched footage (06-23 had a random walking torso under
  "16 MILLION COLORS" and a janky red-door AR clip under "IT SEES WHAT YOU SEE"). For news/product videos,
  cut the cutaway from the OFFICIAL reveal/demo (step 4b official-source-first) or use a real product photo;
  if the literal moment isn't available, relabel the card to what the asset HONESTLY shows (06-23: the Evan
  card became "SWISS TR90" over a real worn-Specs photo, matching the "plastic titanium" quote). Read every
  panel against its label on the grid — a label that doesn't describe the visual = BLOCKER.
- **PRODUCT-GROUNDED HERO (HARD FAIL when the video has a real product, retrofit-2026-06-23)** — the
  full-screen purple-cow hero must be generated with the real PRODUCT photo as a second `--ref-image`
  (alongside the owner's face frame) so he's shown with the GENUINE product, not an AI-invented generic one.
  See `HOOK_BROLL_PLAYBOOK.md` → PREMIUM i2v recipe → PRODUCT-GROUNDED HERO. QA: if the hero shows a
  gadget that doesn't match the real product, it's a BLOCKER — regenerate with the product reference.

## Safe zones — IG Reels + YouTube Shorts (shared constants — keep spec, compositions, QA in sync)

9:16, **1080×1920**. Every video ships to **both Instagram Reels and YouTube Shorts**, so QA
checks against the **intersection** (stricter of the two) of their UI-safe areas. Each platform
paints chrome (action rail, caption, title, channel, Subscribe, progress bar) over bottom/right.

**Measured unsafe bands @ 1080×1920 (px):**

| edge | Instagram Reels | YouTube Shorts | USE (stricter) |
|------|-----------------|----------------|----------------|
| top    | 0–250    | 0–150    | **0–250** |
| bottom | 1500–1920 (420) | 1380–1920 (540) | **1380–1920** |
| left   | 0–60     | 0–60     | **0–60** |
| right  | 890–1080 (190) | 880–1080 (200) | **880–1080** |

**→ COMBINED SAFE RECTANGLE: `x ∈ [60, 880]`, `y ∈ [250, 1380]` (820×1130).**

> **AUTHORING RULE — CORRECTED (retrofit-2026-06-15 "everything looks left-shifted" re-render).**
> The earlier version of this rule told you to center wide content on the **safe-rect center x470**
> (via asymmetric insets like `left:70; right:210`). That cleared the action rail but made every
> "centered" element read **visibly off-center / left-shifted on the RAW mp4 the owner reviews** — which
> is exactly the defect he flagged. The two goals (look centered **and** clear the x880 rail) only
> reconcile one way:
>
> **→ Cap every readable block at width ≤ ~660px and center it on the TRUE frame center x540**
> (symmetric `left:N; right:N`, or `left:50%; translateX(-50%)`, or `max-width:660px;margin:auto`).
> A ≤660px block centered on x540 spans **x210–870** — visually centered AND fully inside the safe
> rect [60,880]. Width 680 lands the right edge exactly on x880; stay ≤660 for a cushion.
>
> If a row genuinely needs to be wider than ~660px: **don't dodge it with asymmetric margins** —
> reduce the width instead (wrap a logo/chip row to 3-per-row, shrink the chips, stack cards
> vertically, shorten a label). Asymmetric centering is a LAST resort and always reads off-center.
> `pipeline_check.py` now lints for `position:absolute` + `text-align:center`/`translateX(-50%)`
> containers whose left/right insets differ by >40px and warns to re-verify them on the raw mp4.
> Still pixel-measure each readable row's CENTER ≈ x540 (±15) and its max-x ≤ x870, not just eyeball.
Anything **readable** (captions, titles, number badge, stats, logos, CTAs, key graphics) must
sit fully inside it. Avatar / PiP / b-roll / decorative full-bleed backgrounds MAY bleed to the
edges. **Any readable element touching or crossing a boundary = the ON-SCREEN HARD FAIL above
(BLOCKER).** Note the bottom is tight: YT-Shorts chrome reaches up to **y1380**, so the caption
band must sit **≤ y1380** (recommended ~y1120–1360), NOT the old y1280–1490.

### QA verification — paint the RED unsafe zone, then look for intrusions
HyperFrames has no built-in safe-zone overlay, so QA **draws the measured unsafe bands in RED
(with bright boundary lines) over the snapshot frames** and fails any element whose pixels enter
the red. Overlay every snapshot/contact-sheet frame with this ffmpeg filter before reviewing:

```
ffmpeg -y -i frame.png -vf "\
drawbox=x=0:y=0:w=1080:h=250:color=red@0.35:t=fill,\
drawbox=x=0:y=1380:w=1080:h=540:color=red@0.35:t=fill,\
drawbox=x=0:y=0:w=60:h=1920:color=red@0.35:t=fill,\
drawbox=x=880:y=0:w=200:h=1920:color=red@0.35:t=fill,\
drawbox=x=0:y=250:w=1080:h=3:color=yellow:t=fill,\
drawbox=x=0:y=1380:w=1080:h=3:color=yellow:t=fill,\
drawbox=x=60:y=0:w=3:h=1920:color=cyan:t=fill,\
drawbox=x=880:y=0:w=3:h=1920:color=cyan:t=fill,\
drawbox=x=0:y=1500:w=1080:h=2:color=orange@0.7:t=fill" frame_safe.png
```
- **Red bands** = combined unsafe (top 250 · bottom 1380 · left 60 · right 880).
- **Yellow/cyan lines** = the measured safe-rect boundaries (the lines you verify padding against).
- **Orange line @ y1500** = the looser IG-Reels bottom, for reference only — design to the red.
- **PASS** = no caption/badge/stat/logo/CTA/key-graphic pixel sits in any red band or crosses a
  boundary line. **FAIL (BLOCKER)** = any readable element intrudes into red. (Decorative
  bleed of avatar/b-roll into red is allowed.)
- Run this on the dense (~1s) snapshot pass so EVERY scene's frame is checked against the lines.

`build_composition.py` keeps captions in the lower third and pushes the talking head DOWN
(spring `#base-wrap` to `y:+330`) when a top graphic appears, so overlays never cover the face.
`inspect` still catches the mechanical off-canvas/overflow cases; the red overlay catches the
"inside the canvas but inside platform chrome" cases that `inspect` cannot see.

---

## CRITICAL QA RULE — check EVERY frame, EVERY scene

Do **not** review only a few focused beats. **Scan every cell of every contact sheet, every
scene, start to end.** The defects that ship are almost always in the frames nobody looked
at:

- text off-screen (off-canvas) for one scene only
- a tiny logo, or an element sitting **on the face**
- frozen / non-moving b-roll (a "video" that's actually static)
- a held graphic with no motion for 5s+ (dead air)
- a caption that never cleared, lingering over the next scene

A dense (~1s) snapshot pass exists precisely so that EVERY scene lands in the grid. Read all
of `snapshots/contact-sheet-1.jpg`, `-2.jpg`, … — not just the first sheet. One unchecked
scene is one shipped defect.

---

## The loop, concretely

1. Edit the composition (e.g. re-run `python3 build_composition.py` to regenerate `index.html`).
2. `npm run check` — lint + validate + **inspect**. Fix every error; review overflow/off-canvas warnings.
3. `npx hyperframes snapshot --at <dense csv>` — dense set across the whole piece.
4. **Read** every `snapshots/contact-sheet-N.jpg` and run the checklist + rubric on **every frame**.
5. Fix the worst offenders; for a single problem scene, snapshot just that window at ~0.4s spacing.
6. Repeat 1–5 until the rubric passes clean. Only then `npm run render`.

## Gotchas

- **Snapshot writes into `snapshots/`** and overwrites prior PNGs/contact sheets — Read them
  immediately after the command, before the next snapshot run.
- A dense pass produces **multiple** contact sheets. Reading only sheet 1 is the #1 way to miss
  a late-scene defect. Read them all.
- The contact sheet is a JPG — **you must actually open/Read it; nothing judges it for you.**
- Label raw VO time in your notes when A-roll is sped up (e.g. a 1.10× edit) so a "mistimed
  reveal" finding maps back to the right spoken word.
- Intentional full-bleed overflow (slam words, edge-to-edge b-roll) trips `inspect` —
  annotate with `data-layout-allow-overflow` rather than ignoring the warning.

## `npm run check` = lint + validate + inspect

Run it after **every** edit. (Was `npm run lint` + the planned `design_lint.py` /
`grid_review.py --rubric` in Remotion — HyperFrames ships `lint` + `validate` + `inspect`
today, so the mechanical half of the bar is already enforceable; the FILL / NOT-FLAT /
NO-OVERLAP / MOTION / DENSITY-RUN rubric remains a **visual** judgment you make from the
contact sheet.)

## Template / placeholder-text check (automated)
Vendor registry blocks ship with demo text (code-snippet's "Official VS Code built-in theme /
Light Modern" header, x-post's "Prompt to replace this text", demo handles). **Strip it before
rendering.** Run `python3 tools/video_review/template_text_check.py` — it scans `index.html` +
`compositions/*.html` for placeholder patterns and exits non-zero on block-level matches
(lorem, "prompt to replace", demo headers, vendor handles). It's wired into `npm run check`.
Review-level hits (demo code, theme labels) are FYI — confirm they're intentional. Also
eyeball every contact-sheet frame for any leftover demo text on screen.
