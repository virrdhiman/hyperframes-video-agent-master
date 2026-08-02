# Giant two-tone hash + number (#NN signature mark)

The single most recognisable mark of the Vaibhav listicle: an oversized **silver `#`** with a big
**lime number** beside it — `#02`, `#08`, … The hash acts as a chunky decorative anchor; the lime
number reads as the live counter. Use it as the item label on every beat (or as a standalone big
section marker). From `topic_fetch/style_reel_2/fr/f_58s.png`, `f_18s.png`.

## Look (measured)
- **`#` glyph:** silver `#A5A5A5`, ultra-bold grotesque, SAME cap height as the number, set flush to
  its left and slightly overlapping/tucked behind the number so it reads as a backing element — NOT a
  faded watermark, a solid same-size hash in muted silver.
- **Number:** lime `#C4FB00`, ultra-bold, cap height ~110–130px (lower-third scale) — scale up freely
  for a full-screen section marker.
- Two-tone discipline: ONLY these two colors. The silver hash + lime number is the whole identity;
  don't add a third accent. Lime is reserved for the number — never the caption or hash.
- Pairs with the white caption directly below (see `numbered-pip-lowerthird.md`) or stands alone big.

## Motion (seek-safe on `tl`)
```js
// hash fades in first as the backing, number stamps over it with an overshoot
tl.fromTo("#hash", { opacity: 0, x: -12 }, { opacity: 1, x: 0, duration: 0.18, ease: "power2.out" }, t0);
tl.fromTo("#num",  { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.30, ease: "back.out(2.2)" }, t0);
// on item change: keep the hash mounted, crossfade/roll only the number
tl.to("#num", { opacity: 0, y: -18, duration: 0.14, ease: "power2.in" }, tSwap);
tl.fromTo("#num", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.18, ease: "back.out(2)" }, tSwap + 0.14);
```

## Key ideas
- Hash mounts once and persists; only the number swaps per item → snappy counter feel.
- Keep the hash a touch behind the number (z-order / negative letter-spacing) so they read as one mark.
- Works at two scales: small in the lower-third item module, or huge as a full-screen section divider.
- All `tl`-driven (no rAF/Date) so the stamp + roll are frame-exact on render.
