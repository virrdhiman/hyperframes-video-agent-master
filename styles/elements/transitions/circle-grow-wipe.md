# Circle-grow wipe (signature morph)

A small circle pops at a point, scales up to fill the frame, and BECOMES the next scene's
backdrop. The webveda hero "morph" move. Verified from `fb_ref/morph/` dense frame bursts.

## Timing
- Pop in at a point (~0.08s).
- Scale to fill the frame over ~0.3–0.4s (diameter ≥ frame width ≥ 1080px).
- Reverse (radius → 0) to wipe OUT.
- White or brand-blue `#1D31FA`.

## Implement (seek-safe on `tl`)
```js
// transform-origin at the pop point; scale a circle div OR animate clip-path radius
tl.fromTo("#wipe",{scale:0},{scale:1,duration:0.35,ease:"power3.in"},T);
// OR clip-path:
tl.fromTo("#scene",{clipPath:"circle(0% at 50% 40%)"},
                   {clipPath:"circle(150% at 50% 40%)",duration:0.4,ease:"power3.inOut"},T);
```
```css
#wipe{ position:absolute; border-radius:50%; transform-origin:center; will-change:transform; }
```

## Variants
- **Blob / liquid:** wobble `border-radius` / `clip-path` corners as it grows for a liquid morph.
- **Hand-off:** combine with a hard beat cut so the wipe carries text/backdrop into the next scene.

## Rules
- SEEK-SAFE on the GSAP timeline `tl` only — no rAF / Date.
- transform-origin at the actual pop point, not always center.
