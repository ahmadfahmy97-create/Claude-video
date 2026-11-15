# Claude-video – Remotion edits for TikTok & Instagram Reels

Vertical 1080×1920 / 30 fps shorts built with Remotion. Each video is a **project**:

| project | video |
|---|---|
| `simpang4` | Lawatan FAMA – Pasar Tani Kekal Simpang 4 |
| `libaturus` | Libat Urus & Perjumpaan Kumpulan Sasar FAMA Perlis – ucapan Pengerusi FAMA Malaysia (#FAMASantuni, KopieSatu) |

```
projects/<project>/edl.py          the edit (pieces, captions, b-roll, graphics, SFX, zooms)
projects/<project>/transcripts/    Whisper transcripts with word timings
src/data/<project>/timeline.json   generated: what Remotion plays
public/footage/<project>/base.mp4  generated: cut picture + cleaned voice (not committed)
```

## Pipeline

1. `scripts/transcribe.py <raw_dir> projects/<p>/transcripts` – faster-whisper (large-v3-turbo), word timestamps.
2. Write `projects/<p>/edl.py` from the transcript (hook first, repeats and awkward pauses left out).
3. `scripts/refine.py <p>` – re-transcribes only the ranges the EDL uses with large-v3 for tighter caption sync
   (falls back to the turbo model when large-v3 hallucinates).
4. `scripts/build.py <p>` – snaps cuts to quiet points, trims pauses, cuts footage + cleaned voice into
   `public/footage/<p>/base.mp4`, writes `src/data/<p>/timeline.json`.
5. `scripts/faces.py <p>` – face detection (YuNet); moves captions/graphics off faces, anchors punch-ins on the face.
6. Remotion (`src/`) – captions, motion graphics, music ducked under the voice, SFX.

```bash
npm install
python3 scripts/build.py libaturus && python3 scripts/faces.py libaturus
npm run studio                          # live preview (pick the composition)
scripts/render.sh libaturus preview     # 720p preview  -> out/libaturus_preview.mp4
scripts/render.sh libaturus final       # 1080p final   -> out/libaturus_final.mp4
```

Raw footage is not committed. Each EDL sets `RAW_DIR` (clips named by their 4-digit DJI number, e.g. `0561.MP4`).
The face model is expected at `/home/user/models/yunet.onnx` (OpenCV Zoo `face_detection_yunet_2023mar.onnx`).

## Layout rules
- Safe area: x 60–940, y 230–1480 (TikTok + IG Reels UI clear).
- Captions & graphics never overlap the largest face on screen.
- Music sits ~-22 dB under speech and rises in gaps; final mix normalised to -14 LUFS.

## Assets
- SFX & music: Mixkit (free licence, commercial use, no attribution required). `libaturus` uses "Raising Me Higher" (`m34.mp3`).
- Fonts: Montserrat, Anton (SIL Open Font Licence), bundled in `public/fonts`.
