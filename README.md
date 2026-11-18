# Lawatan FAMA – Pasar Tani Kekal Simpang 4 (Remotion edit)

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
- SFX & music: Mixkit (free licence, commercial use, no attribution required).
- Fonts: Montserrat, Anton (SIL Open Font Licence), bundled in `public/fonts`.

---

# Mengenali Pengerusi FAMA – 16:9 waiting-room montage (Remotion composition `Montage`)

1920×1080 / 25 fps, 2:00 incl. the 5 s closing logo. Built for lobby / waiting-area screens.

Footage: Drive folder "Video Raw CM" (Firstday CM ke FAMA, Shooting Simbol FAMA, MAHA, Media Tour MAHA,
Program Jualan Pertanian Melaka, Bidara Flour Mill, Majlis Watikah Sahabat Ilmuwan, FX3/Program Kecergasan).

```bash
python3 scripts/montage/list_drive.py <folderId> /home/user/work/cm_files.json   # list the shared folder
python3 scripts/montage/fetch.py        # download → 1080p25 H.264 mezzanine in /home/user/mezz (raw deleted)
python3 scripts/montage/transcribe.py   # faster-whisper word timestamps (finds the MC announcement)
python3 scripts/montage/faces.py        # YuNet face boxes per clip
python3 scripts/montage/sheets.py       # contact sheets for picking shots
python3 scripts/montage_edl.py          # the edit → src/montage/montage.json, copies used clips to public/mz
scripts/render_montage.sh preview       # 720p preview → out/montage_preview.mp4
scripts/render_montage.sh final         # 1080p final  → out/montage_final.mp4
```

Music: Mixkit #839 "Tears of Joy" (Happy / Uplifting / Folk Pop, 124 BPM), started 13.4 s in on a downbeat
so its own ending lands after the logo. Passing b-roll plays at 1.6× with 1–2 beat cuts.
Voice-over: the chairman's media statement at Pasar Tani Kekal Simpang 4, Perlis (FAMA CH › JAM-PTK PERLIS,
clip 0545) — six complete lines cut at word level, pauses tightened, cleaned and normalised (`public/vo/`).

Edit structure (every cut on the beat; every clip used once):
cold open on the chairman's portrait with the MC's arrival announcement as voice-over → title
"Mengenali Pengerusi FAMA" → name card → 01 Hari Pertama di FAMA → (drum drop) 02 MAHA 2026 →
03 Bersama Rakyat (Melaka) → 04 Memperkasa Industri (Bidara) → breakdown 05 Ilmu & Kesejahteraan →
final recap → "Selamat Datang ke FAMA" → closing logo.
