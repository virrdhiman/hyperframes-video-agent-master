#!/usr/bin/env python3
"""prem_i2v.py — premium image-to-video on Replicate with model selection.

Picks the right input keys per model so you can A/B different engines for
better physics / realism:

  hailuo  -> minimax/hailuo-02        (first_frame_image[, last_frame_image], 1080p, strong physics)
  seedance-> bytedance/seedance-1-pro (image[, last_frame_image], good motion)
  veo     -> google/veo-3-fast        (image, prompt-adherence; 16:9 native)
  kling   -> kwaivgi/kling-v2.5-turbo-pro (start_image[, end_image])

Usage:
  python3 tools/ai_assets/prem_i2v.py --model hailuo \
    --start <img> [--end <img>] --prompt "..." [--duration 5] \
    [--resolution 1080p] [--negative "..."] --out <file.mp4>
"""
import argparse, os, sys, time, urllib.request, json, mimetypes, uuid
from pathlib import Path

API = "https://api.replicate.com/v1"
ROOT = Path(__file__).resolve().parents[2]

MODELS = {
    "hailuo": "minimax/hailuo-02",
    "seedance": "bytedance/seedance-1-pro",
    "veo": "google/veo-3-fast",
    "kling": "kwaivgi/kling-v2.5-turbo-pro",
}
# key for the start image / end image per model
START_KEY = {"hailuo": "first_frame_image", "seedance": "image", "veo": "image", "kling": "start_image"}
END_KEY = {"hailuo": "last_frame_image", "seedance": "last_frame_image", "kling": "end_image"}


def token():
    t = os.environ.get("REPLICATE_API_TOKEN")
    if not t:
        for ln in (ROOT / ".env").read_text().splitlines():
            if ln.startswith("REPLICATE_API_TOKEN="):
                t = ln.split("=", 1)[1].strip().strip('"').strip("'")
    if not t:
        sys.exit("prem_i2v: no REPLICATE_API_TOKEN")
    return t


def req(method, url, tok, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", "Bearer " + tok)
    r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read())


def upload(path, tok):
    if path.startswith("http"):
        return path
    boundary = "----prem" + uuid.uuid4().hex
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    body = b"".join([
        ("--" + boundary + "\r\n").encode(),
        ('Content-Disposition: form-data; name="content"; filename="%s"\r\n' % p.name).encode(),
        ("Content-Type: %s\r\n\r\n" % mime).encode(),
        p.read_bytes(), b"\r\n",
        ("--" + boundary + "--\r\n").encode(),
    ])
    r = urllib.request.Request(API + "/files", data=body, method="POST")
    r.add_header("Authorization", "Bearer " + tok)
    r.add_header("Content-Type", "multipart/form-data; boundary=" + boundary)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read())["urls"]["get"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=list(MODELS))
    ap.add_argument("--start", required=True)
    ap.add_argument("--end")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--duration", type=int, default=5)
    ap.add_argument("--resolution")
    ap.add_argument("--negative", default="text, watermark, captions, logos, distorted face, extra fingers, blurry, deformed hands")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tok = token()
    model = MODELS[a.model]

    inp = {"prompt": a.prompt, "duration": a.duration}
    inp[START_KEY[a.model]] = upload(a.start, tok)
    if a.end and a.model in END_KEY:
        inp[END_KEY[a.model]] = upload(a.end, tok)
    if a.resolution:
        inp["resolution"] = a.resolution
    if a.model == "veo":
        inp["negative_prompt"] = a.negative
    if a.model == "kling":
        inp["negative_prompt"] = a.negative

    print(f"prem_i2v: {model} keys={list(inp)}", flush=True)
    pred = req("POST", f"{API}/models/{model}/predictions", tok, body={"input": inp})
    t0 = time.time()
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(4)
        pred = req("GET", f"{API}/predictions/{pred['id']}", tok)
        print(f"prem_i2v: {pred['status']} ({int(time.time()-t0)}s)", flush=True)
    if pred["status"] != "succeeded":
        sys.exit("prem_i2v: " + pred["status"] + " " + str(pred.get("error")))
    out = pred["output"]
    url = out[0] if isinstance(out, list) else out
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, a.out)
    print("prem_i2v: saved " + a.out, flush=True)


if __name__ == "__main__":
    main()
