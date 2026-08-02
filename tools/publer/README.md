# Publer

Publish & schedule finished renders to social channels via the [Publer API](https://publer.com/docs).

Take an `out/*.mp4` reel, upload it, and push it to a connected channel (Instagram
Reels, TikTok, YouTube Shorts, Pinterest, …) — either scheduled for later or live now.

**Script:** `tools/publer/publer.py`
**Auth:** Reads `PUBLER_API_KEY` (+ optional `PUBLER_WORKSPACE_ID`) from `.env` at the project root. Never hardcoded.
**Plan:** API access requires a Publer **Business** or **Enterprise** plan.

| | |
|---|---|
| Base URL | `https://app.publer.com/api/v1` |
| Auth headers | `Authorization: Bearer-API <key>` + `Publer-Workspace-Id: <id>` |
| Rate limit | 100 requests / 2-min window (per user) |
| Upload cap | 200 MB per direct file upload (use `--url` for larger, hosted files) |

If `PUBLER_WORKSPACE_ID` isn't set, the tool auto-resolves the first workspace and
tells you which one it used. Set it in `.env` to skip that extra request per call.

---

## Quick Start

```bash
cd tools/publer

# Who am I / which plan?
python3 publer.py whoami

# List workspaces and connected channels (grab the account id you want)
python3 publer.py workspaces
python3 publer.py accounts

# Upload a render → prints a media id
python3 publer.py upload ../../out/diogenes.mp4

# Publish immediately as a reel
python3 publer.py publish \
  --provider instagram --type reel \
  --accounts <account_id> \
  --media <media_id> \
  --text "Diogenes would hate your group chat 🪣" --wait

# …or schedule it
python3 publer.py schedule \
  --provider tiktok --type video \
  --accounts <account_id> --media <media_id> \
  --text "caption" --at 2026-06-10T09:00:00Z --wait
```

---

## Commands

| Command | What it does |
|---|---|
| `whoami` | Show the authenticated user (plan, email, default workspace) |
| `workspaces` | List all workspaces you can access |
| `accounts` | List connected social channels as a table (`--json` for raw) |
| `posts` | List posts — filter with `--state`, `--query`, `--account`, `--page` |
| `media` | List media-library items — filter with `--types photo\|video\|gif` |
| `upload <file>` | Direct-upload a local file (≤200 MB) → returns media id |
| `upload --url <U>` | Upload from a hosted URL (async → `job_id`; add `--wait` to poll) |
| `job <job_id>` | Check a job's status; `--wait` polls to completion |
| `schedule` | Schedule a post for a future time (`--at` required) |
| `publish` | Publish a post immediately |

Most commands print the raw JSON response, so you can pipe into `jq`.

### Post options (`schedule` / `publish`)

| Flag | Default | Notes |
|---|---|---|
| `--accounts` | required | One or more target account ids (space-separated) |
| `--provider` | `instagram` | `facebook`, `instagram`, `twitter`, `linkedin`, `pinterest`, `youtube`, `tiktok`, `threads`, `bluesky`, … |
| `--type` | `reel` | `status`, `photo`, `video`, `reel`, `story`, `carousel`, `poll`, … |
| `--text` | — | Caption / post body |
| `--media` | — | Uploaded media id(s) to attach (space-separated) |
| `--at` | — | ISO 8601 timestamp (required for `schedule`) e.g. `2026-06-10T09:00:00Z` |
| `--wait` | off | Poll the returned `job_id` until `completed`/`failed` |
| `--workspace` | env/first | Override the workspace id (global flag, before the subcommand) |

---

## Pipeline integration

This is the **last** step of the pipeline (after render) — distribution, not editing:

```
… → 9. Render → out/<file>.mp4 → 10. Publish:  publer.py upload + publish/schedule
```

Typical flow for a finished 9:16 short:

```bash
# 1. find the channel
python3 publer.py accounts                        # → copy the account id

# 2. upload the render (prints media id)
python3 publer.py upload ../../out/upi_explained.mp4

# 3. schedule the reel for a morning slot
python3 publer.py schedule \
  --provider instagram --type reel \
  --accounts 65607402db2797a3cbbdef67 \
  --media <media_id_from_step_2> \
  --text "How UPI actually works ⚡️ #fintech" \
  --at 2026-06-10T09:00:00Z --wait
```

The post call returns a `job_id`; `--wait` polls `/job_status/{job_id}` and reports
`completed` or `failed` (with a `payload.failures` map if a channel rejected it).

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `PUBLER_API_KEY not found` | Missing `.env` | Add `PUBLER_API_KEY=…` to `.env` at the project root |
| `403` / access denied | Plan without API access | Publer API needs Business/Enterprise |
| `429 Rate limit exceeded` | >100 reqs / 2 min | Wait and retry; the tool warns when <5 remain |
| `… exceeds 200 MB` on upload | File too big for direct upload | Host it and use `upload --url <hosted-url>` |
| Job stays `working` | Channel still processing | Re-run `job <id> --wait`, or check the Publer dashboard |
| Post `failed` | Per-channel validation | Inspect `payload.failures` in the job response for the reason |
```
