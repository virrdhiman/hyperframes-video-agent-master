#!/usr/bin/env python3
"""kling_gen.py — premium image-to-video via Kling v2.5 Turbo Pro on Replicate.
Supports start_image (+ optional end_image for transformations) and an action prompt.

Usage:
  python3 tools/ai_assets/kling_gen.py --start <img> [--end <img>] \
    --prompt "..." [--duration 5] [--negative "..."] --out <file.mp4>
"""
import argparse, os, sys, time, urllib.request, json
from pathlib import Path

API = "https://api.replicate.com/v1"
MODEL = "kwaivgi/kling-v2.5-turbo-pro"
ROOT = Path(__file__).resolve().parents[2]


def token():
    t = os.environ.get("REPLICATE_API_TOKEN")
    if not t:
        for ln in (ROOT / ".env").read_text().splitlines():
            if ln.startswith("REPLICATE_API_TOKEN="):
                t = ln.split("=", 1)[1].strip().strip('"').strip("'")
    if not t:
        sys.exit("kling_gen: no REPLICATE_API_TOKEN")
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
    import mimetypes, uuid
    boundary = "----kling" + uuid.uuid4().hex
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
    ap.add_argument("--start", required=True)
    ap.add_argument("--end")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--duration", type=int, default=5, choices=[5, 10])
    ap.add_argument("--negative", default="text, watermark, captions, logos, distorted face, extra fingers, blurry")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tok = token()

    inp = {"prompt": a.prompt, "duration": a.duration,
           "negative_prompt": a.negative,
           "start_image": upload(a.start, tok)}
    if a.end:
        inp["end_image"] = upload(a.end, tok)

    pred = req("POST", f"{API}/models/{MODEL}/predictions", tok, body={"input": inp})
    t0 = time.time()
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(4)
        pred = req("GET", f"{API}/predictions/{pred['id']}", tok)
        print(f"kling_gen: {pred['status']} ({int(time.time()-t0)}s)", flush=True)
    if pred["status"] != "succeeded":
        sys.exit("kling_gen: " + pred["status"] + " " + str(pred.get("error")))
    out = pred["output"]
    url = out[0] if isinstance(out, list) else out
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, a.out)
    print("kling_gen: saved " + a.out, flush=True)


if __name__ == "__main__":
    main()
