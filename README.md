# Lawatan Pengerusi FAMA – PPDK Anak Istimewa Perlis (Remotion edit)

_Previous edit (FAMA Pasar Tani Simpang 4) is in git history before this commit._

Vertical 1080×1920 / 30 fps short for TikTok & Instagram Reels, built with Remotion.

## Pipeline

1. `scripts/transcribe.py <raw_dir> transcripts` – faster-whisper (large-v3-turbo) with word timestamps.
2. `scripts/edl.py` – the edit: which sentences are used, b-roll, motion graphics, SFX and punch-ins
   (all anchored to source-audio timestamps).
3. `scripts/build.py` – trims pauses, cuts the footage + cleaned voice into `public/footage/base.mp4`
   and writes `src/timeline.json` (captions, graphics, SFX, zooms, speech intervals).
4. `scripts/faces.py` – face detection (YuNet) on the cut; moves captions/graphics off faces and
   anchors punch-in zooms on the main face.
5. Remotion (`src/`) – captions, graphics, music ducking, SFX.

```bash
npm install
python3 scripts/build.py && python3 scripts/faces.py
npm run studio        # live preview
npm run preview       # half-res preview render -> out/preview.mp4
npm run render        # full-res final -> out/final.mp4
```

Raw footage (`/home/user/raw/*.MP4`) and `public/footage/` are not committed (too large).

## Layout rules
- Safe area: x 60–940, y 230–1480 (TikTok + IG Reels UI clear).
- Captions & graphics never overlap the largest face on screen.
- Music sits ~-22 dB under speech and rises in gaps.

## Assets
- SFX & music: Mixkit (free licence, commercial use, no attribution required). Music: "The Long Road" (m709).
- Fonts: Montserrat, Anton (SIL Open Font Licence), bundled in `public/fonts`.
