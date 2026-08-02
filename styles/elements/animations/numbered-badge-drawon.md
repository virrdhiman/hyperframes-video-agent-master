# Numbered-badge draw-on (count-up list reveal)

Small numbered badges (1 → N) appear one-by-one along a path, count-up style — for "rule of N"
lists, step sequences, or word-stacks. From the webveda reel (`fb_ref/`).

## Effect
- Badges ①→⑦ pop in sequence along a curved/vertical path, each a quick scale+fade ~0.1–0.15s apart.
- Variant: a word-stack ("TRY / LOSE / LEARN") rises in one line at a time inside a circle.
- Variant: "100 VIDEOS"-style card badges scale-pop (back.out overshoot) over b-roll.

## Motion (seek-safe on `tl`)
```js
var TB=[ ... ];                 // per-badge entrance times, ~0.12s apart
badges.forEach(function(id,i){
  tl.fromTo(id,{scale:0.2,opacity:0},{scale:1,opacity:1,duration:0.18,ease:"back.out(2.4)"},TB[i]);
});
// word-stack variant: staggered y-rise + fade
words.forEach(function(id,i){
  tl.fromTo(id,{y:30,opacity:0},{y:0,opacity:1,duration:0.22,ease:"power3.out"}, T0 + 0.08*i);
});
```

## Key ideas
- Stagger ~0.08–0.15s = readable count-up, not a blur.
- `back.out` overshoot gives the sticker/badge pop.
- Keep badges in the top band / dedicated zone — never over the face.
