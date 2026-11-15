# Lawatan Pengerusi FAMA – Pusat Jualan & Agropelancongan Harumanis Y.A (Remotion edit)

Vertical 1080×1920 / 30 fps short for TikTok & Instagram Reels, built with Remotion.
Footage: 10 Nov 2026, Kg. Baru Panggas, Chuping, Perlis (Drive folder "YA Harum manis").
The previous project (FAMA Pasar Tani Simpang 4) is kept in `archive/fama-simpang4/`.

## Story (≈57 s incl. closing) – the Pengerusi FAMA engaging with the pengusaha
1. **Hook** – the pengusaha's Harumanis gift; Pengerusi: "Kalau ikut tadi, kuning ni premium." (GRED PREMIUM)
2. Turun padang – orchard walk with the pengusaha
3. Listening to the pengusaha's briefing
4. Casual chat – "Cikgu, universiti apa?" … NUS … "sampai mereka pun mai buat kajian"
5. Pengusaha's thank-you speech, cutaway to the Pengerusi listening (DULU rangka → KINI agropelancongan)
6. Handshake over the RM195,000 Geran Naik Taraf cheque, natural applause
7. Laughing together over the visitors' book
8. Group photo – "Kita tunjuk agropelancongan kita. Satu, dua, tiga!" + end card
9. Abang Kerdee closing (logo animation)

## Closing
`public/closing/closing_abang_kerdee.mp4` (16:9 logo animation, 5 s) is appended by `src/Closing.tsx`:
scaled to 56 %, centred on the safe area, 8-frame cross-fade from the end card, soft whoosh + logo hit,
music carried through and faded out.

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
