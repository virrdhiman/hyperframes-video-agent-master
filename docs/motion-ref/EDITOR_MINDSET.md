# Editor Mindset — How This Video Was Cut

Source: `reference.mp4` (13:46) + `reference.en.srt`
This doc explains the *why* behind every edit — the pacing logic, graphic triggers, and narrative structure. Use this before building any HyperFrames composition that wants to match this style.

> General motion-design reference, kept as knowledge. Where it once described Remotion, the encoding now maps to **HyperFrames** (HTML elements with `data-start` / `data-duration` / `data-track-index` in seconds, animated by a paused GSAP timeline on `window.__timelines`). The *insights* below are framework-agnostic.

---

## Video structure

| Section | Timestamps | What's happening |
|---------|-----------|-----------------|
| Hook | 0:00–1:40 | Dense, rapid — earns the viewer |
| Background: What is VC? | 1:40–4:00 | Slower, foundational |
| VC origin story (US) | 4:00–6:00 | Historical narrative, evidence |
| India vs US comparison | 6:00–7:20 | Argument building |
| Problem 1: Foreign money | 7:20–8:12 | Evidence-heavy |
| Problem 2: Risk aversion | 8:12–9:35 | Vinod Khosla quote |
| Problem 3: No domestic institutions | 9:35–11:20 | Data/numbers |
| Solutions (#1 #2 #3) | 11:20–13:40 | Prescriptive, cards stack on screen |

**Section breaks are explicit.** The editor uses "Big problem with Indian Venture Capital **2**" as an on-screen chapter title. Viewers always know where they are.

---

## The core pacing rule

**Never more than ~20s of pure talking head without a visual break.**

Measured from the SRT against grids:

| Talking-head run | Duration | What broke it |
|-----------------|----------|---------------|
| 0:00–0:15 | 15s | Paper stack / news articles |
| 0:27–0:58 | 31s | India unicorn bubbles (long run — intro hook) |
| 1:00–1:40 | 40s | Star diagram → phrase type → jingle |
| 2:00–2:33 | 33s | 75/25 circles |
| 4:30–4:40 | 10s | Scrambled text reveal |
| 5:00–5:13 | 13s | USA map + label popins |

**Average visual break interval: ~15–20s.** If you're writing a composition and a section of narration is >25s with no graphic, the editor would have inserted one.

---

## Graphic trigger logic

The editor uses different patterns for different *types* of information:

### When to use what

| What the script is doing | Pattern to use |
|--------------------------|---------------|
| Introducing a new term/concept | **Definition box card (F)** |
| Multiple forces on one thing | **Star/wedge diagram (A)** |
| Comparing two numbers at scale | **Two-circle comparison (B)** |
| Dramatic number reveal (single figure) | **Scrambled text (C)** or standalone text card |
| Geographic distribution | **Map + label popins (D)** |
| Delivering the "punchline" argument | **Staggered phrase type (E)** |
| Backing a claim with evidence | **Article/screenshot overlay (H)** |
| Expert voice (not the host) | **Quote bubble card (I)** |
| Listing solutions/recommendations | **Numbered cards (G)** — they stack as they're added |
| Introducing a real person | **Cutout photo card (J)** |
| Showing a tiny % of a whole | **Pie chart (M)** |
| Currency conversion or 100x scale | **Equation card (K)** |

---

## The "setup → punchline" cut pattern

The most important pattern in the video:

1. **Graphic sets up the visual structure** (e.g. star diagram with Startups, Valuation, Copycat Models)
2. **Hard cut to white** (a brief flash of pure white or black)
3. **Staggered phrase type delivers the argument** ("You will rarely see a startup solving an actual problem")

The graphic is a visual metaphor; the text is the editorial position. They never appear simultaneously.

> In HyperFrames terms, the "hard cut to white" is a scene boundary: the outgoing scene is fully visible, then a short white-flash transition (a GSAP `opacity` flash on a full-bleed white clip) carries into the next scene. Per the scene-transition rules, the transition *is* the exit — don't exit-animate the diagram before it.

**Other examples of this pattern:**
- 75/25 circles (visually: Medici kept most) → cut to talking head ("and this single investment proved…")
- $70k circle vs $355M circle → cut back → "5000 TIMES" impact word over talking head
- "Big problem 2" section header → cut to talking head to start the explanation

---

## How the hook works (0:00–1:40)

The first 100 seconds do 4 things in rapid succession:

1. **Credential shot** (0:00): Talking head, direct-to-camera, high confidence opener
2. **Problem evidence** (0:15): News articles — shows scale of the problem *before* explaining it
3. **Data point** (0:27): "100+ UNICORNS" India map — shows we're not failing by simple metrics
4. **Core thesis** (1:00): Star diagram + "You will rarely see a startup solving an actual problem" — the **whole video in one graphic**
5. **Intro jingle** (1:30–1:40): Breather, channel branding

**Key lesson:** The thesis graphic (star diagram) appears at ~1:00 — *before* any explanation. The viewer sees the conclusion first, then the video explains why. This is a hook-first, evidence-second structure.

---

## Historical narrative section (2:00–5:00)

The editor uses **B-roll illustrations** to cover the long historical narration:

| SRT content | Visual used |
|------------|------------|
| "15th century Europe, rich ruling class gave money to explorers" | Medieval king painting (slow Ken-Burns pan) |
| "Medici Bank commenda contracts" | 75/25 circle comparison |
| "Merchants made voyages, ship sank or came back empty" | Stormy ship painting |
| "Countries used VC concept — Portugal 1419, Spain 1492…" | Historical map + flag timeline |
| "US post-WW2 — MIT, Harvard, Stanford" | Blank ground (transition) → Wright Brothers photo |
| "ARD invested $70,000 in Ken Olsen and Harlan Anderson" | Scrambled text → "70,000 DOLLARS" |
| "Worth $355–450 million at liquidation" | Two-circle comparison |
| "Greylock, Bessemer, Kleiner Perkins, Sequoia" | USA map + label popins |
| "Apple, Microsoft, Google, Amazon" | Company logos cluster |

**Pattern:** Every named entity gets a visual. The editor never lets a proper noun hang without something to look at.

---

## Evidence-stacking technique

In the Problems section (7:00–11:20), the editor front-loads evidence *before* the argument:

**Sequence for each problem:**
1. Section header card ("Big problem with Indian Venture Capital 2")
2. 2–3 pieces of evidence (articles, quotes, data)
3. Host articulates the argument
4. One punchy text card summarizes the point
5. Back to talking head for transition

**Evidence types used per problem:**

| Problem | Evidence shown |
|---------|---------------|
| #1: Foreign money | Byju's ad → India-US relations news → funding winter article |
| #2: Risk aversion | Vinod Khosla quote card → Forbes Bugworks article → founder quote ("I would have had to shut") |
| #3: No domestic institutions | ET article ("LIC/EPFO invest in startups") → LIC AUM news |

---

## Solutions section — card-stacking pattern (11:20–13:40)

This section feels different because the cards **accumulate on screen** rather than replacing each other:

- Solution #1 appears alone
- Solution #2 appears, #1 stays → both visible
- Solution #3 appears, #1 and #2 stay → all 3 visible

This works because the host is summarizing, not arguing — the viewer needs to see all options simultaneously to compare. It's a deliberate switch from the "one thing at a time" pacing of the Problems section.

> In HyperFrames, accumulation is natural: give each card its own `data-start` (staggered ~2s apart) and a long enough `data-duration` to stay on screen through the end of the section. They occupy different `data-track-index` values (no time overlap on a single track), and GSAP `gsap.from()` entrances reveal each one as it arrives.

After each solution card, the editor cuts to an article/announcement that proves it's already happening (IIT Madras fund, SIDBI fund, etc.) — evidence that the solution is viable.

---

## Background aesthetic rules

- **Primary bg:** Off-white with a slight paper texture — NOT pure #FFFFFF. This is consistent across ALL motion graphic plates.
- **Heavier beats:** Some plates use a darker, muted ground with light text for more serious/heavy moments (the "Indian Founder building a startup" card and "Byju's" cards). Keep these muted and warm, not a high-contrast cold void.
- **Never mix** two background treatments in the same scene — each plate is consistently one or the other.

---

## Typography rules

| Usage | Style |
|-------|-------|
| Concept labels (in diagram nodes) | White text, bold, inside colored circle |
| Phrase type (punchlines) | Helvetica-weight sans, gray for context / bold black for emphasis |
| Definition title | Large, bold, centered |
| Definition body | Small, light-weight, gray |
| Numbers on circles | Very large, bold, same color as circle but lighter tint |
| Section headers (#1 #2 #3) | Huge number + small body, left-aligned |
| Article overlays | Replicated from real source fonts |

> HyperFrames guardrails apply: headlines 60px+, body 20px+, labels 16px+, and `font-variant-numeric: tabular-nums` on the big numerals so counters don't jitter.

---

## What NOT to do (anti-patterns this editor avoids)

- ❌ **No crossfades between scenes** — every cut is a hard cut (including to/from graphics). (Note: HyperFrames multi-scene comps require a transition between scenes — a *hard cut* here means a fast/instant transition, e.g. a 1–2 frame white flash, not a slow dissolve.)
- ❌ **No text animations that take >1s** per phrase — stagger is fast, ~0.25s per phrase group
- ❌ **No decorative transitions** (wipes, slow zooms between sections) — keep cuts hard and fast
- ❌ **No graphics without a clear argument reason** — every visual earns its screen time
- ❌ **No on-screen text during talking head** unless it's a brief overlay impact word ("5000 TIMES")
- ❌ **No text on generated images** — all labels/numbers are rendered by HyperFrames typography (HTML + CSS), not baked into illustrations

---

## Grid inventory

All grids saved in `grids/`. Use them — don't re-generate what's already here.

| Grid file | Content | Resolution |
|-----------|---------|-----------|
| `01_full_overview_4x4.jpg` | Whole video, 16 frames, ~52s apart | Overview map |
| `02_first_2min_4x4.jpg` | 0:00–2:00, ~7.5s/cell | Hook section |
| `03_intro_45s_3x3.jpg` | 0:00–0:45, ~5s/cell | Dense intro |
| `04_min2-4_4x4.jpg` | 2:00–4:00, ~7.5s/cell | Historical narrative |
| `05_min4-6min30_4x4.jpg` | 4:30–6:30, ~7.5s/cell | ARD/70k story + USA map |
| `06_min7-8_4x4.jpg` | 7:00–8:20, ~5s/cell | Problem 1 evidence |
| `07_min8_45-10_20_4x4.jpg` | 8:50–10:20, ~5.6s/cell | Problem 2–3 evidence |
| `08_min10_20-12_40_4x4.jpg` | 10:20–12:40, ~8.75s/cell | Flipkart + Solutions |
| `zoom_startups_anim_3x3.jpg` | 62s–68s, ~0.67s/cell | **Star diagram animation** |
| `zoom_startups_hunt_4x4.jpg` | ~1:00–1:15, ~0.9s/cell | Star diagram wide |
| `zoom_startups_star_4x4.jpg` | Medieval king section, ~2s/cell | Ken Burns B-roll |
| `zoom_paper_stack_4x4.jpg` | ~1:46–1:79, ~2s/cell | Definition cards |
| `zoom_pie_4x4.jpg` | ~8:10, ~2s/cell | 70k circles (zoomed) |
| `zoom_75_25_medici_3x3.jpg` | 2:33–2:42, ~1s/cell | **75/25 circle animation** |
| `zoom_70k_355M_3x3.jpg` | 4:40–4:52, ~1.5s/cell | **Scrambled text + circles** |
| `zoom_usa_vc_map_4x4.jpg` | 4:58–5:13, ~1s/cell | **Map label popins** |
| `zoom_2pct_pie_3x3.jpg` | 11:36–11:50, ~1.75s/cell | **2-3% pie + solutions cards** |
| `zoom_10kcrore_3x3.jpg` | 12:22–12:34, ~1.5s/cell | **Equation card + 100x** |
