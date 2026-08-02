# Red-box sweep caption (TikTok highlight — NO per-word blink)

**DEFAULT captions when you want word-level emphasis** (the owner, 2026-06-25 — rejected the
old per-word fade-in stagger captions as "blinking"). The phrase appears ONCE and HOLDS;
only a red box sweeps the active word in time with the VO. No flicker, no per-word pop.
Based on the HyperFrames `caption-highlight` catalog block, re-tinted to the alert-red accent.

## Why the old one blinked (don't repeat)
Per-word `opacity` fade-in with a stagger + a fast block hide/show = every word flashes
on/off = "blinking". Fix = the whole grouped phrase fades in once and stays static; the
only motion is a red highlight box growing behind the current word.

## CSS (measured, retrofit-2026-06-25)
```css
.capwrap{ position:absolute; left:60px; right:60px; bottom:176px; z-index:72; height:230px;
  display:flex; align-items:flex-end; justify-content:center; }
.capblock{ position:absolute; bottom:0; left:0; right:0; display:flex; flex-wrap:wrap;
  gap:10px 14px; justify-content:center; align-items:flex-end;
  opacity:0; visibility:hidden; will-change:opacity; }
.capblock .w{ position:relative; display:inline-block; font-family:"Outfit",sans-serif;
  font-weight:800; text-transform:uppercase; letter-spacing:0.01em; color:#F4F6FA;
  line-height:1; padding:6px 14px 8px; text-shadow:0 5px 16px rgba(6,8,12,0.7);
  transform-origin:50% 58%; will-change:filter; }
/* the sweeping box — NOTE: NO css `transform` here (gsap owns scaleX; css transform = lint conflict) */
.capblock .w .bg{ position:absolute; inset:0; z-index:-1;
  background:linear-gradient(135deg,#FF5066 0%,#E5384F 100%); border-radius:11px;
  box-shadow:0 12px 30px rgba(229,56,79,0.34); opacity:0; transform-origin:0% 50%; }
.capblock .w .tx{ position:relative; z-index:1; }
```
Each word = `<span class="w"><span class="bg"></span><span class="tx">WORD</span></span>`.

## Timeline (per phrase group, seek-safe)
```js
// phrase appears ONCE and holds — single fade, no per-word stagger
tl.set(blk,{visibility:"visible"},showT);
tl.fromTo(blk,{opacity:0},{opacity:1,duration:0.14,ease:"power2.out",immediateRender:false},showT);
// red box sweeps the active word in time with the VO
g.forEach(function(i,idx){
  var wd=blk.children[idx], bg=wd.querySelector(".bg");
  var ws=WORDS[i][1], we=Math.max(WORDS[i][2],ws+0.14);
  tl.fromTo(bg,{opacity:0,scaleX:0},{opacity:1,scaleX:1,duration:0.16,ease:"power2.out",immediateRender:false},ws);
  tl.fromTo(wd,{filter:"brightness(1)"},{filter:"brightness(1.08)",duration:0.08,ease:"power2.out",immediateRender:false},ws);
  tl.to(wd,{filter:"brightness(1)",duration:0.18,ease:"power2.out"},ws+0.08);
  tl.to(bg,{opacity:0,duration:0.12,ease:"power2.in"},we);   // opacity-only fade-out (no scaleX)
});
tl.to(blk,{opacity:0,duration:0.12,ease:"power2.in"},hideT);
tl.set(blk,{opacity:0,visibility:"hidden"},hideT+0.13);
```
Grouping: ≤4 words per phrase, break on a sentence-end or a >0.45s VO gap. `WORDS[i]` =
`[text, startSec, endSec]` from the aligned transcript (`words.json`).

## Lint gotchas (learned 2026-06-25)
- The `.bg` reveal MUST be `fromTo` (`immediateRender:false`) — a plain `.to(scaleX)` against
  a CSS `transform` triggers `gsap_css_transform_conflict`. Keep `.bg` CSS free of any
  `transform` declaration (opacity:0 hides it pre-roll); the fromTo sets scaleX 0→1 each pass.
- Fade-out is OPACITY-ONLY (no scaleX) so there's no stray transform tween to flag.
