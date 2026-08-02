#!/usr/bin/env python3
"""Quick HeyGen session/health debug: load app via SOCKS proxy with saved cookies, screenshot state."""
import json
import sys
import time
from playwright.sync_api import sync_playwright

COOKIES = "tools/heygen_session.json"
PROXY = "socks5://127.0.0.1:1080"
OUT_DIR = "~/workspace/workspace"


def load_cookies():
    d = json.load(open(COOKIES))
    cks = d if isinstance(d, list) else d.get("cookies", [])
    norm = []
    for c in cks:
        nc = {
            "name": c.get("name"),
            "value": c.get("value"),
            "domain": c.get("domain"),
            "path": c.get("path", "/"),
        }
        exp = c.get("expires", c.get("expirationDate"))
        if exp and exp > 0:
            nc["expires"] = float(exp)
        ss = c.get("sameSite")
        if ss in ("Strict", "Lax", "None"):
            nc["sameSite"] = ss
        if c.get("secure") is not None:
            nc["secure"] = bool(c.get("secure"))
        if c.get("httpOnly") is not None:
            nc["httpOnly"] = bool(c.get("httpOnly"))
        if nc["name"] and nc["domain"]:
            norm.append(nc)
    return norm


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, proxy={"server": PROXY},
                                    args=["--no-sandbox"])
        ctx = browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
            locale="en-US", timezone_id="Asia/Kolkata",
            viewport={"width": 1366, "height": 900},
        )
        try:
            ctx.add_cookies(load_cookies())
        except Exception as e:
            print(f"COOKIE-LOAD-ERROR: {e}")
        page = ctx.new_page()
        result = {}
        try:
            page.goto("https://app.heygen.com/home", wait_until="domcontentloaded", timeout=60000)
            time.sleep(8)
            result["url"] = page.url
            result["title"] = page.title()
            body = (page.inner_text("body")[:600] if page.query_selector("body") else "")
            result["body_snippet"] = body.replace("\n", " ")[:600]
            page.screenshot(path=f"{OUT_DIR}/heygen_debug_home.png", full_page=False)
            # heuristics
            low = (result["url"] + " " + body).lower()
            if "login" in result["url"].lower() or "sign in" in low or "log in" in low or "/login" in low:
                result["verdict"] = "LOGGED-OUT / session expired (login wall)"
            elif "create" in low or "project" in low or "avatar" in low or "home" in low:
                result["verdict"] = "LOGGED-IN (dashboard reachable)"
            else:
                result["verdict"] = "UNKNOWN (see screenshot)"
        except Exception as e:
            result["error"] = str(e)
            try:
                page.screenshot(path=f"{OUT_DIR}/heygen_debug_home.png", full_page=False)
            except Exception:
                pass
        print(json.dumps(result, indent=2))
        browser.close()


if __name__ == "__main__":
    sys.exit(main())
