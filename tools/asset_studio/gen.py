#!/usr/bin/env python3
"""
asset_studio/gen.py — minimal manifest-driven Replicate asset generator (pilot).

Dispatches each asset by capability to the right Replicate model, caches by
content hash, downloads into the target dir. This is the seed of the future
asset_studio; for the v3 pilot the manifest is embedded below.

Usage:
  python3 tools/asset_studio/gen.py --out public/openai-aws-bedrock/elements [--only id1,id2] [--force]
  python3 tools/asset_studio/gen.py --dry      # print prompts + est cost, no calls
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

try:
    import replicate, requests
except ImportError:
    sys.exit("pip install replicate requests  (activate .venv)")

# Load REPLICATE_API_TOKEN from .env (repo root) without extra deps.
def _load_env():
    root = Path(__file__).resolve().parents[2]
    envf = root / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_load_env()
if not os.environ.get("REPLICATE_API_TOKEN"):
    sys.exit("REPLICATE_API_TOKEN not found in environment or .env")

# ── SIGNAL palette (kept in sync with src/components/asset-system/signal.ts) ──
CORAL = "#FF4A2E"; COBALT = "#2B59FF"; INK = "#16120E"; PAPER = "#EDE6D6"

# Per-run price estimates (USD) — for --dry preview only.
PRICE = {"flux": 0.04, "svg": 0.08, "loop": 0.09}

# Style suffix appended to every cinematic background/hero for channel consistency.
CINE = ("cinematic, dramatic volumetric lighting, fine film grain, subtle haze, "
        "deep depth of field, photographic, premium editorial, no text, no watermark, "
        "no logos, no captions")
ICON_STYLE = ("minimalist single-color icon, bold solid black fill, centered, generous "
              "padding, flat, transparent background, no text, no shadow")

# ── MANIFEST ──────────────────────────────────────────────────────────────────
# type: flux (raster 9:16 bg/hero) | hero (flux 9:16 hero) | svg (recraft icon) | loop (seedance i2v)
MANIFEST = [
  # Backgrounds (depth + grain — kill the void). 9:16 full frame.
  {"id":"bg_cold","type":"flux","ar":"9:16",
   "prompt":f"abstract dark background, deep cobalt blue to warm near-black ({INK}) vertical gradient, "
            f"cold controlled corporate mood, faint single cold light from top, heavy negative space, {CINE}"},
  {"id":"bg_ember","type":"flux","ar":"9:16",
   "prompt":f"abstract dark background, warm near-black ({INK}) with a soft coral ({CORAL}) ember glow rising "
            f"from the bottom, hopeful warm mood, volumetric light, heavy negative space, {CINE}"},
  {"id":"bg_grid","type":"flux","ar":"9:16",
   "prompt":f"abstract dark technical background, warm near-black, faint blueprint perspective grid receding into "
            f"depth, a single coral ({CORAL}) accent glow, engineering mood, heavy negative space, {CINE}"},
  # Hero illustrations (cinematic metaphors).
  {"id":"hero_street","type":"hero","ar":"9:16",
   "prompt":"two tall glowing skyscraper towers at night facing each other across one narrow dark street, "
            "the LEFT tower lit cold electric blue, the RIGHT tower lit warm orange, a single tiny glowing human "
            "figure walking across the street from the blue tower toward the orange tower, fog, rain-slick street "
            "reflecting the lights, dramatic vertical composition, " + CINE},
  {"id":"hero_multicloud","type":"hero","ar":"9:16",
   "prompt":"three distinct glowing stylized cloud server forms floating at different depths in a vast night sky, "
            "thin luminous data streams flowing between all three equally, no single cloud dominant, balanced "
            "blue and warm orange light, sense of an open decentralized network, vertical composition, " + CINE},
  # Icons (style-locked, recolorable). Square.
  {"id":"ic_chip","type":"svg","prompt":f"AI processor chip, {ICON_STYLE}"},
  {"id":"ic_cloud","type":"svg","prompt":f"cloud computing server, {ICON_STYLE}"},
  {"id":"ic_lock","type":"svg","prompt":f"security shield with a padlock, {ICON_STYLE}"},
  {"id":"ic_dollar","type":"svg","prompt":f"dollar money stack, {ICON_STYLE}"},
  {"id":"ic_code","type":"svg","prompt":f"code brackets terminal, {ICON_STYLE}"},
  {"id":"ic_dev","type":"svg","prompt":f"software developer at a desk, {ICON_STYLE}"},
  # Ambient loop (subtle motion). image-to-video off bg_ember.
  {"id":"loop_embers","type":"loop","src":"bg_ember.png",
   "prompt":"slow drifting glowing embers and gentle volumetric light haze, very subtle ambient motion, "
            "camera locked"},
]

MODELS = {
  "flux":"black-forest-labs/flux-1.1-pro",
  "hero":"black-forest-labs/flux-1.1-pro",
  "svg":"recraft-ai/recraft-v3-svg",
  "loop":"bytedance/seedance-1-lite",
}

def cache_key(a):
    raw = json.dumps({k:a[k] for k in a if k!="id"}, sort_keys=True)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def download(out, dest):
    # replicate.run may return FileOutput, list, or url string
    items = out if isinstance(out, list) else [out]
    o = items[0]
    if hasattr(o, "read"):
        data = o.read()
    else:
        data = requests.get(str(o), timeout=120).content
    Path(dest).write_bytes(data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="public/openai-aws-bedrock/elements")
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cache = out / ".cache.json"
    idx = json.loads(cache.read_text()) if cache.exists() else {}
    only = set(filter(None, a.only.split(",")))

    est = 0.0; todo = []
    for asset in MANIFEST:
        if only and asset["id"] not in only: continue
        ext = {"flux":"png","hero":"png","svg":"svg","loop":"mp4"}[asset["type"]]
        dest = out / f"{asset['id']}.{ext}"
        key = cache_key(asset)
        if not a.force and dest.exists() and idx.get(asset["id"]) == key:
            print(f"  cache-hit  {asset['id']}"); continue
        todo.append((asset, dest, key, ext))
        est += PRICE.get("svg" if asset["type"]=="svg" else ("loop" if asset["type"]=="loop" else "flux"), 0.04)

    print(f"\n{len(todo)} to generate · est ${est:.2f}\n")
    if a.dry:
        for asset,_,_,_ in todo: print(f"  [{asset['type']:5}] {asset['id']}: {asset['prompt'][:90]}...")
        return 0

    for asset, dest, key, ext in todo:
        model = MODELS[asset["type"]]
        try:
            if asset["type"] in ("flux","hero"):
                inp = {"prompt":asset["prompt"], "aspect_ratio":asset["ar"],
                       "output_format":"png", "safety_tolerance":2, "prompt_upsampling":True}
            elif asset["type"]=="svg":
                inp = {"prompt":asset["prompt"], "style":"line_art", "size":"1024x1024"}
            elif asset["type"]=="loop":
                srcp = out / asset["src"]
                if not srcp.exists():
                    print(f"  SKIP {asset['id']}: needs {asset['src']} first"); continue
                inp = {"image":open(srcp,"rb"), "prompt":asset["prompt"],
                       "duration":5, "resolution":"720p", "camera_fixed":True}
            t0=time.time()
            print(f"  gen  {asset['id']} via {model} ...", flush=True)
            res = replicate.run(model, input=inp)
            download(res, dest)
            idx[asset["id"]] = key; cache.write_text(json.dumps(idx, indent=2))
            print(f"   ✓ {dest}  ({time.time()-t0:.0f}s, {dest.stat().st_size//1024}kb)")
        except Exception as e:
            print(f"   ✗ {asset['id']} FAILED: {e}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
