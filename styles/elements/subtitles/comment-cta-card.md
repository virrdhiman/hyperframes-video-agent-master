# End CTA "comment" card (DM-the-link outro)

**Effect:** a clean white card pops up at the end asking viewers to comment a keyword to get a
DM'd link, with a follow row (avatar + handle + Follow pill). Source: Postiz promo end card
(`projects/postiz`, track 8, ~37.7–41.1s).

## Card (white rounded card, lower area, above the safe zone)
```css
.cta { position:absolute; left:60px; right:60px; bottom:360px; z-index:8;
       border-radius:34px; background:#ffffff; padding:44px 46px;
       box-shadow:0 30px 80px rgba(0,0,0,.5), 0 0 0 1.5px rgba(168,85,247,.3); }
.cta-top  { font-size:38px; font-weight:800; color:#6b6480; margin-bottom:14px; } /* "Want the link?" */
.cta-main { font-size:76px; font-weight:900; color:#16121f; letter-spacing:-.02em; line-height:1.02; }
.cta-main b { color:#7c3aed; }                                                     /* keyword highlight */
.cta-sub  { font-size:36px; font-weight:700; color:#6b6480; margin-top:18px; }     /* "→ I'll DM you..." */
.cta-foot { display:flex; align-items:center; gap:18px; margin-top:30px; padding-top:26px;
            border-top:1.5px solid rgba(0,0,0,.08); }
.cta-badge{ width:76px; height:76px; border-radius:50%;                            /* avatar initial */
            background:linear-gradient(150deg,#a855f7,#7c3aed); color:#fff;
            display:flex; align-items:center; justify-content:center; font-size:38px; font-weight:900; }
.cta-handle{ flex:1; font-size:38px; font-weight:800; color:#16121f; }             /* channel name */
.cta-follow{ padding:16px 34px; border-radius:999px; font-size:32px; font-weight:800; color:#fff;
             background:linear-gradient(150deg,#a855f7,#7c3aed); }                 /* Follow pill */
```
Copy pattern: top="Want the link?" · main=`Comment "KEYWORD"` (keyword in brand color) ·
sub="→ I'll DM you the free setup link" · foot = avatar + "Channel Name" + "Follow".

## Motion (seek-safe on `tl`)
```js
tl.fromTo("#cta",{opacity:0,y:50,scale:0.95},{opacity:1,y:0,scale:1,duration:0.5,ease:"back.out(1.4)"},37.80);
tl.to("#cta .cta-follow",{scale:1.08,duration:0.4,ease:"sine.inOut",repeat:3,yoyo:true},38.8); // pulsing Follow pill
```
- Card rises + scales in with a `back.out` overshoot.
- Follow pill gently pulses (yoyo) to draw the eye.
- Captions are SUPPRESSED during the card window (the card owns the lower third) — gate them:
  `if(grp.start<CTA_HI && grp.end>CTA_LO) return;` (CTA_LO≈37.55, CTA_HI≈41.2).

## Reuse notes
- Recolor `--vio/--vio-dk` to the project's brand. Keep card white for contrast on any bg.
- Swap KEYWORD + handle per video. Keep one short keyword (all-caps) for comment automation.
- Sits at `bottom:360px` so it clears the very bottom and any system UI.
