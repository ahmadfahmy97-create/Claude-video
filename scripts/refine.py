"""Re-transcribe only the source ranges an EDL uses, with the slower large-v3 model, and replace the
word timings inside those ranges in projects/<project>/transcripts/<clip>.json (better caption sync).

Usage: python3 scripts/refine.py <project>
"""
import importlib.util
import json
import os
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = sys.argv[1]
PDIR = f"{ROOT}/projects/{PROJECT}"
spec = importlib.util.spec_from_file_location("edl", f"{PDIR}/edl.py")
edl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edl)
RAW = getattr(edl, "RAW_DIR", "/home/user/raw")
PAD = 1.0

model = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
fallback = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
HALLU = ("menonton", "terima kasih")


def words_in(m, x, s0, vad):
    segs, _ = m.transcribe(x, language="ms", word_timestamps=True, beam_size=5, condition_on_previous_text=False,
                           vad_filter=vad, initial_prompt="Ucapan Pengerusi FAMA Malaysia. FAMA, KopieSatu, santuni.")
    return [{"w": w.word, "s": round(s0 + w.start, 3), "e": round(s0 + w.end, 3), "p": round(w.probability, 3)}
            for s in segs for w in (s.words or [])]


def plausible(words, a, b):
    txt = " ".join(w["w"] for w in words).lower()
    return len(words) >= 1.2 * (b - a) and not any(h in txt for h in HALLU)


by_clip = {}
for p in edl.PIECES:
    if p.get("caption"):
        by_clip.setdefault(p["clip"], []).extend(p["ranges"])

for clip, ranges in by_clip.items():
    path = f"{PDIR}/transcripts/{clip}.json"
    d = json.load(open(path))
    done = d.setdefault("refined", [])
    for (a, b) in sorted(ranges):
        if any(abs(a - x) < 1e-3 and abs(b - y) < 1e-3 for x, y in done):
            continue
        s0 = max(0.0, a - PAD)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s0:.3f}", "-t", f"{b - s0 + PAD:.3f}", "-i", f"{RAW}/{clip}.MP4",
                              "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32)
        words = []
        for m, vad in ((model, False), (model, True), (fallback, True)):  # large-v3 sometimes hallucinates
            words = [w for w in words_in(m, x, s0, vad) if w["e"] > a - 0.05 and w["s"] < b + 0.05]
            if plausible(words, a, b):
                break
        if not plausible(words, a, b):
            print(f"{clip} {a:.2f}-{b:.2f}: no plausible re-transcription, keeping the original words")
            continue
        # drop the old words inside the range and splice in the new ones as their own segment
        for s in d["segments"]:
            s["words"] = [w for w in s["words"] if not (w["s"] >= a - 0.05 and w["e"] <= b + 0.05)]
        d["segments"].append({"start": a, "end": b, "text": " ".join(w["w"].strip() for w in words), "words": words})
        d["segments"].sort(key=lambda s: s["start"])
        done.append([a, b])
        print(f"{clip} {a:.2f}-{b:.2f}:", " ".join(w["w"].strip() for w in words), flush=True)
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)
