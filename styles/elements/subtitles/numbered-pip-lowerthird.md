# Numbered PiP lower-third (the "#NN" item module) — SIGNATURE

The constant lower-band module of the Vaibhav listicle style: talking-head PiP bottom-left + giant
`#NN` (silver # + lime number) + emphasized white caption. Build ONCE, reuse every item. From the
reference reel (`topic_fetch/style_reel_2/fr/f_18s.png`, `f_58s.png`).

## Layout (1080×1920)
- **PiP avatar:** bottom-left, rounded-rect ~r30, **thin white/gray ~2px border**, ~330–340px wide,
  ~y1235–1465. Warm-tinted to match section. The avatar talks; it's the constant human anchor.
- **`#NN`:** to the RIGHT of the PiP, baseline ~y1250–1365. The `#` in silver `#A5A5A5`, the NUMBER
  in lime `#C4FB00`, ultra-bold grotesque, number ~110–130px cap height.
- **Caption:** directly UNDER the number, white `#F9F6FA`, bold SF-Pro-ish, 2–4 lines, tight leading.
  KEY stats/words emphasized inline (heavier weight) — e.g. "AirDrop up to **80% faster**, apps … **30%**".
- All of it lives in the lower band so the upper ⅔ stays free for the content beat.

## Motion (seek-safe on `tl`)
```js
// number stamps in (slight overshoot), then the caption slides up
tl.fromTo("#numNN",{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.30,ease:"back.out(2.2)"}, T0);
tl.fromTo("#hashNN",{opacity:0},{opacity:1,duration:0.18,ease:"power2.out"}, T0);
tl.fromTo("#capNN",{y:24,opacity:0},{y:0,opacity:1,duration:0.26,ease:"power3.out"}, T0+0.12);
// PiP persists; on item-change just crossfade the number+caption, keep the PiP mounted
```

## Key ideas
- The number both LABELS and TRACKS progress through the list — keep it huge and lime.
- PiP stays mounted across items (no re-intro each time); only number + caption swap → fast pace.
- Emphasize the payoff numbers INSIDE the caption sentence; don't make a separate stat card every time.
- Keep the whole module inside the safe band; never let the number/caption touch the PiP avatar.
