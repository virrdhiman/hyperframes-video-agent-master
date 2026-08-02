#!/usr/bin/env python3
"""
freesound.py — fetch PREMADE (not generated) royalty-free SFX + background music
from Freesound.org. Token-only: searches the API and downloads the high-quality
mp3 PREVIEW (public CDN, no OAuth needed), which is plenty for a video bed/SFX.

  # one-shot search
  python3 tools/stock_fetcher/freesound.py -q "transition whoosh" --type sfx -n 5
  python3 tools/stock_fetcher/freesound.py -q "lofi background" --type music -n 3

  # curated reusable packs (commonly-used SFX + 2026-popular + background music)
  python3 tools/stock_fetcher/freesound.py --pack sfx
  python3 tools/stock_fetcher/freesound.py --pack music
  python3 tools/stock_fetcher/freesound.py --pack all

Auth: FREESOUND_API_KEY in the repo-root .env (free key: https://freesound.org/apiv2/apply).
License: defaults to CC0 (no attribution needed — safest for a commercial feed). Use
--license any to widen; every download's license + author is logged to assets/common/CREDITS.md.
Output: SFX -> assets/common/sfx/ , music -> assets/common/music/.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
API = "https://freesound.org/apiv2"
UA = "Mozilla/5.0 (Retrofit-AI asset fetcher)"

# curated, reusable query sets. Each: (filename_prefix, query, min_dur, max_dur)
PACK_SFX = [
    ("whoosh",       "transition whoosh swoosh",        0.2, 2.5),
    ("swipe",        "swipe transition ui",             0.1, 1.5),
    ("pop",          "pop ui click bubble",             0.05, 1.0),
    ("click",        "click tap ui interface",          0.05, 0.8),
    ("impact",       "cinematic impact hit boom",       0.4, 3.0),
    ("subdrop",      "sub bass drop deep boom",         0.5, 3.0),
    ("riser",        "riser",                           1.0, 6.0),
    ("swell",        "reverse swell",                   0.8, 5.0),
    ("glitch",       "glitch",                          0.1, 2.5),
    ("notification", "notification ding",               0.2, 2.5),
    ("typewriter",   "keyboard typing mechanical",      0.3, 2.5),
    # 2026-popular / short-form flavour
    ("viral_swoosh", "swoosh transition",               0.1, 2.0),
    ("trap_impact",  "boom impact",                     0.2, 2.5),
    ("woosh_reverse","reverse whoosh",                  0.3, 2.5),
]
PACK_MUSIC = [
    ("lofi_chill",        "lofi chill hip hop instrumental loop", 20, 180),
    ("upbeat_corporate",  "upbeat corporate motivational",        20, 180),
    ("cinematic_inspire", "cinematic inspiring uplifting",        20, 180),
    ("tech_ambient",      "tech ambient electronic background",   20, 180),
    ("energetic_pop",     "energetic upbeat pop electronic",      20, 180),
    ("warm_acoustic",     "acoustic background",                  20, 180),
]

def load_key():
    k = os.environ.get("FREESOUND_API_KEY")
    if not k:
        envf = ROOT / ".env"
        if envf.exists():
            for line in envf.read_text().splitlines():
                line = line.strip()
                if line.startswith("FREESOUND_API_KEY") and "=" in line:
                    k = line.split("=", 1)[1].strip().strip('"').strip("'"); break
    if not k:
        sys.exit("FREESOUND_API_KEY not found (env or .env). Get a free key: https://freesound.org/apiv2/apply")
    return k

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def search(query, key, license_mode, min_dur, max_dur, n):
    flt = [f"duration:[{min_dur} TO {max_dur}]"]
    if license_mode == "cc0":
        flt.append('license:"Creative Commons 0"')
    elif license_mode == "commercial":
        # CC0 + Attribution only — commercially safe. EXCLUDES any NonCommercial license.
        flt.append('license:("Creative Commons 0" OR "Attribution" OR "Attribution 4.0")')
    params = {
        "query": query, "token": key,
        "filter": " ".join(flt),
        "sort": "downloads_desc",          # most-used / popular first
        "fields": "id,name,previews,license,duration,username,url",
        "page_size": max(n * 3, 15),
    }
    url = API + "/search/text/?" + urllib.parse.urlencode(params)
    try:
        data = json.loads(_get(url))
    except urllib.error.HTTPError as e:
        sys.exit(f"freesound search failed ({e.code}): {e.read().decode(errors='ignore')[:300]}")
    return data.get("results", [])

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]

def credit(outdir, item, fname):
    cred = ROOT / "assets" / "common" / "CREDITS.md"
    cred.parent.mkdir(parents=True, exist_ok=True)
    line = f"- `{fname}` — \"{item['name']}\" by {item['username']} · {item['license']} · {item.get('url','')}\n"
    with open(cred, "a") as f:
        f.write(line)

def download(item, prefix, outdir):
    prev = item.get("previews", {})
    purl = prev.get("preview-hq-mp3") or prev.get("preview-lq-mp3")
    if not purl:
        return None
    outdir = ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    fname = f"{prefix}_{item['id']}_{slug(item['name'])}.mp3"
    out = outdir / fname
    if out.exists():
        print(f"  skip {fname} (exists)"); return out
    try:
        blob = _get(purl)
    except Exception as e:
        print(f"  ! failed {item['id']}: {e}"); return None
    out.write_bytes(blob)
    credit(outdir, item, fname)
    print(f"  → {out.relative_to(ROOT)} ({len(blob)//1024} KB · {item['license']})")
    return out

def run_query(prefix, query, key, lic, mn, mx, n, kind):
    outdir = "assets/common/sfx" if kind == "sfx" else "assets/common/music"
    print(f"[{kind}] {prefix}: \"{query}\"")
    got = 0
    for item in search(query, key, lic, mn, mx, n):
        if download(item, prefix, outdir):
            got += 1
        if got >= n:
            break
    if got == 0:
        print(f"  (nothing matched — try --license any)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query"); ap.add_argument("--type", choices=["sfx", "music"], default="sfx")
    ap.add_argument("-n", "--count", type=int, default=4)
    ap.add_argument("--license", choices=["cc0", "commercial", "any"], default="commercial",
                    help="cc0=no attribution; commercial=CC0+Attribution (safe, credit logged); any=incl. NonCommercial (NOT for commercial use)")
    ap.add_argument("--min-dur", type=float); ap.add_argument("--max-dur", type=float)
    ap.add_argument("--pack", choices=["sfx", "music", "all"])
    a = ap.parse_args()
    key = load_key()

    if a.pack:
        if a.pack in ("sfx", "all"):
            for prefix, q, mn, mx in PACK_SFX:
                run_query(prefix, q, key, a.license, mn, mx, 2, "sfx")
        if a.pack in ("music", "all"):
            for prefix, q, mn, mx in PACK_MUSIC:
                run_query(prefix, q, key, a.license, mn, mx, 1, "music")
        print("\ndone. Review assets/common/ and assets/common/CREDITS.md.")
        return
    if not a.query:
        sys.exit("provide -q QUERY (or --pack sfx|music|all)")
    mn = a.min_dur if a.min_dur is not None else (0.1 if a.type == "sfx" else 20)
    mx = a.max_dur if a.max_dur is not None else (4.0 if a.type == "sfx" else 180)
    run_query(slug(a.query), a.query, key, a.license, mn, mx, a.count, a.type)

if __name__ == "__main__":
    main()
