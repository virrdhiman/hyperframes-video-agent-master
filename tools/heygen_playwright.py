#!/usr/bin/env python3
"""
heygen_playwright.py — Drive HeyGen's web editor to generate an avatar video on
your *subscription* credits (no paid API plan) and download the finished MP4.

Why this exists: HeyGen's REST API is billed from a separate paid balance, but the
web app generates from your subscription's credit pool. This script automates the
web UI with a persistent browser profile (you log in by hand once), so it never
handles your password and reuses the saved session on every run.

  pip install playwright requests
  playwright install chromium

  # First run: a browser opens. Log into HeyGen, then press Enter in the terminal.
  python3 tools/heygen_playwright.py --script projects/<slug>/script.txt \
      --title "Google Photos Wardrobe" --out out/google_photos_wardrobe.mp4

All selectors below were captured live against HeyGen app-v4 (June 2026). The
robust parts (script typing, motion engine, generate modal, status poll, download)
are verified end-to-end. The avatar-picker block is the most likely to drift if
HeyGen changes that panel — re-capture with `playwright codegen` if it misfires.

NOTE: Automating your own account for your own content is a personal-automation
use, but it is against HeyGen's ToS to script their site. Keep volume low/personal.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import requests
from playwright.sync_api import Error as PWError, Page, TimeoutError as PWTimeout, sync_playwright

# --- config -----------------------------------------------------------------
PROFILE_DIR = Path.home() / ".heygen_pw_profile"   # persistent login lives here
CREATE_URL = "https://app.heygen.com/create-v4/draft?panel=scene"
LOGIN_URL = "https://auth.heygen.com/login"
ITEMS_API = (
    "https://api2.heygen.com/v1/project/items"
    "?limit=20&filter_groups=avatar_video&filter_groups=avatar_video_draft"
    "&filter_groups=batch_video&sort_key=created_ts&sort_order=desc&is_trash=false"
)

# Retrofit AI look library: name -> stable HeyGen character_id (img-src carries it).
# Selecting by id is order-independent, so the grid never silently reuses the saved
# default look. Keep in sync with docs/reference/heygen-avatar-looks.md.
LOOKS = {
    "authority": "b56ff77c19e64f7781f2ff7d978f5c98",   # suit — serious/landmark/regulation
    "pro": "a12efdc233dd4f31bebc919e360cbd6b",          # blazer — business/funding/markets
    "desk": "ba5264c5f4904949a3b80627314ca5b3",         # whiteboard — hardware/chips/dev-tools/tutorial
    "hype": "02b6f12b86964938b557641987651103",         # blue polo — exciting reveal / big launch
    "explainer": "506b7b172c02483c928f38e1d4644b7b",    # beige — standard news (default)
    "realtalk": "a4103a1de9a44c8e90f8bcb4ff3d63b0",     # dark crew — opinion/warning/hot take
    "fun": "10c0a730f96548e28cde385250dc27a3",          # orange tee — playful/quirky/light
    "update": "c171fdb4653c4170a3015e248641c285",        # car — quick "just happened" breaking
    "lifestyle": "09199dcca4324ccaa465a48ba5bd77d2",    # balcony — consumer/everyday
    "casual": "ba58cec5be6b4af99d06b120963b963e",       # navy tee — relaxed/mid-energy
    "pro2": "1b0d9411c593488ca7b13a45893d6819",         # backup
}

DEFAULTS = dict(
    avatar="the owner",          # name as it appears under "My Avatars"
    look=None,               # look name (key in LOOKS) or None to keep --look-index
    motion_engine="Avatar III",
    fps="30",
    resolution="1080p",      # left as-is in the modal (already the default)
    auto_enhance=True,
    portrait=True,           # 9:16 — already the HeyGen default
)


# --- auth via existing Chrome cookies ---------------------------------------
def _chrome_cookie_file(profile: str) -> str | None:
    """Resolve the Cookies DB path for a given Google Chrome profile (e.g. 'Profile 1')."""
    base = Path.home() / "Library/Application Support/Google/Chrome" / profile
    for cand in (base / "Network" / "Cookies", base / "Cookies"):
        if cand.exists():
            return str(cand)
    return None


def _collect_chrome_cookies(browser: str = "chrome", profile: str = "Default") -> list[dict]:
    """Pull the logged-in HeyGen cookies from your real browser's cookie store and
    return them as Playwright cookie dicts. Cookie values stay inside this process.
    On macOS this may trigger a one-time Keychain prompt."""
    import browser_cookie3 as bc3

    getter = getattr(bc3, browser, None) or bc3.chrome
    kwargs = {}
    if browser in ("chrome", "chromium", "brave", "edge", "arc") and profile and profile != "Default":
        cf = _chrome_cookie_file(profile)
        if cf:
            kwargs["cookie_file"] = cf
    jar = getter(**kwargs)  # reads + decrypts the browser's cookie DB
    cookies = []
    for c in jar:
        if "heygen" not in (c.domain or ""):
            continue
        try:
            http_only = c.has_nonstandard_attr("HttpOnly") or c.has_nonstandard_attr("httponly")
        except Exception:
            http_only = False
        ck = {
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path or "/",
            "secure": bool(c.secure),
            "httpOnly": bool(http_only),
            "sameSite": "None" if c.secure else "Lax",
        }
        if c.expires:
            ck["expires"] = float(c.expires)
        cookies.append(ck)
    if not cookies:
        raise SystemExit(f"No HeyGen cookies found in {browser} — are you logged in there?")
    return cookies


def _load_chrome_cookies(context, browser: str = "chrome", profile: str = "Default") -> int:
    """Collect HeyGen cookies from the local browser and inject them into Playwright."""
    cookies = _collect_chrome_cookies(browser, profile)
    context.add_cookies(cookies)
    return len(cookies)


# --- auth via an exported cookie/session bundle (for a headless server) ------
def _load_cookies_from_file(context, path: str) -> int:
    """Inject HeyGen cookies from a JSON bundle exported on another machine, so a
    headless server with no local browser can reuse a Mac login. Accepts either a
    bare list of Playwright cookie dicts or a session bundle {"cookies": [...]}."""
    import json
    data = json.loads(Path(path).read_text())
    cookies = data["cookies"] if isinstance(data, dict) else data
    cookies = [c for c in cookies if "heygen" in (c.get("domain") or "")]
    if not cookies:
        raise SystemExit(f"No HeyGen cookies in {path}")
    context.add_cookies(cookies)
    return len(cookies)


def _read_session_bundle(path: str) -> dict:
    """Read the env recorded next to the cookies (user_agent/timezone_id/locale) so
    the server can replay the Mac's browser environment and not look like a new device."""
    import json
    try:
        data = json.loads(Path(path).read_text())
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _local_timezone_id() -> str | None:
    """Best-effort IANA tz name on macOS/Linux (e.g. 'Asia/Kolkata') from /etc/localtime."""
    import os
    try:
        link = os.readlink("/etc/localtime")
        if "zoneinfo/" in link:
            return link.split("zoneinfo/")[-1]
    except OSError:
        pass
    return None


def export_session(out_path: str, browser: str, profile: str) -> None:
    """MAC-SIDE: capture the live HeyGen cookies + this machine's browser environment
    (real Chrome UA / timezone / locale) into one JSON bundle to copy to the server.
    Replaying these keeps a relocated session looking like the machine it was made on
    (cookies + UA + tz + locale match). It does NOT change the server's IP or device
    fingerprint — see the script header and the SSH-tunnel note."""
    import json, os
    cookies = _collect_chrome_cookies(browser, profile)
    ua = None
    try:  # grab the real Chrome UA so the server can match it byte-for-byte
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome", headless=True)
            ua = b.new_page().evaluate("() => navigator.userAgent")
            b.close()
    except Exception:
        ua = None
    bundle = {
        "cookies": cookies,
        "user_agent": ua,
        "timezone_id": _local_timezone_id(),
        "locale": (os.environ.get("LANG", "en_US").split(".")[0].replace("_", "-") or "en-US"),
    }
    Path(out_path).write_text(json.dumps(bundle, indent=2))
    print(f"✓ exported {len(cookies)} cookies + env (ua={'yes' if ua else 'no'}, "
          f"tz={bundle['timezone_id']}, locale={bundle['locale']}) -> {out_path}")
    print("  copy it to the server (scp), then run there with:  --cookies-file <thatfile>")


# --- native login on the server (magic link) — born on the box, no cookie transfer
def login_request(email: str, headless: bool, proxy: str | None = None) -> None:
    """Phase 1 (run ON the server): open HeyGen login, switch to email, and email a
    magic link to `email`. Any pending-login state persists in PROFILE_DIR so Phase 2
    (--login-complete) can finish in the same profile. Writes debug screenshots to /tmp."""
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR), headless=headless, channel="chrome",
            proxy={"server": proxy} if proxy else None,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2500)
            page.get_by_text("Use email", exact=True).first.click()   # reveal email form
            page.wait_for_timeout(1200)
            box = page.get_by_placeholder("Enter your email")
            if not box.count():
                box = page.locator('input[type="email"]:visible')
            box.first.fill(email)
            page.wait_for_timeout(400)
            page.screenshot(path="/tmp/heygen_login_email.png")
            clicked = False
            for name in ("Send a secure magic link", "Continue", "Sign in", "Log in"):
                btn = page.get_by_role("button", name=name)
                if btn.count() and btn.first.is_visible():
                    btn.first.click(); clicked = True
                    print(f"• clicked {name!r}")
                    break
            page.wait_for_timeout(3500)
            page.screenshot(path="/tmp/heygen_login_requested.png")
            print(f"{'✓' if clicked else '⚠'} magic-link request for {email} "
                  f"({'submitted' if clicked else 'NO submit button matched — see /tmp/heygen_login_email.png'}).")
            print("  Check the inbox, then finish with:  --login-complete --link '<full url>'")
        finally:
            ctx.close()


def login_complete(link: str, headless: bool, proxy: str | None = None) -> None:
    """Phase 2 (run ON the server): open the magic link in the saved profile to finish
    login, then confirm the editor loads. Session persists in PROFILE_DIR afterward."""
    if not link.startswith("http"):
        raise SystemExit("--link must be the full https:// magic-link URL from the email")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR), headless=headless, channel="chrome",
            proxy={"server": proxy} if proxy else None,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(link, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(6000)
            landed = page.url
            page.screenshot(path="/tmp/heygen_login_done.png")
            ok = False
            try:
                page.goto(CREATE_URL, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)
                ok = bool(page.locator(".tiptap.ProseMirror").count()) or "create" in page.url
            except Exception:
                ok = False
            page.screenshot(path="/tmp/heygen_login_verify.png")
            print(f"landed after link: {landed}")
            print(f"editor url: {page.url}")
            print("✓ logged in — session saved to the server profile."
                  if ok else "⚠ could not confirm the editor loaded — check /tmp/heygen_login_*.png")
        finally:
            ctx.close()


# --- small helpers ----------------------------------------------------------
def _ensure_logged_in(page: Page, timeout_s: int = 300) -> None:
    """Wait (non-blocking) until the editor is loaded. On first run, the user logs
    into HeyGen once in the opened browser window; the session is then cached in
    PROFILE_DIR and future runs skip straight through."""
    print("→ If a HeyGen login page appears, sign in once in the browser window.")
    print(f"  Waiting up to {timeout_s}s for the editor to load...")
    deadline = time.time() + timeout_s
    modal_warned = False
    while time.time() < deadline:
        # FALSE-POSITIVE TRAP (seen 2026-07-05): HeyGen renders the full editor shell —
        # including .tiptap.ProseMirror — for ANONYMOUS visitors, with a sign-in modal on
        # top. The editor selector alone does NOT prove login; check for the modal first.
        try:
            signed_out = page.get_by_text("Sign in with Google", exact=True).count() > 0
        except PWError:
            signed_out = False
        if signed_out:
            if not modal_warned:
                print("  ⚠ SIGN-IN MODAL visible — session is NOT authenticated "
                      "(bundle likely missing the HttpOnly 'heygen_session' cookie). "
                      "Headless runs cannot recover: re-auth via --login-request/"
                      "--login-complete, or export from the Mac's cookie DB with "
                      "--export-cookies (NOT a document.cookie-style export).")
                modal_warned = True
            time.sleep(5)
            continue
        if page.locator(".tiptap.ProseMirror").count():
            return
        url = page.url
        if any(k in url for k in ("login", "auth", "sso", "signin")):
            time.sleep(3)
            continue
        try:
            page.goto(CREATE_URL, wait_until="domcontentloaded", timeout=90_000)
            # slow SOCKS tunnel: the SPA can take >30s to boot — don't thrash with re-gotos
            page.wait_for_selector(".tiptap.ProseMirror", timeout=75_000)
            return
        except PWTimeout:
            time.sleep(3)
        except PWError as e:
            # flaky SOCKS tunnel: ERR_NETWORK_CHANGED / ERR_TIMED_OUT — retry within deadline
            print(f"  transient nav error, retrying: {str(e).splitlines()[0][:120]}")
            time.sleep(5)
    raise SystemExit(
        "Timed out waiting for login / editor — session not authenticated. "
        + ("The sign-in modal was visible: the cookie bundle is missing the HttpOnly "
           "'heygen_session' cookie. Re-auth: --login-request --email <addr> then "
           "--login-complete --link '<url>', or --export-cookies on the Mac."
           if modal_warned else "Are you logged in?"))


def _wait_draft_ready(page: Page, timeout_s: int = 90) -> None:
    """The editor renders a full-screen 'DraftLoadingPrism' overlay that swallows
    clicks until the draft finishes loading. Wait for it to detach before driving."""
    try:
        page.wait_for_selector(
            '[data-pacific-component="DraftLoadingPrism"]', state="detached",
            timeout=timeout_s * 1000,
        )
    except PWTimeout:
        pass  # overlay may already be gone, or never appeared
    page.wait_for_timeout(500)


def _dismiss_promo(page: Page, attempts: int = 4) -> None:
    """Close the occasional 'Introducing ...' promo modal if it's covering the UI.

    The modal can appear LATE (after the draft finishes loading), so this is called
    both after login and again right before the first editor click. It's a Radix
    dialog: a full-screen `div[data-state="open"].tw-stack-dialog` overlay that
    intercepts pointer events (this blocked the 2026-07-07 run). Verify the overlay
    is actually GONE before returning.
    """
    overlay = page.locator('div[data-state="open"].tw-stack-dialog')
    for _ in range(attempts):
        try:
            if overlay.count() == 0 or not overlay.first.is_visible():
                return
        except Exception:
            return
        closed = False
        # Prefer the dialog's own close (X) button; fall back to Escape.
        for sel in ('div[role="dialog"] button[aria-label="Close"]',
                    'div[role="dialog"] [class*="close" i]',
                    'div[data-state="open"] button[aria-label="Close"]'):
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=600):
                    el.click(timeout=1500)
                    closed = True
                    break
            except Exception:
                pass
        if not closed:
            page.keyboard.press("Escape")
        page.wait_for_timeout(900)


def _set_portrait(page: Page) -> None:
    btn = page.locator('button[aria-label="Portrait (9:16)"]')
    if btn.get_attribute("aria-pressed") != "true":
        btn.click()


def _type_script(page: Page, text: str) -> None:
    editor = page.locator(".tiptap.ProseMirror").first
    editor.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    # ProseMirror needs real keystrokes; .fill() won't register.
    editor.type(text, delay=2)


def _auto_enhance(page: Page) -> None:
    page.get_by_text("Delivery style", exact=False).first.click()
    page.get_by_text("Auto-enhance", exact=False).first.click()
    # Auto-enhance rewrites the script with [emotion] tags server-side.
    page.wait_for_timeout(7000)


# Named background colors. magenta is the recommended chroma key for the the owner
# avatar: green (#00FF00) clashes with the mic's green status LED and blue
# (#0000FF) clashes with the blue polo shirt — both would key out as holes.
# Magenta appears nowhere on the avatar, so it keys cleanly.
BG_COLORS = {
    "green": "#00FF00",
    "blue": "#0000FF",
    "magenta": "#FF00FF",
    "pink": "#FF00FF",
    "chroma": "#FF00FF",
    "white": "#FFFFFF",
    "black": "#000000",
}


def _set_background_color(page: Page, spec: str) -> None:
    """Set the scene avatar's background. `spec` is one of: 'remove' (transparent
    alpha), a named color (green/blue/magenta/white/black/...), or a literal hex
    '#RRGGBB'. Drives the Avatar Background controls on the Avatar & Voice panel.

    NOTE: HeyGen composites the solid color (or alpha) only at render time — the
    editor preview keeps showing the avatar's original footage, so this does NOT
    visibly change the preview. Verified the picker accepts the value; the final
    result only shows in the rendered output."""
    spec = (spec or "").strip().lower()
    if not spec or spec in ("none", "original", "keep"):
        return
    if spec == "remove":
        try:
            page.get_by_text("Remove", exact=True).first.click(timeout=6000)
            print("  background: Remove (transparent)")
        except PWTimeout:
            print("  WARN could not click Background → Remove")
        return
    hex_val = spec if spec.startswith("#") else BG_COLORS.get(spec)
    if not hex_val:
        print(f"  WARN unknown --background '{spec}'; leaving original")
        return
    hex_val = hex_val.upper()
    if not hex_val.startswith("#"):
        hex_val = "#" + hex_val
    try:
        page.get_by_text("Color", exact=True).first.click(timeout=6000)
        page.wait_for_timeout(1500)
    except PWTimeout:
        print("  WARN could not open Background → Color")
        return
    # react-colorful's HexColorInput ignores .fill() and typed keystrokes; set the
    # value via the native input setter + React's input/change events instead.
    res = page.evaluate(
        """(hex)=>{
            const input=[...document.querySelectorAll('input')]
              .find(i=>typeof i.value==='string'&&i.value.startsWith('#'));
            if(!input) return 'no-input';
            const setter=Object.getOwnPropertyDescriptor(
              window.HTMLInputElement.prototype,'value').set;
            input.focus();
            setter.call(input,hex);
            input.dispatchEvent(new Event('input',{bubbles:true}));
            input.dispatchEvent(new Event('change',{bubbles:true}));
            input.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true}));
            input.blur();
            return input.value;
        }""",
        hex_val,
    )
    page.wait_for_timeout(1500)
    print(f"  background: Color {hex_val} (picker reads {res})")


def _select_avatar(page: Page, name: str, look_index: int = 0, look_name: str | None = None) -> None:
    """Ensure the scene's avatar is `name`, applying its look at `look_index`
    (0 = first). HeyGen's moderation can disable Generate for some default avatars,
    so selecting a known-good avatar+look is required, not optional.

    The avatar card and voice card are both `SceneRowButton`s; the avatar is first.
    """
    rows = page.locator('[data-pacific-component="SceneRowButton"]')
    current = ""
    try:
        current = rows.first.inner_text(timeout=5000)
    except PWTimeout:
        pass
    print(f"  detected scene avatar: {current.splitlines()[0] if current else '(unknown)'!r}")
    if not name:
        print("  avatar selection skipped (no --avatar)")
        return
    target_id = LOOKS.get((look_name or "").lower()) if look_name else None
    if look_name and not target_id:
        print(f"  WARN unknown look '{look_name}' — not in LOOKS map; using --look-index {look_index}")
    want_look = bool(target_id) or look_index != 0
    avatar_ok = name.lower() in current.lower()
    if avatar_ok and not want_look:
        print(f"  avatar already '{name}', no specific look requested — skipping picker")
        return
    if avatar_ok:
        print(f"  avatar already '{name}'; opening picker to APPLY look {look_name or look_index!r}")

    # Open the avatar card -> looks panel -> full picker.  Always run this when a look
    # is requested, even if the avatar already matches — otherwise the look is never
    # applied and the scene silently keeps its saved default look (the Hype-repeat bug).
    rows.first.click()
    page.wait_for_timeout(800)
    # NEWER UI (2026-06): clicking the avatar row opens the "Choose Avatar & Look" panel
    # with the current avatar's looks grid ALREADY shown — there is no "Replace avatar"
    # button to click (that only switches to a DIFFERENT avatar). So only run the old
    # replace->My-Avatars->search->tile flow when that button is actually present; when
    # the avatar already matches and the looks grid is open, skip straight to look pick.
    grid_already_open = False
    try:
        page.get_by_role("button", name="Replace avatar").click(timeout=4000)
    except PWTimeout:
        if avatar_ok:
            grid_already_open = True
            print("  'Replace avatar' not present — looks grid already open for current avatar; "
                  "selecting look directly")
        else:
            raise
    if not grid_already_open:
        page.wait_for_timeout(500)
        page.get_by_role("tab", name="My Avatars").click()
        search = page.get_by_placeholder("Search")
        search.click()
        search.fill(name)
        page.wait_for_timeout(1500)
        # Click the avatar tile (its thumbnail img has alt=<name>). The tile shows a
        # shimmer-skeleton overlay until the thumbnail lazy-loads — that overlay
        # intercepts clicks, so wait for the image to finish loading first.
        tile = page.locator(f'img[alt="{name}"]').first
        tile.wait_for(state="visible", timeout=15000)
        try:
            page.wait_for_function(
                "(alt) => { const i = document.querySelector(`img[alt=\"${alt}\"]`);"
                " return i && i.complete && i.naturalWidth > 0; }",
                arg=name, timeout=12000,
            )
        except PWTimeout:
            pass
        page.wait_for_timeout(800)
        try:
            tile.click(timeout=8000)
        except PWTimeout:
            tile.click(force=True)  # skeleton still intercepting — click through it
    # Apply the look at look_index from the library. Older UI uses LooksDetailPageInner;
    # the newer "Choose Avatar & Look" panel uses a plain look grid. Try both containers
    # so the character_id matcher below can find the tiles either way. Look thumbnails
    # lazy-load behind a shimmer skeleton, so scroll into view and force-click if needed.
    looks = page.locator(
        '[data-pacific-component="LooksDetailPageInner"] div.tw-cursor-pointer.tw-group'
    )
    try:
        looks.first.wait_for(timeout=6000)
    except PWTimeout:
        # newer panel: look tiles are cursor-pointer groups that contain an <img>
        # carrying the look's character_id in its src; exclude the Design/Upload tiles.
        alt = page.locator('div.tw-cursor-pointer.tw-group:has(img)')
        if alt.count():
            looks = alt
            print(f"  using fallback look-grid selector ({alt.count()} tiles)")
        looks.first.wait_for(timeout=15000)
    look = None
    n = looks.count()
    # Match the tile whose <img> src carries the look's character_id (order-independent,
    # so a reordered/lazy grid can't make us reuse the saved default look).
    if target_id:
        for i in range(n):
            cand = looks.nth(i)
            cand.scroll_into_view_if_needed()
            page.wait_for_timeout(250)
            src = ""
            try:
                src = cand.locator("img").first.get_attribute("src", timeout=2000) or ""
            except Exception:
                src = ""
            print(f"    look tile {i}: src={src[:120]}")
            if target_id in src:
                look = cand
                print(f"  matched look '{look_name}' ({target_id}) at tile {i}")
                break
        if look is None:
            print(f"  WARN look id {target_id} not found in {n} tiles; falling back to index {look_index}")
    if look is None:
        look = looks.nth(look_index)
    look.scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    try:
        look.click(timeout=8000)
    except PWTimeout:
        look.click(force=True)
    page.wait_for_timeout(2500)  # avatar (and voice) apply to the scene
    # No back-navigation needed: Motion Engine is set BEFORE this step (it survives
    # an avatar change), and auto-enhance runs AFTER (it lives in the left panel).


def _open_avatar_voice_panel(page: Page) -> None:
    """Ensure the 'Avatar & Voice' settings panel is showing (where Motion Engine lives)."""
    if page.get_by_text("Motion Engine", exact=True).count():
        return
    # Click the right-rail "Avatar" tab to bring the panel back.
    try:
        page.get_by_role("tab", name="Avatar").click(timeout=2000)
    except PWTimeout:
        page.get_by_text("Avatar", exact=True).first.click()
    page.wait_for_timeout(800)


def _set_motion_engine(page: Page, engine: str) -> None:
    _open_avatar_voice_panel(page)
    # The dropdown trigger is a Radix button whose label is the current engine.
    for current in ("Avatar IV", "Avatar V", "Avatar III"):
        trig = page.get_by_role("button", name=current)
        if trig.count() and trig.first.is_visible():
            if current == engine:
                return
            trig.first.click()
            break
    page.wait_for_timeout(400)
    page.get_by_text(engine, exact=True).first.click()
    page.wait_for_timeout(500)


def _open_generate_modal(page: Page, title: str, fps: str) -> None:
    """Open the Generate/export modal and fill title + fps."""
    page.get_by_role("button", name="Generate").click()
    page.wait_for_timeout(1500)
    # Title — the modal's box; "Untitled Video" also matches the editor's inline
    # title, so take the last (modal) match to avoid a strict violation.
    title_box = page.get_by_placeholder("Untitled Video").last
    title_box.click()
    title_box.fill(title)
    # Fps (Radix select; default is 25)
    try:
        page.get_by_text("25", exact=True).first.click()
        page.get_by_text(fps, exact=True).first.click()
    except Exception:
        pass
    page.wait_for_timeout(1500)  # let "Calculating credits usage..." begin


def _try_click_submit(page: Page, wait_ms: int) -> bool:
    """Wait up to wait_ms for the Submit button to enable, then click it exactly
    once. Returns True if it clicked, False if it stayed disabled the whole time."""
    btn = page.get_by_role("button", name="Submit")
    try:
        btn.wait_for(state="visible", timeout=5000)
    except PWTimeout:
        return False
    deadline = time.time() + wait_ms / 1000.0
    while time.time() < deadline:
        try:
            if btn.is_enabled():
                btn.click(timeout=10000)   # ONE click only -> one render
                page.wait_for_timeout(3000)
                return True
        except Exception:
            pass
        page.wait_for_timeout(500)
    return False


def _close_modal(page: Page) -> None:
    """Dismiss the export modal (the Radix dialog closes on Escape)."""
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(1000)


def _submit_generate(page: Page, title: str, fps: str) -> None:
    """Open the export modal and Submit the render. Submit stays disabled while
    HeyGen runs "Calculating credits usage..." server-side, which over the
    residential proxy can exceed the click default. Robust recovery:
      - wait up to 40s per attempt for the button to enable, then click ONCE;
      - if it never enables, close + reopen the modal and retry (up to 3 times);
      - if still stuck, refresh the browser, reopen the modal, and try once more;
      - only then fail. Submit is clicked at most once on any success path, so
        this never triggers more than one render."""
    PER_ATTEMPT_MS = 40000
    _open_generate_modal(page, title, fps)
    for attempt in range(1, 4):
        if _try_click_submit(page, PER_ATTEMPT_MS):
            print(f"  Submit clicked on attempt {attempt} -> render queued")
            return
        print(f"  Submit not clickable after {PER_ATTEMPT_MS // 1000}s "
              f"(attempt {attempt}/3); closing + reopening modal")
        _close_modal(page)
        _open_generate_modal(page, title, fps)
    print("  3 reopen attempts failed; refreshing browser and retrying once")
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    _open_generate_modal(page, title, fps)
    if _try_click_submit(page, 60000):
        print("  Submit clicked after browser refresh -> render queued")
        return
    raise RuntimeError(
        "Submit never became clickable after 3 modal reopens + a browser refresh")


# --- status poll + download (verified mechanism) ---------------------------
def _fetch_items(page: Page) -> list[dict]:
    """Call HeyGen's internal list API from *inside* the page (shares auth)."""
    return page.evaluate(
        """async (url) => {
            const r = await fetch(url, {credentials: 'include'});
            const j = await r.json();
            const d = j.data || {};
            return d.items || d.list || (Array.isArray(d) ? d : (j.items || []));
        }""",
        ITEMS_API,
    )


def wait_for_completion(page: Page, title: str, timeout_s: int = 900) -> dict:
    """Poll until the named video reports status == 'completed'. Returns the item."""
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        items = _fetch_items(page)
        match = next((x for x in items if (x.get("name") or "") == title), None)
        if match:
            status = match.get("status")
            if status != last:
                print(f"  status: {status}")
                last = status
            if status == "completed":
                return match
            if status in ("failed", "error"):
                raise RuntimeError(f"Render failed: {match.get('error_message')}")
        time.sleep(8)
    raise TimeoutError(f"'{title}' did not complete within {timeout_s}s")


def download_video(item: dict, out_path: str) -> None:
    url = item.get("video_url")
    if not url:
        raise RuntimeError("Completed item has no video_url")
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    # video_url is a pre-signed files2.heygen.ai link — no auth header needed.
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done = 0
        with open(out, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
                done += len(chunk)
        print(f"  downloaded {done/1e6:.1f} MB -> {out}")


# --- orchestration ----------------------------------------------------------
def run(script_text: str, title: str, out_path: str, cfg: dict, headless: bool) -> None:
    # If a session bundle is given, replay its recorded browser env (UA/tz/locale)
    # unless explicitly overridden on the CLI — so the relocated session matches the
    # machine the cookies were exported from.
    sess = _read_session_bundle(cfg["cookies_file"]) if cfg.get("cookies_file") else {}
    user_agent = cfg.get("user_agent") or sess.get("user_agent")
    timezone_id = cfg.get("timezone_id") or sess.get("timezone_id")
    locale = cfg.get("locale") or sess.get("locale")

    ctx_kwargs = dict(
        user_data_dir=str(PROFILE_DIR),
        headless=headless,
        channel="chrome",   # use system Chrome — bundled Chromium lacks H.264,
                            # so HeyGen's avatar *preview* video fails to render
                            # there and the Generate button stays disabled.
        accept_downloads=True,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1440, "height": 900},
    )
    if cfg.get("proxy"):
        ctx_kwargs["proxy"] = {"server": cfg["proxy"]}
    if user_agent:
        ctx_kwargs["user_agent"] = user_agent
    if timezone_id:
        ctx_kwargs["timezone_id"] = timezone_id
    if locale:
        ctx_kwargs["locale"] = locale

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(**ctx_kwargs)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        # Cold residential SOCKS5 route loads the HeyGen SPA slower than the
        # 30s Playwright default, which made page.goto time out. Raise budget.
        page.set_default_navigation_timeout(90000)
        try:
            if cfg.get("cookies_file"):
                n = _load_cookies_from_file(ctx, cfg["cookies_file"])
                extra = " + replayed Mac env (UA/tz/locale)" if (user_agent or timezone_id or locale) else ""
                print(f"• loaded {n} HeyGen cookies from {cfg['cookies_file']}{extra}")
            elif cfg.get("chrome_cookies"):
                n = _load_chrome_cookies(ctx, cfg.get("chrome_browser", "chrome"),
                                         cfg.get("chrome_profile", "Default"))
                print(f"• loaded {n} HeyGen cookies from {cfg.get('chrome_browser','chrome')}/{cfg.get('chrome_profile','Default')}")
            page.goto(CREATE_URL, wait_until="domcontentloaded")

            _ensure_logged_in(page)   # with cookies this returns immediately
            _dismiss_promo(page)
            _drive(page, script_text, title, out_path, cfg)
        except Exception:
            try:
                page.screenshot(path="logs/heygen_error.png", full_page=False)
                print("• saved failure screenshot -> logs/heygen_error.png")
            except Exception:
                pass
            raise
        finally:
            ctx.close()


def _drive(page: Page, script_text: str, title: str, out_path: str, cfg: dict) -> None:
        print("• waiting for draft to finish loading")
        _wait_draft_ready(page)
        print("• configuring scene")
        _dismiss_promo(page)  # promo modals can appear after the draft loads
        if cfg["portrait"]:
            _set_portrait(page)
        _type_script(page, script_text)
        # Order matters: Motion Engine first (it survives an avatar swap), THEN the
        # avatar (which resets voice + delivery style), THEN auto-enhance last so its
        # emotion tags stick. This also avoids navigating back from the looks panel.
        _set_motion_engine(page, cfg["motion_engine"])
        if cfg["avatar"]:
            _select_avatar(page, cfg["avatar"], cfg.get("look_index", 0), cfg.get("look"))
        if cfg.get("background"):
            _set_background_color(page, cfg["background"])
        if cfg["auto_enhance"]:
            _auto_enhance(page)

        print("• submitting render")
        _submit_generate(page, title, cfg["fps"])

        print("• waiting for render to finish")
        item = wait_for_completion(page, title)

        print("• downloading")
        download_video(item, out_path)
        print(f"✓ done: {out_path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate + download a HeyGen avatar video via the web UI.")
    ap.add_argument("--script", help="path to a .txt file with the script")
    ap.add_argument("--title", help="video title (also used to find it when polling)")
    ap.add_argument("--out", help="output .mp4 path")
    ap.add_argument("--avatar", default=DEFAULTS["avatar"])
    ap.add_argument("--look-index", type=int, default=0,
                    help="which look of the avatar to use, 0-based (e.g. the owner's PC-desk look is 2)")
    ap.add_argument("--look", default=None,
                    help="look NAME from LOOKS (authority/pro/desk/hype/explainer/realtalk/fun/update/"
                         "lifestyle/casual/pro2) — selected by stable character_id, order-independent. "
                         "Preferred over --look-index.")
    ap.add_argument("--motion-engine", default=DEFAULTS["motion_engine"])
    ap.add_argument("--background", default=None,
                    help="avatar background: 'remove' (transparent alpha), a named color "
                         "(green/blue/magenta/white/black) or a hex '#RRGGBB'. For the the owner "
                         "avatar use 'magenta' for chroma keying — green clashes with the mic "
                         "LED and blue with the polo shirt. Default: leave original untouched.")
    ap.add_argument("--fps", default=DEFAULTS["fps"])
    ap.add_argument("--no-auto-enhance", action="store_true")
    ap.add_argument("--headless", action="store_true", help="run headless (works with --chrome-cookies / --cookies-file)")
    ap.add_argument("--chrome-cookies", action="store_true",
                    help="reuse your logged-in browser's HeyGen cookies instead of a manual login")
    ap.add_argument("--chrome-browser", default="chrome",
                    help="cookie source: chrome, brave, edge, chromium, firefox, safari, arc")
    ap.add_argument("--chrome-profile", default="Default",
                    help="browser profile holding the HeyGen login, e.g. 'Profile 1'")
    # headless-server path: export a session bundle on the Mac, inject it on the server
    ap.add_argument("--export-cookies", metavar="PATH",
                    help="MAC-SIDE: write live HeyGen cookies + browser env (UA/tz/locale) to PATH and exit; copy to server and use with --cookies-file")
    ap.add_argument("--cookies-file", metavar="PATH",
                    help="inject cookies from a JSON bundle exported via --export-cookies (for a headless server with no local browser)")
    ap.add_argument("--user-agent", help="override navigator.userAgent (match your Mac's Chrome); defaults to the bundle's value")
    ap.add_argument("--timezone-id", help="override timezone as an IANA name, e.g. Asia/Kolkata; defaults to the bundle's value")
    ap.add_argument("--locale", help="override locale, e.g. en-US; defaults to the bundle's value")
    # native server login via magic link (no cookie transfer needed)
    ap.add_argument("--login-request", action="store_true",
                    help="SERVER: open HeyGen login and email a magic link to --email")
    ap.add_argument("--login-complete", action="store_true",
                    help="SERVER: finish login by opening the magic --link in the saved profile")
    ap.add_argument("--email", help="email address for --login-request")
    ap.add_argument("--link", help="full magic-link URL for --login-complete")
    ap.add_argument("--proxy", help="route the browser via a proxy, e.g. socks5://127.0.0.1:1080 (server->home-IP reverse tunnel)")
    args = ap.parse_args()

    # Export mode: capture the Mac session and exit (no script/title/out needed).
    if args.export_cookies:
        export_session(args.export_cookies, args.chrome_browser, args.chrome_profile)
        return 0

    # Native server login (magic link) — no script/title/out needed.
    if args.login_request:
        if not args.email:
            ap.error("--login-request requires --email")
        login_request(args.email, headless=args.headless, proxy=args.proxy)
        return 0
    if args.login_complete:
        if not args.link:
            ap.error("--login-complete requires --link")
        login_complete(args.link, headless=args.headless, proxy=args.proxy)
        return 0

    missing = [n for n in ("script", "title", "out") if not getattr(args, n)]
    if missing:
        ap.error("required unless --export-cookies: " + ", ".join("--" + m for m in missing))

    cfg = dict(DEFAULTS)
    cfg.update(avatar=args.avatar, look_index=args.look_index, look=args.look,
               motion_engine=args.motion_engine, fps=args.fps, background=args.background,
               auto_enhance=not args.no_auto_enhance,
               chrome_cookies=args.chrome_cookies, chrome_browser=args.chrome_browser,
               chrome_profile=args.chrome_profile,
               cookies_file=args.cookies_file, proxy=args.proxy,
               user_agent=args.user_agent, timezone_id=args.timezone_id, locale=args.locale)

    script_text = Path(args.script).read_text(encoding="utf-8").strip()
    run(script_text, args.title, args.out, cfg, headless=args.headless)
    return 0


if __name__ == "__main__":
    sys.exit(main())
