# Calendar-fill signature (Postiz)

A month-grid card slides in and fills progressively with glowing dots — visual metaphor for
"schedule one evening → a whole month posts itself". Source: `hf-agent/projects/postiz`.

## Layout (1080×1920)
```css
.cal-kicker{ position:absolute; top:300px; left:0; right:0; text-align:center; font-size:48px;
  font-weight:900; letter-spacing:.03em; color:var(--vio-lt);
  text-shadow:0 0 30px rgba(168,85,247,.5); }      /* "ONE EVENING → A WHOLE MONTH" */
.cal-card{ position:absolute; left:130px; top:470px; width:820px; border-radius:28px;
  background:#100d1a; border:1.5px solid rgba(168,85,247,.4);
  box-shadow:0 30px 80px rgba(0,0,0,.55), 0 0 50px rgba(168,85,247,.2); padding:30px; }
.cal-grid{ display:grid; grid-template-columns:repeat(7,1fr); gap:12px; }   /* 35 cells (5 weeks) */
.cell{ aspect-ratio:1/1; border-radius:14px; background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.06); position:relative; }
.pdot{ position:absolute; left:50%; top:50%; width:34px; height:34px; border-radius:50%;
  transform:translate(-50%,-50%) scale(0);
  background:linear-gradient(150deg,var(--vio-lt),var(--vio));
  box-shadow:0 0 16px rgba(168,85,247,.7); }
```

## Motion (seek-safe on `tl`; example anchored at ~33.6s)
```js
// build 35 cells, each holding a .pdot
tl.fromTo("#calKick",{opacity:0,y:-16},{opacity:1,y:0,duration:0.4,ease:"power3.out"},33.64);
tl.fromTo("#calCard",{opacity:0,y:40,scale:0.95},{opacity:1,y:0,scale:1,duration:0.5,ease:"back.out(1.5)"},33.60);
// fill ~24 of 35 cells progressively over 2.4s (staggered, seek-safe)
var fillIdx=[0,1,3,5,6,7,9,10,11,13,14,16,17,18,20,21,23,24,26,27,28,30,32,33];
var t0=34.0, span=2.4;
fillIdx.forEach(function(ci,k){
  tl.fromTo(cells[ci],{scale:0},{scale:1,duration:0.26,ease:"back.out(2.4)"}, t0+span*k/fillIdx.length);
});
tl.to(["#calKick","#calCard"],{opacity:0,y:20,duration:0.3,ease:"power2.in"},37.10);
```

## Key ideas to reuse
- Dots pop with `back.out(2.4)` overshoot, staggered across the grid (not all at once) = "filling up".
- Leave a few cells empty (24/35) so it reads organic, not a solid block.
- Glow via box-shadow in the brand color; card on the dark panel for contrast.
