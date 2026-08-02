#!/usr/bin/env python3
"""
publer.py — Publish & schedule short-form videos to social channels via the Publer API.

Publer is a social-media scheduling platform. This tool wraps the Publer API v3
(https://publer.com/docs) so you can take a finished render from out/ and push it
to connected channels (TikTok, Instagram Reels, YouTube Shorts, etc.) — either
scheduled for later or published immediately.

Reads PUBLER_API_KEY (and optionally PUBLER_WORKSPACE_ID) from the .env at the
project root. The key never gets hardcoded.

  Base URL : https://app.publer.com/api/v1
  Auth     : Authorization: Bearer-API <key>   +   Publer-Workspace-Id: <id>
  Access   : Business / Enterprise plans only
  Limits   : 100 requests / 2-min window; 200 MB per direct media upload

Usage:
    python3 publer.py whoami
    python3 publer.py workspaces
    python3 publer.py accounts
    python3 publer.py posts --state scheduled
    python3 publer.py upload out/my_reel.mp4
    python3 publer.py upload --url https://example.com/clip.mp4
    python3 publer.py job <job_id>
    python3 publer.py schedule --media <media_id> --accounts <acct_id> \
        --text "caption" --at 2026-06-10T09:00:00Z
    python3 publer.py publish --media <media_id> --accounts <acct_id> --text "caption"

Quick end-to-end (render → reel):
    python3 publer.py accounts                       # find the channel id
    python3 publer.py upload out/diogenes.mp4        # → prints media id
    python3 publer.py publish --media <id> --accounts <acct_id> \
        --type reel --text "Diogenes would hate your group chat 🪣"

Most commands print the raw JSON response so you can pipe into jq.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
BASE_URL = "https://app.publer.com/api/v1"

# Social providers Publer supports (for reference / validation in --provider).
PROVIDERS = [
    "facebook", "instagram", "twitter", "linkedin", "pinterest", "youtube",
    "tiktok", "google", "wordpress", "telegram", "mastodon", "threads", "bluesky",
]


# ── Auth ──────────────────────────────────────────────────────────────────────
def load_creds(workspace_override: str | None = None):
    load_dotenv(ENV_FILE)
    key = os.getenv("PUBLER_API_KEY")
    if not key:
        print(f"[ERROR] PUBLER_API_KEY not found in {ENV_FILE}", file=sys.stderr)
        sys.exit(1)
    workspace = workspace_override or os.getenv("PUBLER_WORKSPACE_ID")
    return key, workspace


def headers(key: str, workspace: str | None = None, json_body: bool = True) -> dict:
    h = {"Authorization": f"Bearer-API {key}"}
    if workspace:
        h["Publer-Workspace-Id"] = workspace
    if json_body:
        h["Content-Type"] = "application/json"
    return h


# ── HTTP helper ───────────────────────────────────────────────────────────────
def request(method: str, path: str, key: str, workspace: str | None = None,
            *, params=None, json_body=None, files=None, data=None):
    url = f"{BASE_URL}{path}"
    h = headers(key, workspace, json_body=files is None)
    try:
        resp = requests.request(
            method, url, headers=h, params=params, json=json_body,
            files=files, data=data, timeout=120,
        )
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    remaining = resp.headers.get("X-RateLimit-Remaining")
    if remaining is not None and int(remaining) < 5:
        print(f"[warn] Rate limit nearly exhausted ({remaining} left)", file=sys.stderr)

    if resp.status_code == 429:
        print("[ERROR] 429 Rate limit exceeded — retry later.", file=sys.stderr)
        sys.exit(1)
    if not resp.ok:
        print(f"[ERROR] {resp.status_code} {resp.reason}\n{resp.text}", file=sys.stderr)
        sys.exit(1)

    if not resp.text:
        return {}
    try:
        return resp.json()
    except ValueError:
        return {"raw": resp.text}


def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def resolve_workspace(key: str, workspace: str | None) -> str:
    """Return a workspace id — use the override/env, else the first workspace."""
    if workspace:
        return workspace
    spaces = request("GET", "/workspaces", key)
    items = spaces if isinstance(spaces, list) else spaces.get("workspaces", [])
    if not items:
        print("[ERROR] No workspaces found for this API key.", file=sys.stderr)
        sys.exit(1)
    wid = items[0].get("id") or items[0].get("_id")
    print(f"[publer] Using workspace: {items[0].get('name', wid)} ({wid})", file=sys.stderr)
    return wid


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_whoami(args):
    key, _ = load_creds(args.workspace)
    pretty(request("GET", "/users/me", key))


def cmd_workspaces(args):
    key, _ = load_creds(args.workspace)
    pretty(request("GET", "/workspaces", key))


def cmd_accounts(args):
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)
    data = request("GET", "/accounts", key, workspace)
    accounts = data if isinstance(data, list) else data.get("accounts", data)
    if args.json:
        pretty(accounts)
        return
    # Compact table — the common case is "which id do I post to?"
    rows = accounts if isinstance(accounts, list) else []
    print(f"\n{'ID':<28} {'PROVIDER':<12} {'TYPE':<12} NAME")
    print("-" * 80)
    for a in rows:
        aid = a.get("id") or a.get("_id", "")
        print(f"{str(aid):<28} {a.get('provider',''):<12} {a.get('type',''):<12} {a.get('name','')}")


def cmd_posts(args):
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)
    params = {"page": args.page}
    if args.state:
        params["state"] = args.state
    if args.query:
        params["query"] = args.query
    if args.account:
        params["account_ids[]"] = args.account
    pretty(request("GET", "/posts", key, workspace, params=params))


def fetch_media(key, workspace, types=None, page=0):
    """One page of media. The API requires used[] (true/false) or it returns []."""
    params = [("page", page), ("used[]", "true"), ("used[]", "false")]
    for t in (types or ["photo", "video", "gif"]):
        params.append(("types[]", t))
    return request("GET", "/media", key, workspace, params=params)


def cmd_media(args):
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)
    types = [args.types] if args.types else None

    if not args.all:
        pretty(fetch_media(key, workspace, types, args.page))
        return

    # Walk every page and collect the full set.
    items, page = [], 0
    while True:
        data = fetch_media(key, workspace, types, page)
        batch = data.get("media", []) if isinstance(data, dict) else data
        if not batch:
            break
        items.extend(batch)
        page += 1
    pretty({"media": items, "total": len(items)})


def cmd_upload(args):
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)

    if args.url:
        body = {
            "media": [{"url": args.url, "name": args.name or ""}],
            "type": "single",
            "direct_upload": True,
            "in_library": args.library,
        }
        print(f"[publer] Uploading from URL: {args.url}", file=sys.stderr)
        resp = request("POST", "/media/from-url", key, workspace, json_body=body)
        job_id = resp.get("job_id")
        if job_id and args.wait:
            resp = wait_for_job(key, workspace, job_id)
        pretty(resp)
        return

    path = Path(args.file).expanduser()
    if not path.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 200:
        print(f"[ERROR] {path.name} is {size_mb:.0f} MB — exceeds 200 MB direct-upload limit. "
              f"Use --url with a hosted file instead.", file=sys.stderr)
        sys.exit(1)

    print(f"[publer] Uploading {path.name} ({size_mb:.1f} MB)…", file=sys.stderr)
    with open(path, "rb") as f:
        files = {"file": (path.name, f)}
        data = {
            "direct_upload": "true",
            "in_library": "true" if args.library else "false",
        }
        resp = request("POST", "/media", key, workspace, files=files, data=data)
    mid = resp.get("id")
    if mid:
        print(f"[publer] Uploaded → media id: {mid}", file=sys.stderr)
    pretty(resp)


def cmd_job(args):
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)
    if args.wait:
        pretty(wait_for_job(key, workspace, args.job_id))
    else:
        pretty(request("GET", f"/job_status/{args.job_id}", key, workspace))


def wait_for_job(key, workspace, job_id, interval=2.0, timeout=300):
    """Poll /job_status until completed or failed."""
    print(f"[publer] Polling job {job_id}…", file=sys.stderr)
    waited = 0.0
    while waited < timeout:
        resp = request("GET", f"/job_status/{job_id}", key, workspace)
        status = resp.get("status")
        if status in ("completed", "failed"):
            print(f"[publer] Job {status}.", file=sys.stderr)
            return resp
        time.sleep(interval)
        waited += interval
    print(f"[publer] Timed out after {timeout}s waiting for job.", file=sys.stderr)
    return resp


def build_post_payload(args, state: str) -> dict:
    """Assemble the bulk-post body shared by schedule & publish."""
    networks = {
        args.provider: {
            "type": args.type,
            "text": args.text or "",
        }
    }
    if args.media:
        networks[args.provider]["media"] = [{"id": m} for m in args.media]

    accounts = []
    for acct in args.accounts:
        entry = {"id": acct}
        if args.at:
            entry["scheduled_at"] = args.at
        accounts.append(entry)

    return {
        "bulk": {
            "state": state,
            "posts": [{"networks": networks, "accounts": accounts}],
        }
    }


def cmd_schedule(args):
    if not args.at:
        print("[ERROR] --at <ISO timestamp> is required for scheduling.", file=sys.stderr)
        sys.exit(1)
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)
    body = build_post_payload(args, state="scheduled")
    resp = request("POST", "/posts/schedule", key, workspace, json_body=body)
    _finish_post(args, key, workspace, resp)


def cmd_publish(args):
    key, workspace = load_creds(args.workspace)
    workspace = resolve_workspace(key, workspace)
    body = build_post_payload(args, state="scheduled")
    resp = request("POST", "/posts/schedule/publish", key, workspace, json_body=body)
    _finish_post(args, key, workspace, resp)


def _finish_post(args, key, workspace, resp):
    job_id = resp.get("job_id")
    if job_id and args.wait:
        resp = wait_for_job(key, workspace, job_id)
    pretty(resp)


# ── CLI ───────────────────────────────────────────────────────────────────────
def build_parser():
    p = argparse.ArgumentParser(
        description="Publish & schedule videos to social channels via the Publer API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run a command with -h for its options. See tools/publer/README.md.",
    )
    p.add_argument("--workspace", help="Workspace id (default: PUBLER_WORKSPACE_ID or first workspace)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("whoami", help="Show the authenticated user").set_defaults(func=cmd_whoami)
    sub.add_parser("workspaces", help="List workspaces").set_defaults(func=cmd_workspaces)

    pa = sub.add_parser("accounts", help="List connected social accounts")
    pa.add_argument("--json", action="store_true", help="Raw JSON instead of a table")
    pa.set_defaults(func=cmd_accounts)

    pp = sub.add_parser("posts", help="List posts")
    pp.add_argument("--state", help="scheduled | published | draft | failed | recurring | …")
    pp.add_argument("--query", help="Full-text search")
    pp.add_argument("--account", help="Filter by account id")
    pp.add_argument("--page", type=int, default=0)
    pp.set_defaults(func=cmd_posts)

    pm = sub.add_parser("media", help="List media library items")
    pm.add_argument("--types", choices=["photo", "video", "gif"], help="Filter by media type")
    pm.add_argument("--page", type=int, default=0)
    pm.add_argument("--all", action="store_true", help="Walk every page (full library)")
    pm.set_defaults(func=cmd_media)

    pu = sub.add_parser("upload", help="Upload media (file or --url)")
    pu.add_argument("file", nargs="?", help="Local file to upload (≤200 MB)")
    pu.add_argument("--url", help="Upload from a hosted URL instead of a local file")
    pu.add_argument("--name", help="Optional display name")
    pu.add_argument("--library", action="store_true", help="Save into the media library")
    pu.add_argument("--wait", action="store_true", help="Poll job to completion (URL uploads)")
    pu.set_defaults(func=cmd_upload)

    pj = sub.add_parser("job", help="Check a job_id status")
    pj.add_argument("job_id")
    pj.add_argument("--wait", action="store_true", help="Poll until completed/failed")
    pj.set_defaults(func=cmd_job)

    common_post = argparse.ArgumentParser(add_help=False)
    common_post.add_argument("--accounts", nargs="+", required=True, help="One or more account ids")
    common_post.add_argument("--provider", default="instagram", choices=PROVIDERS,
                             help="Network key for the post (default: instagram)")
    common_post.add_argument("--type", default="reel",
                             help="Post type: status|photo|video|reel|story|carousel|… (default: reel)")
    common_post.add_argument("--text", help="Caption / post text")
    common_post.add_argument("--media", nargs="*", help="Uploaded media id(s) to attach")
    common_post.add_argument("--wait", action="store_true", help="Poll the job to completion")

    ps = sub.add_parser("schedule", parents=[common_post], help="Schedule a post for later")
    ps.add_argument("--at", required=True, help="ISO 8601 timestamp, e.g. 2026-06-10T09:00:00Z")
    ps.set_defaults(func=cmd_schedule)

    pb = sub.add_parser("publish", parents=[common_post], help="Publish a post immediately")
    pb.add_argument("--at", help=argparse.SUPPRESS)  # ignored for immediate publish
    pb.set_defaults(func=cmd_publish)

    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
