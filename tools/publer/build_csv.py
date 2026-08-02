#!/usr/bin/env python3
"""
build_csv.py — Build a Publer bulk-import CSV for the 22 Pzynor March videos.

Publer's dashboard CSV import creates posts with NO API key — so this is the
robust path around the short-lived key. The only key-dependent step is grabbing
each video's public cdn.publer.com URL (one media fetch); after that the CSV is
written and you import it in the Publer UI:
    Publer → Create → Bulk → Import CSV → pick the Pzynor channel → upload.

The 22 videos are already in Publer's library, so their cdn URLs are reused
directly (no re-upload). Reloads .env every attempt, so you can refresh the
short-lived key while this is already running.

Output: projects/pzynor/publer_bulk.csv  (Publer's 12-column template)

Columns we fill: Date (IST), Text (description), Media URL (video), Title (YT title).
Date is written in IST (+05:30) because Publer schedules in the workspace timezone;
each row = the every-alternate-day slot from march_batch.json (19:00 UTC target).

Usage:
    python3 build_csv.py
"""

import csv
import datetime
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
CSV_FILE = ROOT / "projects" / "pzynor" / "publer_bulk.csv"
BASE = "https://app.publer.com/api/v1"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

# Publer's 12-column bulk template, in order.
COLUMNS = ["Date", "Text", "Link", "Media URL", "Title", "Label", "Alt text(s)",
           "Comment(s)", "Pin board, FB album, or Google category", "Post subtype",
           "CTA", "Reminder Column"]


def creds():
    load_dotenv(ENV_FILE, override=True)
    key, ws = os.getenv("PUBLER_API_KEY"), os.getenv("PUBLER_WORKSPACE_ID")
    if not key or not ws:
        sys.exit("[ERROR] PUBLER_API_KEY / PUBLER_WORKSPACE_ID missing in .env")
    return key, ws


def call(path, params, tries=240, wait=1.5):
    last = None
    for i in range(tries):
        key, ws = creds()
        h = {"Authorization": f"Bearer-API {key}", "Publer-Workspace-Id": ws}
        r = requests.get(BASE + path, headers=h, params=params, timeout=60)
        last = r
        if r.status_code in (401, 403, 429):
            if i % 5 == 0:
                print(f"  [{r.status_code}] waiting for a valid key — refresh it in .env "
                      f"(attempt {i+1}/{tries})", file=sys.stderr)
            time.sleep(wait)
            continue
        return r
    return last


def fetch_paths():
    """name -> public cdn url for the March videos."""
    out, page = {}, 0
    while True:
        r = call("/media", [("page", page), ("search", "output_2026-03"),
                            ("used[]", "true"), ("used[]", "false"), ("types[]", "video")])
        if not r.ok:
            sys.exit(f"[ERROR] /media {r.status_code}: {r.text[:160]}")
        items = r.json().get("media", []) if isinstance(r.json(), dict) else r.json()
        if not items:
            break
        for m in items:
            out[(m.get("name") or "").rsplit(".", 1)[0]] = {"id": m.get("id"), "path": m.get("path")}
        page += 1
        time.sleep(0.3)
    return out


def main():
    batch = json.loads(BATCH_FILE.read_text())
    print(f"[csv] fetching cdn URLs for {len(batch)} videos…")
    info = fetch_paths()

    rows, missing = [], []
    for e in batch:
        rec = info.get(e["name"], {})
        url = rec.get("path")
        if not url:
            missing.append(e["name"])
        # cache id + url back into the batch file
        e["media_id"] = e.get("media_id") or rec.get("id")
        e["media_url"] = url
        ist = datetime.datetime.strptime(e["scheduled_at"], "%Y-%m-%dT%H:%M:%SZ") \
            .replace(tzinfo=datetime.timezone.utc).astimezone(IST)
        row = {c: "" for c in COLUMNS}
        row["Date"] = ist.strftime("%Y/%m/%d %H:%M")
        row["Text"] = e["description"]
        row["Media URL"] = url or ""
        row["Title"] = e["title"]
        rows.append(row)

    BATCH_FILE.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    print(f"[csv] wrote {CSV_FILE}  ({len(rows)} rows)")
    print(f"[csv] media URLs resolved: {len(rows)-len(missing)}/{len(rows)}")
    if missing:
        print(f"[WARN] missing URLs (left blank): {missing}", file=sys.stderr)
    print("\n[next] Publer → Create → Bulk → Import CSV → choose the Pzynor channel → "
          "upload projects/pzynor/publer_bulk.csv → review → schedule.\n"
          "Dates are in IST (workspace timezone). Attach thumbnails from "
          "public/pzynor/thumbs/ during review.")


if __name__ == "__main__":
    main()
