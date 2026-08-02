#!/usr/bin/env python3
"""
myinstants.py — fetch popular meme / soundboard SFX from myinstants.com.

The site's HTML is Cloudflare-challenged, but (a) an unofficial API resolves a
search term -> the sound's direct mp3 URL, and (b) the /media/sounds/ CDN is open.
So: search via the API, download the mp3 straight from the CDN.

  python3 tools/stock_fetcher/myinstants.py -q "vine boom" -n 1
  python3 tools/stock_fetcher/myinstants.py --pack            # curated popular meme pack
  python3 tools/stock_fetcher/myinstants.py -q "airhorn" -n 3 --out assets/common/memes

Meme / soundboard SFX. the owner treats these as fair-use commentary accents for short-form;
provenance (title + source URL) is logged to memes/SOURCE.md. Freesound (`freesound.py`)
remains the bulk royalty-free library; reach for these for personality/comedic beats.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
API = "https://myinstants-api.vercel.app"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
OUTDIR = "assets/common/memes"

# curated popular meme pack — prefix -> search query (first result wins)
PACK = [
    ("iphone_notification", "iphone notification"),
    ("heavenly",            "heavenly angelic choir"),
    ("faaah",               "faaah"),
    ("aww",                 "aww"),
    ("roblox_oof",          "roblox oof"),
    ("fart",                "fart"),
    ("vine_boom",           "vine boom"),
    ("bruh",                "bruh"),
    ("airhorn",             "airhorn"),
    ("sad_violin",          "sad violin"),
    ("rimshot",             "ba dum tss"),
    ("windows_error",       "windows error"),
    ("anime_wow",           "anime wow"),
    ("emotional_damage",    "emotional damage"),
    ("nope",                "nope"),
    ("discord_ping",        "discord notification"),
    ("among_us",            "among us role"),
    ("wow",                 "wow"),
    ("crickets",            "awkward cricket"),
    ("taco_bell",           "taco bell bong"),
    # --- 2026 trending / brainrot (search-verified) ---
    ("sad_cat_meow",        "sad cat meow"),
    ("huh_cat",             "huh cat"),
    ("oi_oi_oi",            "oi oi oi"),
    ("tung_sahur",          "tung tung tung sahur"),
    ("tralalero",           "tralalero tralala"),
    ("ballerina_capuccina", "ballerina cappuccina"),
    ("skibidi",             "skibidi"),
    ("what_the_sigma",      "what the sigma"),
    ("metal_pipe",          "metal pipe falling"),
    ("rubber_chicken",      "rubber chicken"),
    ("goofy_run",           "goofy run"),
    ("angry_birds",         "angry birds"),
    ("mario_coin",          "mario coin"),
    ("duolingo",            "duolingo"),
    ("aura",                "aura"),
    ("let_him_cook",        "let him cook"),
    ("nuh_uh",              "nuh uh"),
    ("chipi_chapa",         "chipi chipi chapa chapa"),
    ("ice_cream_so_good",   "ice cream so good"),
    ("crashout",            "crashout"),
]

def _get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read() if binary else r.read().decode("utf-8", "ignore")

def search(q):
    url = API + "/search?q=" + urllib.parse.quote(q)
    try:
        return json.loads(_get(url)).get("data", [])
    except Exception as e:
        print(f"  ! API search failed for '{q}': {e}")
        return []

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]

def note_source(fname, item):
    src = ROOT / OUTDIR / "SOURCE.md"
    src.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        src.write_text("# Meme SFX provenance — source: myinstants.com (fair-use commentary accents)\n\n")
    with open(src, "a") as f:
        f.write(f"- `{fname}` — \"{item['title']}\" · {item.get('url','')}\n")

def download(item, prefix, outdir):
    mp3 = item.get("mp3")
    if not mp3:
        return None
    outdir = ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    fname = f"{prefix}_{slug(item['title'])}.mp3"
    out = outdir / fname
    if out.exists():
        print(f"  skip {fname} (exists)"); return out
    try:
        blob = _get(mp3, binary=True)
    except Exception as e:
        print(f"  ! download failed {item.get('title')}: {e}"); return None
    if len(blob) < 200:
        print(f"  ! tiny/empty file for {item.get('title')}, skipping"); return None
    out.write_bytes(blob)
    note_source(fname, item)
    print(f"  → {out.relative_to(ROOT)} ({len(blob)//1024} KB) — {item['title']}")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query")
    ap.add_argument("-n", "--count", type=int, default=1)
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--out", default=OUTDIR)
    a = ap.parse_args()

    if a.pack:
        got = 0
        for prefix, q in PACK:
            print(f"[meme] {prefix}: \"{q}\"")
            res = search(q)
            if res and download(res[0], prefix, a.out):
                got += 1
        print(f"\ndone — {got}/{len(PACK)} meme sounds in {a.out}. Provenance: {a.out}/SOURCE.md.")
        return
    if not a.query:
        sys.exit("provide -q QUERY (or --pack)")
    res = search(a.query)
    if not res:
        sys.exit("no results")
    for item in res[:a.count]:
        download(item, slug(a.query), a.out)

if __name__ == "__main__":
    main()
