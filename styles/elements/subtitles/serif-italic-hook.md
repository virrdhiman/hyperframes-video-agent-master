# Serif-italic hook headline (cold-open over concept image)

The cold-open title treatment: an elegant serif headline with the key phrase in ITALIC, laid over an
AI-composited concept image, presenter below. From the reference reel (`fr/f_3s.png`:
"So *Apple handed it to Google*").

## Look
- Headline centered in the mid-frame, **white**, mixed weight: plain serif for connective words
  ("So", "it to") + **serif ITALIC** for the punch phrase ("Apple handed").
- Sits over the TOP concept image (e.g. a fabricated "handoff" keynote composite); the presenter
  talking-head occupies the LOWER portion of the frame (not yet a PiP — full cold-open framing).
- Subtle dark scrim behind the text if the image is busy, so the white stays legible.

## Motion (seek-safe on `tl`)
```js
// words rise + fade in, italic phrase a beat later for emphasis
tl.fromTo("#hk-a",{y:26,opacity:0},{y:0,opacity:1,duration:0.32,ease:"power3.out"}, 0.20);
tl.fromTo("#hk-italic",{y:26,opacity:0},{y:0,opacity:1,duration:0.34,ease:"power3.out"}, 0.40);
tl.fromTo("#hk-b",{y:26,opacity:0},{y:0,opacity:1,duration:0.32,ease:"power3.out"}, 0.60);
```

## Key ideas
- Serif + italic = "editorial / credible" tone, a deliberate contrast to the ultra-bold lime numbers
  that follow. The hook feels like a magazine pull-quote; the body feels like a tech deck.
- Pair with ONE strong concept image (real or AI-composited) that states the claim visually.
- Keep the claim short and provocative — it's the scroll-stopper before the list begins.
