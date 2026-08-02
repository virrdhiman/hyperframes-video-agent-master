#!/usr/bin/env python3
"""Fetch free stock VIDEOS from Pixabay (concept b-roll). Reads PIXABAY_API_KEY from
the project-root .env. Usage:
  python3 pixabay.py --query "server room data center" --count 3 [--list] [--min-width 1080] [--out ...]
Pixabay license: free for commercial use, no attribution required."""
import argparse, os, pathlib, sys, urllib.parse, urllib.request, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
load_env()
KEY = os.environ.get("PIXABAY_API_KEY")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", "-q", required=True)
    ap.add_argument("--count", "-n", type=int, default=3)
    ap.add_argument("--out", "-o", default=str(ROOT / "assets/stock/videos"))
    ap.add_argument("--prefix", default=None)
    ap.add_argument("--min-width", type=int, default=1080)
    ap.add_argument("--list", "-l", action="store_true")
    a = ap.parse_args()
    if not KEY: sys.exit("[ERROR] PIXABAY_API_KEY not found in %s/.env" % ROOT)
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({
        "key": KEY, "q": a.query, "per_page": max(3, a.count * 3), "safesearch": "true"})
    data = json.load(urllib.request.urlopen(url, timeout=30))
    hits = data.get("hits", [])
    if not hits: sys.exit("[pixabay] no results for %r" % a.query)
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    pref = a.prefix or "pix_" + "".join(c if c.isalnum() else "" for c in a.query.split()[0])
    got = 0
    for h in hits:
        vs = h.get("videos", {})
        # prefer the largest variant meeting min-width
        cand = sorted(vs.values(), key=lambda v: v.get("width", 0), reverse=True)
        pick = next((v for v in cand if v.get("width", 0) >= a.min_width), cand[0] if cand else None)
        if not pick: continue
        vid, w, hh = h.get("id"), pick.get("width"), pick.get("height")
        tags = h.get("tags", "")
        if a.list:
            print(f"  [{vid}] {w}x{hh}  {h.get('duration')}s  tags: {tags}")
            got += 1
            if got >= a.count * 3: break
            continue
        dest = out / f"{pref}_{vid}.mp4"
        try:
            req = urllib.request.Request(pick["url"], headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"})
            with urllib.request.urlopen(req, timeout=60) as r:
                dest.write_bytes(r.read())
            print(f"  -> {dest}  ({w}x{hh}, {h.get('duration')}s)  [{tags}]")
            got += 1
        except Exception as e:
            print(f"  !! {vid} failed: {e}")
        if got >= a.count: break
    if not a.list:
        print(f"[pixabay] saved {got} video(s)")

if __name__ == "__main__":
    main()
