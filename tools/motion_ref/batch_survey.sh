#!/usr/bin/env bash
# PRJs runner | platform: mac | scope: repo-local
# Quick survey: generate standard grids for a downloaded reference video.
# Usage: ./tools/motion_ref/batch_survey.sh assets/inspo/motion-ref-Guufmu3rIx4/reference.mp4

set -euo pipefail
VIDEO="${1:?Usage: batch_survey.sh <video.mp4>}"
DIR="$(dirname "$VIDEO")/grids"
mkdir -p "$DIR"
PY="$(dirname "$0")/contact_grid.py"

echo "=== Level 1: full overview ==="
python3 "$PY" "$VIDEO" --rows 4 --cols 4 --out "$DIR/01_full_overview_4x4.jpg"

echo "=== Level 2: first 2 minutes ==="
python3 "$PY" "$VIDEO" --start 0 --end 120 --rows 4 --cols 4 --out "$DIR/02_first_2min_4x4.jpg"

echo "=== Level 2: intro 45s (3x3) ==="
python3 "$PY" "$VIDEO" --start 0 --end 45 --rows 3 --cols 3 --out "$DIR/03_intro_45s_3x3.jpg"

echo "Done. Open $DIR and pick timestamps for zoom grids:"
echo "  python3 tools/motion_ref/contact_grid.py \"$VIDEO\" --start T0 --end T1 --rows 4 --cols 4 --out \"$DIR/zoom_NAME_4x4.jpg\""
