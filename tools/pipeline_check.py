#!/usr/bin/env python3
"""Definition-of-done gate for the daily pipeline. Usage: python3 tools/pipeline_check.py <slug>
Exits 1 (and lists what is missing) until a video is truly ready to deliver."""
import sys, os, json, subprocess, glob, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
slug = sys.argv[1] if len(sys.argv) > 1 else None
if not slug: sys.exit("usage: pipeline_check.py <slug>")
proj = ROOT / "projects" / slug
out  = ROOT / "out" / slug
fails = []
def need(cond, msg):
    if not cond: fails.append(msg)
# 1) brief + director approval
need((proj/"BRIEF.md").exists(), "BRIEF.md missing (director did not lock a brief)")
qa = proj/"QA-REPORT.md"
need(qa.exists() and "APPROVED" in qa.read_text(errors="ignore"), "QA-REPORT.md missing or not APPROVED by director")
# 2) render + properties — the DELIVERABLE is the audio-mastered <slug>_final.mp4
finals = sorted(glob.glob(str(out/"*_final.mp4")))
mp4s   = sorted(glob.glob(str(out/"*.mp4")))
need(bool(finals), "no <slug>_final.mp4 — audio_finish pass (AUDIO_GUIDE) was not run; deliver the mastered file")
probe_target = finals[0] if finals else (mp4s[0] if mp4s else None)
if not probe_target:
    fails.append(f"no rendered mp4 in out/{slug}/")
else:
    try:
        pr = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
            "stream=width,height,r_frame_rate:format=duration","-of","json",probe_target],
            capture_output=True,text=True,timeout=30)
        d = json.loads(pr.stdout); st=d["streams"][0]; dur=float(d["format"]["duration"])
        w=st["width"]; h=st["height"]; need(w==1080 and h==1920, "render not 1080x1920 (%sx%s)" % (w,h))
        need(30 <= dur <= 70, f"duration {dur:.1f}s out of 30-70s range")
    except Exception as e:
        fails.append(f"could not probe render: {e}")
# 2b) AUDIO master — sound-design pass ran + mastered to social loudness (-14 LUFS target)
afj = proj/"audio_finish.json"
if not afj.exists():
    fails.append("audio_finish.json missing (run tools/audio_finish.py — music bed + SFX + -14 LUFS master)")
else:
    try:
        li = json.loads(afj.read_text()).get("measured_lufs")
        need(li is not None and -16.0 <= float(li) <= -12.0,
             f"final loudness {li} LUFS out of -16..-12 target (re-run audio_finish)")
    except Exception as e:
        fails.append(f"could not read audio_finish.json: {e}")
# 2c) BLANK / INVISIBLE-SCENE gate (HARD) — added after retrofit-2026-06-19 shipped "empty after 33s".
#     ROOT CAUSE that this catches: a GSAP fOut() (a .to(opacity:0)) applied to a SCENE CONTAINER that
#     was faded in with fIn (fromTo immediateRender:false) corrupts the opacity baseline when the frame
#     renderer SEEKS a paused timeline → the whole scene renders at opacity 0 for its entire span. QA
#     missed it because `hyperframes snapshot` uses the same seek path (so the snapshots were ALSO blank)
#     and the rubric only checked margins/overflow — a blank frame trips no margin rule. This gate samples
#     the FINAL mp4 once per second, measures whole-frame luma spatial stddev (a flat/empty frame ≈ 0,
#     any real text/cards/face/broll ≫ 15), and BLOCKS if there is a sustained run of near-flat frames.
#     A single transition flash won't trip it; a dead beat (≥3s) will. If it can't run, that is a blocker
#     (never silently skip — same policy as the layout gate).
if finals:
    try:
        import tempfile as _tf, numpy as _np
        from PIL import Image as _Img
        bf = _tf.mkdtemp(prefix="blankcheck_")
        rr = subprocess.run(["ffmpeg","-nostats","-loglevel","error","-i",finals[0],
            "-vf","fps=1,scale=270:480,format=gray", os.path.join(bf,"f_%04d.png")],
            capture_output=True,text=True,timeout=180)
        frames = sorted(glob.glob(os.path.join(bf,"f_*.png")))
        if not frames:
            fails.append(f"blank-frame gate could not sample frames (ffmpeg: {rr.stderr.strip()[:120]})")
        else:
            stds = [float(_np.asarray(_Img.open(p),dtype=_np.float32).std()) for p in frames]
            med = float(_np.median(stds))
            thr = max(10.0, 0.35*med)          # adaptive floor: works for light AND dark themes
            longest = cur = 0; start = -1; worst_start = -1
            for i,s in enumerate(stds):
                if s < thr:
                    cur += 1
                    if cur > longest: longest = cur; worst_start = i-cur+1
                else:
                    cur = 0
            need(longest < 3,
                 "BLANK/INVISIBLE-SCENE: %ds of near-flat frames (std<%.1f) starting ~%ss in %s — a scene "
                 "likely rendered at opacity 0 (check for fOut() on a scene CONTAINER; fade inner content "
                 "instead). Eyeball that stretch in the mp4." % (longest, thr, max(worst_start,0), os.path.basename(finals[0])))
    except Exception as e:
        fails.append(f"blank-frame gate could not run ({e}) — cannot certify the video isn't blank; install numpy+PIL+ffmpeg or eyeball the mp4")
# 3) A-roll present (or tts fallback declared in brief)
brief_txt = (proj/"BRIEF.md").read_text(errors="ignore").lower() if (proj/"BRIEF.md").exists() else ""
has_aroll = bool(glob.glob(str(proj/"avatar*.mp4"))) or bool(glob.glob(str(proj/"*aroll*.mp4")))
need(has_aroll or "tts" in brief_txt or "kokoro" in brief_txt, "no HeyGen A-roll (avatar*.mp4) and no TTS fallback declared in BRIEF")
# 3b) HOOK engineering — the brief must spec hook variants (the Director picks one)
need("hook" in brief_txt, "BRIEF has no hook plan (HOOK ENGINEERING: spec 2-3 hook variants, pick the strongest)")
# 3c) A-ROLL ALPHA gate (HARD) — added after retrofit-2026-07-05 shipped a solid WHITE studio box behind
#     the talking head. ROOT CAUSE: the cutout webm was pix_fmt=yuv420p (NO alpha plane) yet still carried
#     an `alpha_mode=1` metadata TAG, so it rendered fully opaque over the B-roll. The old verification
#     trusted the TAG (a false-positive that survives a re-encode). This gate probes every cutout .webm the
#     composition references: pix_fmt MUST be yuva420p AND the alpha plane must actually VARY (transparent bg
#     + opaque subject), else delivery is BLOCKED. See docs/guides/CHROMAKEY_TRANSPARENT_VIDEO.md.
idx = proj/"index.html"
if not idx.exists(): idx = ROOT/"index.html"
_idx_html = idx.read_text(errors="ignore") if idx.exists() else ""
_cutouts = set(re.findall(r'src\s*=\s*["\']([^"\']+\.webm)["\']', _idx_html))
for _p in glob.glob(str(proj/"avatar_cut*.webm")):
    _cutouts.add(os.path.relpath(_p, str(proj)))
_cutouts = {c for c in _cutouts if "backup" not in c.lower()}  # skip *_backup.webm archives
for _rel in sorted(_cutouts):
    _wp = proj/_rel
    if not _wp.exists():
        continue
    try:
        _pf = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
            "stream=pix_fmt","-of","csv=p=0",str(_wp)],capture_output=True,text=True,timeout=30).stdout.strip()
        _amode = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
            "stream_tags=alpha_mode","-of","csv=p=0",str(_wp)],capture_output=True,text=True,timeout=30).stdout.strip()
        # VP8/VP9 WebM store alpha as a hidden secondary plane: a plain probe reports the BASE pix_fmt
        # (yuv420p) even for a fully valid alpha cutout, so pix_fmt ALONE cannot judge. Require EITHER a
        # yuva pix_fmt OR an alpha_mode tag to proceed, then PROVE the alpha by actually decoding it.
        if "yuva" not in _pf and _amode != "1":
            fails.append(f"A-ROLL ALPHA: cutout {_rel} has no alpha (pix_fmt={_pf}, no alpha_mode tag) — it "
                         f"will render a solid WHITE/studio box over the B-roll. Re-cut to ProRes4444 .mov then "
                         f"encode -c:v libvpx-vp9 -pix_fmt yuva420p -auto-alt-ref 0 (see CHROMAKEY_TRANSPARENT_VIDEO.md).")
            continue
        # AUTHORITATIVE check — decode the alpha plane (force libvpx-vp9 so it is EXPOSED; the default
        # decoder hides it) and confirm it VARIES: transparent bg (min<=32) AND opaque subject (max>=200).
        # A flat min~255 = the white-box bug (bg not removed); a flat max~0 = an invisible host. Both blocked.
        import tempfile as _tf2
        _ad = _tf2.mkdtemp(prefix="alphachk_")
        _ap = os.path.join(_ad, "a.png")
        subprocess.run(["ffmpeg","-v","error","-c:v","libvpx-vp9","-ss","1","-i",str(_wp),"-vf","alphaextract",
            "-frames:v","1",_ap,"-y"],capture_output=True,text=True,timeout=60)
        if os.path.exists(_ap):
            import numpy as _np2
            from PIL import Image as _Img2
            _aarr = _np2.asarray(_Img2.open(_ap))
            _amin = int(_aarr.min()); _amax = int(_aarr.max())
            need(_amin <= 32 and _amax >= 200,
                 f"A-ROLL ALPHA: cutout {_rel} alpha does not vary (min={_amin}, max={_amax}) — a real cutout "
                 f"needs a transparent bg (min<=32) AND an opaque subject (max>=200). min~255 = white-box bug; "
                 f"max~0 = invisible host. Re-cut the subject.")
        else:
            fails.append(f"A-ROLL ALPHA: could not decode alpha from {_rel} (alpha plane missing) — re-cut the subject")
    except Exception as e:
        fails.append(f"A-ROLL ALPHA gate could not probe {_rel} ({e}) — cannot certify the cutout has real alpha")
# 4) no leftover template text in the composition
idx = proj/"index.html"
if not idx.exists(): idx = ROOT/"index.html"
if idx.exists():
    tc = ROOT/"tools"/"template_text_check.py"
    if tc.exists():
        r = subprocess.run([sys.executable,str(tc)],cwd=str(idx.parent),capture_output=True,text=True)
        need(r.returncode==0, "template-text check failed (vendor placeholder text on screen) — see template_text_check")
    # 4b) FINISHING grade — the unified warm finishing layer must be present
    html = idx.read_text(errors="ignore")
    need(("finish-warm" in html) or ("class=\"finish\"" in html) or ("finishing" in html.lower()),
         "finishing grade layer missing (FINISHING_GRADE: add the warm finish layer for one unified look)")
    # 4c) LAYOUT AUDIT (automated, HARD) — the mechanical collision/overflow/off-canvas gate.
    #     Added after retrofit-2026-06-15 shipped with caption-on-chips + notch-over-logo overlaps that
    #     the *manual* `hyperframes inspect` pass was supposed to catch but was skipped in the rushed
    #     cron run. Code-enforcing it here means delivery is BLOCKED unless inspect runs clean — diligence
    #     is no longer the only thing standing between a bug and the owner. Dense 40-sample pass; any
    #     ERROR-level layout issue is a blocker. If the tool can't run at all, that is ALSO a blocker
    #     (never silently skip the layout gate).
    try:
        ir = subprocess.run(["npx","hyperframes","inspect",str(proj),"--samples","40","--json"],
            cwd=str(ROOT),capture_output=True,text=True,timeout=240)
        ij = json.loads((ir.stdout or "{}").strip() or "{}")
        ec = int(ij.get("errorCount", 0))
        ic = int(ij.get("issueCount", 0))
        need(ec == 0, f"layout inspect found {ec} ERROR-level collision/overflow issue(s) — run `npx hyperframes inspect {slug}` and fix before delivery")
        if ec == 0 and ic > ec:
            print(f"  ⚠ layout inspect: {ic-ec} non-error layout warning(s) — eyeball `npx hyperframes inspect {slug}`")
    except Exception as e:
        fails.append(f"layout inspect could not run ({e}) — cannot certify layout; run `npx hyperframes inspect {slug}` manually and fix")
    # 4d) CENTERING + WIDTH lint (automated) — root cause of the retrofit-2026-06-15 "everything looks
    #     left-shifted" re-render. A readable block that is text-align:center / translateX(-50%) but laid
    #     out with ASYMMETRIC left/right insets centers on the safe-rect center (~x470), NOT the true
    #     frame center (x540), so it reads off-center on the raw mp4. The correct pattern is symmetric
    #     insets + a width cap (<=~660px) so it both looks centered AND clears the x880 action-rail line.
    #     Flag asymmetric centered containers (insets differing by >40px) for a human centering check.
    import re as _re
    asym = []
    for m in _re.finditer(r"\.([A-Za-z][\w-]*)\s*\{([^}]*)\}", html):
        sel, body = m.group(1), m.group(2)
        if "position:absolute" not in body.replace(" ", ""):
            continue
        centered = ("text-align:center" in body.replace(" ", "")) or ("translateX(-50%)" in body.replace(" ", ""))
        lm = _re.search(r"left:\s*(\d+)px", body); rm = _re.search(r"right:\s*(\d+)px", body)
        if centered and lm and rm:
            l, r = int(lm.group(1)), int(rm.group(1))
            if abs(l - r) > 40:
                asym.append(f".{sel} (left:{l} right:{r}, off by {abs(l-r)}px)")
    if asym:
        print("  ⚠ centering lint: %d centered container(s) with asymmetric L/R insets — verify they look centered on the RAW mp4 (x540), not just inside the safe rect (x470): %s" % (len(asym), "; ".join(asym[:6])))
# 5) the 3 deliverable assets
post = proj/"post.md"
pt = post.read_text(errors="ignore").lower() if post.exists() else ""
need(post.exists(), "post.md missing (no caption/title/thumbnail assets)")
need("caption" in pt, "post.md missing the Instagram caption")
need(("title" in pt) , "post.md missing the YouTube title")
need("thumbnail" in pt or "thumb" in pt, "post.md missing the thumbnail prompt")
if fails:
    print(f"PIPELINE CHECK: FAIL ({len(fails)}) for {slug}")
    for f in fails: print("  ✗", f)
    sys.exit(1)
print(f"PIPELINE CHECK: PASS — {slug} is ready to deliver.")
