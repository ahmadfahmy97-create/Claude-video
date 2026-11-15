"""Transcribe every clip in a folder with word-level timestamps (faster-whisper).

Usage: python3 scripts/transcribe.py <raw_dir> <out_dir>
Writes <out_dir>/<clip>.json with segments + words, and <out_dir>/all.txt for reading.
"""
import json
import os
import subprocess
import sys

import numpy as np

from faster_whisper import WhisperModel

raw_dir, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)

clips = sorted(f for f in os.listdir(raw_dir) if f.upper().endswith(".MP4"))
lines = []
for clip in clips:
    name = os.path.splitext(clip)[0]
    out_json = os.path.join(out_dir, name + ".json")
    if not os.path.exists(out_json):
        wav = os.path.join(out_dir, name + ".wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(raw_dir, clip),
                        "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", "-acodec", "pcm_s16le", "-bitexact", "-map_metadata", "-1", wav], check=True)
        audio = np.fromfile(wav, dtype=np.int16, offset=44).astype(np.float32) / 32768.0
        segs, info = model.transcribe(
            audio, language="ms", word_timestamps=True, vad_filter=True, vad_parameters={"min_silence_duration_ms": 400, "speech_pad_ms": 300, "threshold": 0.35},
            beam_size=3, condition_on_previous_text=False,
            initial_prompt="Video TikTok bahasa Melayu santai, campur sikit English.")
        data = []
        for s in segs:
            data.append({
                "start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
                "words": [{"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3),
                           "p": round(w.probability, 3)} for w in (s.words or [])],
            })
        json.dump({"clip": name, "duration": info.duration, "segments": data},
                  open(out_json, "w"), ensure_ascii=False, indent=1)
        print("transcribed", name, flush=True)
    d = json.load(open(out_json))
    lines.append(f"\n===== {name} ({d['duration']:.1f}s) =====")
    for s in d["segments"]:
        lines.append(f"[{s['start']:7.2f}-{s['end']:7.2f}] {s['text']}")

open(os.path.join(out_dir, "all.txt"), "w").write("\n".join(lines))
