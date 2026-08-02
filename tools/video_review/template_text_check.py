#!/usr/bin/env python3
"""Template-text QA check — scan the composition + components for leftover
placeholder/demo text that a vendor block shipped with (e.g. the code-snippet
"Official VS Code built-in theme / Light Modern" header, x-post "Prompt to replace
this text", lorem ipsum, demo handles). Run BEFORE rendering.

  python3 tools/video_review/template_text_check.py [--root .]

Exit code 1 if any HIGH-confidence template text is found (so it can gate CI / npm run check).
"""
import argparse, pathlib, re, sys

# (pattern, label, severity)  severity: "block" = clear template, "review" = probably template
PATTERNS = [
    (r"lorem ipsum", "lorem ipsum", "block"),
    (r"prompt to replace", "x-post/placeholder 'Prompt to replace…'", "block"),
    (r"your\s*hashtag|#yourhashtag", "placeholder hashtag", "block"),
    (r"official vs code built-?in theme", "code-snippet demo header", "block"),
    (r"replace (this|with your)", "'replace this/with your…' placeholder", "block"),
    (r"\bplaceholder\b", "literal 'placeholder'", "block"),
    (r"hello,?\s*world", "'Hello World' demo text", "block"),
    (r"example\.com|john doe|jane doe|acme", "example.com / John Doe / ACME demo", "block"),
    (r"@hyperframes|@heygen|>\s*heygen\s*<|heygen\.com", "vendor demo handle/name (HeyGen/Hyperframes)", "block"),
    (r"functional[_ ]toolkit|a small functional toolkit", "code-snippet demo code (functional_toolkit.py)", "review"),
    (r"light modern|dark modern|monokai|solarized", "code-snippet theme-name label (may be on-screen)", "review"),
    (r"\bsample (text|title|caption)\b|dummy text", "sample/dummy text", "review"),
]

def scan(root):
    root = pathlib.Path(root)
    files = [root / "index.html"] + sorted((root / "compositions").rglob("*.html")) if (root / "compositions").exists() else [root / "index.html"]
    hits = {"block": [], "review": []}
    for f in files:
        if not f.exists():
            continue
        for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            low = line.lower()
            for pat, label, sev in PATTERNS:
                if re.search(pat, low):
                    hits[sev].append((f.relative_to(root) if root in f.parents or f.parent == root else f, i, label, line.strip()[:90]))
                    break
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    hits = scan(a.root)
    if not hits["block"] and not hits["review"]:
        print("✓ No template/placeholder text found."); return 0
    for sev, icon in (("block", "✗ TEMPLATE TEXT"), ("review", "⚠ REVIEW")):
        for f, i, label, snippet in hits[sev]:
            print(f"  {icon}: {f}:{i}  [{label}]\n      {snippet}")
    if hits["block"]:
        print(f"\n{len(hits['block'])} blocking match(es) — remove before rendering.")
        return 1
    print(f"\n{len(hits['review'])} review match(es) — confirm they're intentional.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
