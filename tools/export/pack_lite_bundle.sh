#!/usr/bin/env bash
# Builds a minimal copy of the repo for upload (subset of compositions + assets).
# Usage (from anywhere):  bash tools/export/pack_lite_bundle.sh
# Override output dir:      LITE_EXPORT_DIR=my-bundle bash tools/export/pack_lite_bundle.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
TARGET="${LITE_EXPORT_DIR:-lite-export}"
rm -rf "$TARGET"
mkdir -p "$TARGET"

cp package.json package-lock.json tsconfig.json remotion.config.ts eslint.config.mjs postcss.config.mjs tailwind.config.js .gitignore .prettierrc "$TARGET/" 2>/dev/null || true

mkdir -p "$TARGET/editing-styles"
cp *.md "$TARGET/" 2>/dev/null || true
cp editing-styles/*.md "$TARGET/editing-styles/" 2>/dev/null || true

cp -r tools "$TARGET/"

mkdir -p "$TARGET/src"
cp src/index.ts src/index.css "$TARGET/src/" 2>/dev/null || true

cp src/AtlassianMain_v1.tsx src/AtlassianMain_v2.tsx "$TARGET/src/" 2>/dev/null || true
cp src/Digit360Main_v2.tsx src/ShazamExplainedMain_v2.tsx "$TARGET/src/" 2>/dev/null || true

mkdir -p "$TARGET/src/components"
cp -r src/components/atlassian-v2 src/components/digit-360-v2 src/components/shazam-v2 src/components/shared-v2 "$TARGET/src/components/" 2>/dev/null || true
cp -r src/components/brand-autopsy "$TARGET/src/components/" 2>/dev/null || true

mkdir -p "$TARGET/projects/atlassian" "$TARGET/projects/shazam"
cp projects/atlassian/subtitles.json "$TARGET/projects/atlassian/" 2>/dev/null || true
cp projects/shazam/subtitles.json "$TARGET/projects/shazam/" 2>/dev/null || true
mkdir -p "$TARGET/projects/digit360"
cp projects/digit360/subtitles.json "$TARGET/projects/digit360/" 2>/dev/null || true

mkdir -p "$TARGET/public"
cp -r public/atlassian public/digit_360 public/shazam public/common public/stock "$TARGET/public/" 2>/dev/null || true
cp -r public/ai-taking-jobs "$TARGET/public/" 2>/dev/null || true

mkdir -p "$TARGET/raw_videos"
cp raw_videos/Atlassian.mp4 raw_videos/Digit_360_Meta.mp4 raw_videos/Shazam.mp4 "$TARGET/raw_videos/" 2>/dev/null || true

echo "Lite bundle written to $ROOT/$TARGET"
