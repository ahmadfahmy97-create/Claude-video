# Abang Kerdee – Remotion edits

Vertical 1080×1920 / 30 fps shorts for TikTok & Instagram Reels, built with Remotion.
Each video is a **project**:

| Project | Composition | Video |
|---|---|---|
| `fama-delegasi-indonesia` | `FamaDelegasiIndonesia` | Kunjungan hormat delegasi Pengusaha Muda Indonesia ke FAMA (19 Nov 2026) |
| `fama-simpang4` | `FamaSimpang4` | Lawatan FAMA – Pasar Tani Kekal Simpang 4, Perlis |

```
projects/<project>/edl.py          the edit (sentences, b-roll, graphics, SFX, punch-ins) + RAW/WORK dirs
projects/<project>/transcripts/    faster-whisper word timestamps per clip
src/projects/<project>/            timeline.json + faces.json (generated) and the composition config
public/footage/<project>/base.mp4  cut picture + cleaned voice (generated, not committed)
```

## Pipeline

1. `python3 scripts/transcribe.py <raw_dir> projects/<project>/transcripts` – faster-whisper (large-v3-turbo), word timestamps.
2. `projects/<project>/edl.py` – the edit, anchored to source-audio timestamps.
3. `python3 scripts/build.py <project>` – trims pauses, cuts footage + cleaned voice into `public/footage/<project>/base.mp4`,
   writes `src/projects/<project>/timeline.json` (captions, graphics, SFX, zooms, speech intervals).
4. `python3 scripts/faces.py <project>` – face detection (YuNet, `/home/user/models/yunet.onnx`) on the cut; moves captions/graphics
   off faces and anchors punch-in zooms on the main face.
5. Remotion (`src/`) – captions, motion graphics, music ducking, SFX, closing logo.

```bash
npm install
python3 scripts/build.py fama-delegasi-indonesia && python3 scripts/faces.py fama-delegasi-indonesia
npm run studio                                         # live preview
npm run preview -- FamaDelegasiIndonesia preview      # 720p preview -> out/FamaDelegasiIndonesia_preview.mp4
npm run render -- FamaDelegasiIndonesia final         # full-res final -> out/FamaDelegasiIndonesia_final.mp4
```

Raw footage and `public/footage/` are not committed (too large).

## Layout rules
- Safe area: x 60–940, y 230–1480 (TikTok + IG Reels UI clear).
- Captions & graphics never overlap the largest face on screen.
- Music sits ~-22 dB under speech and rises in gaps; final mix loudness-normalised to -14 LUFS.

## Assets
- SFX & music: Mixkit (free licence, commercial use, no attribution required).
- Fonts: Montserrat, Anton (SIL Open Font Licence), bundled in `public/fonts`.
- Flags are drawn as SVG (`src/GraphicsExtra.tsx`).
