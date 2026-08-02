# Editor texture pass — de-AI the containers (measured, from retrofit-2026-07-11 recut)

**Problem it solves (the owner, 2026-07-12):** clean rounded cards with soft blur shadows and
letterspaced labels read as "AI/UI-designer", not as an editor's cut. This pass makes every
container look physically cut, taped and stamped. Apply to ALL cards/chips/stamps by default.

## The five ingredients (copy-paste CSS)

```css
/* 1. Cards = paper, stacked: crisp corners + HARD offset block shadow (not soft blur) */
.clipcard{background:var(--paper2);border-radius:3px;border:1px solid rgba(20,18,15,.10);
  box-shadow:0 2px 0 rgba(20,18,15,.06),12px 16px 0 rgba(35,28,15,.10),0 26px 54px rgba(35,28,15,.24);}

/* 2. Paper grain multiplied into every container (works over photos too) */
.clipcard::after,.texcard::after{content:"";position:absolute;inset:0;pointer-events:none;
  border-radius:inherit;background-image:url('assets/tex/grain.png');background-size:260px;
  mix-blend-mode:multiply;opacity:.16;}

/* 3. Masking-tape strip, top-centre, slightly rotated (clippings/evidence cards only) */
.clipcard::before{content:"";position:absolute;top:-16px;left:50%;width:150px;height:36px;z-index:3;
  transform:translateX(-50%) rotate(-2.2deg);opacity:.92;pointer-events:none;
  background:linear-gradient(180deg,rgba(233,224,199,.92),rgba(240,233,211,.78));
  box-shadow:0 5px 12px rgba(35,28,15,.18),inset 0 0 10px rgba(35,28,15,.06);}

/* 4. Kicker labels = highlighter swipe, not sterile letterspacing on nothing */
.kick{display:inline-block;padding:3px 12px 5px;transform:rotate(-.5deg);
  background:linear-gradient(101deg,transparent 0 3%,rgba(240,199,76,.42) 3% 97%,transparent 97%);}

/* 5. Red stamps/plates = worn rubber-stamp ink (grain screened OVER the red) */
.stamp-el{position:relative;overflow:hidden;}
.stamp-el::after{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:url('assets/tex/grain.png');background-size:170px;mix-blend-mode:screen;opacity:.22;}
```

## Rules of application
- Every card, chip, ticket-stub, price tag, CTA card: grain (2) + hard shadow (1).
- Photo/logo/evidence clippings + full front-page mocks: also tape (3).
- Every solid red stamp/plate (SOLD OUT, PRICIER, FEEDS, date stamp, follow chip): ink speckle (5).
- Every `.kick`-style label on a light card: highlighter (4). Dark-plate kickers (`.kickl`) stay clean.
- Keep the existing per-card rotation jitter (±0.5–2.4°) and the warm finish layer — this pass
  stacks on top of `warm-finish-layer.md`, it does not replace it.
- Photos inside cards keep their halftone-dot overlay (`radial-gradient` dots, multiply ~.5)
  and `grayscale/contrast/sepia` grade — grain + halftone together read as print.

Companion rules: hosts/annotations in `styles/elements/animations/robust-anchoring.md`;
the "video, not website" beat rules in `docs/guides/HUMAN_EDIT_GUIDE.md` §2b.
