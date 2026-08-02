# FINISHING_GRADE.md — one unified grade so the whole video reads as ONE film

Today the three layers — HeyGen A-roll, stock b-roll, CSS graphics — each have their own color.
Stock b-roll skews cold/dark and clashes with the LIGHT/warm theme. A single finishing grade on
top of everything (plus a warm color-match on b-roll) makes the piece feel deliberately shot and
graded, not assembled. **This pass is now standard** — applied in the composition (seek-safe) and
optionally reinforced on the final render.

There are two parts: **(A) the in-composition finishing layer** (always) and **(B) the b-roll
color-match** (per clip). Both are LIGHT — never darken the frame.

---

## A) The finishing layer (paste once, top z-index, spans the whole timeline)
A fixed full-frame overlay that unifies color + adds filmic texture. Pure CSS + one GSAP tween
(seek-safe; no rAF/Date). Keep it SUBTLE — it should be felt, not seen.

```html
<div class="finish" aria-hidden="true">
  <div class="finish-warm"></div>   <!-- warm color wash (screen, light)   -->
  <div class="finish-vig"></div>    <!-- gentle edge focus (NOT a dark box) -->
  <div class="finish-grain"></div>  <!-- 35mm grain, very low opacity       -->
</div>
<style>
  .finish { position:absolute; inset:0; z-index:9000; pointer-events:none; }
  .finish-warm  { position:absolute; inset:0; mix-blend-mode:screen; opacity:.06;
                  background:radial-gradient(circle at 50% 40%, #FFE9C7 0%, transparent 70%); }
  .finish-vig   { position:absolute; inset:0; mix-blend-mode:multiply; opacity:.18;
                  background:radial-gradient(circle at 50% 46%, transparent 58%, #6B5A3E 100%); }
  .finish-grain { position:absolute; inset:-50%; opacity:.05; mix-blend-mode:overlay;
                  background-image:url('assets/common/tex/grain.png'); background-size:300px; }
</style>
<script>
  // imperceptible grain drift so a paused frame never looks like a static PNG (finite/seek-safe)
  tl.to(".finish-grain", { backgroundPositionX: 300, backgroundPositionY: 300,
                           duration: DURATION, ease: "none" }, 0);
</script>
```
Tunables: warmth = `.finish-warm` opacity (.04–.08) + hue (#FFE9C7 warm / #FFF6E0 neutral);
edge focus = `.finish-vig` opacity (.12–.22) — keep the *color* warm-brown, never black;
grain = `.finish-grain` opacity (.03–.07). If `vignette` / `grain-overlay` registry blocks are
installed, you may use those instead — same intent, one consistent look per video.

## B) B-roll color-match (per stock clip)
Stock footage rarely matches the warm palette. Wrap each b-roll element and grade it toward warm
with a CSS filter so it belongs (the video element itself is never animated — grade the wrapper):
```css
.broll-graded { filter: saturate(1.08) contrast(1.05) sepia(0.14) brightness(1.04); }
```
- Cold/blue tech footage → bump `sepia` 0.16–0.22 + `brightness` 1.06 to warm + lift it.
- Already-warm daylight/people footage → `sepia` 0.06–0.10 is enough.
- Goal: a viewer can't tell which shots were stock. Match, don't tint to orange.

## C) Optional final-render grade (ffmpeg)
For a last unifying touch on the delivered file (pairs with the audio master), a light global
warm curve + grain on the mp4:
```bash
ffmpeg -i out/<slug>/<slug>_final.mp4 \
  -vf "curves=r='0/0.03 0.5/0.55 1/1':b='0/0 0.5/0.46 1/0.96',eq=saturation=1.06:contrast=1.04,noise=alls=6:allf=t" \
  -c:v libx264 -crf 17 -preset slow -c:a copy out/<slug>/<slug>_graded.mp4
```
Use sparingly — if the in-composition layer (A) already reads well, skip C. Never crush blacks
or cool the image; this feed is warm + light.

## Reuse
The finishing layer + the b-roll-grade filter live in the style library
(`styles/elements/finishing/warm-finish-layer.md`) — pull them in by reference, don't re-derive.
Tune warmth/grain per video so it's cohesive but not identical frame-to-frame.
