#!/usr/bin/env python3
"""
noto_lottie.py — fetch premade Lottie animations from Google's Noto Animated Emoji
(keyless, CC BY 4.0 — credit Google, logged to assets/common/CREDITS.md).

~600 hand-animated emoji as production Lottie JSON (60fps, 1024px, transparent) —
perfect accent bursts: confetti, fire, rocket, eyes, 100, mind-blown, siren…
Browse the full set: https://googlefonts.github.io/noto-emoji-animation/

  python3 tools/stock_fetcher/noto_lottie.py --pack            # curated starter set
  python3 tools/stock_fetcher/noto_lottie.py --emoji "🎉" --name confetti
  python3 tools/stock_fetcher/noto_lottie.py --code 1f680 --name rocket

Embed per the lottie skill: lottie-web adapter, autoplay:false, loop:false,
register on window.__hfLottie. Tint via Lottie color layers or CSS filter.
"""
import argparse, json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "common" / "lottie"
CREDITS = ROOT / "assets" / "common" / "CREDITS.md"
URL = "https://fonts.gstatic.com/s/e/notoemoji/latest/{code}/lottie.json"

PACK = {  # curated for tech shorts: reveals, reactions, accents
    "confetti":       "🎉", "confetti-ball": "🎊", "fire": "🔥", "rocket": "🚀",
    "eyes":           "👀", "hundred":       "💯", "mind-blown": "🤯", "clap": "👏",
    "money-bag":      "💰", "money-wings":   "💸", "chart-up": "📈", "check": "✅",
    "light-bulb":     "💡", "siren":         "🚨", "zap": "⚡", "thinking": "🤔",
    "partying-face":  "🥳", "warning":       "⚠️", "lock": "🔒", "unlock": "🔓",
    "robot":          "🤖", "brain":         "🧠", "star-struck": "🤩", "boom": "💥",
}

def code_of(emoji):
    return "_".join(f"{ord(c):x}" for c in emoji if ord(c) != 0xFE0F)

def fetch(name, code):
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{name}.json"
    if dest.exists():
        print(f"noto_lottie: SKIP {name} (exists)"); return True
    try:
        with urllib.request.urlopen(URL.format(code=code), timeout=30) as r:
            data = r.read()
        d = json.loads(data)
        assert "layers" in d and d.get("op"), "not a lottie"
        dest.write_bytes(data)
        print(f"noto_lottie: saved {dest.relative_to(ROOT)}  ({d.get('op')}f @ {d.get('fr')}fps)")
        return True
    except Exception as e:
        print(f"noto_lottie: MISS {name} ({code}) — {e}")
        return False

def log_credit():
    line = ("- `assets/common/lottie/*` (Noto Animated Emoji) — Google, **CC BY 4.0** — "
            "credit \"Animated emoji by Google (Noto)\" in post.md when used.\n")
    if CREDITS.exists() and "Noto Animated Emoji" in CREDITS.read_text(): return
    with open(CREDITS, "a") as f: f.write("\n" + line)
    print("noto_lottie: credit line added to CREDITS.md")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pack", action="store_true", help="fetch the curated starter set")
    ap.add_argument("--emoji", help="emoji character to fetch")
    ap.add_argument("--code", help="codepoint(s), e.g. 1f389 or 1f62e_200d_1f4a8")
    ap.add_argument("--name", help="output filename (no extension)")
    a = ap.parse_args()
    ok = 0
    if a.pack:
        for name, em in PACK.items(): ok += fetch(name, code_of(em))
    elif a.emoji:
        ok += fetch(a.name or code_of(a.emoji), code_of(a.emoji))
    elif a.code:
        ok += fetch(a.name or a.code, a.code)
    else:
        ap.error("need --pack, --emoji, or --code")
    if ok: log_credit()

if __name__ == "__main__":
    main()
