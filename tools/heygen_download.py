#!/usr/bin/env python3
"""Poll HeyGen for a finished video (by title) using the browser's cookies, then
download the MP4. Standalone counterpart to heygen_playwright's poll+download."""
import argparse, os, time
import browser_cookie3, requests

API = ("https://api2.heygen.com/v1/project/items?limit=20&filter_groups=avatar_video"
       "&filter_groups=avatar_video_draft&filter_groups=batch_video"
       "&sort_key=created_ts&sort_order=desc&is_trash=false")
H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/148.0 Safari/537.36",
     "Origin": "https://app.heygen.com", "Referer": "https://app.heygen.com/"}

def cookie_file(profile):
    base = os.path.expanduser(f"~/Library/Application Support/Google/Chrome/{profile}")
    for c in (f"{base}/Network/Cookies", f"{base}/Cookies"):
        if os.path.exists(c): return c

def items(jar):
    j = requests.get(API, cookies=jar, headers=H, timeout=30).json()
    d = j.get("data", {})
    return d.get("items") or d.get("list") or (d if isinstance(d, list) else []) or j.get("items", [])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--profile", default="Profile 1"); ap.add_argument("--timeout", type=int, default=1200)
    a = ap.parse_args()
    jar = browser_cookie3.chrome(cookie_file=cookie_file(a.profile))
    deadline = time.time() + a.timeout; last = None
    while time.time() < deadline:
        try:
            m = next((x for x in items(jar) if (x.get("name") or "") == a.title), None)
        except Exception as e:
            print("poll error:", e); time.sleep(8); continue
        if m:
            st = m.get("status")
            if st != last: print("status:", st); last = st
            if st == "completed":
                url = m.get("video_url")
                os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
                with requests.get(url, stream=True, timeout=120) as r:
                    r.raise_for_status(); n = 0
                    with open(a.out, "wb") as f:
                        for ch in r.iter_content(1 << 20): f.write(ch); n += len(ch)
                print(f"downloaded {n/1e6:.1f} MB -> {a.out}"); return
            if st in ("failed", "error"):
                print("RENDER FAILED:", m.get("error_message")); return
        time.sleep(8)
    print("TIMEOUT waiting for render")

if __name__ == "__main__":
    main()
