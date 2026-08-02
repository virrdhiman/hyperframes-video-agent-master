#!/usr/bin/env bash
# Export PNG stills from AIStylistMain-v1 for tuning OUTFIT_SCENE6_BEATS / OUTFIT_PAN_X_MUL
# in src/AIStylistMain_v1.tsx. Requires: npx remotion (from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/public/ai_stylist/pan_debug"
mkdir -p "$OUT"
COMPOSITION="AIStylistMain-v1"
ENTRY="$ROOT/src/index.ts"

# Absolute timeline frames @ 30fps — scene 6 starts at 32.159s (see S.s6_outfits).
BASE=$(node -e "console.log(Math.round(32.159 * 30))")
frames=(
  $((BASE + 50))   # mid casual hold
  $((BASE + 115))  # mid pan to semi
  $((BASE + 160))  # semi hold
  $((BASE + 210))  # mid pan to formal
  $((BASE + 235))  # formal hold
)

for fr in "${frames[@]}"; do
  dest="$OUT/s6_frame_${fr}.png"
  echo "[still] frame=$fr -> $dest"
  cd "$ROOT" && npx remotion still "$ENTRY" "$COMPOSITION" --frame="$fr" --output="$dest"
done
echo "Done. Open $OUT and adjust OUTFIT_PAN_X_MUL / OUTFIT_SCENE6_BEATS if columns are off-center."
