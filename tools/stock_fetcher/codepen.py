#!/usr/bin/env python3
"""
codepen.py — fetch a CodePen pen's full source for use as a motion reference.

codepen.io itself blocks non-browser clients (Cloudflare 403 from any IP), but
CodePen's embed CDN serves the complete rendered pen keylessly:
    https://cdpn.io/{user}/fullpage/{slug}
The pen's HTML+CSS+JS arrives inline in the iframe srcdoc; we unescape it and
save a standalone HTML file.

  python3 tools/stock_fetcher/codepen.py https://codepen.io/Ayachem/pen/KaLbZK
  python3 tools/stock_fetcher/codepen.py --user Ayachem --slug KaLbZK --name svg-stroke-text

Saved to docs/motion-ref/codepen/ (they are REFERENCES to adapt, not drop-in
assets): CSS-keyframe pens port near-verbatim (HyperFrames can pause/seek CSS
animations — see the css-animations skill); rAF/canvas/random-driven pens must
be rebuilt as paused GSAP timelines before use. License: public pens are MIT
(https://blog.codepen.io/legal/licensing/) — author credited in CREDITS.md.
"""
import argparse, html as htmllib, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "motion-ref" / "codepen"
CREDITS = ROOT / "assets" / "common" / "CREDITS.md"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

def die(msg): sys.exit("codepen: " + msg)

def fetch(url, proxy=None):
    cmd = ["curl", "-s", "-m", "30", "-H", f"User-Agent: {UA}", url]
    if proxy: cmd[1:1] = ["--proxy", proxy]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", nargs="?", help="https://codepen.io/<user>/pen/<slug>")
    ap.add_argument("--user"); ap.add_argument("--slug")
    ap.add_argument("--name", help="output filename (default <user>-<slug>)")
    a = ap.parse_args()

    user, slug = a.user, a.slug
    if a.url:
        m = re.search(r"codepen\.io/([^/]+)/(?:pen|details|full|debug)/([A-Za-z]+)", a.url)
        if not m: die("could not parse pen URL: " + a.url)
        user, slug = m.group(1), m.group(2)
    if not (user and slug): die("need a pen URL or --user + --slug")

    cdn = f"https://cdpn.io/{user}/fullpage/{slug}"
    page = fetch(cdn)
    if "srcdoc=" not in page:
        page = fetch(cdn, proxy="socks5h://127.0.0.1:1080")   # office-IP fallback
    if "srcdoc=" not in page: die(f"no srcdoc in {cdn} (pen private/deleted?)")

    m = re.search(r'srcdoc="(.*?)"\s*\n?\s*sandbox=', page, re.S)
    if not m: die("could not extract srcdoc")
    doc = htmllib.unescape(m.group(1))

    tm = re.search(r"<title>([^<]*)</title>", doc)
    title = tm.group(1).strip() if tm else f"{user}/{slug}"
    name = a.name or f"{user}-{slug}"
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{name}.html"
    header = (f"<!-- SOURCE: https://codepen.io/{user}/pen/{slug}\n"
              f"     TITLE: {title}\n"
              f"     LICENSE: MIT (public CodePen pen)\n"
              f"     NOTE: motion REFERENCE — adapt to seek-safe HyperFrames form before use\n"
              f"           (CSS keyframes: css-animations skill; JS/rAF: rebuild as paused GSAP tl) -->\n")
    dest.write_text(header + doc)
    print(f"codepen: saved {dest.relative_to(ROOT)}  ({len(doc)} bytes, \"{title}\")")

    line = f"- `docs/motion-ref/codepen/{name}.html` — \"{title}\" by {user} (codepen.io/{user}/pen/{slug}), **MIT**\n"
    if CREDITS.exists() and f"codepen/{name}.html" not in CREDITS.read_text():
        with open(CREDITS, "a") as f: f.write(line)
        print("codepen: credited in CREDITS.md")

if __name__ == "__main__":
    main()
