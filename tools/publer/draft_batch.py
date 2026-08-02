#!/usr/bin/env python3
"""
draft_batch.py — Create all 22 Pzynor March drafts in ONE fast burst.

Built for a short-lived Publer API key: it does the whole job in the fewest
possible calls so it fits inside a ~1-minute key window:
  1. fetch the March media ids (server-side search, a few calls) and cache them
     back into the batch file, then
  2. create every draft in a SINGLE bulk POST /posts/schedule (state=draft).

Each draft is fully populated — YouTube title, description, tags, the video
(by media id), and the intended scheduled_at — so you can open Publer, eyeball
each one, attach its thumbnail (public/pzynor/thumbs/<name>.jpg), and click
publish/schedule. Drafts persist even after the key expires.

Reads PUBLER_API_KEY + PUBLER_WORKSPACE_ID from the project-root .env.

Usage:
    python3 draft_batch.py --dry-run      # print the bulk payload, no API calls
    python3 draft_batch.py                # fetch media ids + create the 22 drafts
    python3 draft_batch.py --ids-only     # only resolve + cache media ids
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
BATCH_FILE = ROOT / "projects" / "pzynor" / "march_batch.json"
BASE = "https://app.publer.com/api/v1"
PZYNOR_ACCOUNT_ID = "69655d06260e24dee0b7b1b7"   # Pzynor (youtube)


def creds():
    # override=True so a mid-run key refresh in .env is picked up
    load_dotenv(ENV_FILE, override=True)
    key = os.getenv("PUBLER_API_KEY")
    ws = os.getenv("PUBLER_WORKSPACE_ID")
    if not key or not ws:
        sys.exit("[ERROR] PUBLER_API_KEY / PUBLER_WORKSPACE_ID missing in .env")
    return key, ws


def H(key, ws, json_body=True):
    h = {"Authorization": f"Bearer-API {key}", "Publer-Workspace-Id": ws}
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def call(method, path, *, params=None, body=None, tries=45, wait=4):
    """Resilient call — reloads .env each attempt so a mid-run key refresh is
    picked up, and retries through the short-lived-key 401 flicker + 429s.
    With the defaults it keeps trying for ~3 min, so you can refresh the key
    while the script is already running."""
    last = None
    for i in range(tries):
        key, ws = creds()  # re-read every attempt (key may have just been refreshed)
        r = requests.request(method, BASE + path, headers=H(key, ws, body is not None),
                             params=params, json=body, timeout=60)
        last = r
        if r.status_code in (401, 429):
            if i == 0 or i % 5 == 0:
                print(f"  [{r.status_code}] {path} — waiting for a valid key "
                      f"(refresh it in .env now; attempt {i+1}/{tries})", file=sys.stderr)
            time.sleep(wait)
            continue
        return r
    return last


def aslist(d, k):
    if isinstance(d, list):
        return d
    v = d.get(k, [])
    return v if isinstance(v, list) else []


def resolve_media_ids(batch):
    """Fill media_id for any entry missing one, via server-side search."""
    need = [e for e in batch if not e.get("media_id")]
    if not need:
        print(f"[ids] all {len(batch)} media ids already cached")
        return True
    print(f"[ids] resolving {len(need)} missing media id(s)…")
    found = {}
    page = 0
    while True:
        r = call("GET", "/media",
                 params=[("page", page), ("search", "output_2026-03"),
                         ("used[]", "true"), ("used[]", "false"), ("types[]", "video")])
        if not r.ok:
            print(f"[ERROR] /media {r.status_code}: {r.text[:120]}", file=sys.stderr)
            return False
        items = aslist(r.json(), "media")
        if not items:
            break
        for m in items:
            found[(m.get("name") or "").rsplit(".", 1)[0]] = m["id"]
        page += 1
        time.sleep(0.3)
    for e in batch:
        if not e.get("media_id"):
            e["media_id"] = found.get(e["name"])
    BATCH_FILE.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
    missing = [e["name"] for e in batch if not e.get("media_id")]
    print(f"[ids] resolved {len(batch)-len(missing)}/{len(batch)}; cached to {BATCH_FILE.name}")
    if missing:
        print(f"[ERROR] still missing ids: {missing}", file=sys.stderr)
        return False
    return True


def build_bulk(batch, state="draft"):
    posts = []
    for e in batch:
        posts.append({
            "networks": {
                "youtube": {
                    "type": "video",
                    "title": e["title"],
                    "text": e["description"],
                    "description": e["description"],
                    "media": [{"id": e["media_id"]}],
                }
            },
            "accounts": [{"id": PZYNOR_ACCOUNT_ID, "scheduled_at": e["scheduled_at"]}],
        })
    return {"bulk": {"state": state, "posts": posts}}


def main():
    ap = argparse.ArgumentParser(description="Create the 22 Pzynor March drafts in one burst")
    ap.add_argument("--dry-run", action="store_true", help="Print payload, no API calls")
    ap.add_argument("--ids-only", action="store_true", help="Only resolve + cache media ids")
    ap.add_argument("--state", default="draft", choices=["draft", "scheduled"],
                    help="Create as drafts (default) or directly scheduled")
    args = ap.parse_args()

    batch = json.loads(BATCH_FILE.read_text())

    if args.dry_run:
        # show payload using whatever ids are cached (may be null)
        payload = build_bulk(batch, args.state)
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:3000])
        print(f"\n[dry-run] {len(batch)} posts, state={args.state}; "
              f"{sum(1 for e in batch if e.get('media_id'))}/{len(batch)} have media ids")
        return

    if not resolve_media_ids(batch):
        sys.exit("[ERROR] could not resolve all media ids — fix the key and re-run")
    if args.ids_only:
        return

    payload = build_bulk(batch, args.state)
    print(f"[create] POST /posts/schedule — {len(batch)} {args.state} posts (one bulk call)…")
    r = call("POST", "/posts/schedule", body=payload)
    if not r.ok:
        sys.exit(f"[ERROR] create failed {r.status_code}: {r.text[:300]}")
    job = r.json().get("job_id")
    print(f"[create] submitted — job_id: {job}")
    # poll a couple times
    for _ in range(15):
        time.sleep(2)
        jr = call("GET", f"/job_status/{job}")
        st = jr.json().get("status") if jr.ok else None
        if st in ("completed", "failed"):
            print(f"[create] job {st}")
            print(json.dumps(jr.json(), indent=2)[:600])
            break
    print("\n[done] Open Publer → Drafts to review, attach thumbnails "
          "(public/pzynor/thumbs/<name>.jpg), and publish/schedule.")


if __name__ == "__main__":
    main()
