# SPLITSCREEN_GUIDE — split-screen & speaker-framing patterns (handoff doc)

Self-contained guide to keeping the talking head and graphics on screen together
**without text or graphics ever covering the face**, in **HyperFrames** (9:16, 1080×1920,
HTML + GSAP). Hand this to any agent/chat.

Core rule: graphics and the speaker occupy **separate zones**. Text never overlaps the face;
the speaker stays in a designated band. Pick the variant that fits the beat.

### HyperFrames mechanics you must respect

- The talking head is a full-frame `<video muted playsinline>` with a separate `<audio>` for
  the VO (never use the video element for audio).
- **You cannot animate or `transform` the `<video>` element directly.** Wrap it in a
  **non-timed** `<div>` and transform/animate the wrapper. (Was `transform: translateY()`
  applied straight to the talking-head layer / `<OffthreadVideo>` in Remotion.)
- Static framing (a fixed crop that pushes the face into a band) = a CSS `transform` on the
  wrapper, set once. Animated framing (face dodging in/out) = a GSAP tween on the wrapper,
  registered on the paused `window.__timelines[...]` timeline.
- Build the static "hero frame" in HTML+CSS first, then add GSAP entrances. Every timed
  visible `div`/`img` needs `class="clip"` + `data-start` + `data-duration` +
  `data-track-index`; the `<video>`/`<audio>` elements OMIT `class="clip"`.
- Verify face-clear with `npx hyperframes snapshot --at <csv>` → Read `snapshots/contact-sheet*.jpg`,
  and `npx hyperframes inspect` for off-canvas/overflow. See **QA_GRID_GUIDE.md**.

> **Cross-reference — the realized face-clear technique in this repo.**
> `build_composition.py` already implements the face-clear principle as a **PUSH-DOWN**: when
> a top graphic appears it springs the talking-head wrapper (`#base-wrap`) DOWN (`y:+330`) so
> the face drops to lower-center and the freed headspace (y≈0–660) becomes a clean graphics
> canvas; it releases (`y:0`) when the graphic exits. That is the HyperFrames realization of
> "push the face into its band so graphics never cover it." The Variants below are the same
> idea applied as fixed bands rather than a momentary dodge.

---

## Variant A — TH-bottom split (content top 55% / talking head bottom 45%)

The default. Overlay content fills the top; the talking head plays underneath and shows
through the bottom band. NOT a card-on-top — fill the top with **large typography, icons, or
B-roll**, not a floating chip on a void.

```html
<!-- talking head: full-frame video, wrapped so we can push the face into the bottom band.
     The wrapper is NON-TIMED (no class="clip" / data-start) — it's the framing layer. -->
<div id="th-wrap" style="position:absolute; inset:0; z-index:1; overflow:hidden;">
  <video id="th" src="assets/talking_head.mp4"
         data-start="0" data-duration="58" data-track-index="0"
         style="width:1080px; height:1920px; object-fit:cover;
                transform: translateY(-180px);"  <!-- face up into the visible bottom band -->
         muted playsinline></video>
</div>
<audio src="assets/talking_head.mp4" data-start="0" data-duration="58"
       data-track-index="1" data-volume="1"></audio>

<!-- top content panel — the freed top 55% (≈0–1056px) -->
<div id="splitA-top" class="clip"
     data-start="6" data-duration="5" data-track-index="2"
     style="position:absolute; top:0; left:0; width:1080px; height:1056px; z-index:5;
            background:#efeae2; overflow:hidden;
            display:flex; flex-direction:column; align-items:center;
            justify-content:center; gap:26px; padding:80px;">
  <!-- BIG type / icons / B-roll here -->
</div>
```

```js
// entrance for the top panel (timeline is paused + registered on window.__timelines)
tl.from("#splitA-top", { y: -40, opacity: 0, duration: 0.5, ease: "back.out(1.7)" }, 6);
```

If the speaker's face sits too low in the source frame, increase the wrapper's
`translateY(-Npx)` to push the face further up into the visible bottom band. The transform is
on `#th-wrap`/`#th` (the framing layer), **never a GSAP tween on the bare `<video>`**. For a
momentary version of this (face dodges down only while the panel is up), use the PUSH-DOWN
pattern from `build_composition.py` instead of a fixed crop.

---

## Variant B — comparison / VS split (two states)

Screen divided to contrast two things (e.g. AWS vs Azure, before/after). Two equal bordered
panels with a **VS** (or arrow) between. Talking head hidden or pushed to a corner.

```html
<div id="splitB" class="clip"
     data-start="15" data-duration="4" data-track-index="3"
     style="position:absolute; inset:0; z-index:6; display:flex; flex-direction:column;
            background:#efeae2;">
  <div class="vs-panel" style="flex:1; margin:60px 60px 12px; border:6px solid #16140f;
       box-shadow:12px 12px 0 rgba(20,18,12,0.85); overflow:hidden;
       display:flex; align-items:center; justify-content:center;">
    <!-- option A: logo / chart / label -->
  </div>
  <div class="vs-badge" style="position:absolute; top:50%; left:50%;
       transform:translate(-50%,-50%) rotate(-3deg); z-index:7;
       font-weight:900; font-size:120px; color:#e5143a;
       -webkit-text-stroke:5px #16140f; text-shadow:8px 8px 0 rgba(20,18,12,0.25);">VS</div>
  <div class="vs-panel" style="flex:1; margin:12px 60px 60px; border:6px solid #16140f;
       box-shadow:12px 12px 0 rgba(20,18,12,0.85); overflow:hidden;
       display:flex; align-items:center; justify-content:center;">
    <!-- option B -->
  </div>
</div>
```

```js
tl.from("#splitB .vs-panel:first-child", { x: -80, opacity: 0, duration: 0.45, ease: "back.out(1.8)" }, 15);
tl.from("#splitB .vs-panel:last-child",  { x:  80, opacity: 0, duration: 0.45, ease: "back.out(1.8)" }, 15.1);
tl.from("#splitB .vs-badge", { scale: 0, rotate: -20, duration: 0.4, ease: "back.out(2)" }, 15.4);
```

---

## Variant C — broadcast band + hero stage (the modern variant)

The whole upper frame is a real hero image / graphic **STAGE** (y≈150–1130); the speaker sits
in a **LOWER band** (y≈1150–1920) behind a hard accent **seam line**; captions sit at the very
bottom, **below the chin**. This reads as a deliberate broadcast cut, not a shrunk rectangle
on a void.

The geometry that makes the face land in the band (full-frame source, face high in frame):

```html
<!-- HERO STAGE — top -->
<div id="heroC" class="clip" data-start="30" data-duration="6" data-track-index="2"
     style="position:absolute; top:150px; left:0; width:1080px; height:980px; z-index:4;
            overflow:hidden; display:flex; align-items:center; justify-content:center;">
  <img src="assets/hero.jpg" style="width:100%; height:100%; object-fit:cover;" />
  <!-- kinetic text over the hero goes here, with its own scrim -->
</div>

<!-- SPEAKER BAND — bottom. A positioned wrapper CROPS the full-frame video, pushing the
     face UP into the band via translateY on a NON-TIMED wrapper (never on the bare video). -->
<div id="th-band"
     style="position:absolute; top:1150px; left:0; width:1080px; height:770px;
            z-index:3; overflow:hidden;">
  <video id="th" src="assets/talking_head.mp4"
         data-start="0" data-duration="58" data-track-index="0"
         style="width:1080px; height:1920px; object-fit:cover;
                transform: translateY(-120px);"  <!-- crop up so the face lands in the band -->
         muted playsinline></video>
  <!-- ink scrim at the TOP edge of the band blends the hard crop into the seam -->
  <div style="position:absolute; top:0; left:0; width:1080px; height:140px;
              background:linear-gradient(to bottom, rgba(0,0,0,0.55), rgba(0,0,0,0));
              pointer-events:none;"></div>
</div>
<audio src="assets/talking_head.mp4" data-start="0" data-duration="58"
       data-track-index="1" data-volume="1"></audio>

<!-- ACCENT SEAM LINE at the seam Y (top of the band) -->
<div id="seam" class="clip" data-start="30" data-duration="6" data-track-index="5"
     style="position:absolute; top:1150px; left:0; width:1080px; height:8px;
            z-index:6; background:#e5143a;
            box-shadow:0 4px 0 rgba(20,18,12,0.35);"></div>

<!-- captions: anchored to the very bottom, below the chin -->
```

```js
// hero stage entrance + seam wipe-in (timeline paused, registered on window.__timelines)
tl.from("#heroC", { scale: 1.06, opacity: 0, duration: 0.5, ease: "power3.out" }, 30);
tl.from("#seam",  { scaleX: 0, transformOrigin: "left center", duration: 0.35, ease: "power3.in" }, 30.1);
```

Notes:
- The `<video>` keeps its full 1080×1920 size; the **`#th-band` wrapper** (overflow:hidden)
  does the cropping and the **`translateY` on the video** lifts the face into the band — both
  are static framing, not timed animation. If you need the face to *enter* the band (animated),
  tween `#th-band` (the wrapper), never the `<video>`.
- The scrim is a child div at the band's top edge — it blends the hard crop into the seam so
  the cut doesn't look like a torn rectangle.
- Captions for broadcast beats anchor to the very bottom (e.g. `bottom: 120px` / extra
  `padding-bottom`) so they sit below the chin, clear of the face.
- This is the same family as `build_composition.py`'s split-screen beat (it springs
  `#base-wrap` DOWN to `y:720` and drops a polaroid-framed stage on top) — Variant C just
  uses a fixed band + seam instead of a momentary push.

---

## Reusable pattern (generic equal split)

For a generic **equal top/bottom split** with rounded bordered panels (e.g. a chart over
B-roll), use two stacked `.clip` panels with a gap — the same structure as Variant A's top
panel, duplicated top and bottom. (Was the `TopBottomSplit_9x16_NewsExplainer_v1.tsx`
reusable component in Remotion; in HyperFrames it's just two positioned `div`s — or install a
split block via `npx hyperframes catalog` / `npx hyperframes add <block>` and check
`docs/guides/COMPONENT_CATALOG.md` for a registry match.) For TH-bottom, prefer **Variant A**
so the speaker shows through full-bleed underneath instead of inside a bordered card.

---

## When to use which (and when NOT to split)

- **Reaction / punchline / hook** → DON'T split. Full-bleed talking head, caption only.
- **Listing models, benefits, steps, a connector flow** → Variant A or C (graphics up top).
- **Two competing things / before-after** → Variant B.
- **A cinematic stat or metaphor** (e.g. a hero image) → hide the speaker, go full-bleed hero,
  put the kinetic text over the image with a scrim.
- Vary it: don't use the same split framing on 3 beats in a row (see the **DENSITY-RUN** rule
  in QA_GRID_GUIDE.md).

## Face-safe rules (non-negotiable)

- Caption band (~y1280–1500) and graphics band must **not** enter the face zone.
- In any split, push the face fully into its band via `translateY` **on the wrapper, not the
  `<video>`** — never let the seam cut the eyes.
- One text block per safe zone at a time; phrase N exits before N+1 enters.
- Never animate the `<video>`'s width/height/top/left or call play/pause/seek — wrap and
  animate the wrapper (HyperFrames owns media playback).
- Verify with `npx hyperframes snapshot` → Read `snapshots/contact-sheet*.jpg` (check the
  seam isn't on the eyes, no graphic on the face) **on every scene**, plus `npx hyperframes
  inspect` for off-canvas. See QA_GRID_GUIDE.md.
