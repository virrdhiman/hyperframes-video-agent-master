#!/usr/bin/env python3
"""
replicate_gen.py — AI asset generation via Replicate (the Google key is SUSPENDED,
so tools/image_generator/imagen.py and tools/video_generator/veo.py are DEAD —
use this instead).

Two subcommands:

  image — Nano Banana 2 (google/nano-banana-2): generate OR edit images.
          Reference images (up to 14) ground the output: pass the Claude logo to
          get a lifelike branded scene, or a frame grabbed from avatar.mp4 to put
          the owner into a scenario. Local files are uploaded via the Replicate Files
          API automatically.

  i2v   — Wan i2v (wan-video/wan-2.5-i2v, or --fast for wan-2.2-i2v-fast):
          animate a still image into a 5s/10s motion clip. Feed it a Nano Banana
          output (or any still) to get bespoke b-roll.

Examples:
  # lifelike branded still from the official logo
  python3 tools/ai_assets/replicate_gen.py image \
      -p "the Claude asterisk logo as a warm clay-colored 3D sculpture on a cream desk, soft daylight, shallow depth of field, photorealistic" \
      --ref-image assets/images/claude-logo.png --ratio 9:16 -o projects/<slug>/assets/ai

  # put the owner in a scenario (ground with a frame from the A-roll)
  ffmpeg -y -ss 2 -i projects/<slug>/avatar.mp4 -frames:v 1 /tmp/face_ref.jpg
  python3 tools/ai_assets/replicate_gen.py image \
      -p "this exact man, same face, sitting at a cluttered startup desk at 2am surrounded by empty chai cups, staring at a terminal, cinematic warm light" \
      --ref-image /tmp/face_ref.jpg --ratio 9:16 -o projects/<slug>/assets/ai

  # add motion to a still (5s vertical clip)
  python3 tools/ai_assets/replicate_gen.py i2v \
      -p "slow cinematic push-in, dust motes drifting in the light, subtle parallax" \
      --image projects/<slug>/assets/ai/nb2_01.png --duration 5 -o projects/<slug>/assets/ai

Auth: REPLICATE_API_TOKEN from the repo .env (or environment).
Outputs land in --out (default assets/images/ for image, assets/stock/ for i2v).
NOTE: generated video is NOT render-ready — dense-keyframe re-encode like any
other external clip before embedding (see BROLL_GUIDE.md).
"""
import argparse, base64, json, mimetypes, os, pathlib, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[2]
API = "https://api.replicate.com/v1"

MODELS = {
    "image": "google/nano-banana-2",
    "i2v": "wan-video/wan-2.5-i2v",
    "i2v_fast": "wan-video/wan-2.2-i2v-fast",
}

def die(msg): sys.exit("replicate_gen: " + msg)

def token():
    t = os.getenv("REPLICATE_API_TOKEN")
    if not t:
        env = ROOT / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("REPLICATE_API_TOKEN="):
                    t = line.split("=", 1)[1].strip()
    if not t: die("REPLICATE_API_TOKEN not set (env or repo .env)")
    return t

def req(method, url, tok, body=None, headers=None, raw=False):
    h = {"Authorization": f"Bearer {tok}"}
    if headers: h.update(headers)
    data = None
    if body is not None and not raw:
        data = json.dumps(body).encode(); h["Content-Type"] = "application/json"
    elif raw:
        data = body
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        die(f"{method} {url} -> {e.code}: {e.read().decode()[:500]}")

def upload_file(path, tok):
    """Upload a local file via the Replicate Files API; returns a fetchable URL."""
    p = pathlib.Path(path)
    if not p.exists(): die("input file not found: " + str(path))
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    boundary = "----replicate-gen-multipart"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"content\"; "
            f"filename=\"{p.name}\"\r\nContent-Type: {mime}\r\n\r\n").encode()
    body += p.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    out = req("POST", f"{API}/files", tok, body=body, raw=True,
              headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return out["urls"]["get"]

def resolve_image(ref, tok):
    if ref.startswith("http://") or ref.startswith("https://") or ref.startswith("data:"):
        return ref
    return upload_file(ref, tok)

def run_model(model, inp, tok, timeout_s):
    pred = req("POST", f"{API}/models/{model}/predictions", tok, body={"input": inp})
    pid, url = pred["id"], pred["urls"]["get"]
    t0 = time.time()
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        if time.time() - t0 > timeout_s: die(f"prediction {pid} timed out after {timeout_s}s")
        time.sleep(4)
        pred = req("GET", url, tok)
        print(f"replicate_gen: {model} … {pred['status']} ({int(time.time()-t0)}s)", flush=True)
    if pred["status"] != "succeeded":
        die(f"prediction {pid} {pred['status']}: {str(pred.get('error'))[:500]}")
    out = pred["output"]
    return out if isinstance(out, list) else [out]

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
        paths.append(dest); print("replicate_gen: saved", dest)
    return paths

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    im = sub.add_parser("image", help="Nano Banana 2 generate/edit")
    im.add_argument("-p", "--prompt", required=True)
    im.add_argument("--ref-image", action="append", default=[],
                    help="reference/input image (local path or URL); repeatable, max 14")
    im.add_argument("--image", action="append", default=[], dest="ref_image",
                    help="alias of --ref-image (for edit-style calls)")
    im.add_argument("-r", "--ratio", default="9:16",
                    help="9:16 | 16:9 | 1:1 | 4:5 | match_input_image | …")
    im.add_argument("--resolution", default="2K", choices=["1K", "2K", "4K"])
    im.add_argument("--format", default="png", choices=["png", "jpg"])
    im.add_argument("-n", "--count", type=int, default=1)
    im.add_argument("-o", "--out", default=str(ROOT / "assets/images"))
    im.add_argument("--prefix", default="nb2")

    iv = sub.add_parser("i2v", help="Wan image-to-video motion")
    iv.add_argument("-p", "--prompt", required=True)
    iv.add_argument("--image", required=True, help="input still (local path or URL)")
    iv.add_argument("--duration", type=int, default=5, choices=[5, 10])
    iv.add_argument("--resolution", default="1080p", choices=["480p", "720p", "1080p"])
    iv.add_argument("--negative", default="text, watermark, captions, distorted face, extra fingers")
    iv.add_argument("--seed", type=int)
    iv.add_argument("--fast", action="store_true", help="wan-2.2-i2v-fast (cheaper, 480/720p)")
    iv.add_argument("-o", "--out", default=str(ROOT / "assets/stock"))
    iv.add_argument("--prefix", default="wan")

    a = ap.parse_args()
    tok = token()

    if a.cmd == "image":
        inp = {"prompt": a.prompt, "aspect_ratio": a.ratio,
               "resolution": a.resolution, "output_format": a.format}
        if a.ref_image:
            inp["image_input"] = [resolve_image(r, tok) for r in a.ref_image[:14]]
            if a.ratio == "9:16" and len(a.ref_image) == 1:
                pass  # keep explicit ratio; use --ratio match_input_image to inherit
        for _ in range(max(1, a.count)):
            urls = run_model(MODELS["image"], inp, tok, timeout_s=300)
            download(urls, a.out, a.prefix, "." + a.format)
    else:
        model = MODELS["i2v_fast"] if a.fast else MODELS["i2v"]
        inp = {"prompt": a.prompt, "image": resolve_image(a.image, tok)}
        if a.fast:
            inp["resolution"] = "720p" if a.resolution != "480p" else "480p"
            inp["num_frames"] = 81
            inp["interpolate_output"] = True
        else:
            inp.update({"duration": a.duration, "resolution": a.resolution,
                        "negative_prompt": a.negative})
        if a.seed is not None: inp["seed"] = a.seed
        urls = run_model(model, inp, tok, timeout_s=1200)
        download(urls, a.out, a.prefix, ".mp4")

if __name__ == "__main__":
    main()
