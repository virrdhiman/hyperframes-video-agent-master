# Ken Burns zoom + pan b-roll (mobile-friendly)

**Scope:** use this for HORIZONTAL (landscape) source clips placed in a VERTICAL 9:16 edit.
(Vertical/9:16 source already fills the frame — no special framing needed; just pan/zoom if wanted.)

**Why:** horizontal screen-recording b-roll looks tiny on a 9:16 phone. Make it BIG, then
slowly pan/zoom so detail is readable and the clip feels alive (it "bounces in" then drifts).
Source: Postiz promo (`projects/postiz`).

## ⚠️ SIZE THE WHOLE FRAME — fill 80–90% of screen width (the owner correction, 2026-06-07)
The impact comes from how BIG the b-roll FRAME (the `.pwin` window) is on screen — NOT from
zooming the video inside a small fixed window.
- **Mistake to avoid:** keeping a small/medium window and only scaling the inner `.pvid` (e.g.
  1.16→1.24). The frame's overall footprint stays the same → viewer perceives NO impact. ❌
- **Do this instead:** make the WINDOW itself fill ~**80–90% of the 1080px screen width**
  (~**864–972px wide**) so the horizontal clip reads large on a phone. The Postiz window
  (956px ≈ 88%) is the right footprint — lead with that size. ✅
- **Entrance = grow the FRAME:** bounce the whole `.pwin` in (scale ~0.92→1 or width small→full)
  so the big frame itself is the moment of impact. THEN run the inner Ken Burns drift.
- Inner `.pvid` zoom/pan is the secondary "alive" layer on top — keep it, but it is NOT what
  creates the size impact.

## Structure (overflow-clipped window + over-scaled inner video)
```css
.pwin { position:absolute; left:62px; top:526px; width:956px; height:642px;
        overflow:hidden; border-radius:..; z-index:4; }   /* the visible frame */
.pvid { position:absolute; inset:0; width:100%; height:100%;
        object-fit:cover; will-change:transform; backface-visibility:hidden; }
```
HTML: `<div class="pwin" data-layout-allow-overflow><video class="pvid clip" .../></div>`
The inner video is scaled >1 so transform pan/zoom NEVER spills the window.

## Motion (per panel, seek-safe on `tl`)
```js
// PANELS: [winId, vidId, chromeId, start, dur, kenburns{tx0,tx1,ty0,ty1,s0,s1}]
tl.fromTo(vid,{x:kb.tx0,y:kb.ty0,scale:kb.s0},
              {x:kb.tx1,y:kb.ty1,scale:kb.s1,duration:dur,ease:"sine.inOut"},start);
```
- Start scale ~**1.16**, end ~**1.22–1.27** (slow zoom-in over the clip).
- Pan ±~62px horizontal / ±~14–28px vertical; alternate direction per clip so it feels varied:
  - channels: pan L→R  `{tx0:-62,tx1:62, ty0:-14,ty1:14, s0:1.16,s1:1.24}`
  - composer: pan R→L  `{tx0:62, tx1:-62,ty0:12, ty1:-12,s0:1.16,s1:1.24}`
  - calendar: zoom + pan DOWN `{tx0:18,tx1:-18,ty0:-28,ty1:28,s0:1.16,s1:1.27}`
  - docker:   pan L→R up-drift `{tx0:-62,tx1:62,ty0:14,ty1:-14,s0:1.16,s1:1.22}`
- Ease `sine.inOut` = smooth start/stop (no jerk).
- Entrance pop = bounce the WHOLE `.pwin` frame in (scale ~0.92→1, `back.out`) so the big frame
  is the impact, then let the inner drift continue. Don't rely on inner-video zoom for impact.

## Rules
- Re-encode source clips with DENSE keyframes first (1/sec) or the render crashes
  ("video did not decode within 45000ms" → black frames). See MEMORY sparse-keyframe note.
- 60fps render makes the slow pan buttery (graphics are 60; source video stays its native fps).
- Keep the window out of the speaker's face zone.
