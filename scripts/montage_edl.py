"""EDL for the 16:9 waiting-room montage "Mengenali Pengerusi FAMA".

Builds src/montage/montage.json (shots, overlays, SFX, music ducking) from the mezzanine clips in
/home/user/mezz (1080p25 H.264 made from the raw FX3/DJI files), anchored to the beat grid of the
music track. Face boxes (YuNet) decide Ken-Burns origins and which side titles go on, so text never
sits on a face. Used clips are copied to public/mz.

Usage: python3 scripts/montage_edl.py
"""
import json
import os
import shutil
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZZ = os.environ.get("MEZZ", "/home/user/mezz")
FACES = os.environ.get("FACES", "/home/user/work/faces")
TR = os.environ.get("TR", "/home/user/work/tr")
FPS = 25

# ---- music: Mixkit #128, 103 BPM; drums enter at 42.0 s. We start the track 9 s in. ----
MUSIC = "music/m128.mp3"
OFFSET = 9.0
B0, BEAT = 42.005 - OFFSET, 0.5813  # first downbeat after the drop (video time) and beat length
DROP = B0  # 33.0 s
END_MUSIC = 153.5 - OFFSET  # music resolves here


def beat(n):
    return B0 + n * BEAT


def F(t):
    return int(round(t * FPS))


CLIP = {
    "BK": "Shooting_Simbol_FAMA__C6606", "BENCH": "Shooting_Simbol_FAMA__C6604",
    "READ": "Shooting_Simbol_FAMA__C6605", "LOOK": "Shooting_Simbol_FAMA__C6607",
}


def clip(key):
    if key in CLIP:
        return CLIP[key]
    for f in os.listdir(MEZZ):
        if f.endswith(".mp4") and f[:-4].endswith(key):
            return f[:-4]
    raise KeyError(key)


DUR = json.load(open("/home/user/work/durations.json"))

# --------------------------------------------------------------------------------------------
# Shot list.  (clip, in-point s, length) – lengths before the drop are seconds, after it beats.
# --------------------------------------------------------------------------------------------
pre = [  # cold open + title + name + day one (slow, dissolves)
    ("BK", 1.0, 3.2), ("BENCH", 4.0, 2.8), ("READ", 9.0, 3.2),
    ("LOOK", 13.0, 6.2),            # title over the look-to-camera
    ("C5636", 2.5, 5.4),            # name card: chairing at the FAMA backdrop
    ("C5613", 9.0, 2.6), ("C5617", 1.5, 2.2), ("C5622", 1.5, 2.2), ("C5626", 1.0, 1.6),
    ("C5630", 0.3, 1.8), ("C5627", 1.0, 1.8),
]
post = [  # MAHA 2026 (drop) – 2-beat cuts with a few 4-beat breathers
    ("C7204", 2.0, 4), ("C7208", 1.0, 2), ("C6706", 5.0, 2), ("C6686", 3.0, 2), ("C6624", 1.5, 2),
    ("C6626", 1.5, 2), ("C6651", 4.0, 2), ("C6660", 3.0, 2), ("C6714", 3.0, 4), ("C6720", 5.0, 2),
    ("C7213", 0.5, 2), ("C7230", 2.0, 4), ("C7252", 8.0, 2), ("C7259", 2.0, 2), ("C7256", 2.0, 2),
    ("C6662", 2.0, 2), ("C6655", 1.0, 2), ("C6676", 10.0, 4), ("C7217", 1.0, 2), ("C7261", 1.0, 2),
    ("C6635", 2.0, 2), ("C7222", 1.0, 4),
    "MELAKA",
    # Program Jualan Pertanian Melaka
    ("C0447", 2.0, 4), ("C0408", 1.0, 2), ("C0410", 1.5, 2), ("C0431", 3.0, 2), ("C0442", 0.5, 2),
    ("C0443", 2.0, 4), ("C0444", 0.3, 2), ("C0450", 0.5, 2),
    "BIDARA",
    # Bidara Flour Mill
    ("C9661", 1.0, 2), ("C9680", 2.0, 4), ("C9682", 0.5, 2), ("C9695", 2.0, 4), ("C9699", 0.5, 2),
    ("C9697", 1.0, 2), ("C9703", 2.0, 4), ("C9686", 0.2, 2),
]
breakdown = [  # softer: Majlis Watikah + Program Kecergasan (2.6 s, dissolves)
    ("0035_D", 0.5, 2.7), ("0019_D", 1.0, 2.6), ("0045_D", 0.0, 2.6), ("C6262", 4.0, 2.7),
    ("C6356", 1.0, 2.6), ("C6380", 0.5, 2.6), ("C6449", 1.0, 2.7), ("C6438", 2.0, 3.3),
]
final = [  # last peak: recap of the chairman, ends on the group photo
    ("C0443", 6.0, 2), ("C7252", 14.0, 2), ("C6660", 8.0, 2), ("C6703", 1.0, 2), ("C6713", 2.0, 2),
    ("C6720", 11.0, 2), ("C9703", 7.0, 2), ("C5623", 0.5, 2), ("C6616", 1.0, 4), ("C7206", 1.0, 2),
    ("C0431", 9.0, 2), ("C6683", 2.0, 2), ("C0444", 0.3, 2), ("C7259", 5.0, 2), ("C6624", 5.0, 2),
    ("C9680", 7.0, 2), ("C0447", 7.0, 4), ("C6636", 1.0, 2), ("READ", 20.0, 4), ("LOOK", 15.0, 4),
    ("C6438", 12.0, 99),  # held under the end title
]

shots = []


def add(key, t0, t1, tin, vol=0.0, fade=0, z=(1.0, 1.06)):
    c = clip(key)
    dur = t1 - t0
    tin = max(0.0, min(tin, DUR[c + ".mp4"] - dur - 0.05))
    shots.append(dict(src=c + ".mp4", t0=t0, t1=t1, **{"in": round(tin, 2)}, vol=vol, fadeIn=fade, z=z))


t = 0.0
for i, (k, tin, d) in enumerate(pre):
    add(k, t, t + d, tin, fade=10 if i else 0, z=(1.0, 1.08) if i < 4 else (1.02, 1.08))
    t += d
assert abs(t - DROP) < 0.05, t
t = DROP
n = 0
marks = {}
for item in post:
    if isinstance(item, str):
        marks[item] = n
        continue
    k, tin, nb = item
    add(k, beat(n), beat(n + nb), tin, z=(1.04, 1.1) if n % 4 == 0 else (1.1, 1.04))
    n += nb

BREAK = 97.6 - OFFSET  # 88.6
print("post ends", shots[-1]["t1"], "break", BREAK)
shots[-1]["t1"] = BREAK
t = BREAK
for k, tin, d in breakdown:
    add(k, t, t + d, tin, fade=8, z=(1.0, 1.06))
    t += d
PEAK2 = 118.9 - OFFSET  # 109.9
print("break ends", shots[-1]["t1"], "peak2", PEAK2)
shots[-1]["t1"] = PEAK2
n0 = round((PEAK2 - B0) / BEAT)
n = n0
for k, tin, nb in final:
    t1 = beat(n + nb) if nb < 99 else END_MUSIC + 1.5
    add(k, beat(n) if n > n0 else PEAK2, t1, tin, z=(1.04, 1.1) if nb < 99 else (1.0, 1.05))
    n += nb
MAIN_END = shots[-1]["t1"]

# --------------------------------------------------------------------------------------------
# Faces → Ken Burns origin + free side for text
# --------------------------------------------------------------------------------------------
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("faces", "/home/user/work/faces.py")
fmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fmod)


def faces_for(c, a, b):
    p = f"{FACES}/{c}.json"
    if not os.path.exists(p):
        fmod.run(c + ".mp4")
    fr = [f for f in json.load(open(p)) if a - 0.2 <= f["t"] <= b + 0.2]
    boxes = [bx for f in fr for bx in f["b"]]
    return boxes


for s in shots:
    c = s["src"][:-4]
    boxes = faces_for(c, s["in"], s["in"] + (s["t1"] - s["t0"]))
    s["faces"] = boxes
    if boxes:
        big = sorted(boxes, key=lambda b: -b[2] * b[3])[: max(1, len(boxes) // 3)]
        cx = float(np.mean([b[0] + b[2] / 2 for b in big])) / 1920
        cy = float(np.mean([b[1] + b[3] / 2 for b in big])) / 1080
        s["ox"], s["oy"] = round(min(0.8, max(0.2, cx)), 3), round(min(0.7, max(0.2, cy)), 3)
    else:
        s["ox"], s["oy"] = 0.5, 0.45


def shot_at(tt):
    for s in shots:
        if s["t0"] <= tt < s["t1"]:
            return s
    return shots[-1]


def boxes_in(t0, t1):
    out = []
    for s in shots:
        if s["t1"] > t0 and s["t0"] < t1:
            out += s["faces"]
    return out


def overlap(boxes, rect):
    x0, y0, x1, y1 = rect
    tot = 0
    for x, y, w, h, *_ in boxes:
        ix = max(0, min(x + w, x1) - max(x, x0))
        iy = max(0, min(y + h, y1) - max(y, y0))
        tot += ix * iy
    return tot


def pick(t0, t1, options):
    """options: {name: rect}; returns the rect name with least face overlap (first wins ties)."""
    b = boxes_in(t0, t1)
    best = min(options, key=lambda k: overlap(b, options[k]) * 1.0 + list(options).index(k) * 1e-3)
    return best


overlays = []


def ov(t0, t1, **g):
    overlays.append(dict(from_=F(t0), dur=F(t1) - F(t0), **g))


# MC voice-over subtitle (karaoke) over the cold open
VO_AT, VO_IN, VO_LEN = 2.6, 0.0, 6.5
vo_words = [
    ("Mengumumkan", 0.0), ("ketibaan", 0.88), ("Yang", 1.58), ("Berusaha", 1.86), ("Tuan", 2.38), ("Haji", 2.72),
    ("Abang", 3.0), ("Ahmad", 3.26), ("Kerdee", 3.6), ("bin", 4.16), ("Abang", 4.36), ("Masagus,", 4.66),
    ("Pengerusi", 5.64), ("FAMA", 6.04),
]
pos = pick(VO_AT, VO_AT + VO_LEN, {"bottom": (200, 860, 1720, 1060), "top": (200, 20, 1720, 220)})
ov(VO_AT, VO_AT + VO_LEN + 0.3, type="sub", pos=pos, words=[dict(w=w, s=s) for w, s in vo_words])

# Title over the look-to-camera
T0 = pre[0][2] + pre[1][2] + pre[2][2]
side = pick(T0, T0 + 6.0, {"left": (80, 280, 1000, 800), "right": (920, 280, 1840, 800), "center": (300, 330, 1620, 750)})
ov(T0 + 0.1, T0 + 6.1, type="title", side=side, kicker="MENGENALI", title="PENGERUSI FAMA")

# Name card over the meeting shot
N0 = T0 + pre[3][2]
nside = pick(N0, N0 + 5.4, {"left": (100, 560, 1060, 980), "right": (860, 560, 1820, 980)})
npos = "bottom"
if overlap(boxes_in(N0, N0 + 5.4), (100, 560, 1820, 980)) > 60000:
    npos = "top"
ov(N0 + 0.3, N0 + 5.3, type="name", side=nside, pos=npos, honor="YBRS. TUAN HAJI",
   name="Abang Ahmad Kerdee\nbin Abang Masagus", role="PENGERUSI FAMA", note="Berkhidmat sejak 1 Ogos 2026")


def chapter(t0, t1, num, title, sub):
    opts = {"tl": (60, 60, 900, 360), "tr": (1020, 60, 1860, 360), "bl": (60, 760, 900, 1040), "br": (1020, 760, 1860, 1040)}
    k = pick(t0, t1, opts)
    ov(t0 + 0.15, t1, type="chapter", side="right" if k[1] == "r" else "left", pos="bottom" if k[0] == "b" else "top",
       num=num, title=title, sub=sub)


C1 = N0 + pre[4][2]
chapter(C1, C1 + 3.6, "01", "Hari Pertama di FAMA", "4 Ogos 2026  ·  Ibu Pejabat FAMA")
chapter(DROP, DROP + 3.4, "02", "MAHA 2026", "Pameran Pertanian, Hortikultur & Agro-Pelancongan Malaysia")
idx_melaka, idx_bidara = marks["MELAKA"], marks["BIDARA"]
chapter(beat(idx_melaka), beat(idx_melaka) + 3.2, "03", "Bersama Rakyat", "Program Jualan Pertanian  ·  Melaka")
chapter(beat(idx_bidara), beat(idx_bidara) + 3.2, "04", "Memperkasa Industri", "Lawatan ke Bidara Flour Mill")
chapter(BREAK, BREAK + 3.8, "05", "Ilmu & Kesejahteraan", "Majlis Watikah Sahabat Ilmuwan  ·  Program Kecergasan FAMA")

ENDT = END_MUSIC - 6.5
ov(ENDT, MAIN_END, type="end", kicker="SELAMAT DATANG KE", title="FAMA", sub="LEMBAGA PEMASARAN PERTANIAN PERSEKUTUAN")

# --------------------------------------------------------------------------------------------
# SFX (Mixkit, already in public/sfx) and flashes
# --------------------------------------------------------------------------------------------
sfx = []


def fx(name, tt, vol):
    sfx.append(dict(name=name, at=max(0, F(tt)), volume=vol))


fx("whoosh_cine", T0 - 0.35, 0.35)
fx("impact_big", T0, 0.42)
fx("swoosh_accent", N0 + 0.2, 0.3)
fx("whoosh_air", C1 - 0.3, 0.25)
fx("shutter", C1 + 2.6 + 4.4, 0.25)  # booklet close-up
fx("riser", DROP - 2.6, 0.4)
fx("impact_whoosh", DROP, 0.45)
fx("whoosh_cine", beat(idx_melaka) - 0.3, 0.3)
fx("whoosh_cine", beat(idx_bidara) - 0.3, 0.3)
fx("whoosh_air", BREAK - 0.4, 0.25)
fx("shutter", BREAK + 7.9 + 0.1 + 2.6 * 4 + 2.7, 0.25)  # Fun Fit group photo
fx("riser", PEAK2 - 2.6, 0.32)
fx("impact_big", PEAK2, 0.36)
fx("whoosh_cine", ENDT - 0.3, 0.3)
fx("impact_whoosh", ENDT, 0.32)

flashes = [F(DROP), F(beat(idx_melaka)), F(beat(idx_bidara)), F(PEAK2), F(ENDT)]

# MC voice-over (separate audio, cleaned by a gentle fade in Remotion)
vo = [dict(src=clip("0013_D") + ".mp4", at=F(VO_AT), **{"in": VO_IN}, dur=F(VO_LEN), volume=1.0)]
ducks = [[F(VO_AT) - 2, F(VO_AT + VO_LEN)]]

# --------------------------------------------------------------------------------------------
os.makedirs(f"{ROOT}/public/mz", exist_ok=True)
used = sorted({s["src"] for s in shots} | {v["src"] for v in vo})
for f in os.listdir(f"{ROOT}/public/mz"):
    if f not in used:
        os.remove(f"{ROOT}/public/mz/{f}")
for f in used:
    dst = f"{ROOT}/public/mz/{f}"
    if not os.path.exists(dst):
        shutil.copy(f"{MEZZ}/{f}", dst)

out = dict(
    durationInFrames=F(MAIN_END),
    music=dict(src=MUSIC, offset=OFFSET, volume=0.55),
    shots=[dict(src=s["src"], **{"from": F(s["t0"])}, dur=F(s["t1"]) - F(s["t0"]), **{"in": s["in"]}, vol=s["vol"],
                z0=s["z"][0], z1=s["z"][1], ox=s["ox"], oy=s["oy"], fadeIn=s["fadeIn"]) for s in shots],
    overlays=[{("from" if k == "from_" else k): v for k, v in o.items()} for o in overlays],
    sfx=sfx,
    flashes=flashes,
    vo=vo,
    ducks=ducks,
)
json.dump(out, open(f"{ROOT}/src/montage/montage.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(shots)} shots, {MAIN_END:.1f}s main, {len(used)} clips")
for o in out["overlays"]:
    print(o["type"], o["from"] / FPS, o.get("side"), o.get("pos"), o.get("title", ""))
