#!/usr/bin/env bash
# Render a composition, then loudness-normalise to -14 LUFS (TikTok / Reels) without touching the picture.
# Usage: scripts/render.sh <CompositionId> preview|final
set -euo pipefail
cd "$(dirname "$0")/.."
comp=${1:?composition id}
mode=${2:-preview}
mkdir -p out
if [ "$mode" = final ]; then
  npx remotion render "$comp" "out/_${comp}_final_raw.mp4" --crf=16 --concurrency=4 --log=error
  src="out/_${comp}_final_raw.mp4"; dst="out/${comp}_final.mp4"
else
  npx remotion render "$comp" "out/_${comp}_preview_raw.mp4" --scale=0.6666666666666666 --crf=24 --concurrency=4 --log=error
  src="out/_${comp}_preview_raw.mp4"; dst="out/${comp}_preview.mp4"
fi
ffmpeg -v error -y -i "$src" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 256k -movflags +faststart "$dst"
rm -f "$src"
echo "wrote $dst"
