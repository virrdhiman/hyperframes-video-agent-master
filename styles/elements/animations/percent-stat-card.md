# Percent stat card (big % count-up, full-screen)

A single giant percentage slammed full-screen as the proof beat — "30%", "70%", "80%". The number
counts up and pops; a short label sits under it. Cheapest high-impact beat in the system.

## Look
- ONE big number, screen-centered or upper-center, ultra-bold grotesque, ~360–520px cap height.
- Number color = section accent or near-white on the re-tinted gradient foot; the `%` glyph slightly
  smaller and/or lighter. (In the Vaibhav system the giant glyphs stay neutral — lime is numbers-only
  in the LOWER MODULE; a full-bleed stat can use white `#F9F6FA` on the dark gradient foot.)
- Tight label under it (SF Pro, ~38–46px, `#C9C9C9`): "faster AirDrop", "less battery", etc.
- Background = the per-section vertical gradient (light top → section tone bottom). One stat per card.

## Motion (seek-safe on `tl`)
```js
// count-up via a tweened proxy object, written into the DOM each tick (deterministic on seek)
const o = { v: 0 };
tl.to(o, { v: target, duration: 0.7, ease: "power2.out",
           onUpdate: () => { el.textContent = Math.round(o.v) + "%"; } }, t0);
// number pop + label rise on the same tl
tl.fromTo("#stat-num", { scale: 0.6, opacity: 0 },
                       { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.7)" }, t0);
tl.fromTo("#stat-lbl", { y: 24, opacity: 0 },
                       { y: 0, opacity: 1, duration: 0.32, ease: "power3.out" }, t0 + 0.35);
```

## Key ideas
- Count-up MUST be a tweened proxy (`o.v`) written in `onUpdate`, NOT a JS timer/`setInterval` —
  that keeps it frame-exact when HyperFrames seeks during render.
- One number, one label, lots of negative space. Restraint is the premium signal.
- Great rhythm-breaker between a diagram beat and a list beat; hold ~2s then cut.
- Pair multiple stat cards (30/70/80) back-to-back only if each gets its own full beat — never crowd
  two giant numbers on one frame (overlap rule).
