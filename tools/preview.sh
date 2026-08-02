#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────────────────────
# preview.sh — render only a slice of a composition for fast iteration.
#
# Usage:
#   ./tools/preview.sh <COMP_ID> <START_SEC> <END_SEC> [output.mp4]
#
# Examples:
#   ./tools/preview.sh AIStylistMain-v1 19 32                 # scene 5 only
#   ./tools/preview.sh AIStylistMain-v1 44.3 55.8 /tmp/s8.mp4 # custom output
#
# Why: Studio is great for scrubbing, but a 60-second composition takes
# minutes to scrub through and the chromakey'd talking head doesn't preview
# pixel-accurately. Rendering just the scene you're working on is faster than
# Studio + matches what the final render will look like.
#
# Defaults:
#   - 30fps (overridable with FPS env var)
#   - --concurrency=4
#   - output → out/_preview_<COMP>.mp4 if not specified
# ────────────────────────────────────────────────────────────────────────────
set -euo pipefail

COMP="${1:-}"
START_SEC="${2:-}"
END_SEC="${3:-}"
OUT="${4:-}"
FPS="${FPS:-30}"

if [ -z "$COMP" ] || [ -z "$START_SEC" ] || [ -z "$END_SEC" ]; then
  echo "Usage: $0 <COMP_ID> <START_SEC> <END_SEC> [output.mp4]" >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  $0 AIStylistMain-v1 19 32" >&2
  exit 1
fi

# Compute frame range — bash arithmetic doesn't do floats, use awk.
START_FR=$(awk -v s="$START_SEC" -v f="$FPS" 'BEGIN{ printf "%d", s*f }')
END_FR=$(awk -v s="$END_SEC" -v f="$FPS" 'BEGIN{ printf "%d", s*f - 1 }')

if [ "$START_FR" -lt 0 ] || [ "$END_FR" -le "$START_FR" ]; then
  echo "[ERROR] invalid frame range: $START_FR-$END_FR" >&2
  exit 1
fi

if [ -z "$OUT" ]; then
  mkdir -p out
  OUT="out/_preview_${COMP}.mp4"
fi

DURATION=$(awk -v a="$START_SEC" -v b="$END_SEC" 'BEGIN{ printf "%.2f", b-a }')

echo "[preview] $COMP  ${START_SEC}s → ${END_SEC}s  (${DURATION}s, frames ${START_FR}-${END_FR})"
echo "[preview] → $OUT"

npx remotion render src/index.ts "$COMP" "$OUT" \
  --frames="${START_FR}-${END_FR}" \
  --concurrency=4

# Try to surface the output path nicely on macOS.
if command -v open >/dev/null 2>&1; then
  echo "[preview] opening…"
  open "$OUT" 2>/dev/null || true
fi

echo "[preview] ✓ done"
