# Motion Pattern Catalog — Indian Venture Capital Reference

Source: `reference.mp4` (~13:46, 1920×1080, 30fps)
All grids are in `grids/`. Each grid has a matching `.json` with exact timestamps.

> General pattern reference, kept as knowledge. Each pattern ends with a **HyperFrames translation** — the same animation expressed as HTML elements (`data-start` / `data-duration` / `data-track-index`, all in seconds) driven by a paused GSAP timeline on `window.__timelines`. Where the original noted a frame number `N` at 30fps, the HyperFrames time is `N / 30` seconds. `gsap.from()` provides entrances; eases that overshoot (`back.out(1.7)`, `elastic.out(1, 0.5)`) replace bouncy springs.

---

## Pattern Index

| # | Pattern | First timestamp | Key grid |
|---|---------|----------------|----------|
| A | Star/wedge diagram | 1:00–1:10 | `zoom_startups_anim_3x3` |
| B | Two-circle scale comparison | 2:34–2:40 | `zoom_75_25_medici_3x3` |
| C | Scrambled text reveal | 4:40–4:42 | `zoom_70k_355M_3x3` |
| D | Map + staggered label popins | 4:58–5:10 | `zoom_usa_vc_map_4x4` |
| E | Staggered phrase type | 1:05–1:08 | `zoom_startups_anim_3x3` |
| F | Definition box card | 1:42–1:52 | `zoom_paper_stack_4x4` |
| G | Numbered solution cards | 11:23–13:15 | `zoom_2pct_pie_3x3` |
| H | Article/screenshot overlay | 0:15, 7:15, 9:55 | `07_min8_45-10_20_4x4` |
| I | Quote bubble card | 8:45 | `07_min8_45-10_20_4x4` |
| J | Cutout photo card | scattered | `zoom_paper_stack_4x4` |
| K | Equation card (X = Y) | 12:28–12:35 | `zoom_10kcrore_3x3` |
| L | Section header card | 8:12 | `06_min7-8_4x4` |
| M | Pie chart (tiny slice) | 11:36–11:42 | `zoom_2pct_pie_3x3` |

---

## A — Star/Wedge Diagram

**When used:** Introducing a multi-part problem where one central entity (Startups) is pulled in conflicting directions.

**Visual structure:**
- 4-pointed black geometric star (not soft — sharp angular spikes)
- Large red filled circle in center, white label text ("Startups")
- Each diagonal wedge has: one colored dot + one label text
  - Top-right wedge: pink dot + "Valuation"
  - Bottom-right wedge: green dot + "Copycat Models"
  - Top-left wedge: blue dot + "Tech" (seen earlier in hunt grid)
  - Bottom-left wedge: yellow dot + "Innovation"
- Light-blue fluid blob connects the star center to the Valuation wedge (bridge metaphor)
- Off-white textured paper background (not pure white)

**Animation sequence** (from `zoom_startups_anim_3x3`, 62s–68s, ~0.67s/frame):
1. Star + center Startups circle + Valuation in top-right + fluid blue bridge → appear together
2. Bridge grows/animates for ~1.5s
3. Camera **pans down-right** (not zoom) — Copycat Models slides into frame from bottom
4. Full composition held ~1s
5. Hard cut to white → staggered phrase type begins

**Key insight:** Pan replaces zoom. The diagram is larger than the frame — you reveal it by moving the camera across it. Each concept lives in its own quadrant.

**HyperFrames translation:**
```js
// Wrap the whole diagram in a non-timed <div class="stage"> larger than the frame.
// Pan by animating the wrapper's x/y (never animate width/height on media).
const tl = gsap.timeline({ paused: true });
// Nodes: scale 0→1 + opacity, overshoot ease
tl.from(".node", { scale: 0, opacity: 0, ease: "back.out(1.7)", stagger: 0.12 }, 0.2);
// Blue bridge: an SVG <path> drawn via stroke-dashoffset 100%→0
tl.from(".bridge", { strokeDashoffset: bridgeLen, duration: 1.5, ease: "power2.out" }, 0.4);
// Camera pan: translate the stage wrapper down-right to reveal the lower wedge
tl.to(".stage", { x: -150, y: -90, duration: 1, ease: "power2.inOut" }, 2.0);
window.__timelines["star-diagram"] = tl;
```

---

## B — Two-Circle Scale Comparison

**When used:** Any time two quantities need visual scale (75%/25% split, $70k vs $355M). Used **twice** in this video — same template both times.

**Visual variants:**
1. **75/25 Medici** (2:34–2:40, `zoom_75_25_medici_3x3`): Blue (75%) + orange (25%). Blue circle large top-left, orange smaller bottom-right. Each has a small icon inside. Labels are large bold numerals inside or beside the circles.
2. **$70k / $355M** (4:44–4:50, `zoom_70k_355M_3x3`): Blue left ("70,000 Dollars"), orange right ("355 & 450 / MILLION DOLLARS"). Orange is MUCH larger, showing the 5000× return. Followed immediately by "5000 TIMES" impact word over talking head.

**Animation sequence (75/25 version):**
1. Talking head hard cut to graphic
2. Blue circle slides **upward** from bottom of frame, settles with overshoot → "75%" label appears
3. Orange circle slides in from bottom-right → "25%" label appears
4. Small icon inside each circle animates in
5. Hold ~2s
6. Cut back to talking head

**Animation sequence (70k/$355M version):**
1. Before the circles: scrambled text → "70,000 DOLLARS" (Pattern C below) — separate beat
2. Then circles: blue comes from **left**, orange from **right**
3. Both settle → hold with numbers
4. Talking head resumes with "5000 TIMES" white text overlaid briefly

**HyperFrames translation:**
```js
// Circle = <div class="clip circle"> with border-radius:50%; background-color.
// Enter via translateY (vertical slide) or translateX (horizontal) with overshoot.
tl.from(".circle-blue",  { y: 400, opacity: 0, ease: "back.out(1.4)", duration: 0.5 }, 0);
tl.from(".circle-orange",{ x: 300, opacity: 0, ease: "back.out(1.4)", duration: 0.5 }, 0.25);
// Labels reveal AFTER the circle settles
tl.from(".label", { opacity: 0, y: 12, ease: "power2.out", stagger: 0.1 }, 0.6);
// "5000 TIMES" impact overlay: a separate clip on its own track over the talking-head scene,
//   opacity 0→1 with a back.out pop.
```

---

## C — Scrambled Text Reveal

**When used:** Dramatic reveal of a specific number or name (e.g., "70,000 DOLLARS"). Feels like a ticker or slot machine.

**Visual:**
- Dollar-bill aesthetic: ornate/condensed serif, greenish color (mimics currency printing)
- Letters shuffle randomly for ~1.5s, then lock into final word
- White background, centered, large type
- Timestamp: 4:40–4:42 (`zoom_70k_355M_3x3` frame 1–2)

**HyperFrames translation:**
```js
// DETERMINISM: no Math.random() at render time. Use a SEEDED PRNG (mulberry32) so the
// scramble is byte-identical every render. Drive per-character locking via tl.call()
// at absolute times, or a single gsap.to({}) proxy with an onUpdate that writes textContent.
const rand = mulberry32(1234);            // seeded
const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ$0123456789";
// Each char locks at a staggered time (left → right); before its lockTime it shows a
// deterministic pseudo-random glyph derived from the current proxy value, not Date.now().
const scramble = (finalChar, t, lockT) =>
  t < lockT ? ALPHABET[Math.floor(rand() * ALPHABET.length)] : finalChar;
// Font: a display serif (e.g. a currency-style face), compiler-embedded by HyperFrames.
```

---

## D — Map + Staggered Label Pop-ins

**When used:** Showing geographic distribution of entities (VC firms, countries). Creates a "filling in the map" effect.

**Visual structure:**
- "VC FIRMS" title fades in on white bg first (~1s)
- USA outline map appears (state border lines only, no fill — drop shadow gives depth)
- Green rectangle label boxes appear one by one, each with a diagonal leader line pointing to its map location
- Label content: company logo icon + name (green fill, white text)
- Sequence: Greylock (East) → Bessemer (East) → Kleiner Perkins (West) → Sequoia (West)
- Spacing: ~1 second between each label appearing

**Animation per label** (from `zoom_usa_vc_map_4x4`, row 2):
- Box pops in with a quick scale from 0
- Leader line draws from map point to box simultaneously

**HyperFrames translation:**
```js
// Map = static asset (img or inline SVG). Labels stagger ~1s apart.
tl.from(".vc-label", { scale: 0, opacity: 0, ease: "back.out(1.7)", stagger: 1.0 }, 1.0);
// Leader line: SVG <line>/<path> with stroke-dashoffset 100%→0 at the same stagger time.
tl.from(".leader", { strokeDashoffset: (i, el) => el.dataset.len, ease: "power2.out",
                     duration: 0.4, stagger: 1.0 }, 1.0);
```

---

## E — Staggered Phrase Type

**When used:** Delivering a pointed verbal argument in text form. Phrase reveals progressively so viewer reads at the narrator's pace.

**Visual:**
- Off-white bg (same paper texture as star diagram)
- Multi-line text, each phrase/clause appears as a unit
- Gray for context words, **bold black** for key words
- All previous phrases stay on screen (cumulative — does NOT wipe)
- Font: clean sans-serif, ~48–60px equivalent

**Exact sequence** (from `zoom_startups_anim_3x3`, cells 5–9):
```
t=2.5s: "You will"                              (gray)
t=2.77s: "You will rarely see a"                (gray)
         "startup"                              (gray, new line)
t=3.03s: "You will rarely see a"
         "startup solving an Actual Problem"     ("Actual Problem" = bold black)
t=3.30s: same, fully settled
t=3.57s: Text repositions/fades for next beat
```

**Timing:** ~0.27s per phrase group (the original's ~8 frames at 30fps).

**HyperFrames translation:**
```html
<span class="phrase">You will </span>
<span class="phrase">rarely see a startup </span>
<span class="phrase">solving an </span>
<span class="phrase bold">Actual Problem</span>
```
```js
// Each .phrase reveals as a unit, ~0.27s apart, and STAYS (cumulative).
tl.from(".phrase", { opacity: 0, y: 8, ease: "power2.out", stagger: 0.27 }, 2.5);
// .bold gets the editorial emphasis (heavier weight, near-black) via CSS, not animation.
```

---

## F — Definition Box Card

**When used:** Introducing a term or concept that needs a quick definition before the argument continues.

**Visual:**
- White/paper bg
- Title word: large, bold, centered ("Venture Capital")
- Thin pink/red rectangle slides in horizontally underneath the title as a highlight bar
- Body text in small gray sans-serif below the bar, types out left-to-right
- Optional: thin border around the whole card

**Sequence** (from `zoom_paper_stack_4x4`, row 2):
1. Title word appears
2. Pink underline box slides in from left (~0.65s) — `scaleX 0→1` from the left origin
3. Body copy fades/types in phrase by phrase

**Variant:** "Venture Capital = Risk Capital" (from `07_min8_45-10_20_4x4`, row 1) — same card but equation format, with supporting paragraph below.

> HyperFrames: the underline bar is the highlight-sweep marker emphasis (`transform-origin:left; scaleX 0→1`, `ease:"power2.out"`). The body "type-out" is a char-by-char reveal via `tl.call(...)` with `steps(1)`-style stepping, kept deterministic.

---

## G — Numbered Solution Cards

**When used:** Solutions/recommendations section. All N cards end up visible on screen simultaneously.

**Visual:**
- Each card: "#1" in large bold left-aligned, short title line, body text below
- Cards appear one at a time (each ~2s)
- They stack/appear side by side on screen — when #2 arrives, #1 stays; when #3 arrives, both #1 and #2 stay
- Font small-medium, body text fills in progressively
- Clean paper bg, minimal styling (just the number and text, no card border)

**Sequence** (from `zoom_2pct_pie_3x3`, cells 4–8):
```
Cell 4: #1 alone — "Try to get more Indian money in the VC Ecosystem"
Cell 5: #1 + #2 — "Encourage our top colleges and"
Cell 6: #1 + #2 fully filled — "...to have their own endowment funds"
Cell 7: All 3 visible (implied)
```

**HyperFrames translation:**
```html
<div class="clip solution" data-start="0"  data-duration="8" data-track-index="0">#1 …</div>
<div class="clip solution" data-start="2"  data-duration="6" data-track-index="1">#2 …</div>
<div class="clip solution" data-start="4"  data-duration="4" data-track-index="2">#3 …</div>
```
```js
// Each card enters on its own data-start and stays (long data-duration through section end).
tl.from(".solution", { y: 30, opacity: 0, ease: "back.out(1.4)", stagger: 2.0 }, 0);
```

---

## H — Article/Screenshot Overlay

**When used:** Evidence for a claim. The editor shows the real article rather than paraphrasing. Used ~5 times.

**Visual variants:**
1. **Full-screen overlay**: Article fills the frame (e.g. Byju's layoff news). Key text highlighted in yellow.
2. **Floating card**: Article appears as a card on the paper bg (e.g. Economic Times, Forbes Bugworks)
3. **Progressive highlight**: First shows the article plain, then highlight box appears over specific text

**Key articles used:**
- YourStory (failing startup collage) — ~0:15
- Byju's layoffs (4500+ employees) — ~0:30
- India-US relations news — ~7:40
- "Funding Winter 2023-2024" — ~7:55
- Forbes "Fighting Superbugs" (Bugworks) — ~8:55
- Economic Times "LIC/EPFO invest in startups" — ~9:54
- LIC AUM ₹54 Lakh Crore — ~10:10
- SIDBI Fund of Funds — ~12:22
- IIT Madras 600 Crore fund — ~11:48

**HyperFrames translation:** Use an `<img>` of the screenshot from `assets/`. For the highlight, sweep a yellow `<div>` marker over the key text region (`scaleX 0→1` from the left, `ease:"power2.out"`).

---

## I — Quote Bubble Card

**When used:** When a founder or expert is being quoted (not the host). Adds credibility + breaks up talking head.

**Visual:**
- Circular headshot photo (no rectangular crop)
- Speech bubble shape behind/around the quote text
- Attribution: "Name, Title, Company" in small text beneath
- Seen at ~8:45 for Sudarshan Kamath (Similibot.ai)
- Another variant at ~7:25: "I would have had to shut [down]" — Anant Anantharaman (Bugworks)

---

## J — Cutout Photo Card

**When used:** Introducing real people (founders, inventors) or a key product.

**Visual:**
- Person/product cut out from background (no white box, isolated figure)
- Placed on paper background
- Label below in simple serif: name + title
- Sometimes 2 people side by side with a shared frame/bubble
- Examples: Robert Noyce + Gordon Moore (rows 2), Flipkart founders (rows 3-4), PDP-1 computer

**HyperFrames translation:** A pre-cut alpha PNG (`remove-background`), placed with a slight tilt, entering via a `gsap.from()` translateY with a settle (`back.out`).

---

## K — Equation Card (X = Y, then × 100)

**When used:** Showing a conversion or scale (currency, multiples).

**Visual sequence** (from `zoom_10kcrore_3x3`, cells 6–9):
1. "10,000 Crore Rupees" — simple centered text, slight gray border box
2. " = " symbol appears
3. "1 Billion Dollars" — second box pops in to the right
4. "100x" with an arrow appears below — implying we need this much MORE

**Spacing:** Clean, wide margins. Equation is the only thing on screen.

---

## M — Pie Chart (minimal slice)

**When used:** Showing a tiny percentage relative to a whole (to emphasize how small the number is).

**Visual** (from `zoom_2pct_pie_3x3`):
- Clean pie circle, almost entirely light blue
- A tiny sliver (2-3%) is dark blue
- Label "2-3%" points to the sliver with a thin line
- "Total Assets" label in the center
- "Even that is [more than enough]" text appears to the right ~1s later

**Insight:** The pie is used to make 2-3% look visually tiny — the argument is even THIS tiny slice is huge in absolute terms.

---

## Additional one-off patterns

### Colorful geometric shape burst (transition plate)
- Appears at ~5:45 for ~0.5s between sections
- Pink/red starburst + blue rectangles + circles + squiggly lines scattered
- A brand transition between major chapters
- Not worth replicating directly but the energy = "visual breath" between dense sections

### "Indian Founder building a startup in…" building illustration
- Flat illustration of a modern office building (~7:00)
- Text types in below the building
- Darker, muted ground (not the paper bg — this section is heavier)

### Chat bubble overlay on founders
- Real photo of Flipkart founders + simulated chat bubble ("if they have to give exit")
- The chat bubble is added in post to simulate a WhatsApp conversation or internal dialogue
- Seen at ~10:20
