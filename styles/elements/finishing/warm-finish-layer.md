# Warm finishing layer + b-roll color-match (reusable element)

The house finishing grade — one unified warm/filmic pass so A-roll + b-roll + graphics read as
one film. Full spec + rationale: `docs/guides/FINISHING_GRADE.md`. Drop these in by reference.

## Finishing layer (top z-index, spans whole timeline, seek-safe)
```html
<div class="finish" aria-hidden="true">
  <div class="finish-warm"></div><div class="finish-vig"></div><div class="finish-grain"></div>
</div>
<style>
  .finish{position:absolute;inset:0;z-index:9000;pointer-events:none}
  .finish-warm{position:absolute;inset:0;mix-blend-mode:screen;opacity:.06;
    background:radial-gradient(circle at 50% 40%,#FFE9C7 0%,transparent 70%)}
  .finish-vig{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.18;
    background:radial-gradient(circle at 50% 46%,transparent 58%,#6B5A3E 100%)}
  .finish-grain{position:absolute;inset:-50%;opacity:.05;mix-blend-mode:overlay;
    background-image:url('assets/common/tex/grain.png');background-size:300px}
</style>
<script>tl.to(".finish-grain",{backgroundPositionX:300,backgroundPositionY:300,duration:DURATION,ease:"none"},0);</script>
```
Measured tunables: warm opacity .04–.08 · vig opacity .12–.22 (color always warm-brown #6B5A3E,
NEVER black) · grain opacity .03–.07. Vignette is *edge focus*, not a dark theme.

## B-roll color-match (wrap each stock clip; never animate the video element)
```css
.broll-graded{filter:saturate(1.08) contrast(1.05) sepia(0.14) brightness(1.04)}
```
Cold/blue tech footage → sepia .16–.22 + brightness 1.06. Warm daylight → sepia .06–.10.

Seek-safe: only the grain background-position is tweened on `tl` (finite, duration-bound). No
rAF / Date / random. Keep warmth consistent within a video, varied across videos.
