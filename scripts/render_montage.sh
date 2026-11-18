#!/usr/bin/env bash
# Render the 16:9 montage, then loudness-normalise to -16 LUFS (screen playback) without touching the picture.
# Usage: scripts/render_montage.sh preview|final
set -euo pipefail
cd "$(dirname "$0")/.."
mode=${1:-preview}
if [ "$mode" = final ]; then
  npx remotion render Montage out/_m_raw.mp4 --crf=16 --concurrency=4 --log=error
  dst=out/montage_final.mp4
else
  npx remotion render Montage out/_m_raw.mp4 --scale=0.6666666666666666 --crf=23 --concurrency=4 --log=error
  dst=out/montage_preview.mp4
fi
ffmpeg -v error -y -i out/_m_raw.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 256k -movflags +faststart "$dst"
rm -f out/_m_raw.mp4
echo "wrote $dst"
