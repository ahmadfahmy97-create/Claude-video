# Lawatan Pengerusi FAMA – Pusat Jualan & Agropelancongan Harumanis Y.A (Remotion edit)

Vertical 1080×1920 / 30 fps short for TikTok & Instagram Reels, built with Remotion.
Footage: 10 Nov 2026, Kg. Baru Panggas, Chuping, Perlis (Drive folder "YA Harum manis").
The previous project (FAMA Pasar Tani Simpang 4) is kept in `archive/fama-simpang4/`.

## Story (≈56 s)
1. **Hook** – owner: "Cuma ada rangka saja yang saya buat. Rangka tiang, rangka bumbung..."
2. **Payoff** – RM195,000 Geran Naik Taraf cheque, natural applause
3. Arrival montage – DULU rangka → KINI Pusat Agropelancongan, location card
4. Mango orchard
5. Group photo at the FAMA agrotourism sign – Pengerusi: "Kita tunjuk agropelancongan kita. Satu, dua, tiga!"
6. Owner's thank-you speech (b-roll of FAMA officials, cheque, slide)
7. Grant – TAHNIAH!
8. "Kalau ikut tadi, kuning ni premium."
9. Visitors' book
10. Group photo at the welcome banner + end card

## Pipeline

1. `scripts/transcribe.py <raw_dir> transcripts/turbo` – faster-whisper large-v3-turbo first pass.
   Speech clips were re-run with large-v3 (no VAD) into `transcripts/` – that is what build.py aligns to.
2. `scripts/edl.py` – the edit: sentences used, b-roll, motion graphics, SFX, punch-ins
   (all anchored to source-audio timestamps). `ambient=True` pieces keep natural sound (applause).
3. `scripts/build.py` – trims pauses, cuts footage + cleaned voice into `public/footage/base.mp4`
   and writes `src/timeline.json`.
4. `scripts/faces.py` – YuNet face detection; moves captions/graphics off faces, anchors zooms.
5. Remotion (`src/`) – captions, graphics, music ducking, SFX.

```bash
npm install
RAW_DIR=/home/user/raw python3 scripts/build.py && python3 scripts/faces.py
npm run studio        # live preview
npm run preview       # 2/3-res preview render -> out/preview.mp4
npm run render        # full-res final -> out/final.mp4
```

Raw clips are renamed to their 4-digit DJI number (`/home/user/raw/0565.MP4` …); raw footage and
`public/footage/` are not committed (too large).

## Layout rules
- Safe area: x 60–940, y 230–1480 (TikTok + IG Reels UI clear).
- Captions & graphics never overlap the largest face on screen.
- Music (m33, from 0:14) sits ~-24 dB under speech and opens up in montage / applause pieces.
- Output loudness-normalised to -14 LUFS.

## Assets
- SFX & music: Mixkit (free licence, commercial use, no attribution required).
- Fonts: Montserrat, Anton (SIL Open Font Licence), bundled in `public/fonts`.
