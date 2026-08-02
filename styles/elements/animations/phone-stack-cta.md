# Phone-stack community CTA (tilted 3D stack, "Want to stay…")

The closing beat: a tilted, 3D-perspective STACK of phone mockups showing a community/WhatsApp page
(presenter avatar, member rows, Add/Search controls), with a "Want to stay updated?" headline and a
join CTA. Drives the viewer to a community/follow action.

## Look
- 2–3 phone frames fanned in a stack, the front one in focus showing the "AI Updates Community"
  page (group avatar = presenter, member-count, Add Members / Groups / Search rows in SF Pro).
- 3D tilt via CSS `transform: perspective(1200px) rotateY(-18deg) rotateX(6deg)`; soft drop shadow
  behind the stack for depth; back phones slightly smaller + dimmed for parallax.
- Headline above/beside: bold ("Want to stay updated?"), CTA chip below ("Join →" / "Tap to join").
- Background = section gradient; keep the avatar full-bleed OR off the stack — never a graphic on the
  face (if avatar is full-bleed at CTA, the stack + headline live in the LOWER third, top ≥ ~1130).

## Motion (seek-safe on `tl`)
```js
// stack flies in tilted + settles; back phones parallax; headline + CTA follow
tl.fromTo("#stack", { y: 80, opacity: 0, rotateY: -32 },
                    { y: 0, opacity: 1, rotateY: -18, duration: 0.6, ease: "power3.out" }, t0);
tl.fromTo("#phone-back", { x: 40, opacity: 0 }, { x: 0, opacity: 0.85, duration: 0.5, ease: "power2.out" }, t0 + 0.1);
tl.fromTo("#cta-head", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, t0 + 0.45);
tl.fromTo("#cta-chip", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }, t0 + 0.7);
// gentle idle float to keep it alive (seek-safe: a yoyo tween on tl, not rAF)
tl.to("#stack", { y: -10, duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: 1 }, t0 + 1.0);
```

## Key ideas
- All transforms on `tl` (incl. the idle float as a yoyo tween) — no rAF/CSS-infinite loops, so it
  renders frame-exact.
- The tilt + parallax + shadow sell "3D stack" cheaply; keep the front phone's text readable.
- This is the payoff frame — make the action unmissable (one headline, one CTA chip). Don't clutter.
- Recolor the mock to whatever community you're driving to (WhatsApp green, Telegram blue, etc.);
  keep real platform UI cues so it reads as a genuine page.
