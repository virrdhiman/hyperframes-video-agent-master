# Orbit ring — icons rotate one-by-one to equidistant, then gently spin

**Effect:** platform/social icons fly in one at a time, each rotating into its slot until all
sit **equidistant** around a hub, then the whole ring drifts with a slow continuous spin while
each glyph counter-rotates to stay upright. Source: Postiz promo (`projects/postiz`).

## Layout (hub-centered ring; spokes carry connector line + node)
```css
.orbit { position:absolute; left:540px; top:1000px; width:0; height:0; }  /* hub center */
.spoke { position:absolute; left:0; top:0; width:0; height:0; }
.spoke-line { left:-2.5px; top:-245px; width:5px; height:150px; border-radius:3px; }  /* connector */
.node-wrap { left:-75px; top:-365px; width:150px; height:150px; }                      /* node at spoke end */
.node { width:150px; height:150px; border-radius:50%; }  .node svg { width:92px; height:92px; }
.nlabel { top:158px; left:50%; transform:translateX(-50%); font-size:28px; font-weight:800; }
```

## Motion (all seek-safe on `tl`)
```js
var ANG=[0,72,144,216,288];                 // equidistant final angles (360/5)
var TE =[20.60,21.28,22.06,22.40,22.76];    // staggered entrance times
var SWEEP=50, EDUR=0.45, EASE="back.out(1.6)";
gsap.set("#orbit",{rotation:0,transformOrigin:"50% 50%"});
for(var i=0;i<5;i++){
  // spoke rotates from (angle-50°) trailing INTO its slot; node counter-rotates -> upright
  gsap.set("#sp"+i,{rotation:ANG[i]-SWEEP});
  gsap.set("#nd"+i,{opacity:0,scale:0.2,rotation:-(ANG[i]-SWEEP)});
  gsap.set("#ln"+i,{opacity:0,scaleY:0,transformOrigin:"50% 100%"});
  tl.fromTo("#sp"+i,{rotation:ANG[i]-SWEEP},{rotation:ANG[i],duration:EDUR,ease:EASE},TE[i]);
  tl.fromTo("#nd"+i,{rotation:-(ANG[i]-SWEEP)},{rotation:-ANG[i],duration:EDUR,ease:EASE},TE[i]);
  tl.fromTo("#nd"+i,{opacity:0,scale:0.2},{opacity:1,scale:1,duration:EDUR,ease:"back.out(2.2)"},TE[i]+0.02);
  tl.fromTo("#ln"+i,{opacity:0,scaleY:0},{opacity:0.55,scaleY:1,duration:0.30,ease:"power2.out"},TE[i]);
}
// "all settled" pulse
tl.to(["#hub","#nd0".."#nd4"],{scale:1.14,duration:0.22},23.74);
tl.to(["#hub","#nd0".."#nd4"],{scale:1,duration:0.4,ease:"sine.inOut"},23.96);
// gentle continuous spin of the whole ring; glyphs counter-rotate to stay upright
var SPIN=12;  // ~10°/s over the drift window
tl.fromTo("#orbit",{rotation:0},{rotation:SPIN,duration:1.25,ease:"none"},23.30);
for(var j=0;j<5;j++) tl.fromTo("#nd"+j,{rotation:-ANG[j]},{rotation:-(ANG[j]+SPIN),duration:1.25,ease:"none"},23.30);
```

## Key ideas to reuse
- **Equidistant = 360/N degrees apart.** Reveal staggered, each sweeping in from a trailing
  offset (`angle - SWEEP`) with `back.out` so it overshoots into the slot.
- **Counter-rotate every glyph** by `-angle` (and `-(angle+SPIN)` during drift) so icons never
  tilt — they always read upright while the ring rotates.
- Centre on a hub; spokes have zero size, the line + node are positioned along each spoke.
- Slow `SPIN` (~10°/s) on `ease:"none"` = the "keeps rotating slightly" living feel the owner wanted.
