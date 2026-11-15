"""Turn scripts/edl.py into:
  public/footage/base.mp4   – cut picture (A-roll + B-roll) with cleaned voice track
  src/timeline.json         – captions, graphics, sfx, zooms, speech intervals (output seconds)

Usage: python3 scripts/build.py [--skip-video]
"""
import difflib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from edl import PIECES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.environ.get("RAW_DIR", "/home/user/raw")
WORK = os.environ.get("WORK_DIR", "/home/user/work")
FPS = 30
SR = 48000
os.makedirs(WORK, exist_ok=True)
os.makedirs(f"{ROOT}/public/footage", exist_ok=True)
SKIP_VIDEO = "--skip-video" in sys.argv

# ------------------------------------------------------------------ audio helpers
_audio = {}


def audio(clip):
    if clip not in _audio:
        npy = f"{WORK}/{clip}_48k.npy"
        if not os.path.exists(npy):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{RAW}/{clip}.MP4", "-vn", "-ac", "1",
                                  "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
            np.save(npy, np.frombuffer(raw, dtype=np.float32))
        _audio[clip] = np.load(npy)
    return _audio[clip]


def band_db(x):
    """10 ms frame energy (dB) of the voice band (rough 200-3500 Hz via FFT mask)."""
    hop = SR // 100
    n = len(x) // hop
    if n == 0:
        return np.array([])
    fr = x[: n * hop].reshape(n, hop)
    spec = np.abs(np.fft.rfft(fr * np.hanning(hop), axis=1)) ** 2
    freqs = np.fft.rfftfreq(hop, 1 / SR)
    m = (freqs > 200) & (freqs < 3500)
    return 10 * np.log10(spec[:, m].sum(axis=1) + 1e-10)


def words_of(clip):
    d = json.load(open(f"{ROOT}/transcripts/{clip}.json"))
    return [w for s in d["segments"] for w in s["words"]]


def tighten_range(clip, a, b, keep_gap):
    """Split [a,b] into sub-ranges, removing silent runs longer than keep_gap+0.18s."""
    if keep_gap is None:
        return [(a, b)]
    x = audio(clip)[int(a * SR): int(b * SR)]
    db = band_db(x)
    if len(db) < 10:
        return [(a, b)]
    speech = np.percentile(db, 90)
    k = 5  # 50 ms median smoothing
    pad = np.pad(db, (k // 2, k // 2), mode="edge")
    sm = np.array([np.median(pad[i:i + k]) for i in range(len(db))])
    silent = sm < speech - 15
    # smooth: ignore tiny blips
    out, i, n = [], 0, len(silent)
    cuts = []
    while i < n:
        if silent[i]:
            j = i
            while j < n and silent[j]:
                j += 1
            dur = (j - i) / 100
            if dur >= keep_gap + 0.18 and i > 0 and j < n:
                s0 = a + i / 100 + keep_gap / 2
                s1 = a + j / 100 - keep_gap / 2
                cuts.append((s0, s1))
            i = j
        else:
            i += 1
    cur = a
    for s0, s1 in cuts:
        out.append((cur, s0))
        cur = s1
    out.append((cur, b))
    return [r for r in out if r[1] - r[0] > 0.05]


# ------------------------------------------------------------------ build the timeline
timeline_frames = 0
voice_parts = []
video_chunks = []  # (clip, src_in, nframes)
pieces_out = []

for p in PIECES:
    subs = []
    for (a, b) in p["ranges"]:
        subs += tighten_range(p["clip"], a, b, p.get("tighten"))
    # frame quantise
    mapped = []  # (src_a, src_b, out_frame_start, nframes)
    for (a, b) in subs:
        n = max(1, round((b - a) * FPS))
        mapped.append((a, a + n / FPS, timeline_frames, n))
        timeline_frames += n
    piece_start = mapped[0][2]
    piece_end = timeline_frames

    def to_out(t, mapped=mapped):
        for (a, b, f, n) in mapped:
            if t < a:
                return f / FPS
            if t <= b:
                return f / FPS + (t - a)
        last = mapped[-1]
        return (last[2] + last[3]) / FPS

    # ---- voice audio
    gain = p.get("voice_gain", 1.0)
    for (a, b, f, n) in mapped:
        seg = audio(p["clip"])[int(round(a * SR)): int(round(a * SR)) + int(round(n * SR / FPS))].copy()
        need = int(round(n * SR / FPS))
        if len(seg) < need:
            seg = np.pad(seg, (0, need - len(seg)))
        fade = int(0.008 * SR)
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        voice_parts.append((p["id"], seg, gain, p.get("ambient", False)))

    # ---- video schedule
    switches = sorted(p.get("broll", []))
    bounds = sorted(set([m[2] for m in mapped] + [piece_end] +
                        [min(max(round(to_out(s) * FPS), piece_start), piece_end) for (s, _, _) in switches]))
    for f0, f1 in zip(bounds[:-1], bounds[1:]):
        if f1 <= f0:
            continue
        active = None
        for (s, vc, vin) in switches:
            if round(to_out(s) * FPS) <= f0:
                active = (s, vc, vin)
        if active is None or active[1] is None:
            # speaker in sync
            for (a, b, f, n) in mapped:
                if f <= f0 < f + n:
                    video_chunks.append((p["clip"], a + (f0 - f) / FPS, f1 - f0))
                    break
        else:
            fs = round(to_out(active[0]) * FPS)
            video_chunks.append((active[1], active[2] + (f0 - fs) / FPS, f1 - f0))

    pieces_out.append(dict(p=p, mapped=mapped, to_out=to_out, start=piece_start, end=piece_end))

TOTAL = timeline_frames
print(f"total duration {TOTAL / FPS:.2f}s ({TOTAL} frames)")

# merge contiguous chunks
merged = []
for c in video_chunks:
    if merged and merged[-1][0] == c[0] and abs(merged[-1][1] + merged[-1][2] / FPS - c[1]) < 0.02:
        merged[-1] = (c[0], merged[-1][1], merged[-1][2] + c[2])
    else:
        merged.append(c)
video_chunks = merged
print(f"{len(video_chunks)} video chunks")

# ------------------------------------------------------------------ voice track
def norm_piece(x, ambient=False):
    db = band_db(x)
    if len(db) == 0:
        return x
    act = db > np.percentile(db, 60)
    hop = SR // 100
    frames = x[: len(db) * hop].reshape(len(db), hop)
    rms = np.sqrt((frames[act] ** 2).mean()) if act.any() else 1e-3
    target = 10 ** (-20 / 20)
    # speech is levelled to -20 dBFS; natural sound (applause, room tone) is only nudged
    return x * min(target / max(rms, 1e-4), 2.0 if ambient else 8.0)


by_piece = {}
for pid, seg, g, amb in voice_parts:
    by_piece.setdefault(pid, []).append((seg, g, amb))
voice = np.concatenate([norm_piece(np.concatenate([s for s, _, _ in v]), v[0][2]) * v[0][1] for pid, v in by_piece.items()])
raw_voice = f"{WORK}/voice_raw.f32"
voice.astype(np.float32).tofile(raw_voice)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw_voice,
                "-af", "highpass=f=85,afftdn=nf=-28:nr=10,equalizer=f=3200:t=q:w=1.2:g=2.5,"
                       "acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3,alimiter=limit=0.89",
                "-ar", str(SR), "-ac", "2", f"{WORK}/voice.wav"], check=True)

# ------------------------------------------------------------------ render picture
def render_chunk(i_c):
    i, (clip, src, n) = i_c
    out = f"{WORK}/chunk_{i:03d}.mp4"
    key = f"{clip}|{src:.4f}|{n}"
    if os.path.exists(out) and os.path.exists(out + ".key") and open(out + ".key").read() == key:
        return out
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src:.4f}", "-i", f"{RAW}/{clip}.MP4",
                    "-map", "0:v:0", "-an", "-vf",
                    "fps=30,scale=1080:1920:flags=lanczos,eq=contrast=1.04:saturation=1.10,format=yuv420p",
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast", "-crf", "15",
                    "-g", "30", "-threads", "2", out], check=True)
    open(out + ".key", "w").write(key)
    return out


if not SKIP_VIDEO:
    with ThreadPoolExecutor(3) as ex:
        files = list(ex.map(render_chunk, enumerate(video_chunks)))
    with open(f"{WORK}/concat.txt", "w") as f:
        for fn in files:
            f.write(f"file '{fn}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/concat.txt",
                    "-i", f"{WORK}/voice.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", f"{ROOT}/public/footage/base.mp4"], check=True)
    print("wrote public/footage/base.mp4")

# ------------------------------------------------------------------ captions
def norm_tok(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


caption_pages = []
speech = []
for po in pieces_out:
    p = po["p"]
    if not p.get("caption"):
        continue
    ws = [w for w in words_of(p["clip"])
          if any(a - 0.05 <= w["s"] and w["e"] <= b + 0.05 for (a, b) in p["ranges"])]
    drop = set(norm_tok(d) for d in p.get("drop_words", []))
    ws = [w for w in ws if norm_tok(w["w"]) not in drop]
    # merge whisper tokens that are glued pieces like "79" ".77", "sayur" "-sayuran"
    merged_w = []
    for w in ws:
        t = w["w"].strip()
        if merged_w and (t.startswith("-") or t.startswith(".") or t.startswith(",") or t == "%"):
            merged_w[-1] = dict(w=merged_w[-1]["w"] + t, s=merged_w[-1]["s"], e=w["e"])
        else:
            merged_w.append(dict(w=t, s=w["s"], e=w["e"]))
    ws = merged_w
    toks = p["caption"].split()
    A = [norm_tok(w["w"]) for w in ws]
    B = [norm_tok(t) for t in toks]
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    times = [None] * len(toks)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(j2 - j1):
                times[j1 + k] = (ws[i1 + k]["s"], ws[i1 + k]["e"])
        elif tag == "replace" or (tag == "insert" and i1 > 0):
            s0 = ws[i1]["s"] if i1 < len(ws) else ws[-1]["e"]
            e0 = ws[i2 - 1]["e"] if i2 > i1 else s0 + 0.25 * (j2 - j1)
            if tag == "insert":
                s0 = ws[i1 - 1]["e"]
                e0 = ws[i1]["s"] if i1 < len(ws) else s0 + 0.25 * (j2 - j1)
            step = (e0 - s0) / max(1, j2 - j1)
            for k in range(j2 - j1):
                times[j1 + k] = (s0 + k * step, s0 + (k + 1) * step)
    # fill any gaps
    for k in range(len(times)):
        if times[k] is None:
            prev = times[k - 1][1] if k > 0 and times[k - 1] else p["ranges"][0][0]
            times[k] = (prev, prev + 0.2)
    to_out = po["to_out"]
    words_out = []
    for t, (s, e) in zip(toks, times):
        so, eo = to_out(s), to_out(e)
        eo = max(eo, so + 0.08)
        words_out.append(dict(text=t, start=round(so, 3), end=round(eo, 3)))
    # monotonic
    for k in range(1, len(words_out)):
        if words_out[k]["start"] < words_out[k - 1]["start"]:
            words_out[k]["start"] = words_out[k - 1]["start"]
    # pages: up to 4 words / 24 chars, break after punctuation
    page = []
    for w in words_out:
        page.append(w)
        chars = sum(len(x["text"]) + 1 for x in page)
        if len(page) >= 4 or chars >= 22 or re.search(r"[.,!?]$", w["text"]):
            caption_pages.append(page)
            page = []
    if page:
        caption_pages.append(page)
    for w in words_out:
        speech.append([w["start"], w["end"]])

pages_out = []
for k, pg in enumerate(caption_pages):
    start = pg[0]["start"]
    end = pg[-1]["end"] + 0.25
    if k + 1 < len(caption_pages):
        end = min(end, caption_pages[k + 1][0]["start"])
    pages_out.append(dict(start=round(start, 3), end=round(end, 3), words=pg))

speech.sort()
speech_m = []
for s, e in speech:
    if speech_m and s - speech_m[-1][1] < 0.5:
        speech_m[-1][1] = max(speech_m[-1][1], e)
    else:
        speech_m.append([s, e])

# ------------------------------------------------------------------ events
gfx, sfx, zooms, pieces_meta = [], [], [], []
for po in pieces_out:
    p, to_out = po["p"], po["to_out"]
    pieces_meta.append(dict(id=p["id"], start=po["start"] / FPS, end=po["end"] / FPS, music=p.get("music", "under")))
    pg = []
    for (t, typ, props) in p.get("gfx", []):
        props = dict(props)
        if typ == "checklist":
            props["items"] = [[name, round(to_out(tt), 3)] for name, tt in props["items"]]
        g = dict(type=typ, start=round(to_out(t), 3), piece=p["id"], **props)
        # never spill into the next section
        spill = {"bigstat": 0.35, "stamp": 0.5, "sticker": 0.5}.get(typ, 0.0)  # let the big number breathe over the cut
        g["dur"] = round(min(g["dur"], po["end"] / FPS + spill - g["start"]), 3)
        pg.append(g)
    pg.sort(key=lambda g: g["start"])
    # a new box graphic replaces the previous one (a stamp may sit on top of a combo card)
    LAYER = ("heat", "flash", "tag", "nametag", "location", "sticker")  # these sit alongside a box graphic
    for a, b in zip(pg, pg[1:]):
        if a["type"] in LAYER or b["type"] in LAYER:
            continue
        if a["type"] == "combo" and b["type"] == "stamp":
            b["over"] = True
            continue
        if a["start"] + a["dur"] > b["start"]:
            a["dur"] = round(b["start"] - a["start"], 3)
    gfx += pg
    for (t, name, vol) in p.get("sfx", []):
        sfx.append(dict(name=name, start=round(to_out(t), 3), volume=vol))
    for (t, scale) in p.get("zoom", []):
        zooms.append(dict(start=round(to_out(t), 3), scale=scale, piece=p["id"]))
    # every piece starts unzoomed unless it says otherwise
    if not any(abs(to_out(t) - po["start"] / FPS) < 0.05 for (t, _) in p.get("zoom", [])):
        zooms.append(dict(start=po["start"] / FPS, scale=1.0, piece=p["id"]))

# hard-cut boundaries (for flash / whoosh alignment)
cuts = []
f = 0
for (clip, src, n) in video_chunks:
    if f > 0:
        cuts.append(round(f / FPS, 3))
    f += n

zooms.sort(key=lambda z: z["start"])
json.dump(dict(fps=FPS, durationInFrames=TOTAL, captions=pages_out, speech=speech_m, gfx=gfx, sfx=sfx,
               zooms=zooms, cuts=cuts, pieces=pieces_meta),
          open(f"{ROOT}/src/timeline.json", "w"), ensure_ascii=False, indent=1)
print("wrote src/timeline.json:", len(pages_out), "caption pages,", len(gfx), "graphics,", len(sfx), "sfx")
