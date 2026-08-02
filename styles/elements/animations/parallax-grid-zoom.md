# Element: Parallax grid zoom / unzoom (squares assemble + focal hero)

A grid of cards where one focal card scales to fill the frame while the siblings
parallax outward (ZOOM) — or the reverse, siblings parallax IN to assemble a grid as
the focal shrinks into place (UNZOOM). Inspired by the eBay Playbook hero transition.
Pure CSS-var driven → SEEK-SAFE (GSAP animates the progress var; no rAF/Date).

Use the pair as a story bridge: ZOOM into a focal card in scene A → UNZOOM out of a
fresh grid in scene B. On the WWDC26 cut: hook = iOS-27 "rumored apps" grid that
parallax-ZOOMs into a glowing Siri orb (semantic bridge into Topic #1 "Siri gets a
brain"); #3 feature grid uses parallax-UNZOOM to assemble 4 glass tiles.

## Source components (HyperFrames registry)
`npx hyperframes catalog --json` → install with `npx hyperframes add parallax-zoom`
and `npx hyperframes add parallax-unzoom`. They install to
`hf-agent/compositions/components/parallax-zoom.html` / `parallax-unzoom.html`
(NOT the project dir). Copy their `<style>` CSS into your project + replicate the
per-card offset JS (the bundled `<script>` runs once at load; in a seek-driven
composition compute offsets yourself at timeline build — see wiring below).

## Mechanism (measured)
ZOOM (`--pz-progress` 0→1):
- `.parallax-zoom-card`: `translate3d(--pz-dx*p, --pz-dy*p, 0) scale(1 - p*0.4)`,
  `opacity: 1 - p*--pz-sibling-fade`.
- focal `[data-pz-focus="true"]`: `scale(1 + p*(--pz-focus-scale - 1))`, opacity 1, z-index 10.
UNZOOM (`--pu-progress` 0→1) is the reverse:
- `.parallax-unzoom-card`: `translate3d(--pu-dx*(1-p), --pu-dy*(1-p), 0) scale(0.7 + 0.3*p)`,
  `opacity: p*--pu-sibling-fade`.
- focal: `scale(--pu-focus-scale - (--pu-focus-scale-1)*p)`, opacity 1.

Each card needs `data-pz-row`/`data-pz-col` (or `data-pu-*`). Per-card dx/dy are derived
from the row/col offset to the focal card, normalized × `--*-sibling-push`.

## Tunables (CSS vars, on the grid)
`--pz-focus-scale` / `--pu-focus-scale` (default 6) · `--pz-sibling-push` /
`--pu-sibling-push` (default 900px) · `--*-sibling-fade` (0–1).
WWDC26 values that read well at 1080×1920: ZOOM `--pz-focus-scale:2.6; --pz-sibling-push:120px;`
UNZOOM `--pu-focus-scale:1.0; --pu-sibling-push:130px;` (a 2×2 grid; focal=top-left at scale 1).

## Seek-safe wiring
1. Add `data-layout-allow-overflow` on the grid (cards translate beyond bounds).
2. Compute per-card offsets ONCE at build (the bundled JS pattern, generalised):
   ```js
   function __pxOffsets(gridSel, cardSel, dxVar, dyVar, prefix, pushVar){
     document.querySelectorAll(gridSel).forEach(grid=>{
       const cards=[...grid.querySelectorAll(cardSel)];
       const f=cards.find(c=>c.dataset[prefix+"Focus"]==="true")||cards[cards.length>>1];
       const fr=+(f.dataset[prefix+"Row"]??0), fc=+(f.dataset[prefix+"Col"]??0);
       const push=parseFloat(getComputedStyle(grid).getPropertyValue(pushVar))||900;
       cards.forEach(c=>{ if(c===f)return;
         const dC=(+c.dataset[prefix+"Col"]||0)-fc, dR=(+c.dataset[prefix+"Row"]||0)-fr;
         const m=Math.hypot(dC,dR)||1;
         c.style.setProperty(dxVar,(dC/m)*push*m+"px");
         c.style.setProperty(dyVar,(dR/m)*push*m+"px"); });
     });
   }
   __pxOffsets(".parallax-zoom-grid",".parallax-zoom-card","--pz-dx","--pz-dy","pz","--pz-sibling-push");
   __pxOffsets(".parallax-unzoom-grid",".parallax-unzoom-card","--pu-dx","--pu-dy","pu","--pu-sibling-push");
   ```
3. Drive progress from the paused GSAP timeline (GSAP CAN tween CSS custom props):
   ```js
   tl.fromTo("#hk-grid",{ "--pz-progress":0 },{ "--pz-progress":1, duration:0.62, ease:"power2.in" }, 7.95);
   tl.fromTo(".grid3", { "--pu-progress":0 },{ "--pu-progress":1, duration:0.8,  ease:"power3.out" }, 40.6);
   ```
4. Pre-hide cards in the master `gsap.set(..., {opacity:0})` and stagger-pop them in
   (`scale 0.3→1, back.out(2), stagger from:"edges"`) BEFORE running the progress tween.

## Face-safe rule
Keep the grid in the lower graphics zone only — the focal scale-up can fill the frame, so
time the zoom for when the avatar is squared/off the hero zone, never over his face.

## Asset note (license-safe glyphs)
For rumored/unannounced products there are NO official assets and leak/concept renders are
copyrighted. Draw your own inline white SVG `<path>` app glyphs (guaranteed to render; the
local snapshot env lacks color-emoji fonts → emoji become tofu). Office-box Chrome HAS color
emoji, so emoji tiles are fine ONLY on office-box renders.

## Reference frames
`out/wwdc26-ios27-top3/` QA frames: `v4_6.7.jpg` (grid + Siri orb, face clear),
`v4_8.3.jpg` (zoom mid-flight), `v4_41.0.jpg` (#3 unzoom grid assembled).
