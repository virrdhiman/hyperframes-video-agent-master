#!/usr/bin/env python3
"""Generate index.html — Azure-vs-AWS HyperFrames composition (v3, physical/editorial style).
Key technique: PUSH-DOWN. When a top graphic appears, the talking-head video springs
DOWN so the face drops to lower-center and the freed headspace becomes a clean canvas
for BIG graphics — overlays never cover the face. Physical aesthetic (harsh solid
shadows, thick borders, imperfect rotation, raw typography), bouncy springs + float,
real b-roll, embedded registry blocks (code-snippet / x-post light / tiktok-follow),
red-sweep + kinetic-slam captions, grain. Re-run after editing to regenerate index.html.

Face map (1080x1920 source): head-top y~330, eyes y~600, chin y~920, mic y1040+.
Push-down +330 drops the face to y~660-1250, freeing y0~660 for graphics."""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
words = json.load(open(ROOT / "transcript.json"))
SPEED = 1.10  # global pace — every Retrofit AI video is sped to 1.10x (removes micro-pauses)
def sp(t): return round(float(t) / SPEED, 3)
WORDS = [{"id": f"w{i}", "text": w["text"], "start": sp(w["start"]), "end": sp(w["end"])}
         for i, w in enumerate(words)]
WORDS_JSON = json.dumps(WORDS, ensure_ascii=False)

HTML = r"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      :root { --ink:#16140f; --paper:#efeae2; --red:#e5143a; --aws:#ff9900; --azure:#0a84ff; }
      #root { position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden;
              font-family: "Montserrat", sans-serif; }

      /* warm canvas revealed when the talking head is pushed down */
      #canvas-bg { position: absolute; inset: 0; z-index: 0; background:
        radial-gradient(ellipse at 50% 22%, #f6f2ea 0%, #e7e1d6 70%, #ddd6c8 100%); }
      #base-wrap { position: absolute; inset: 0; z-index: 2; overflow: hidden; will-change: transform; }
      #base { width: 100%; height: 100%; object-fit: cover; }

      /* split-screen */
      #split-top { position: absolute; top: 0; left: 0; width: 1080px; height: 1010px; z-index: 5;
        opacity: 0; overflow: hidden; will-change: opacity; }
      #split-top .frame { position: absolute; inset: 26px 26px 18px 26px; overflow: hidden;
        border: 14px solid #fff; box-shadow: 16px 16px 0 rgba(20,18,12,0.9); background:#000; }
      #split-top video { width: 100%; height: 100%; object-fit: cover; }
      #split-tag { position: absolute; top: 70px; left: 60px; z-index: 7; transform: rotate(-2deg);
        font-weight: 900; font-size: 46px; letter-spacing: 1px; color:#fff; text-transform: uppercase;
        background: var(--red); padding: 14px 26px; box-shadow: 8px 8px 0 rgba(20,18,12,0.9); opacity: 0; }

      /* b-roll full-frame takeovers */
      .broll-wrap { position: absolute; inset: 0; z-index: 6; opacity: 0; overflow: hidden; will-change: opacity; }
      .broll-wrap video { width: 100%; height: 100%; object-fit: cover; }
      .broll-label { position: absolute; top: 130px; left: 60px; transform: rotate(-2deg);
        font-weight: 900; font-size: 56px; letter-spacing: 1px; text-transform: uppercase; color: #fff;
        background: var(--ink); padding: 16px 30px; box-shadow: 10px 10px 0 var(--red); white-space: nowrap; }

      /* embedded registry blocks (full-frame takeovers on warm fill) */
      .embed-wrap { position: absolute; inset: 0; z-index: 7; opacity: 0; overflow: hidden;
        background: var(--paper); display: flex; align-items: center; justify-content: center; will-change: opacity; }
      .embed-host { width: 1080px; }
      .embed-tag { position: absolute; top: 120px; left: 60px; z-index: 8; transform: rotate(-2deg);
        font-weight: 900; font-size: 44px; letter-spacing: 1px; color:#fff; text-transform: uppercase;
        background: var(--red); padding: 12px 26px; box-shadow: 8px 8px 0 rgba(20,18,12,0.9); opacity: 0; white-space: nowrap; }

      /* top graphic zone — lives ABOVE the pushed-down face (y 70..640) */
      .ov { position: absolute; left: 0; width: 1080px; z-index: 12; display: flex;
            flex-direction: column; align-items: center; gap: 26px; opacity: 0; visibility: hidden;
            will-change: transform, opacity; }
      .kicker { font-weight: 900; font-size: 34px; letter-spacing: 6px; text-transform: uppercase;
        color: #fff; background: var(--red); padding: 10px 22px; box-shadow: 7px 7px 0 rgba(20,18,12,0.9);
        transform: rotate(-1.5deg); }
      /* physical polaroid chip holding a logo */
      .pchip { background: #fff; padding: 22px 30px; border: 5px solid var(--ink);
        box-shadow: 10px 10px 0 rgba(20,18,12,0.9); display: flex; align-items: center; gap: 26px; }
      .logo { height: 150px; object-fit: contain; }
      .logo.md { height: 120px; }
      .arrow { font-weight: 900; font-size: 92px; color: var(--ink); }
      .tagchip { background: var(--ink); color: #fff; font-weight: 900; font-size: 54px; letter-spacing: 1px;
        padding: 14px 30px; box-shadow: 9px 9px 0 var(--red); text-transform: uppercase; }
      .modelchip { background: #fff; border: 5px solid var(--ink); font-weight: 900; font-size: 64px;
        color: var(--ink); padding: 16px 36px; box-shadow: 9px 9px 0 var(--red); letter-spacing: 1px;
        white-space: nowrap; display: flex; align-items: center; gap: 18px; }
      .modelchip .dot { width: 26px; height: 26px; border-radius: 50%; background: var(--red); display:inline-block; }
      .vs { font-weight: 900; font-size: 120px; color: var(--red); -webkit-text-stroke: 5px var(--ink);
        text-shadow: 8px 8px 0 rgba(20,18,12,0.25); }
      .bignum { font-weight: 900; font-size: 230px; color: var(--ink); line-height: 0.9;
        font-variant-numeric: tabular-nums; letter-spacing: -6px; text-shadow: 12px 12px 0 var(--red); }
      .bignum.mid { font-size: 170px; text-shadow: 10px 10px 0 var(--red); letter-spacing: -4px; }
      .undertext { font-weight: 900; font-size: 50px; letter-spacing: 2px; text-transform: uppercase;
        color: #fff; background: var(--ink); padding: 12px 26px; box-shadow: 8px 8px 0 var(--red); }
      /* tape-style checklist labels (flat, marker feel — NOT glassy cards) */
      .tape { background: #fffdf7; border-left: 14px solid #11a86b; font-weight: 800; font-size: 50px;
        color: var(--ink); padding: 20px 34px; box-shadow: 8px 8px 0 rgba(20,18,12,0.85);
        display: flex; align-items: center; gap: 20px; white-space: nowrap; }
      .tape .tick { color: #11a86b; font-weight: 900; font-size: 56px; }

      /* caption scrim + captions */
      #scrim { position: absolute; left: 0; right: 0; bottom: 0; height: 520px; z-index: 15;
        background: linear-gradient(to top, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.0) 100%); pointer-events: none; }
      #cap { position: absolute; inset: 0; z-index: 20; pointer-events: none; }
      .cap-group { position: absolute; bottom: 250px; left: 0; width: 100%; display: flex;
        flex-wrap: wrap; align-items: flex-end; justify-content: center; gap: 10px 8px; padding: 0 70px;
        opacity: 0; visibility: hidden; }
      .cap-word { font-weight: 900; text-transform: uppercase; color: #fff; display: inline-block;
        letter-spacing: 0.01em; line-height: 1.05; position: relative; padding: 6px 12px 8px;
        text-shadow: 0 4px 14px rgba(0,0,0,0.6); transform-origin: 50% 70%; }
      .cap-bg { position: absolute; inset: 0; background: var(--red); border: 3px solid var(--ink);
        box-shadow: 5px 5px 0 rgba(20,18,12,0.9); opacity: 0; transform: scaleX(0) rotate(-1deg);
        transform-origin: 0% 50%; z-index: -1; }
      .cap-txt { position: relative; z-index: 1; }

      /* kinetic-slam impact words (upper zone, above the pushed face) */
      #slam { position: absolute; left: 0; width: 1080px; top: 160px; z-index: 22; pointer-events: none; }
      #slam .slam-word { position: absolute; left: 50%; top: 0; width: 900px; margin-left: -450px;
        text-align: center; font-weight: 900; font-size: 86px; color: #fff; text-transform: uppercase;
        letter-spacing: -1px; line-height: 0.98; -webkit-text-stroke: 3px var(--ink);
        text-shadow: 6px 6px 0 var(--red); opacity: 0; }
      #slam .slam-word .hl { color: var(--red); -webkit-text-stroke: 4px var(--ink); }

      /* transitions */
      #flash { position: absolute; inset: 0; z-index: 30; background: #fff; opacity: 0; pointer-events: none; }
      #wipe { position: absolute; inset: 0; z-index: 30; background: var(--red); opacity: 1;
        transform: scaleX(0); transform-origin: left center; pointer-events: none; }

      /* grain polish (subtle, no darkening) */
      #grain-overlay { position: absolute; inset: 0; pointer-events: none; z-index: 25; mix-blend-mode: overlay; }
      #grain-overlay .grain-texture { position: absolute; top:-50%; left:-50%; width:200%; height:200%;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        opacity: 0.07; animation: hf-grain 0.5s steps(1) infinite; }
      @keyframes hf-grain { 0%,100%{transform:translate(0,0)} 20%{transform:translate(-8%,4%)}
        40%{transform:translate(6%,-9%)} 60%{transform:translate(11%,2%)} 80%{transform:translate(-10%,6%)} }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="azure-aws" data-start="0" data-duration="58"
         data-width="1080" data-height="1920" data-fps="30">

      <div id="canvas-bg"></div>
      <div id="base-wrap">
        <video id="base" src="assets/Azure_vs_Aws.mp4" data-start="0" data-duration="58"
               data-track-index="0" muted playsinline></video>
      </div>
      <audio id="vo" src="assets/Azure_vs_Aws.mp4" data-start="0" data-duration="58"
             data-track-index="1" data-volume="1"></audio>

      <!-- split-screen datacenter (polaroid framed) -->
      <div id="split-top"><div class="frame">
        <video id="splitv" src="assets/stock/videos/dc_14900.mp4" data-start="30.2"
               data-duration="4.7" data-media-start="3" data-track-index="2" data-volume="0" muted playsinline></video>
      </div></div>
      <div id="split-tag">Frontier AI &middot; on AWS</div>

      <!-- street takeover -->
      <div class="broll-wrap" id="br-street">
        <video id="brv-street" src="assets/stock/videos/street_27353851_1.mp4" data-start="25.5" data-duration="3.0"
               data-media-start="2" data-track-index="3" data-volume="0" muted playsinline></video>
        <div class="broll-label">ACROSS THE STREET</div>
      </div>
      <div class="broll-wrap" id="br-money">
        <video id="brv-money" src="assets/stock/videos/money_7947464_1.mp4" data-start="22.6" data-duration="2.7"
               data-media-start="0" data-track-index="11" data-volume="0" muted playsinline></video>
        <div class="broll-label" style="box-shadow:10px 10px 0 var(--aws);">$13&nbsp;BILLION</div>
      </div>
      <div class="broll-wrap" id="br-team">
        <video id="brv-team" src="assets/stock/videos/team_6804122_1.mp4" data-start="43.7" data-duration="1.7"
               data-media-start="3" data-track-index="12" data-volume="0" muted playsinline></video>
        <div class="broll-label">4 MILLION DEVS</div>
      </div>

      <!-- embedded registry blocks -->
      <div class="embed-wrap" id="emb-code">
        <div class="embed-host" data-composition-id="vscode-light-modern"
             data-composition-src="compositions/code-snippet-light-modern.html"
             data-start="40.9" data-duration="3.7" data-track-index="5"></div>
        <div class="embed-tag" id="emb-code-tag">Codex &middot; writes &amp; debugs code</div>
      </div>
      <div class="embed-wrap" id="emb-xpost" style="background:#e8edf2;">
        <div class="embed-host" data-composition-id="x-post"
             data-composition-src="compositions/x-post.html"
             data-start="51.4" data-duration="4.2" data-track-index="7"></div>
      </div>
      <div class="embed-wrap" id="emb-tiktok" style="background:transparent;">
        <div class="embed-host" data-composition-id="tiktok-follow"
             data-composition-src="compositions/tiktok-follow.html"
             data-start="55.8" data-duration="2.2" data-track-index="8"></div>
      </div>

      <!-- TOP GRAPHIC OVERLAYS (sit above the pushed-down face) -->
      <div class="ov" id="s1" style="top:120px;">
        <div class="kicker">The old way</div>
        <div class="pchip" id="s1-chip">
          <img class="logo" src="assets/logos/openai.png" />
          <span class="arrow">&#8594;</span>
          <img class="logo" src="assets/logos/microsoft.png" />
        </div>
      </div>

      <div class="ov" id="s3a" style="top:110px;">
        <div class="kicker">Now live on AWS Bedrock</div>
        <div class="modelchip" id="s3a-1"><span class="dot"></span> GPT&#8209;5.5</div>
        <div class="modelchip" id="s3a-2"><span class="dot"></span> GPT&#8209;5.4</div>
        <div class="modelchip" id="s3a-3"><span class="dot"></span> CODEX</div>
      </div>

      <div class="ov" id="s3b" style="top:150px;">
        <div class="pchip" id="s3b-chip"><img class="logo" src="assets/logos/aws.png" /></div>
        <div class="tagchip">AWS Bedrock</div>
      </div>

      <div class="ov" id="s3c" style="top:170px;">
        <div class="pchip" id="s3c-chip" style="gap:40px;">
          <img class="logo md" src="assets/logos/aws.png" />
          <span class="vs">VS</span>
          <img class="logo md" src="assets/logos/azure.png" />
        </div>
      </div>

      <div class="ov" id="s5" style="top:120px;">
        <div class="kicker">Microsoft &#8594; OpenAI</div>
        <div class="bignum" id="s5-num">$0B</div>
        <div class="tagchip" style="background:var(--red);box-shadow:9px 9px 0 rgba(20,18,12,0.9);">into OpenAI</div>
      </div>

      <div class="ov" id="s9" style="top:130px;align-items:flex-start;padding-left:80px;gap:22px;">
        <div class="tape" id="s9-1"><span class="tick">&#10003;</span> Same OpenAI pricing</div>
        <div class="tape" id="s9-2" style="border-left-color:var(--azure);"><span class="tick" style="color:var(--azure)">&#10003;</span> No extra fees</div>
        <div class="tape" id="s9-3"><span class="tick">&#10003;</span> Security you trust</div>
      </div>

      <div class="ov" id="s11" style="top:120px;">
        <div class="kicker">Codex &middot; every week</div>
        <div class="bignum mid" id="s11-num">0</div>
        <div class="undertext">developers, weekly</div>
      </div>

      <div class="ov" id="s12" style="top:150px;">
        <div class="pchip" id="s12-chip" style="gap:34px;">
          <img class="logo md" src="assets/logos/openai.png" />
          <span class="arrow" style="font-size:64px;">+</span>
          <img class="logo md" src="assets/logos/aws.png" />
          <img class="logo md" src="assets/logos/azure.png" />
        </div>
      </div>

      <!-- caption / polish layers -->
      <div id="scrim"></div>
      <div id="cap"></div>
      <div id="slam" data-layout-allow-overflow></div>
      <div id="grain-overlay"><div class="grain-texture"></div></div>
      <div id="flash"></div>
      <div id="wipe"></div>

      <script>
        (function () {
          window.__timelines = window.__timelines || {};
          var SPEED = 1.10;
          function S(t) { return t / SPEED; }
          var DUR = S(58);
          var tl = gsap.timeline({ paused: true });

          /* ===== CAPTIONS ===== */
          var WORDS = __WORDS__;
          var GROUPS = [], cur = [];
          for (var i = 0; i < WORDS.length; i++) {
            cur.push(i);
            var w = WORDS[i], nxt = WORDS[i + 1];
            var endsSent = /[.?!,]$/.test(w.text), gap = nxt ? nxt.start - w.end : 99;
            if (cur.length >= 4 || (endsSent && cur.length >= 2) || (gap > 0.32 && cur.length >= 2) || !nxt) {
              GROUPS.push({ ws: cur[0], we: cur[cur.length - 1] }); cur = [];
            }
          }
          GROUPS.forEach(function (g, gi) {
            var nextStart = gi + 1 < GROUPS.length ? WORDS[GROUPS[gi + 1].ws].start : DUR;
            g.start = WORDS[g.ws].start; g.end = Math.min(WORDS[g.we].end + 0.45, nextStart - 0.02);
          });
          var cc = document.createElement("canvas"), cx = cc.getContext("2d");
          function fitFont(text, base, maxW) { var s = base; while (s > 38) {
            cx.font = "900 " + s + "px Montserrat"; if (cx.measureText(text).width <= maxW) return s; s -= 2; } return 38; }
          var capRoot = document.getElementById("cap");
          GROUPS = GROUPS.filter(function (g) { return g.start < 55.4; });
          GROUPS.forEach(function (g, gi) {
            var grp = document.createElement("div"); grp.className = "cap-group"; grp.id = "cg-" + gi;
            var text = WORDS.slice(g.ws, g.we + 1).map(function (x) { return x.text.toUpperCase(); }).join(" ");
            var size = fitFont(text, 70, 900);
            for (var k = g.ws; k <= g.we; k++) {
              var wEl = document.createElement("span"); wEl.className = "cap-word"; wEl.id = "cw-" + k; wEl.style.fontSize = size + "px";
              var bg = document.createElement("span"); bg.className = "cap-bg"; bg.id = "cb-" + k;
              var tx = document.createElement("span"); tx.className = "cap-txt"; tx.textContent = WORDS[k].text.replace(/[,]$/, "").toUpperCase();
              wEl.appendChild(bg); wEl.appendChild(tx); grp.appendChild(wEl);
            }
            capRoot.appendChild(grp);
            tl.set(grp, { visibility: "visible" }, g.start);
            tl.fromTo(grp, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }, g.start);
            for (var k2 = g.ws; k2 <= g.we; k2++) {
              var wd = WORDS[k2];
              tl.fromTo("#cw-" + k2, { rotate: 0 }, { rotate: -1, duration: 0.1, ease: "power2.out" }, wd.start);
              tl.to("#cb-" + k2, { opacity: 1, scaleX: 1, duration: 0.12, ease: "back.out(2)" }, wd.start);
              tl.to("#cw-" + k2, { rotate: 0, duration: 0.12 }, wd.end);
              tl.to("#cb-" + k2, { opacity: 0, scaleX: 1.02, duration: 0.1, ease: "power2.in" }, wd.end);
              tl.set("#cb-" + k2, { scaleX: 0 }, wd.end + 0.08);
            }
            tl.to(grp, { opacity: 0, duration: 0.1, ease: "power2.in" }, g.end - 0.1);
            tl.set(grp, { opacity: 0, visibility: "hidden" }, g.end);
          });

          /* ===== HELPERS ===== */
          // push the talking head DOWN to free the headspace; release at end
          function push(start, end, amt) {
            start = S(start); end = S(end); amt = amt || 330;
            tl.to("#base-wrap", { y: amt, duration: 0.55, ease: "back.out(1.3)", overwrite: "auto" }, start);
            tl.to("#base-wrap", { y: 0, duration: 0.45, ease: "power3.inOut", overwrite: "auto" }, end);
          }
          function showOv(id, start, end, fromVars, ease) {
            start = S(start); end = S(end); var el = document.getElementById(id);
            tl.set(el, { visibility: "visible" }, start);
            tl.fromTo(el, Object.assign({ opacity: 0 }, fromVars),
              { opacity: 1, x: 0, y: 0, scale: 1, rotate: 0, duration: 0.5, ease: ease || "back.out(1.7)", overwrite: "auto" }, start);
            tl.to(el, { opacity: 0, y: -22, duration: 0.3, ease: "power2.in", overwrite: "auto" }, end - 0.3);
            tl.set(el, { opacity: 0, visibility: "hidden" }, end);
          }
          function floatEl(id, start, end, dy, dr) { // continuous alive float
            start = S(start); end = S(end); var el = document.getElementById(id), cyc = 2.2;
            var n = Math.max(1, Math.floor((end - start - 0.6) / cyc));
            tl.fromTo(el, { y: 0, rotate: 0 }, { y: dy || -10, rotate: dr || 0.8, duration: cyc / 2,
              ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, start + 0.5);
          }
          function fade(id, start, end, enterDur) {
            start = S(start); end = S(end); var el = document.getElementById(id);
            tl.fromTo(el, { opacity: 0, scale: 1.05 }, { opacity: 1, scale: 1, duration: enterDur || 0.32, ease: "power2.out", overwrite: "auto" }, start);
            tl.to(el, { opacity: 0, duration: 0.3, ease: "power2.in", overwrite: "auto" }, end - 0.3);
          }
          function showEl(id, start, end, fromVars, ease) {
            start = S(start); end = S(end); var el = document.getElementById(id);
            tl.fromTo(el, Object.assign({ opacity: 0 }, fromVars),
              { opacity: 1, x: 0, y: 0, scale: 1, duration: 0.42, ease: ease || "power2.out", overwrite: "auto" }, start);
            tl.to(el, { opacity: 0, duration: 0.25, ease: "power2.in", overwrite: "auto" }, end - 0.25);
          }
          function flash(at) {
            at = S(at);
            tl.fromTo("#flash", { opacity: 0 }, { opacity: 0.9, duration: 0.07, ease: "power2.out", overwrite: "auto" }, at);
            tl.to("#flash", { opacity: 0, duration: 0.2, ease: "power2.in", overwrite: "auto" }, at + 0.07);
          }
          function wipe(at) {
            at = S(at);
            tl.set("#wipe", { scaleX: 0, transformOrigin: "left center", opacity: 1 }, at);
            tl.to("#wipe", { scaleX: 1, duration: 0.16, ease: "power3.in", overwrite: "auto" }, at);
            tl.set("#wipe", { transformOrigin: "right center" }, at + 0.16);
            tl.to("#wipe", { scaleX: 0, duration: 0.2, ease: "power3.out", overwrite: "auto" }, at + 0.18);
          }
          function countUp(id, start, end, to, fmt) {
            start = S(start); end = S(end); var el = document.getElementById(id), o = { v: 0 };
            tl.to(o, { v: to, duration: (end - start) - 0.4, ease: "power2.out",
              onUpdate: function () { el.textContent = fmt(o.v); } }, start);
          }
          function slam(html, at, dur) {
            at = S(at); var el = document.createElement("div"); el.className = "slam-word"; el.innerHTML = html;
            document.getElementById("slam").appendChild(el);
            tl.set(el, { visibility: "visible" }, at);
            tl.fromTo(el, { opacity: 0, scale: 1.25, rotate: -4 },
              { opacity: 1, scale: 1, rotate: -2, duration: 0.3, ease: "back.out(1.6)", overwrite: "auto" }, at);
            tl.to(el, { scale: 1.05, rotate: 0, duration: dur - 0.5, ease: "sine.inOut" }, at + 0.3);
            tl.to(el, { opacity: 0, scale: 0.8, duration: 0.22, ease: "power2.in", overwrite: "auto" }, at + dur - 0.22);
          }

          /* ===== BASE KEN BURNS (gentle, on top of push) ===== */
          tl.fromTo("#base", { scale: 1.0 }, { scale: 1.05, duration: DUR, ease: "none" }, 0);

          /* ===== PUSH-DOWN WINDOWS (face dodges down for top graphics) ===== */
          push(0.3, 5.9);     // S1 + slam
          push(6.1, 19.0);    // model chips / bedrock / vs
          push(20.4, 25.2);   // $13B
          push(35.4, 40.6);   // checklist
          push(44.0, 50.9);   // 4M + multicloud

          /* ===== SCENES ===== */
          // S1 hook
          showOv("s1", 0.3, 4.3, { y: 40, scale: 0.9 }); floatEl("s1-chip", 0.9, 4.3, -10, 1);

          // S2 slam "that just changed"
          flash(4.62);
          slam('THAT JUST<br><span class="hl">CHANGED</span>', 4.7, 1.2);

          // S3 announcement — chips appear AS each model is spoken (word-synced)
          var s3a = document.getElementById("s3a");
          tl.set(s3a, { visibility: "visible" }, S(6.2)); tl.set(s3a, { opacity: 1 }, S(6.2));
          var GPT_WORD = [6.36, 7.60, 10.20]; // GPT-5.5 / GPT-5.4 / Codex spoken starts
          ["#s3a-1", "#s3a-2", "#s3a-3"].forEach(function (sel, idx) {
            tl.fromTo(sel, { opacity: 0, x: -60, scale: 0.7, rotate: -5 }, { opacity: 1, x: 0, scale: 1, rotate: (idx-1)*1.5, duration: 0.32, ease: "back.out(2)" }, S(GPT_WORD[idx]));
          });
          tl.to(s3a, { opacity: 0, y: -22, duration: 0.3, ease: "power2.in" }, S(11.2));
          tl.set(s3a, { opacity: 0, visibility: "hidden" }, S(11.5));

          wipe(11.5);
          showOv("s3b", 11.7, 14.9, { scale: 0.8, rotate: -3 }); floatEl("s3b-chip", 12.2, 14.9, -8, 1.2);
          showOv("s3c", 15.1, 19.0, { scale: 0.8 }); floatEl("s3c-chip", 15.6, 19.0, -8, -1);

          // S5 $13B (counter, then cut to money b-roll)
          showOv("s5", 20.4, 22.6, { y: 30, scale: 0.85 });
          countUp("s5-num", 20.7, 22.4, 13, function (v) { return "$" + Math.round(v) + "B"; });
          wipe(22.55); fade("br-money", 22.6, 25.3);

          // S6 street takeover (full-bleed)
          wipe(25.4); fade("br-street", 25.5, 28.4);

          // S8 split-screen (datacenter top / face pushed to bottom)
          flash(30.1);
          tl.to("#base-wrap", { y: 720, duration: 0.5, ease: "power3.out", overwrite: "auto" }, S(30.2));
          tl.to("#base-wrap", { y: 0, duration: 0.45, ease: "power3.inOut", overwrite: "auto" }, S(34.8));
          showEl("split-top", 30.2, 34.8, { y: -40 });
          showEl("split-tag", 30.4, 34.8, { x: -30, rotate: -6 }, "back.out(1.8)");

          // S9 checklist (tape labels)
          var s9 = document.getElementById("s9");
          tl.set(s9, { visibility: "visible" }, S(35.4)); tl.set(s9, { opacity: 1 }, S(35.4));
          var CHK_WORD = [35.64, 37.10, 38.50]; // "same OpenAI pricing" / "no extra fees" / "security"
          ["#s9-1", "#s9-2", "#s9-3"].forEach(function (sel, idx) {
            tl.fromTo(sel, { opacity: 0, x: -70, rotate: -5 }, { opacity: 1, x: 0, rotate: (idx%2?1.5:-1.5), duration: 0.36, ease: "back.out(1.9)" }, S(CHK_WORD[idx]));
          });
          tl.to(s9, { opacity: 0, y: -22, duration: 0.3, ease: "power2.in" }, S(40.3));
          tl.set(s9, { opacity: 0, visibility: "hidden" }, S(40.6));

          // S10 Codex code-snippet takeover
          wipe(40.8); fade("emb-code", 40.9, 43.9, 0.3); showEl("emb-code-tag", 41.2, 43.9, { x: -30, rotate: -5 }, "back.out(1.7)");

          // S11 4M developers — team b-roll cut, then counter
          wipe(43.7); fade("br-team", 43.7, 45.3);
          flash(45.3);
          showOv("s11", 45.4, 47.6, { y: 30, scale: 0.85 });
          countUp("s11-num", 45.55, 47.4, 4000000, function (v) { return Math.round(v).toLocaleString(); });

          // S12 multi-cloud — ai-network b-roll bg + slam + logos
          flash(47.85);
          slam('<span class="hl">MULTI&#8209;CLOUD</span>', 47.95, 1.0);
          showOv("s12", 49.1, 50.9, { scale: 0.8, rotate: -2 }); floatEl("s12-chip", 49.5, 50.9, -8, 1);

          // S13 social proof x-post
          wipe(51.3); fade("emb-xpost", 51.4, 55.6, 0.3);

          // S14 outro tiktok-follow
          fade("emb-tiktok", 55.8, 58.0, 0.3);

          /* ===== caption exit self-lint ===== */
          GROUPS.forEach(function (g, gi) {
            var el = document.getElementById("cg-" + gi); tl.seek(g.end + 0.02);
            var c = window.getComputedStyle(el);
            if (c.opacity !== "0" && c.visibility !== "hidden") console.warn("[caption-lint] grp " + gi + " @ " + g.end.toFixed(2));
          });
          tl.seek(0);
          window.__timelines["azure-aws"] = tl;
        })();
      </script>
    </div>
  </body>
</html>
"""

out = HTML.replace("__WORDS__", WORDS_JSON)
out = out.replace('src="assets/Azure_vs_Aws.mp4"', 'src="assets/Azure_vs_Aws_1.10x.mp4"')
DURH = round(58 / SPEED, 2)
_subs = [
  ('data-composition-id="azure-aws" data-start="0" data-duration="58"', f'data-composition-id="azure-aws" data-start="0" data-duration="{DURH}"'),
  ('id="base" src="assets/Azure_vs_Aws_1.10x.mp4" data-start="0" data-duration="58"', f'id="base" src="assets/Azure_vs_Aws_1.10x.mp4" data-start="0" data-duration="{DURH}"'),
  ('id="vo" src="assets/Azure_vs_Aws_1.10x.mp4" data-start="0" data-duration="58"', f'id="vo" src="assets/Azure_vs_Aws_1.10x.mp4" data-start="0" data-duration="{DURH}"'),
  ('id="splitv" src="assets/stock/videos/dc_14900.mp4" data-start="30.2"\n               data-duration="4.7"', f'id="splitv" src="assets/stock/videos/dc_14900.mp4" data-start="{sp(30.2)}"\n               data-duration="{sp(4.7)}"'),
  ('id="brv-street" src="assets/stock/videos/street_27353851_1.mp4" data-start="25.5" data-duration="3.0"', f'id="brv-street" src="assets/stock/videos/street_27353851_1.mp4" data-start="{sp(25.5)}" data-duration="{sp(3.0)}"'),
  ('id="brv-money" src="assets/stock/videos/money_7947464_1.mp4" data-start="22.6" data-duration="2.7"', f'id="brv-money" src="assets/stock/videos/money_7947464_1.mp4" data-start="{sp(22.6)}" data-duration="{sp(2.7)}"'),
  ('id="brv-team" src="assets/stock/videos/team_6804122_1.mp4" data-start="43.7" data-duration="1.7"', f'id="brv-team" src="assets/stock/videos/team_6804122_1.mp4" data-start="{sp(43.7)}" data-duration="{sp(1.7)}"'),
  ('data-composition-src="compositions/code-snippet-light-modern.html"\n             data-start="40.9" data-duration="3.7"', f'data-composition-src="compositions/code-snippet-light-modern.html"\n             data-start="{sp(40.9)}" data-duration="{sp(3.7)}"'),
  ('data-composition-src="compositions/x-post.html"\n             data-start="51.4" data-duration="4.2"', f'data-composition-src="compositions/x-post.html"\n             data-start="{sp(51.4)}" data-duration="{sp(4.2)}"'),
  ('data-composition-src="compositions/tiktok-follow.html"\n             data-start="55.8" data-duration="2.2"', f'data-composition-src="compositions/tiktok-follow.html"\n             data-start="{sp(55.8)}" data-duration="{sp(2.2)}"'),
]
for old, new in _subs:
    assert old in out, "HTML anchor missing: " + old[:50]
    out = out.replace(old, new)
(ROOT / "index.html").write_text(out)
print(f"Wrote index.html ({len(out)} bytes), {len(WORDS)} caption words injected.")
