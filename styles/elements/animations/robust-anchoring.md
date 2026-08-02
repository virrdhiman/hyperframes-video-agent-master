# Robust anchoring — stop host malposition & drawing drift for good

**Problem (recurring):** hosts land too low / cut at the bottom, and rough circles/arrows
miss their target text. Root cause is always the same — placing things with **hard-coded
magic numbers** (`host y=442`, `ellipse at svg 480,190`). Any change to the avatar crop,
text length, or font metrics makes them drift, and the "fix" is another magic number that
breaks next time.

**Rule: never place a host or an annotation with absolute pixel guesses. Anchor to what is
actually on screen.** Three reusable patterns below — copy them into every cutout video.

---

## 1. Face-anchored host (`hX`/`hY`)

Measure the avatar's face position **once**, then every beat declares *where the face should
land* + scale. The translate is computed. Change the avatar → update `HOST_F` only; every beat
still frames correctly.

Measure the face centre in the raw 1080×1920 cutout (once per avatar):
```bash
ffmpeg -y -ss 10 -i avatar_cut.webm -frames:v 1 -pix_fmt rgba /tmp/f.png   # any mid frame
python3 - <<'PY'
from PIL import Image
a=Image.open('/tmp/f.png').convert('RGBA').split()[3]; px=a.load(); W,H=a.size
top=next(y for y in range(0,H,4) if sum(px[x,y]>40 for x in range(0,W,4))>8)
xs=sorted(x for y in range(top,top+300,4) for x in range(0,W,4) if px[x,y]>40)
print('HOST_F ~', {'x':xs[len(xs)//2],'y':top+150})   # face centre
PY
```

Helper (transform-origin MUST be `50% 100%`, the bottom-centre pivot the math assumes):
```js
var HOST_O={x:540,y:1920};      // origin (bottom-centre of the 1080x1920 host)
var HOST_F={x:505,y:545};       // measured face centre — the ONLY per-avatar value
function hX(Tx,s){ return Tx - HOST_O.x - s*(HOST_F.x-HOST_O.x); }
function hY(Ty,s){ return Ty - HOST_O.y - s*(HOST_F.y-HOST_O.y); }
```

Beats become `[t, side, FACE_x, FACE_y, scale, lean]` — you say where the FACE goes:
```js
[ 9.50,"R", 815, 715, 0.60, -18],   // face at (815,715), 0.60 scale, in the bottom-right
```
Entry = same-side off-screen (`rx±1300` for L/R, `ry+720` rise for B). **Punch-ins** re-anchor
the same face target at a higher scale so the face never jumps:
```js
function punch(t,Tx,Ty,s1,s2){
  tl.to(H,{x:hX(Tx,s1),y:hY(Ty,s1),scale:s1,duration:0.24,ease:"back.out(1.6)"},t);
  tl.to(H,{x:hX(Tx,s2),y:hY(Ty,s2),scale:s2,duration:0.4,ease:"power2.inOut"},t+0.24);
}
```
**NO FLOATING HOST — the hard rule.** A chest-up cutout is cut at the frame bottom, so any scale
below ~0.85 lifts that cut edge *into* the frame and the host reads as a pasted, floating island.
Fix: **keep on-screen hosts at scale ≥ 0.85 so the bottom stays off-frame (grounded), and make
room by EDGE-DOCKING** — push the face toward the left/right edge so the far shoulder bleeds off
that side and the centre stays free for content. Never shrink into a mid-frame corner PiP.
Grounded check: screen-bottom = `1920 + hY(Ty,s)` must be ≥ 1920, i.e. `Ty ≥ 1920−1380·s`.

**HOST PRESENCE + COMMITMENT (the owner, 2026-07-12 — locked after the Morning Edition recut;
visibility floor added same day):**
1. **Default-ON at every beat.** Host-off is the exception (hero/AI beats, or one ≤1.5s
   cutaway); an 8s stretch without the host reads as a slideshow — "you removed me from
   the video".
2. **Never mid-frame.** Every dock commits to the LEFT or RIGHT edge **with a lean toward
   centre**. A vertical, centred host = template.
3. **≥50% VISIBLE — the hard floor at ANY edge.** No matter how far the host docks, at
   least **half of the avatar's visible body area stays inside the frame**. With the
   measured face (`HOST_F.x=505` on a full-width chest-up cutout) that means
   **`face_x ∈ [~170, ~910]`** at 0.85–0.95 scale — outside that window more than half the
   body bleeds off and the dock reads as a sliver/"removed". (The shipped values compute to
   ~62–66% visible; the old `face_x 1020+` slivers computed to ≤49% = banned.)
4. **Head ALWAYS fully in frame.** The whole head — hair to chin, both sides — never crops
   at any edge, top included. At 0.9 scale that is `face_x ≥ ~160` and `≤ ~920`,
   `face_y ≥ ~165`; the ≥50% window above already satisfies it horizontally, but check the
   head explicitly on every punch-in (a scale bump can push the head off the top).
5. **FUN leans, always toward the video.** rotateZ only, pointing INTO the content
   (left-docked = +°, right-docked = −°), and scale the playfulness with the dock:
   near-thirds ±6–8°, full edge-docks ±10–14°, lower-corner peeks up to ±16°. Never 0°
   (template), never rotated away from the content, never rotateY.
6. **Dense beats → go LOW, not small.** When poster text owns the upper frame, drop the
   face to `y ≈ 1100–1230` in a lower corner (still ≥0.85, still grounded, still ≥50%
   visible) so the head sits under the type instead of shrinking the host.
7. **Stamps/key stats slam OVER the host** (z-index above the host layer): SOLD OUT /
   PRICIER / 7× landing across the chest is an editor move — never politely tuck them
   beside him, and never let them cover the FACE.

Face-target cheat sheet (1080×1920 — all grounded, all ≥50% visible, head fully in frame):
thirds ~`(±760 from centre,720)` @0.9 lean ±6–8°; **R dock `(880–910,705–730)` @0.9 lean
−10–14° · L dock `(170–200,700–780)` @0.88–0.95 lean +10–14° · lower-R under poster text
`(880–910,1100–1230)` @0.85–0.88 lean −12–16° · lower-L `(170–200,1120)` @0.86 lean +12–16° ·
CTA push-down `(780,815)` @0.82 lean −8°** (docked, never centred).

## 2. Element-anchored annotations (`circleEl`)

A rough circle must read the **target's real box at runtime**, never fixed svg coords. One
full-frame overlay `<svg id="annSvg" viewBox="0 0 1080 1920">` placed **inside** the same
transformed wrapper as the content (so it shares the camera transform); measure the target with
the offset chain (transform-independent) up to that wrapper:
```js
function localBox(el, stop){var x=0,y=0,w=el.offsetWidth,h=el.offsetHeight,e=el;
  while(e&&e!==stop){x+=e.offsetLeft;y+=e.offsetTop;e=e.offsetParent;} return {x,y,w,h};}
function circleEl(id,t,dur,opts){var el=document.getElementById(id);if(!el||!annRc)return;
  function build(){var b=localBox(el,_camwob),cx=b.x+b.w/2,cy=b.y+b.h/2;
    var g=annRc.ellipse(cx,cy,b.w+(opts.padx||60)*2,b.h+(opts.pady||42)*2,
      {stroke:opts.color,strokeWidth:9,roughness:1.6,bowing:2,seed:opts.seed});
    annSvg.appendChild(g);
    g.querySelectorAll("path").forEach(function(p){var L=p.getTotalLength();
      gsap.set(p,{strokeDasharray:L,strokeDashoffset:L});tl.set(p,{strokeDashoffset:L},0);
      tl.to(p,{strokeDashoffset:0,duration:dur,ease:"power2.inOut"},t);
      if(opts.hide)tl.set(p,{strokeDashoffset:L},opts.hide);});}
  document.fonts&&document.fonts.ready?document.fonts.ready.then(build):build();}
```
Wrap only the key phrase in its own `<span id>` and circle that span. **Draw the circle when its
phrase FIRST appears (or on an early word), not on the last word of the beat** — late words leave
no dwell time before the beat cuts. Always pass `hide:` = the beat's end so the mark clears.

## 3. Fixed overlays live OUTSIDE the camera transform

Ticker strips, finishing grade, flash — anything that must stay pinned — must be a **sibling of
the `#camera`/`#camwob` zoom wrapper, not a child.** A top bar inside the camera slides off
screen the moment a punch/zoom fires. Rule: if it should never move, it does not go inside the
element that scales/shakes.

---

**Verify by frame, not by eye-balling code:** after building, drive the runtime
(`window.__player.seek(t)`) to each host beat and each annotation and screenshot — face fully in
frame, not cut, not over the text it should sit beside; circle wraps its words. The measured
helpers make this a spot-check, not a debugging session.
