# Transparent Talking Head over B-Roll in HyperFrames

How to overlay a talking head on top of B-roll/backgrounds without jitter, halos, or fading.
**Pre-process the subject into a real alpha channel; don't key at render time.**

## TL;DR - The recipe that works

1. Cut the subject out of its background into a VP9+alpha WebM with one command.
2. Drop it in as a muted `<video>`. Chrome decodes VP9 alpha natively, so the surroundings
   are transparent and the B-roll behind shows through.

```bash
# u2net human segmentation -> VP9 + alpha WebM (plays in a composition <video>)
npx hyperframes remove-background assets/stimulus/talking_head.mp4 \
  -o assets/stimulus/subject.webm --quality best
```

```html
<!-- B-roll behind (track 0) -->
<video src="assets/stimulus/broll/spain-city.mp4" muted playsinline
       class="clip" data-start="0" data-duration="10" data-track-index="0"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>

<!-- Cut-out subject on top (track 1) -->
<video src="assets/stimulus/subject.webm" muted playsinline
       class="clip" data-start="0" data-duration="10" data-track-index="1"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
```

That's it. Smooth, opaque subject, no green halo, no per-frame race — and you don't even need
a green screen, because `remove-background` segments the person directly.

## Why `remove-background` instead of keying at render time

A naive approach — key the green out frame-by-frame in canvas/JS during the render — is
fragile: the framework snapshots each frame deterministically, and any per-frame browser
video-paint timing race shows up as a **jittery / frozen** subject. `remove-background` bakes
the alpha into the asset ahead of time, so every frame is already correct when it's seeked.

- **u2net_human_seg (MIT)** does the segmentation locally, no API key. First run downloads
  ~168MB of model weights into `~/.cache/hyperframes/`.
- Output defaults to **`.webm` (VP9 + alpha)**, which Chromium decodes natively — exactly
  what the renderer uses. Also available: `.mov` ProRes4444 (for editors, large) and `.png`
  (a single still cut-out).
- `--quality fast|balanced|best` maps to VP9 CRF 30/18/12 (the segmentation itself is fixed).
  Use **`best`** for masters. `--device auto|cpu|coreml|cuda`.

> **Coming from Remotion?** This replaces the green-screen -> alpha-WebM ffmpeg recipe and
> `<OffthreadVideo transparent>`. You no longer chromakey by hand or wire a transparent video
> component — `remove-background` produces the alpha asset and a plain muted `<video>` plays it.

## Text behind the subject (the "hole-cut" pattern)

To place a headline or graphic **between** the room and the subject — so text passes behind
the person — use the **`--background-output`** plate:

```bash
npx hyperframes remove-background assets/stimulus/talking_head.mp4 \
  -o assets/stimulus/subject.webm \
  -b assets/stimulus/plate.webm \
  --quality best
```

- `subject.webm` = the cut-out (alpha = the subject's mask).
- `plate.webm` = the **hole-cut plate** (alpha = `255 - mask`): the surroundings are opaque
  and the subject's silhouette is transparent.

Stack them with the text in the middle:

```html
<!-- bottom: original take or the plate (track 0) -->
<video src="assets/stimulus/plate.webm" muted playsinline
       class="clip" data-start="0" data-duration="10" data-track-index="0"
       style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>

<!-- middle: the headline that should sit BEHIND the person (z-index:2) -->
<div id="headline" class="clip" data-start="0" data-duration="10" data-track-index="1"
     style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
            font-size:140px; font-weight:800; color:#1a1a1a; z-index:2">
  STIMULUS
</div>

<!-- top: the cut-out subject, wrapped in a NON-TIMED div (z-index:3) -->
<div style="position:absolute; inset:0; z-index:3">
  <video src="assets/stimulus/subject.webm" muted playsinline
         style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
</div>
```

Two rules from the media pipeline that keep this in sync:

1. **Animate the WRAPPER's opacity, not the video's.** The framework forces `opacity:1` on
   any element that carries `data-start`/`data-duration`, so wrap the cut-out in a non-timed
   div and tween the wrapper if you need to reveal it.
2. **Decode both videos in sync.** Give the plate and the cut-out the same `data-start="0"`
   and `data-media-start="0"` so their frames line up.

Reveal the subject at a cut with `tl.set(cutoutWrap, { opacity: 1 }, 3.3)`.

> Sanity test for hole-cut: *"will anything be visible through the subject's silhouette?"* If
> yes, you want the `--background-output` plate. To show the room **without** the person as a
> standalone clean plate you'd need an inpainter (LaMa/ProPainter) — `remove-background` can't
> reconstruct what was behind them.

## Quality notes

- Use `--quality best` for the master cut-out — lower quality CRF can band colors and read as
  a "faded" subject even though the alpha is correct.
- Putting the cut-out over its **own** source video doubles the RGB — only do that with a
  `best`-quality master. Over a *different* take of the same person it looks like two people;
  don't.

## If you must key a green screen manually (generic ffmpeg fallback)

`remove-background` is the primary path. But if you already have a clean studio green screen
and prefer keying, the classic ffmpeg chain still produces a VP9+alpha WebM you can drop into a
muted `<video>` exactly the same way:

```bash
ffmpeg -y -i assets/stimulus/talking_head_green.mp4 \
  -vf "chromakey=0x00ff00:0.12:0.02,format=yuva420p,despill=type=green:mix=0.5:expand=0,format=yuva420p" \
  -c:v libvpx-vp9 -pix_fmt yuva420p \
  -auto-alt-ref 0 -crf 22 -b:v 0 -deadline good -cpu-used 2 \
  -row-mt 1 -threads 8 \
  assets/stimulus/subject.webm
```

| Step | Purpose | Tuning notes |
|---|---|---|
| `chromakey=0x00ff00:0.12:0.02` | Punch a hole in the green. | Similarity 0.12 is tight (only true studio green). Wider (0.30+) eats subject pixels -> subject looks semi-transparent. Blend 0.02 keeps a thin feathered edge. |
| `format=yuva420p` (1st) | Force the alpha plane after chromakey. | Required, else the next step re-outputs yuv420p. |
| `despill=type=green:mix=0.5` | Remove green light bouncing onto the subject. | Bump `mix` to 0.7 if a green halo persists; lower if skin goes magenta. |
| `format=yuva420p` (2nd) | Re-assert alpha before the encoder. | `despill` can drop alpha tagging in some builds. |

Encoder flags that matter:
- `-c:v libvpx-vp9 -pix_fmt yuva420p` — only this combo writes the alpha plane.
- `-auto-alt-ref 0` — **required** for VP9 alpha; otherwise libvpx silently drops alpha.
- `-crf 22 -b:v 0` — perceptual quality. Don't use a low fixed bitrate; it bands colors.

Verify the alpha actually landed:

> ⚠️ **DO NOT trust the `alpha_mode` tag alone — it lies.** A VP9 WebM can carry
> `TAG:alpha_mode=1` while its real pixel format is `yuv420p` (NO alpha plane). It then
> renders as a **solid opaque rectangle showing the studio/white background** — the classic
> "white box behind the talking head" bug (shipped in retrofit-2026-07-05). The metadata tag
> survives a re-encode even when the alpha plane is gone. ALWAYS verify the pixel format AND
> that alpha actually varies:

```bash
# 1) pixel format MUST be yuva420p (the 'a' = alpha plane). yuv420p = NO alpha = white box.
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of csv=p=0 subject.webm
# -> yuva420p   (if it says yuv420p, the cutout FAILED — do not use it)

# 2) alphaextract must SUCCEED (fails with "Requested planes not available" if no alpha),
#    and the extracted alpha must VARY (not be a flat 255 = fully opaque).
ffmpeg -v error -i subject.webm -vf "alphaextract,signalstats" -frames:v 1 -f null - 2>&1 \
  | grep -oE 'YMIN:[0-9]+|YMAX:[0-9]+'
# -> want YMIN near 0 (transparent bg) and YMAX near 255 (opaque subject).
#    YMIN=255 means fully opaque = white box.
```

**Root-cause note (retrofit-2026-07-05):** even a fresh `remove-background` run, and a
`-pix_fmt yuva420p` re-encode, produced `yuv420p` output — because the *source* fed to the
re-encode had already lost its alpha, so `-pix_fmt yuva420p` just filled a fully-opaque alpha
plane. **Fix chain that works:** cut out to **ProRes4444 `.mov`** first (`-o subject.mov` —
alpha is guaranteed in ProRes4444), verify with the two checks above, THEN encode the render
WebM *from the .mov*: `ffmpeg -i subject.mov -c:v libvpx-vp9 -pix_fmt yuva420p -auto-alt-ref 0
-b:v 0 -crf 22 -g 30 -keyint_min 30 -row-mt 1 -an subject.webm`, and re-verify the WebM.

## Diagnosing what you see

| Symptom in the rendered MP4 | Cause | Fix |
|---|---|---|
| Subject jitters / stutters frame-by-frame | Per-frame keying during render | Use `remove-background` (or the baked ffmpeg WebM) — never key live |
| Subject is semi-transparent (bg shows through skin) | `chromakey` similarity too high | Lower similarity (0.10-0.14), or use `remove-background` |
| Green halo / fringe around hair, shoulders | Spill not removed | Raise `despill` `mix` to 0.6-0.8, or use `remove-background` |
| Whole clip looks faded / washed out | Low encoder bitrate banded colors | Use `--quality best` (or `-crf 22 -b:v 0`) |
| WebM has no alpha (`alpha_mode` missing) | Filter dropped alpha / `-auto-alt-ref` not 0 | End the chain with `format=yuva420p`; set `-auto-alt-ref 0` |
| **Solid WHITE/studio box behind the whole subject** (opaque rectangle over the B-roll) | WebM is `yuv420p` despite an `alpha_mode=1` tag — no real alpha plane. Verifying by the tag alone hides it. | Verify `pix_fmt=yuva420p` + `alphaextract` varies (see verify block above), not the tag. Cut out to ProRes4444 `.mov` first, then encode the WebM from the `.mov`. |
| Subject not revealed even though it's on top | Opacity tween applied to the timed video | Animate the non-timed WRAPPER's opacity instead |

## Preview vs. render parity

Validate by **rendering**, not just by preview. Preview has visual parity with the render but
not performance parity (preview can stutter while the render is always perfect). If you change
anything in the talking-head pipeline, do a short test render before committing:

```bash
# Quick sanity render of the transparent overlay comp
npx hyperframes render -c stimulus.html -o /tmp/_test.mp4 --quality draft
```

## Where the asset lives

- Source: `assets/<project>/talking_head.mp4` (the raw take — green screen optional)
- Cut-out: `assets/<project>/subject.webm` (VP9+alpha; regenerate with `remove-background`)
- Hole-cut plate (optional): `assets/<project>/plate.webm` (from `--background-output`)

When porting to a new project, keep the same naming convention.
