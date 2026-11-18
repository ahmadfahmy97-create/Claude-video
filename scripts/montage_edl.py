"""EDL for the 16:9 waiting-room montage "Mengenali Pengerusi FAMA" (v4, 2:00).

Builds src/montage/montage.json (shots, overlays, voice-over, SFX, music ducking) from the mezzanine
clips in /home/user/mezz (1080p25 H.264 made from the raw FX3/DJI files). Every cut sits on the beat
grid of the music (Mixkit #839 "Tears of Joy", 124 BPM, 2:00). Passing b-roll plays at 1.6x with 1-2 beat cuts.
Every clip is used once (no repeated scenes). Face boxes (YuNet, padded) decide Ken-Burns origins and
where text goes, so text never sits on a face. Used clips are copied to public/mz.

Voice-over: the chairman's own words from his media statement at Pasar Tani Kekal Simpang 4, Perlis
(10 Nov 2026, clip JAM-PTK 0545). Lines are cut at word level (faster-whisper timings in
/home/user/work/w0545.json): pauses tightened, false starts and repeats removed, then cleaned
(high-pass, denoise, presence EQ, compression) and loudness-normalised.

Usage: python3 scripts/montage_edl.py
"""
import importlib.util
import json
import os
import shutil
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZZ = os.environ.get("MEZZ", "/home/user/mezz")
FACES = os.environ.get("FACES", "/home/user/work/faces")
WORK = os.environ.get("WORK", "/home/user/work")
FPS = 25

MUSIC = "music/m839.mp3"  # Mixkit #839 "Tears of Joy" (Happy, Uplifting, Folk Pop), 124 BPM
MUSIC_OFFSET = 13.355  # start on a downbeat so the song's own ending lands after the closing logo
BEAT0, BEAT = 0.0, 0.48388  # video t=0 is a downbeat; beat length (s)
MUSIC_END = 117.6


def bt(n):
    return 0.0 if n == 0 else BEAT0 + n * BEAT


def F(t):
    return int(round(t * FPS))


ALIAS = {
    "BK": "Shooting_Simbol_FAMA__C6606", "BENCH": "Shooting_Simbol_FAMA__C6604",
    "READ": "Shooting_Simbol_FAMA__C6605", "LOOK": "Shooting_Simbol_FAMA__C6607",
    "SPEECH": "JAM_PTK__0545",
}


def clip(key):
    if key in ALIAS:
        return ALIAS[key]
    hits = [f[:-4] for f in os.listdir(MEZZ) if f.endswith(".mp4") and f[:-4].endswith(key)]
    if len(hits) != 1:
        raise KeyError(f"{key}: {hits}")
    return hits[0]


DUR = json.load(open(f"{WORK}/durations.json"))
DUR["JAM_PTK__0545.mp4"] = 413.5

# --------------------------------------------------------------------------------------------
# Voice-over script (source ranges in clip 0545) + clean display text
# --------------------------------------------------------------------------------------------
W0545 = json.load(open(f"{WORK}/w0545.json"))
VO = {
    "taskforce": ([(326.45, 334.85)],
                  "Di peringkat ibu pejabat FAMA, kami telah mengorak langkah. Bermula bulan pertama saya berada "
                  "di pejabat, kami telah mewujudkan satu task force."),
    "sales": ([(37.45, 50.55)],
              "Pada tahun ini, setakat bulan November ini, FAMA telah mengadakan Jualan Agro Madani yang telah "
              "mencatat nilai jualannya sebanyak RM79.77 juta."),
    "bajet": ([(71.28, 86.40)],
              "Pada tahun hadapan, FAMA dan juga beberapa agensi telah diberikan satu angka yang agak besar juga, "
              "iaitu 5,000 aktiviti Jualan Agro Madani yang kita akan buat bagi tahun 2027."),
    "usahawan": ([(92.85, 98.10), (103.70, 110.05)],
                 "Kita telah melibatkan 39,841 usahawan, dengan nilai penjimatan sebanyak RM25.36 juta."),
    "sara": ([(243.00, 259.65)],
             "Bermula 1 Januari, FAMA sebagai salah satu agensi yang menyelia Jualan Agro Madani, SARA itu sendiri "
             "boleh digunakan pembeliannya di Jualan Agro Madani. Dia bukan sahaja memberi keuntungan kepada pengguna, "
             "tapi kepada juga pengeluar dan usahawan."),
    "bekalan": ([(370.20, 377.60)],
                "Bagi pihak FAMA, kami dah bersedia untuk penyediaan bekalan makanan sekurang-kurangnya tiga bulan."),
}
GAP_MAX, GAP_KEEP, PAD = 0.32, 0.16, 0.06


def tighten(ranges):
    """Split each range at word gaps longer than GAP_MAX so long pauses shrink to ~GAP_KEEP."""
    out = []
    for a, b in ranges:
        ws = [w for w in W0545 if a - 0.05 <= w["s"] < b]
        cur = a
        for w0, w1 in zip(ws, ws[1:]):
            if w1["s"] - w0["e"] > GAP_MAX:
                out.append((cur, w0["e"] + PAD))
                cur = w1["s"] - PAD
        out.append((cur, b))
    return [(round(x, 3), round(y, 3)) for x, y in out if y - x > 0.05]


def build_vo(key):
    """Cut, join, clean and normalise one VO line -> public/vo/<key>.m4a; returns (path, length, words)."""
    ranges, text = VO[key]
    parts = tighten(ranges)
    src = f"{MEZZ}/{clip('SPEECH')}.mp4"
    fc, labels = [], []
    for i, (a, b) in enumerate(parts):
        d = b - a
        fc.append(f"[0:a]atrim={a}:{b},asetpts=N/SR/TB,afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.015):.3f}:d=0.015[p{i}]")
        labels.append(f"[p{i}]")
    fc.append("".join(labels) + f"concat=n={len(parts)}:v=0:a=1[cat]")
    fc.append("[cat]highpass=f=90,afftdn=nr=10:nf=-40,equalizer=f=280:t=q:w=1.2:g=-2.5,"
              "equalizer=f=3200:t=q:w=1.0:g=3.5,equalizer=f=9000:t=h:w=1:g=1.5,"
              "acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3,"
              "loudnorm=I=-15:TP=-1.5:LRA=6[o]")
    os.makedirs(f"{ROOT}/public/vo", exist_ok=True)
    out = f"{ROOT}/public/vo/{key}.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(fc), "-map", "[o]",
                    "-ac", "2", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", out], check=True)
    length = sum(b - a for a, b in parts)
    # map spoken word starts onto the joined timeline
    starts, acc = [], 0.0
    for a, b in parts:
        starts += [acc + (w["s"] - a) for w in W0545 if a - 0.02 <= w["s"] < b - 0.05]
        acc += b - a
    disp = text.split()
    words = []
    for i, w in enumerate(disp):
        j = min(len(starts) - 1, int(round(i * (len(starts) - 1) / max(1, len(disp) - 1))))
        words.append(dict(w=w, s=round(max(0.0, starts[j]), 2)))
    return f"vo/{key}.m4a", length, words, parts


def find_word(key, prefix):
    """Joined-timeline time of the first spoken word starting with prefix in a VO line."""
    acc = 0.0
    for a, b in tighten(VO[key][0]):
        for w in W0545:
            if a - 0.02 <= w["s"] < b - 0.05 and w["w"].startswith(prefix):
                return acc + w["s"] - a
        acc += b - a
    raise KeyError(prefix)


# --------------------------------------------------------------------------------------------
# Shot list in beats (one beat = 0.469 s). Strings mark section starts.
# --------------------------------------------------------------------------------------------
edit = [  # (clip, in-point s, beats, speed)
    "OPEN", ("BK", 1.0, 6, 1), ("BENCH", 4.0, 4, 1), ("READ", 9.0, 8, 1),
    "TITLE", ("LOOK", 13.0, 10, 1),
    "NAME", ("C5636", 2.5, 10, 1),
    "DAY1", ("C5613", 9.0, 3, 1), ("C5617", 1.5, 3, 1), ("C5622", 1.5, 3, 1), ("C5626", 1.0, 3, 1), ("C5630", 0.3, 3, 1),
    ("C5627", 1.0, 3, 1),
    "MAHA", ("C7204", 2.0, 2, 1.6), ("C6706", 5.0, 2, 1.6), ("C6686", 3.0, 2, 1.6), ("C6624", 1.5, 2, 1.6),
    ("C6651", 4.0, 2, 1.6), ("C6660", 3.0, 2, 1.6), ("C6714", 3.0, 2, 1.6), ("C6720", 5.0, 2, 1.6), ("C7213", 0.5, 2, 1.6),
    ("C7230", 2.0, 2, 1.6), ("C7252", 8.0, 2, 1.6), ("C7256", 2.0, 2, 1.6), ("C6635", 2.0, 2, 1.6), ("C7222", 1.0, 2, 1.6),
    ("C6630", 4.0, 2, 1.6),
    "MELAKA", ("C0447", 2.0, 2, 1.6), ("C0408", 1.0, 2, 1.6), ("C0410", 1.5, 2, 1.6), ("C0431", 3.0, 2, 1.6),
    ("C0443", 2.0, 2, 1.6), ("C0450", 0.5, 2, 1.6), ("C0437", 1.0, 2, 1.6), ("C0454", 0.5, 2, 1.6), ("C0456", 0.5, 2, 1.6),
    ("C0414", 2.0, 2, 1.6), ("C0657", 0.5, 2, 1.6), ("C6662", 2.0, 2, 1.6), ("C6655", 1.0, 2, 1.6), ("C6683", 2.0, 2, 1.6),
    ("C7253", 0.5, 2, 1.6), ("C7259", 2.0, 2, 1.6), ("C6676", 10.0, 2, 1.6), ("C7261", 1.0, 2, 1.6), ("C6685", 2.0, 2, 1.6),
    ("C6664", 0.5, 2, 1.6), ("C6668", 0.5, 2, 1.6), ("C6672", 1.0, 2, 1.6), ("C6729", 1.0, 2, 1.6), ("C0428", 0.5, 2, 1.6),
    ("C0441", 0.5, 2, 1.6), ("C6644", 0.5, 2, 1.6), ("C6649", 0.5, 2, 1.6), ("C6653", 0.5, 2, 1.6), ("C6658", 2.0, 2, 1.6),
    ("C6674", 0.5, 2, 1.6), ("C6680", 0.3, 2, 1.6),
    "TALK", ("SPEECH", None, 16, 1),
    "TALK_BROLL", ("C0448", 0.5, 2, 1.6), ("C7255", 1.0, 2, 1.6), ("C7217", 1.0, 2, 1.6), ("C6719", 8.0, 2, 1.6),
    ("C6701", 0.5, 2, 1.6), ("C7205", 2.0, 2, 1.6), ("C6716", 1.0, 2, 1.6), ("C6727", 0.5, 2, 1.6), ("C7214", 0.5, 2, 1.6),
    "BIDARA", ("C9661", 1.0, 2, 1.6), ("C9680", 2.0, 2, 1.6), ("C9682", 0.5, 2, 1.6), ("C9695", 2.0, 2, 1.6),
    ("C9692", 0.3, 2, 1.6), ("C9703", 2.0, 2, 1.6), ("C9694", 0.3, 2, 1.6), ("C9691", 6.0, 2, 1.6), ("C9664", 0.5, 2, 1.6),
    ("C9697", 1.0, 2, 1.6),
    "WARGA", ("0035_D", 0.5, 2, 1.6), ("0019_D", 1.0, 1, 1.6), ("0045_D", 0.0, 1, 1.6), ("0027_D", 1.0, 1, 1.6),
    ("0024_D", 1.0, 1, 1.6), ("C6262", 4.0, 2, 1.6), ("C6356", 1.0, 1, 1.6), ("C6380", 0.5, 1, 1.6), ("C6449", 1.0, 1, 1.6),
    ("C6441", 0.5, 1, 1.6), ("C6327", 1.0, 2, 1.6),
    "RECAP", ("C5629", 0.3, 2, 1.6), ("C7248", 1.0, 1, 1.6), ("C5620", 1.0, 1, 1.6), ("C7240", 1.0, 1, 1.6),
    ("C6703", 1.0, 1, 1.6), ("C5621", 0.5, 1, 1.6), ("C6713", 2.0, 1, 1.6), ("C7206", 1.0, 1, 1.6), ("C6616", 1.0, 2, 1.6),
    ("C5619", 1.0, 1, 1.6), ("C5628", 0.5, 1, 1.6),
    "END", ("C6438", 12.0, 0, 1),  # held to MAIN_END under the end title
]

vo_files = {k: build_vo(k) for k in VO}
SARA_SRC_IN = vo_files["sara"][3][0][0]  # talk shot starts where the SARA line starts

shots, marks = [], {}
n = 0
for item in edit:
    if isinstance(item, str):
        marks[item] = n
        continue
    key, tin, nb, sp = item
    c = clip(key)
    t0 = bt(n)
    t1 = bt(n + nb) if nb else MUSIC_END - 2.0
    kind = "talk" if key == "SPEECH" else None
    if kind:
        tin = SARA_SRC_IN - 0.5
    tin = max(0.0, min(tin, DUR[c + ".mp4"] - (t1 - t0) * sp - 0.05))
    early = n < marks.get("MAHA", 10 ** 6)
    shots.append(dict(src=c + ".mp4", t0=t0, t1=t1, **{"in": round(tin, 2)}, vol=0.0, kind=kind, speed=sp,
                      fadeIn=8 if early and n > 0 else (10 if kind else 0),
                      z=(1.0, 1.07) if early else ((1.04, 1.1) if (n // 4) % 2 == 0 else (1.1, 1.04))))
    n += nb
MAIN_END = shots[-1]["t1"]
T = {k: bt(v) for k, v in marks.items()}

srcs = [s["src"] for s in shots]
assert len(srcs) == len(set(srcs)), {s for s in srcs if srcs.count(s) > 1}

# --------------------------------------------------------------------------------------------
# Faces → Ken Burns origin + free regions for text
# --------------------------------------------------------------------------------------------
spec = importlib.util.spec_from_file_location("faces", f"{WORK}/faces.py")
fmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fmod)

for s in shots:
    if s["kind"] == "talk":
        s["faces"], s["ox"], s["oy"] = [[1180, 200, 380, 420]], 0.5, 0.4
        continue
    c = s["src"][:-4]
    if not os.path.exists(f"{FACES}/{c}.json"):
        fmod.run(c + ".mp4")
    a, b = s["in"], s["in"] + (s["t1"] - s["t0"]) * s["speed"]
    boxes = [bx for f in json.load(open(f"{FACES}/{c}.json")) if a - 0.2 <= f["t"] <= b + 0.2 for bx in f["b"]]
    s["faces"] = boxes
    if boxes:
        big = sorted(boxes, key=lambda q: -q[2] * q[3])[: max(1, len(boxes) // 3)]
        s["ox"] = round(min(0.8, max(0.2, float(np.mean([q[0] + q[2] / 2 for q in big])) / 1920)), 3)
        s["oy"] = round(min(0.7, max(0.2, float(np.mean([q[1] + q[3] / 2 for q in big])) / 1080)), 3)
    else:
        s["ox"], s["oy"] = 0.5, 0.45


def faces_hi(c, a, b):
    """Sensitive pass (threshold 0.45, 5 fps, full width) for placement decisions; cached."""
    import cv2
    os.makedirs(f"{FACES}_hi", exist_ok=True)
    p = f"{FACES}_hi/{c}.json"
    if not os.path.exists(p):
        W, H = 1280, 720
        det = cv2.FaceDetectorYN.create(f"{os.path.dirname(MEZZ)}/models/yunet.onnx", "", (W, H), 0.45)
        pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{MEZZ}/{c}.mp4", "-vf", f"fps=5,scale={W}:{H}", "-f", "rawvideo",
                               "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
        res, k = [], 0
        while True:
            buf = pr.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            _, f = det.detect(np.frombuffer(buf, np.uint8).reshape(H, W, 3))
            res.append({"t": round(k / 5, 2), "b": [[round(float(v) * 1.5) for v in r[:4]] for r in (f if f is not None else [])
                                                    if r[2] * r[3] * 2.25 > 1500]})
            k += 1
        json.dump(res, open(p, "w"))
    return [bx for f in json.load(open(p)) if a - 0.2 <= f["t"] <= b + 0.2 for bx in f["b"]]


def boxes_in(t0, t1):
    out = []
    for s in shots:
        if s["t1"] > t0 and s["t0"] < t1:
            out += s["faces"]
            if s["kind"] != "talk":
                # source window actually on screen during [t0, t1]
                a = s["in"] + max(0, t0 - s["t0"]) * s["speed"]
                b = s["in"] + (min(s["t1"], t1) - s["t0"]) * s["speed"]
                out += faces_hi(s["src"][:-4], a, b)
    return out


def overlap(boxes, rect):
    x0, y0, x1, y1 = rect
    tot = 0
    for x, y, w, h, *_ in boxes:
        x, y, w, h = x - 0.4 * w, y - 0.4 * h, w * 1.8, h * 1.8  # padded face
        tot += max(0, min(x + w, x1) - max(x, x0)) * max(0, min(y + h, y1) - max(y, y0))
    return tot


def pick(t0, t1, options):
    b = boxes_in(t0, t1)
    return min(options, key=lambda k: overlap(b, options[k]) + list(options).index(k) * 1e-3)


overlays, vo_tracks, ducks, sfx = [], [], [], []


def ov(t0, t1, **g):
    overlays.append(dict(from_=F(t0), dur=F(t1) - F(t0), **g))


def fx(name, tt, vol):
    sfx.append(dict(name=name, at=max(0, F(tt)), volume=vol))


SUB_OPTS = {"bottom": (200, 860, 1720, 1060), "top": (200, 20, 1720, 220)}


def subs(at, words, length, split_at=None):
    """Karaoke subtitles in chunks of ~2 lines so long lines stay readable."""
    chunks, cur = [], []
    for w in words:
        if split_at and cur and cur[-1]["s"] < split_at - at <= w["s"]:
            chunks.append(cur)
            cur = []
        cur.append(w)
        if len(" ".join(x["w"] for x in cur)) > 95 or w["w"].endswith((".", "?")) and len(cur) > 6:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    for i, ch in enumerate(chunks):
        c0 = ch[0]["s"]
        c1 = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else length + 0.35
        a0, a1 = at + c0, at + c1
        if split_at and a0 < split_at < a1:
            a1 = split_at
        if a1 - a0 < 0.6 and overlays and overlays[-1]["type"] == "sub":
            # too short to read on its own: extend the previous chunk instead
            prev = overlays[-1]
            prev["words"] += [dict(w=x["w"], s=round(x["s"] - c0 + (F(a0) - prev["from_"]) / FPS, 2)) for x in ch]
            prev["dur"] = F(a1) - prev["from_"]
            continue
        pos = "talk" if split_at and a0 < split_at else None
        if pos is None:
            pos = pick(a0, a1, SUB_OPTS)
        ov(a0, a1, type="sub", pos=pos, words=[dict(w=x["w"], s=round(x["s"] - c0, 2)) for x in ch])


def voice(key, at, split_at=None):
    path, length, words, _ = vo_files[key]
    vo_tracks.append(dict(src=path, at=F(at), **{"in": 0}, dur=F(length) + 2, volume=1.0))
    subs(at, words, length, split_at)
    ducks.append([F(at) - 3, F(at + length)])
    return at + length


def chapter(t0, t1, num, title, sub, top_only=True):
    opts = {"tl": (60, 60, 900, 360), "tr": (1020, 60, 1860, 360), "bl": (60, 760, 900, 1040), "br": (1020, 760, 1860, 1040)}
    if top_only:  # subtitles run along the bottom
        opts = {k: v for k, v in opts.items() if k[0] == "t"}
    k = pick(t0, t1, opts)
    ov(t0 + 0.15, t1, type="chapter", side="right" if k[1] == "r" else "left", pos="bottom" if k[0] == "b" else "top",
       num=num, title=title, sub=sub)


def stat(t0, t1, value, label, sub):
    opts = {"right-low": (1100, 520, 1840, 840), "left-low": (80, 520, 820, 840),
            "right": (1100, 330, 1840, 700), "left": (80, 330, 820, 700),
            "right-top": (1100, 120, 1840, 480), "left-top": (80, 120, 820, 480)}
    ov(t0, t1, type="stat", side=pick(t0, t1, opts), value=value, label=label, sub=sub)


# ---- cold open: MC announces his arrival ----
mc_words = [("Mengumumkan", 0.0), ("ketibaan", 0.88), ("Yang", 1.58), ("Berusaha", 1.86), ("Tuan", 2.38),
            ("Haji", 2.72), ("Abang", 3.0), ("Ahmad", 3.26), ("Kerdee", 3.6), ("bin", 4.16), ("Abang", 4.36),
            ("Masagus,", 4.66), ("Pengerusi", 5.64), ("FAMA", 6.04)]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", "6.5", "-i", f"{MEZZ}/{clip('0013_D')}.mp4", "-vn",
                "-af", "highpass=f=90,afftdn=nr=8,equalizer=f=3000:t=q:w=1:g=2,loudnorm=I=-15:TP=-1.5:LRA=6",
                "-ac", "2", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", f"{ROOT}/public/vo/mc.m4a"], check=True)
MC_AT = 1.2
vo_tracks.append(dict(src="vo/mc.m4a", at=F(MC_AT), **{"in": 0}, dur=F(6.5), volume=1.0))
ov(MC_AT, MC_AT + 6.85, type="sub", pos=pick(MC_AT, MC_AT + 6.5, SUB_OPTS), words=[dict(w=w, s=s) for w, s in mc_words])
ducks.append([F(MC_AT) - 3, F(MC_AT + 6.5)])

# ---- title + name ----
side = pick(T["TITLE"], T["NAME"], {"left": (80, 280, 1000, 800), "right": (920, 280, 1840, 800), "center": (300, 330, 1620, 750)})
ov(T["TITLE"] + 0.1, T["NAME"] - 0.1, type="title", side=side, kicker="MENGENALI", title="PENGERUSI FAMA")
ov(T["NAME"] + 0.3, T["DAY1"] - 0.2, type="name", side="left", pos="bottom", honor="YBRS. TUAN HAJI",
   name="Abang Ahmad Kerdee\nbin Abang Masagus", role="PENGERUSI FAMA", note="Berkhidmat sejak 1 Ogos 2026")

# ---- 01 Day one ----
chapter(T["DAY1"], T["DAY1"] + 3.6, "01", "Hari Pertama di FAMA", "4 Ogos 2026  ·  Ibu Pejabat FAMA")
voice("taskforce", T["DAY1"] + 0.9)

# ---- 02 MAHA: Agro Madani sales ----
chapter(T["MAHA"], T["MAHA"] + 3.4, "02", "MAHA 2026", "Pameran Pertanian, Hortikultur & Agro-Pelancongan Malaysia")
s_at = T["MAHA"] + 1.0
voice("sales", s_at)
t79 = s_at + find_word("sales", "79")
stat(t79 - 0.3, t79 + 4.4, "RM79.77 JUTA", "NILAI JUALAN AGRO MADANI", "Seluruh negara · setakat November 2026")
s_end = s_at + vo_files["sales"][1]

# ---- 03 Bersama Rakyat: budget 2027 + entrepreneurs ----
chapter(T["MELAKA"], T["MELAKA"] + 3.2, "03", "Bersama Rakyat", "Program Jualan Pertanian  ·  Melaka")
b_at = max(s_end + 0.6, T["MELAKA"] + 0.6)
b_end = voice("bajet", b_at)
t5k = b_at + find_word("bajet", "5")
stat(t5k - 0.3, t5k + 4.2, "5,000", "AKTIVITI JUALAN AGRO MADANI", "Sasaran tahun 2027")
u_at = b_end + 0.7
u_end = voice("usahawan", u_at)
t39 = u_at + find_word("usahawan", "39")
stat(t39 - 0.3, t39 + 3.8, "39,841", "USAHAWAN TERLIBAT", "Jualan Agro Madani · seluruh negara")
t25 = u_at + find_word("usahawan", "25")
stat(t25 - 0.3, t25 + 3.6, "RM25.36 JUTA", "NILAI PENJIMATAN RAKYAT", "Jualan Agro Madani")
assert u_end < T["TALK"] - 0.3, (u_end, T["TALK"])

# ---- on-camera media statement (SARA) ----
talk = next(s for s in shots if s["kind"] == "talk")
sp_at = talk["t0"] + 0.5
ov(talk["t0"] + 0.3, talk["t1"] - 0.2, type="talklabel", kicker="KENYATAAN MEDIA", title="Pengerusi FAMA",
   sub="Pasar Tani Kekal Simpang 4, Perlis  ·  10 November 2026")
sara_end = voice("sara", sp_at, split_at=talk["t1"])

# ---- 04 Bidara: food supply readiness ----
chapter(T["BIDARA"], T["BIDARA"] + 3.2, "04", "Memperkasa Industri", "Lawatan ke Bidara Flour Mill")
k_at = max(sara_end + 0.8, T["BIDARA"] + 0.8)
k_end = voice("bekalan", k_at)
t3b = k_at + find_word("bekalan", "tiga")
stat(t3b - 0.3, t3b + 4.0, "3 BULAN", "STOK BEKALAN MAKANAN", "Persediaan FAMA mendepani Super El Nino")
assert k_end < T["WARGA"] + 0.5, (k_end, T["WARGA"])

# ---- 05 Warga FAMA (music) ----
chapter(T["WARGA"], T["WARGA"] + 3.6, "05", "Ilmu & Kesejahteraan", "Majlis Watikah Sahabat Ilmuwan  ·  Program Kecergasan FAMA", top_only=False)

# ---- end ----
ENDT = T["END"] + 0.2
ov(ENDT, MAIN_END, type="end", kicker="SELAMAT DATANG KE", title="FAMA", sub="LEMBAGA PEMASARAN PERTANIAN PERSEKUTUAN")

# ---- SFX / flashes ----
fx("whoosh_cine", T["TITLE"] - 0.35, 0.35)
fx("impact_big", T["TITLE"], 0.38)
fx("swoosh_accent", T["NAME"] + 0.2, 0.3)
for k in ["DAY1", "MAHA", "MELAKA", "BIDARA", "WARGA", "RECAP"]:
    fx("whoosh_cine", T[k] - 0.3, 0.28)
for o in overlays:
    if o["type"] == "stat":
        fx("pop_long", o["from_"] / FPS, 0.28)
fx("whoosh_air", T["TALK"] - 0.4, 0.22)
fx("riser", T["END"] - 2.6, 0.3)
fx("impact_whoosh", ENDT, 0.32)
flashes = [F(T[k]) for k in ["MAHA", "MELAKA", "BIDARA", "WARGA", "RECAP"]] + [F(ENDT)]

# --------------------------------------------------------------------------------------------
os.makedirs(f"{ROOT}/public/mz", exist_ok=True)
used = sorted({s["src"] for s in shots})
for f in os.listdir(f"{ROOT}/public/mz"):
    if f not in used:
        os.remove(f"{ROOT}/public/mz/{f}")
for f in used:
    if not os.path.exists(f"{ROOT}/public/mz/{f}"):
        shutil.copy(f"{MEZZ}/{f}", f"{ROOT}/public/mz/{f}")
for f in os.listdir(f"{ROOT}/public/vo"):
    if f[:-4] not in VO and f != "mc.m4a":
        os.remove(f"{ROOT}/public/vo/{f}")

out = dict(
    durationInFrames=F(MAIN_END),
    music=dict(src=MUSIC, offset=MUSIC_OFFSET, volume=0.5, duck=0.13),
    shots=[dict(src=s["src"], **{"from": F(s["t0"])}, dur=F(s["t1"]) - F(s["t0"]), **{"in": s["in"]}, vol=s["vol"],
                z0=s["z"][0], z1=s["z"][1], ox=s["ox"], oy=s["oy"], fadeIn=s["fadeIn"], kind=s["kind"], speed=s["speed"]) for s in shots],
    overlays=[{("from" if k == "from_" else k): v for k, v in o.items()} for o in overlays],
    sfx=sorted(sfx, key=lambda x: x["at"]),
    flashes=flashes,
    vo=vo_tracks,
    ducks=ducks,
)
json.dump(out, open(f"{ROOT}/src/montage/montage.json", "w"), indent=1, ensure_ascii=False)
vo_total = sum(v[1] for v in vo_files.values()) + 6.5
print(f"{len(shots)} shots (all unique), {MAIN_END:.1f}s main, VO {vo_total:.1f}s")
print("sections", {k: round(v, 1) for k, v in T.items()})
for k, v in vo_files.items():
    print(f"  vo {k:10s} {v[1]:5.1f}s  {len(v[3])} pieces")
for o in out["overlays"]:
    if o["type"] != "sub":
        print(f"{o['from'] / FPS:6.2f} {o['dur'] / FPS:5.2f} {o['type']:9s} {o.get('side') or ''} {o.get('pos') or ''} "
              f"{o.get('title') or o.get('value') or ''}")
