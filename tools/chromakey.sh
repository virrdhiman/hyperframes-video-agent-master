#!/usr/bin/env bash
# PRJs runner | platform: mac | scope: repo-local
# ────────────────────────────────────────────────────────────────────────────
# chromakey.sh — green-screen MP4 → VP9 WebM with embedded alpha
#
# Usage:
#   ./tools/chromakey.sh <input.mp4> [output.webm]
#
# Examples:
#   ./tools/chromakey.sh public/ai_stylist/talking_head_safe.mp4
#   ./tools/chromakey.sh public/foo/raw.mp4 public/foo/foo_alpha.webm
#
# If output is omitted, writes alongside input as <name>_alpha.webm.
#
# Tunables (env vars, optional):
#   CK_KEY           hex green to key.       default: 0x00ff00
#   CK_SIMILARITY    chromakey similarity.   default: 0.12  (lower = tighter)
#   CK_BLEND         feathered edge blend.   default: 0.02
#   CK_DESPILL_MIX   green-spill removal.    default: 0.5   (raise for halo)
#   CK_CRF           VP9 perceptual quality. default: 22    (lower = larger/better)
#   CK_THREADS       encoder threads.        default: 8
#
# Why these defaults: see docs/guides/CHROMAKEY_TRANSPARENT_VIDEO.md
# ────────────────────────────────────────────────────────────────────────────
set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <input.mp4> [output.webm]" >&2
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "[ERROR] Input not found: $INPUT" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[ERROR] ffmpeg not on PATH. Install with: brew install ffmpeg" >&2
  exit 1
fi

# Derive default output: same dir, replace ext with _alpha.webm
if [ -z "$OUTPUT" ]; then
  base="${INPUT%.*}"
  OUTPUT="${base}_alpha.webm"
fi

# Tunables with defaults
KEY="${CK_KEY:-0x00ff00}"
SIM="${CK_SIMILARITY:-0.12}"
BLEND="${CK_BLEND:-0.02}"
DESPILL="${CK_DESPILL_MIX:-0.5}"
CRF="${CK_CRF:-22}"
THREADS="${CK_THREADS:-8}"

echo "[chromakey] $INPUT → $OUTPUT"
echo "  key=$KEY similarity=$SIM blend=$BLEND despill=$DESPILL crf=$CRF"

# Filter chain explained in CHROMAKEY_TRANSPARENT_VIDEO.md.
FILTER="chromakey=${KEY}:${SIM}:${BLEND},format=yuva420p,despill=type=green:mix=${DESPILL}:expand=0,format=yuva420p"

ffmpeg -y -i "$INPUT" \
  -vf "$FILTER" \
  -c:v libvpx-vp9 -pix_fmt yuva420p \
  -auto-alt-ref 0 -crf "$CRF" -b:v 0 \
  -deadline good -cpu-used 2 -row-mt 1 -threads "$THREADS" \
  -c:a libopus -b:a 96k \
  "$OUTPUT"

# Verify alpha was actually preserved.
if ! ffprobe -v error -show_entries stream_tags=ALPHA_MODE,alpha_mode \
    -of default "$OUTPUT" 2>/dev/null | grep -qi "alpha_mode=1"; then
  echo "[WARN] alpha_mode tag not found. The WebM may be opaque." >&2
  echo "       Check libvpx-vp9 build supports VP9 alpha (Homebrew ffmpeg does)." >&2
  exit 2
fi

echo "[chromakey] ✓ alpha-WebM ready: $OUTPUT"
echo "  Use in Remotion: <OffthreadVideo src={staticFile(\"…_alpha.webm\")} transparent />"
