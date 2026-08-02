# Render Troubleshooting

Render-time problems and how to fix them in HyperFrames. Start with `npx hyperframes doctor`,
then work down the list.

## First: run the doctor

```bash
npx hyperframes doctor
```

It checks Node (>= 22), FFmpeg + ffprobe, the bundled Chrome (`chrome-headless-shell`), and
Docker (optional). Gate CI on `npx hyperframes doctor --json` -> `.ok`. Most render failures
are an environment gap this surfaces immediately.

---

## The most common cause: assets not under the project root

**External URLs and out-of-project paths don't render reliably.** In preview the browser can
buffer and cache, so a CDN URL or an absolute path outside the project *looks* fine. During
render, HyperFrames seeks every asset frame-by-frame in headless Chrome, hundreds or thousands
of times — and anything it can't resolve relative to the project root stalls or fails.

Symptoms:
- Render hangs, then errors on a specific clip
- "Could not extract frame" / "failed to load" on a video or image
- Works in `npx hyperframes preview` but fails in `npx hyperframes render`

Fix: **download every asset into `assets/` and reference it with a relative path.**

```html
<!-- Bad: external URL or out-of-project path -->
<video src="https://cdn.example.com/video/spain.mp4" ...></video>

<!-- Good: local file under the project root -->
<video src="assets/stimulus/broll/spain-city.mp4" muted playsinline ...></video>
```

Use the stock fetcher to pull clips straight into `assets/` (see
[BROLL_GUIDE.md](./BROLL_GUIDE.md)). Quick way to spot offenders:

```bash
# Any http(s) src in your compositions is a render risk
grep -rnE 'src="https?://' *.html compositions/ 2>/dev/null
```

Then re-run the static checks, which flag missing assets directly:

```bash
npx hyperframes lint        # static HTML checks (incl. unmuted video, bad timing)
npx hyperframes validate    # loads each comp in headless Chrome; reports MISSING ASSETS
npx hyperframes inspect     # overflow / off-canvas elements with timestamps
```

---

## "FFmpeg not found"

The local renderer uses system FFmpeg. Install it, or render in Docker (which bundles it):

```bash
brew install ffmpeg          # provides ffmpeg + ffprobe
# or, no local FFmpeg needed:
npx hyperframes render -c stimulus.html -o out/stimulus.mp4 --docker
```

---

## "No composition found"

The root element of the composition needs `data-composition-id`. Confirm your root has it:

```html
<div id="root" data-composition-id="stimulus" data-width="1920" data-height="1080"
     data-start="0" data-duration="130"> ... </div>
```

Also make sure a paused timeline is registered under that same id on `window.__timelines`.

---

## Preview works but render fails

Almost always the **external-URL / out-of-project asset** problem above. Checklist:
- Every `src` is a relative path under the project (`assets/...`), not a URL
- All referenced files actually exist (`npx hyperframes validate`)
- Each `<video>` is `muted` (audio belongs on a separate `<audio>` element)
- No `Math.random()`, `Date.now()`, or network fetches in composition JS (non-deterministic)

---

## Preview stutters but the render is fine

This is expected. Preview has **visual** parity with the render but **not performance**
parity — the render is always frame-perfect. Stutter in preview usually means heavy paint:
stacked `backdrop-filter` blur, images larger than 4K, or large `filter: blur()` /
`drop-shadow`. To make preview smoother:

```bash
npx hyperframes preview --quality draft
```

The final render is unaffected; you don't need to "fix" preview stutter.

---

## Render doesn't match preview (fonts / anti-aliasing differ)

Local render uses your host Chrome + GPU; small differences in fonts or AA can appear across
machines. For byte-identical, reproducible output (CI, team, agent renders) use Docker:

```bash
npx hyperframes render -c stimulus.html -o out/stimulus.mp4 --docker
```

Docker pins Chrome, fonts, and FFmpeg, so output is identical everywhere (slower,
software-GL).

---

## Recommended render settings

```bash
# Standard high-compatibility MP4
npx hyperframes render -c stimulus.html -o out/stimulus.mp4 \
  --fps 30 --quality standard

# Higher quality
npx hyperframes render -c stimulus.html -o out/stimulus-hq.mp4 \
  --fps 30 --quality high
```

| Flag | Value | Purpose |
|------|-------|---------|
| `--composition / -c` | `stimulus.html` | Which HTML to render (defaults to `index.html`) |
| `--output / -o` | `out/stimulus.mp4` | Output path |
| `--fps` | 24 / 30 / 60 | Frame rate (default 30) |
| `--quality` | draft / standard / high | CRF ~28 / 18 / 15 |
| `--crf` | 0-51 | Manual quality (mutually exclusive with `--video-bitrate`) |
| `--workers` | 1-8 / auto | Parallel Chrome workers (~256MB each) |
| `--gpu` | — | Hardware encode (VideoToolbox/NVENC), local only |
| `--docker` | — | Deterministic, reproducible render |

---

## Slow render?

- `--quality draft` while iterating
- `npx hyperframes benchmark` to find the optimal `--workers` for this machine
- `--gpu` for hardware encode (local)
- `--fps 24` if 24fps is acceptable for the deliverable

---

## If a render still fails

1. **Disk space** — temporary frames need headroom: `df -h /` (aim for a few GB free).
2. **Memory** — lots of workers each spawn a Chrome (~256MB). Drop to `--workers 1` on a
   short/low-memory clip.
3. **Confirm assets** — `ls -lh assets/<project>/` and re-run `npx hyperframes validate`.
4. **Test a short render** — `--quality draft` first to fail fast.
5. **File a clean report** — `npx hyperframes info` dumps the environment for bug reports.

---

> **Coming from Remotion?** The old failure mode here was external Pixabay/Pexels URLs dying
> during render and `staticFile()` fixing it by forcing local files. The principle carries
> over: **assets must live under the project root and be referenced by relative path** — but
> there is no `staticFile()` wrapper, just plain relative `src="assets/..."`.
