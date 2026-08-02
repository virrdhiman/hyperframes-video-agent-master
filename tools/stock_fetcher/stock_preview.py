#!/usr/bin/env python3
"""Thumbnail-FIRST stock video search: fetch only THUMBNAILS for many candidates,
build a labeled contact sheet to review, then download ONLY the clips you pick.
Avoids downloading full clips just to evaluate them.

  # 1) preview thumbnails across sources (no clips downloaded):
  python3 stock_preview.py -q "data center server room" -n 8
  #    -> writes /tmp/stock_preview/contact.jpg + prints a SOURCE:ID table

  # 2) download only the ones you chose, into the project (or a library):
  python3 stock_preview.py --get pexels:7140928 pixabay:68978 --out ../../assets/stock/library

Sources: pexels, pixabay (both have thumbnails in their search API). YouTube previews
come from youtube.py --list (Serper thumbnails); Mixkit needs a headless browser (see notes).
"""
import argparse, json, os, pathlib, subprocess, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
for line in (ROOT / ".env").read_text().splitlines() if (ROOT / ".env").exists() else []:
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
PEXELS = os.environ.get("PEXELS_API_KEY"); PIXABAY = os.environ.get("PIXABAY_API_KEY")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def _get(url, headers=None):
    h = {"User-Agent": UA}
    if headers: h.update(headers)
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30).read()

def search_pexels(q, n):
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "portrait"})
    d = json.loads(_get(url, {"Authorization": PEXELS}))
    out = []
    for v in d.get("videos", []):
        files = sorted(v.get("video_files", []), key=lambda f: (f.get("width") or 0), reverse=True)
        best = files[0] if files else {}
        out.append({"source": "pexels", "id": v["id"], "thumb": v.get("image"),
                    "w": best.get("width"), "h": best.get("height"), "dur": v.get("duration"),
                    "tags": (v.get("url", "").rstrip("/").split("/")[-1].replace("-", " "))[:60],
                    "dl": best.get("link")})
    return out

def search_pixabay(q, n):
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": PIXABAY, "q": q, "per_page": max(3, n), "safesearch": "true"})
    d = json.loads(_get(url))
    out = []
    for h in d.get("hits", [])[:n]:
        lg = h.get("videos", {}).get("large", {})
        out.append({"source": "pixabay", "id": h["id"], "thumb": lg.get("thumbnail"),
                    "w": lg.get("width"), "h": lg.get("height"), "dur": h.get("duration"),
                    "tags": h.get("tags", "")[:60], "dl": lg.get("url")})
    return out

def preview(q, n):
    tmp = pathlib.Path("/tmp/stock_preview"); tmp.mkdir(parents=True, exist_ok=True)
    for f in tmp.glob("*.jpg"): f.unlink()
    results = []
    if PEXELS: results += search_pexels(q, n)
    if PIXABAY: results += search_pixabay(q, n)
    print(f"\n{'#':>2}  {'SOURCE:ID':<18} {'DIMS':<11} {'DUR':>4}  TAGS")
    print("-" * 78)
    labels = []
    for i, r in enumerate(results):
        tag = f"{r['source']}:{r['id']}"
        print(f"{i:>2}  {tag:<18} {str(r['w'])+'x'+str(r['h']):<11} {str(r['dur'])+'s':>4}  {r['tags']}")
        try:
            (tmp / f"{i:02d}_{tag.replace(':','-')}.jpg").write_bytes(_get(r["thumb"]))
            labels.append(tag)
        except Exception as e:
            print(f"    (thumb failed: {e})")
    sheet = "/tmp/stock_preview/contact.jpg"
    subprocess.run(["montage", *sorted(str(p) for p in tmp.glob("*.jpg")),
                    "-tile", "4x", "-geometry", "300x+8+24", "-background", "#222",
                    "-label", "%t", sheet], check=False)
    print(f"\nContact sheet -> {sheet}  ({len(labels)} thumbnails, 0 clips downloaded)")
    print("Pick, then: python3 stock_preview.py --get pexels:<id> pixabay:<id> --out ../../assets/stock/library")

def get(specs, out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        src, _, vid = spec.partition(":")
        if src == "pexels":
            d = json.loads(_get(f"https://api.pexels.com/videos/videos/{vid}", {"Authorization": PEXELS}))
            files = sorted(d.get("video_files", []), key=lambda f: (f.get("width") or 0), reverse=True)
            url = next((f["link"] for f in files if (f.get("width") or 0) <= 1280), files[0]["link"]) if files else None
        elif src == "pixabay":
            d = json.loads(_get(f"https://pixabay.com/api/videos/?key={PIXABAY}&id={vid}"))
            hits = d.get("hits", []); url = hits[0]["videos"]["large"]["url"] if hits else None
        else:
            print(f"  ?? unknown source: {spec}"); continue
        if not url: print(f"  !! {spec}: not found"); continue
        dest = out / f"{src}_{vid}.mp4"
        dest.write_bytes(_get(url)); print(f"  -> {dest}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", "-q"); ap.add_argument("--count", "-n", type=int, default=8)
    ap.add_argument("--get", nargs="+"); ap.add_argument("--out", "-o", default=str(ROOT / "assets/stock/videos"))
    a = ap.parse_args()
    if a.get: get(a.get, a.out)
    elif a.query: preview(a.query, a.count)
    else: ap.error("give --query to preview, or --get SOURCE:ID ... to download")
