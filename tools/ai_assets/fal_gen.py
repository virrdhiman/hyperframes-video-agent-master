#!/usr/bin/env python3
"""
fal_gen.py — AI asset generation via fal.ai (drop-in replacement for replicate_gen.py;
the Replicate token is now DISABLED, use this instead).

Same two subcommands / same flags as replicate_gen.py so existing muscle memory works:

  image — Nano Banana on fal (text-to-image, or edit when you pass reference images).
          Reference images ground the output: pass the Claude logo for a branded scene,
          or a frame grabbed from avatar.mp4 to put the owner into a scenario. Local files
          are inlined as base64 data-URIs (no separate upload step / storage API needed).

  i2v   — Wan image-to-video on fal: animate a still into a 5s/10s motion clip.

Model slugs are configurable (fal renames things often):
  --model <slug>                 override per call
  env FAL_IMAGE_MODEL / FAL_I2V_MODEL / FAL_I2V_FAST_MODEL   override defaults
Defaults:
  image (t2i)  fal-ai/nano-banana
  image (edit) fal-ai/nano-banana/edit        (auto-selected when --ref-image is given)
  i2v          fal-ai/wan-i2v
  i2v --fast   fal-ai/wan/v2.2-a14b/image-to-video/turbo
Pass model-specific fields fal expects with:  --extra '{"guidance_scale":3.5}'

Examples:
  python3 tools/ai_assets/fal_gen.py image \
      -p "the Claude asterisk logo as a warm clay 3D sculpture on a cream desk, photorealistic" \
      --ref-image assets/images/claude-logo.png --ratio 9:16 -o projects/<slug>/assets/ai

  python3 tools/ai_assets/fal_gen.py i2v \
      -p "slow cinematic push-in, dust motes, subtle parallax" \
      --image projects/<slug>/assets/ai/nb_01.png --duration 5 -o projects/<slug>/assets/ai

Auth: FAL_KEY (or FAL_API_KEY) from env or the repo .env / tools/.env.
Outputs land in --out (default assets/images/ for image, assets/stock/ for i2v).
NOTE: generated video is NOT render-ready — dense-keyframe re-encode before embedding.
"""
import argparse, base64, json, mimetypes, os, pathlib, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUEUE = "https://queue.fal.run"

DEF_IMAGE      = os.getenv("FAL_IMAGE_MODEL", "fal-ai/nano-banana")
DEF_IMAGE_EDIT = os.getenv("FAL_IMAGE_EDIT_MODEL", "fal-ai/nano-banana/edit")
DEF_I2V        = os.getenv("FAL_I2V_MODEL", "fal-ai/wan-i2v")
DEF_I2V_FAST   = os.getenv("FAL_I2V_FAST_MODEL", "fal-ai/wan/v2.2-a14b/image-to-video/turbo")

def die(msg): sys.exit("fal_gen: " + msg)

def key():
    k = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")
    if not k:
        for env in (ROOT / ".env", ROOT / "tools" / ".env"):
            if env.exists():
                for line in env.read_text().splitlines():
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    name, _, val = line.partition("=")
                    if name.strip() in ("FAL_KEY", "FAL_API_KEY") and val.strip():
                        k = val.strip(); break
            if k: break
    if not k: die("FAL_KEY not set (env or repo .env / tools/.env)")
    return k

def req(method, url, k, body=None):
    h = {"Authorization": f"Key {k}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); h["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        die(f"{method} {url} -> {e.code}: {e.read().decode()[:600]}")

def data_uri(ref):
    """Local file -> base64 data URI; pass URLs / existing data URIs through unchanged."""
    if ref.startswith(("http://", "https://", "data:")):
        return ref
    p = pathlib.Path(ref)
    if not p.exists(): die("input file not found: " + str(ref))
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

def collect_urls(out):
    """Pull downloadable URLs out of an arbitrary fal result payload."""
    urls = []
    def walk(v):
        if isinstance(v, str):
            if v.startswith(("http://", "https://")): urls.append(v)
        elif isinstance(v, dict):
            if isinstance(v.get("url"), str): urls.append(v["url"])
            else:
                for x in v.values(): walk(x)
        elif isinstance(v, list):
            for x in v: walk(x)
    for key_name in ("images", "image", "video", "videos", "output"):
        if key_name in out: walk(out[key_name])
    if not urls: walk(out)
    # de-dup, preserve order
    seen = set(); uniq = []
    for u in urls:
        if u not in seen: seen.add(u); uniq.append(u)
    return uniq

def run_model(model, inp, k, timeout_s):
    sub = req("POST", f"{QUEUE}/{model}", k, body=inp)
    status_url = sub.get("status_url"); resp_url = sub.get("response_url")
    rid = sub.get("request_id", "?")
    if not status_url or not resp_url:
        # some models answer synchronously
        return collect_urls(sub)
    t0 = time.time()
    while True:
        st = req("GET", status_url, k)
        s = st.get("status")
        print(f"fal_gen: {model} … {s} ({int(time.time()-t0)}s)", flush=True)
        if s == "COMPLETED": break
        if s in ("FAILED", "ERROR", "CANCELED"):
            die(f"request {rid} {s}: {json.dumps(st)[:500]}")
        if time.time() - t0 > timeout_s: die(f"request {rid} timed out after {timeout_s}s")
        time.sleep(4)
    out = req("GET", resp_url, k)
    urls = collect_urls(out)
    if not urls: die(f"no output URL in result: {json.dumps(out)[:500]}")
    return urls

def download(urls, outdir, prefix, ext_hint):
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, u in enumerate(urls, 1):
        ext = pathlib.Path(u.split("?")[0]).suffix or ext_hint
        dest = outdir / f"{prefix}_{i:02d}{ext}"
        n = 1
        while dest.exists():
            n += 1; dest = outdir / f"{prefix}_{i:02d}_v{n}{ext}"
        urllib.request.urlretrieve(u, dest)
        paths.append(dest); print("fal_gen: saved", dest)
    return paths

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    im = sub.add_parser("image", help="Nano Banana generate/edit")
    im.add_argument("-p", "--prompt", required=True)
    im.add_argument("--ref-image", action="append", default=[],
                    help="reference/input image (local path or URL); repeatable")
    im.add_argument("--image", action="append", default=[], dest="ref_image",
                    help="alias of --ref-image (edit-style calls)")
    im.add_argument("-r", "--ratio", default="9:16",
                    help="9:16 | 16:9 | 1:1 | 4:5 | … (sent as aspect_ratio)")
    im.add_argument("--format", default="png", choices=["png", "jpg", "jpeg"])
    im.add_argument("-n", "--count", type=int, default=1)
    im.add_argument("--model", help="override fal model slug")
    im.add_argument("--extra", help="JSON merged into the input payload")
    im.add_argument("-o", "--out", default=str(ROOT / "assets/images"))
    im.add_argument("--prefix", default="nb")

    iv = sub.add_parser("i2v", help="Wan image-to-video motion")
    iv.add_argument("-p", "--prompt", required=True)
    iv.add_argument("--image", required=True, help="input still (local path or URL)")
    iv.add_argument("--duration", type=int, default=5, choices=[5, 10])
    # fal wan-i2v dropped 1080p (2026-07-07: 422 "Input should be '480p' or '720p'") — default 720p
    iv.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p"])
    iv.add_argument("--negative", default="text, watermark, captions, distorted face, extra fingers")
    iv.add_argument("--seed", type=int)
    iv.add_argument("--fast", action="store_true", help="turbo/fast model")
    iv.add_argument("--model", help="override fal model slug")
    iv.add_argument("--extra", help="JSON merged into the input payload")
    iv.add_argument("-o", "--out", default=str(ROOT / "assets/stock"))
    iv.add_argument("--prefix", default="wan")

    a = ap.parse_args()
    k = key()
    extra = json.loads(a.extra) if getattr(a, "extra", None) else {}

    if a.cmd == "image":
        refs = [data_uri(r) for r in a.ref_image]
        model = a.model or (DEF_IMAGE_EDIT if refs else DEF_IMAGE)
        inp = {"prompt": a.prompt, "num_images": 1,
               "aspect_ratio": a.ratio, "output_format": a.format}
        if refs: inp["image_urls"] = refs
        inp.update(extra)
        for _ in range(max(1, a.count)):
            urls = run_model(model, inp, k, timeout_s=300)
            download(urls, a.out, a.prefix, "." + ("jpg" if a.format == "jpeg" else a.format))
    else:
        model = a.model or (DEF_I2V_FAST if a.fast else DEF_I2V)
        inp = {"prompt": a.prompt, "image_url": data_uri(a.image),
               "resolution": a.resolution, "num_frames": 81 if a.fast else None,
               "negative_prompt": a.negative}
        if not a.fast:
            inp["duration"] = a.duration
        inp = {kk: vv for kk, vv in inp.items() if vv is not None}
        if a.seed is not None: inp["seed"] = a.seed
        inp.update(extra)
        urls = run_model(model, inp, k, timeout_s=1200)
        download(urls, a.out, a.prefix, ".mp4")

if __name__ == "__main__":
    main()
