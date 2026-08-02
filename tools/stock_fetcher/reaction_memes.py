#!/usr/bin/env python3
"""
reaction_memes.py — fetch short reaction-meme VIDEO cutaways from YouTube, by emotion.

Wraps youtube.py (Serper search -> yt-dlp download through the home-IP SOCKS proxy ->
trim). Grabs short green-screen reaction shorts (clean, single-subject, easy to chroma-key
and composite between A-roll beats). Output: assets/stock/memes_video/react_<emotion>_*.mp4

  python3 tools/stock_fetcher/reaction_memes.py --pack                 # one per emotion
  python3 tools/stock_fetcher/reaction_memes.py -e funny excited -n 2  # specific emotions
  python3 tools/stock_fetcher/reaction_memes.py -e sad --no-green      # full-frame (not keyable)
  python3 tools/stock_fetcher/reaction_memes.py -e shocked --list      # search only

the owner treats these reaction clips as fair-use commentary accents for short-form. Green-screen
clips: chroma-key them (see docs/guides/CHROMAKEY_TRANSPARENT_VIDEO.md) before compositing. Use
with intent (one or two per video) to punctuate a beat — match the meme's energy to the moment.
"""
import argparse, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
YT = HERE / "youtube.py"
OUTDIR = "assets/stock/memes_video"

# emotion -> base search phrase (the " green screen" suffix is added unless --no-green)
PACK = {
    "funny":     "funny laughing reaction meme",
    "sad":       "crying sad reaction meme",
    "excited":   "excited hype lets go reaction meme",
    "shocked":   "shocked surprised gasp reaction meme",
    "mindblown": "mind blown reaction meme",
    "awkward":   "awkward side eye reaction meme",
    "facepalm":  "facepalm disappointed reaction meme",
    "thinking":  "confused thinking reaction meme",
    "clapping":  "clapping applause reaction meme",
    "scared":    "scared nervous sweating reaction meme",
}

def fetch(emotion, phrase, n, dur, green, list_only):
    q = phrase + (" green screen" if green else "")
    cmd = [sys.executable, str(YT), "-q", q, "--shorts", "-n", str(n),
           "--out", OUTDIR, "--prefix", f"react_{emotion}"]
    if list_only:
        cmd.append("--list")
    else:
        cmd += ["--start", "0", "--duration", str(dur)]
    print(f"\n=== [{emotion}] {q} ===")
    subprocess.run(cmd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", action="store_true", help="fetch one clip for every emotion")
    ap.add_argument("-e", "--emotions", nargs="+", choices=sorted(PACK), help="specific emotions")
    ap.add_argument("-n", "--count", type=int, default=1)
    ap.add_argument("-d", "--duration", type=float, default=3.0, help="trim length (s)")
    ap.add_argument("--no-green", action="store_true", help="full-frame clips (skip 'green screen')")
    ap.add_argument("--list", action="store_true", help="search only, no download")
    a = ap.parse_args()

    emotions = list(PACK) if a.pack else (a.emotions or [])
    if not emotions:
        sys.exit("use --pack or -e EMOTION [EMOTION ...] (choices: " + ", ".join(sorted(PACK)) + ")")
    for e in emotions:
        fetch(e, PACK[e], a.count, a.duration, not a.no_green, a.list)
    if not a.list:
        print(f"\ndone — clips in {OUTDIR}. Green-screen ones: chroma-key before compositing.")

if __name__ == "__main__":
    main()
