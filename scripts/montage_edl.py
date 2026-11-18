"""EDL for the 16:9 waiting-room montage "Mengenali Pengerusi FAMA".

Builds src/montage/montage.json (shots, overlays, voice-over, SFX, music ducking) from the mezzanine
clips in /home/user/mezz (1080p25 H.264 made from the raw FX3/DJI files), anchored to the beat grid of
the music track. Every clip is used once only (no repeated scenes). Face boxes (YuNet) decide Ken-Burns
origins and which side text goes on, so text never sits on a face. Used clips are copied to public/mz.

Voice-over: the chairman's own words from his media statement at Pasar Tani Kekal Simpang 4, Perlis
(10 Nov 2026, clip JAM-PTK 0545), with word timings from faster-whisper (/home/user/work/w0545.json).

Usage: python3 scripts/montage_edl.py
"""
import importlib.util
import json
import os
import shutil

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZZ = os.environ.get("MEZZ", "/home/user/mezz")
FACES = os.environ.get("FACES", "/home/user/work/faces")
WORK = os.environ.get("WORK", "/home/user/work")
FPS = 25

# ---- music: Mixkit #128, 103 BPM; drums enter at 42.0 s. We start the track 9 s in. ----
MUSIC = "music/m128.mp3"
OFFSET = 9.0
B0, BEAT = 42.005 - OFFSET, 0.5813  # first downbeat after the drop (video time) and beat length
DROP = B0  # 33.0 s
BREAK = 97.6 - OFFSET  # 88.6 – breakdown
PEAK2 = 118.9 - OFFSET  # 109.9 – last peak
END_MUSIC = 153.5 - OFFSET  # music resolves


def beat(n):
    return B0 + n * BEAT


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

# ---- chairman voice-over segments (source seconds in clip 0545) ----
W0545 = json.load(open(f"{WORK}/w0545.json"))
VO = {
    # Day one: his first month at FAMA
    "taskforce": dict(a=326.45, b=334.85, text="Di peringkat ibu pejabat FAMA, kami telah mengorak langkah. "
                      "Bermula bulan pertama saya berada di pejabat, kami telah mewujudkan satu task force."),
    # Agro Madani sales
    "sales": dict(a=37.45, b=50.6, text="Pada tahun ini, setakat bulan November ini, FAMA telah mengadakan "
                  "Jualan Agro Madani yang telah mencatat nilai jualannya sebanyak RM79.77 juta."),
    # entrepreneurs
    "usahawan": dict(a=92.85, b=97.75, text="Kita telah melibatkan 39,841 usahawan."),
    # food supply readiness
    "bekalan": dict(a=370.2, b=377.65, text="Bagi pihak FAMA, kami dah bersedia untuk penyediaan bekalan makanan "
                    "sekurang-kurangnya tiga bulan."),
    # on camera: SARA at Agro Madani – benefits consumers, producers and entrepreneurs
    "sara": dict(a=243.0, b=259.1, text="Bermula 1 Januari, FAMA sebagai salah satu agensi yang menyelia Jualan "
                 "Agro Madani, SARA itu sendiri boleh digunakan pembeliannya di Jualan Agro Madani. Dia bukan "
                 "sahaja memberi keuntungan kepada pengguna, tapi kepada juga pengeluar dan usahawan."),
}


def vo_words(key):
    """Karaoke timings: whisper word starts (relative to segment) mapped onto the cleaned display text."""
    v = VO[key]
    ws = [w for w in W0545 if v["a"] - 0.05 <= w["s"] < v["b"]]
    disp = v["text"].split()
    starts = [w["s"] - v["a"] for w in ws]
    # spread display words over the spoken word starts (counts differ slightly after clean-up)
    out = []
    for i, w in enumerate(disp):
        j = min(len(starts) - 1, int(round(i * (len(starts) - 1) / max(1, len(disp) - 1))))
        out.append(dict(w=w, s=round(max(0.0, starts[j]), 2)))
    return out


# --------------------------------------------------------------------------------------------
# Shot list. Before the drop lengths are seconds; after it, beats. Each clip appears once.
# --------------------------------------------------------------------------------------------
pre = [  # cold open + title + name + day one (slow, dissolves)
    ("BK", 1.0, 3.2), ("BENCH", 4.0, 2.8), ("READ", 9.0, 3.2),
    ("LOOK", 13.0, 6.2),            # title over the look-to-camera
    ("C5636", 2.5, 5.4),            # name card: chairing at the FAMA backdrop
    ("C5613", 9.0, 2.6), ("C5617", 1.5, 2.2), ("C5622", 1.5, 2.2), ("C5626", 1.0, 1.6),
    ("C5630", 0.3, 1.8), ("C5627", 1.0, 1.8),
]
post = [
    "MAHA",
    ("C7204", 2.0, 4), ("C6706", 5.0, 2), ("C6686", 3.0, 2), ("C6624", 1.5, 2), ("C6651", 4.0, 2),
    ("C6660", 3.0, 2), ("C6714", 3.0, 2), ("C6720", 5.0, 2), ("C7213", 0.5, 2), ("C7230", 2.0, 2),
    ("C7252", 8.0, 2), ("C7256", 2.0, 2), ("C6635", 2.0, 2), ("C7222", 1.0, 4),
    "MELAKA",
    ("C0447", 2.0, 4), ("C0408", 1.0, 2), ("C0410", 1.5, 2), ("C0431", 3.0, 2), ("C0443", 2.0, 4),
    ("C0450", 0.5, 2), ("C0437", 1.0, 2),
    "BIDARA",
    ("C9661", 1.0, 2), ("C9680", 2.0, 4), ("C9682", 0.5, 2), ("C9695", 2.0, 4), ("C9692", 0.3, 2),
    ("C9703", 2.0, 4), ("C9694", 0.3, 2),
    "WARGA",
    ("0035_D", 0.5, 4), ("0019_D", 1.0, 2), ("0045_D", 0.0, 2), ("0027_D", 1.0, 2), ("C6262", 4.0, 4),
    ("C6356", 1.0, 2), ("C6380", 0.5, 2), ("C6449", 1.0, 2), ("C6441", 0.5, 2), ("0024_D", 1.0, 4),
]
SPEECH_IN = VO["sara"]["a"] - 0.6
breakdown = [  # the chairman on camera (media statement), then two quiet shots
    ("SPEECH", SPEECH_IN, (VO["sara"]["b"] - VO["sara"]["a"]) + 1.3), ("C5629", 0.3, 4.0),
]
final = [  # last peak: unseen moments of the chairman, ends on the Fun Fit group photo
    ("C0454", 0.5, 2), ("C7248", 1.0, 2), ("C6719", 8.0, 2), ("C6716", 1.0, 2), ("C9691", 6.0, 2),
    ("C0456", 0.5, 2), ("C6727", 0.5, 2), ("C7214", 0.5, 2), ("C5620", 1.0, 2), ("C6630", 4.0, 2),
    ("C7240", 1.0, 2), ("C6703", 1.0, 2), ("C0657", 0.5, 2), ("C7253", 0.5, 2), ("C0414", 2.0, 2),
    ("C9664", 0.5, 2), ("C6701", 0.5, 2), ("C7205", 2.0, 2), ("C6683", 2.0, 4), ("C6616", 1.0, 4),
    ("C6438", 12.0, 99),  # held under the end title
]

shots = []


def add(key, t0, t1, tin, vol=0.0, fade=0, z=(1.0, 1.06), kind=None):
    c = clip(key)
    dur = t1 - t0
    tin = max(0.0, min(tin, DUR[c + ".mp4"] - dur - 0.05))
    shots.append(dict(src=c + ".mp4", t0=t0, t1=t1, **{"in": round(tin, 2)}, vol=vol, fadeIn=fade, z=z, kind=kind))


t = 0.0
for i, (k, tin, d) in enumerate(pre):
    add(k, t, t + d, tin, fade=10 if i else 0, z=(1.0, 1.08) if i < 4 else (1.02, 1.08))
    t += d
assert abs(t - DROP) < 0.05, t

n = 0
marks = {}
for item in post:
    if isinstance(item, str):
        marks[item] = n
        continue
    k, tin, nb = item
    add(k, beat(n), beat(n + nb), tin, z=(1.04, 1.1) if n % 4 == 0 else (1.1, 1.04))
    n += nb
print(f"post ends {shots[-1]['t1']:.2f}  break {BREAK:.2f}")
shots[-1]["t1"] = BREAK

t = BREAK
for i, (k, tin, d) in enumerate(breakdown):
    add(k, t, t + d, tin, fade=10, z=(1.0, 1.04), vol=0.0, kind="talk" if k == "SPEECH" else None)
    t += d
print(f"break ends {shots[-1]['t1']:.2f}  peak2 {PEAK2:.2f}")
shots[-1]["t1"] = PEAK2

n0 = round((PEAK2 - B0) / BEAT)
n = n0
for k, tin, nb in final:
    t1 = beat(n + nb) if nb < 99 else END_MUSIC + 1.5
    add(k, beat(n) if n > n0 else PEAK2, t1, tin, z=(1.04, 1.1) if nb < 99 else (1.0, 1.05))
    n += nb
MAIN_END = shots[-1]["t1"]

srcs = [s["src"] for s in shots]
dups = {s for s in srcs if srcs.count(s) > 1}
assert not dups, f"repeated clips: {dups}"

# --------------------------------------------------------------------------------------------
# Faces → Ken Burns origin + free side for text
# --------------------------------------------------------------------------------------------
spec = importlib.util.spec_from_file_location("faces", f"{WORK}/faces.py")
fmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fmod)


def faces_for(c, a, b):
    p = f"{FACES}/{c}.json"
    if not os.path.exists(p):
        fmod.run(c + ".mp4")
    fr = [f for f in json.load(open(p)) if a - 0.2 <= f["t"] <= b + 0.2]
    return [bx for f in fr for bx in f["b"]]


for s in shots:
    if s["kind"] == "talk":
        s["faces"], s["ox"], s["oy"] = [[1180, 200, 380, 420]], 0.5, 0.4  # the framed portrait on the right
        continue
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
        # pad each face by 40% (hair, chin, a safety margin) before measuring overlap
        x, y, w, h = x - 0.4 * w, y - 0.4 * h, w * 1.8, h * 1.8
        tot += max(0, min(x + w, x1) - max(x, x0)) * max(0, min(y + h, y1) - max(y, y0))
    return tot


def pick(t0, t1, options):
    """options: {name: rect}; the rect with the least face overlap wins (earlier wins ties)."""
    b = boxes_in(t0, t1)
    return min(options, key=lambda k: overlap(b, options[k]) + list(options).index(k) * 1e-3)


overlays, vo_tracks, ducks, sfx = [], [], [], []


def ov(t0, t1, **g):
    overlays.append(dict(from_=F(t0), dur=F(t1) - F(t0), **g))


def fx(name, tt, vol):
    sfx.append(dict(name=name, at=max(0, F(tt)), volume=vol))


SUB_OPTS = {"bottom": (200, 860, 1720, 1060), "top": (200, 20, 1720, 220)}


def vo_file(key, src, a, length):
    """Cut a speech segment and loudness-normalise it (-16 LUFS) so every line sits at the same level."""
    import subprocess
    os.makedirs(f"{ROOT}/public/vo", exist_ok=True)
    out = f"{ROOT}/public/vo/{key}.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{length:.3f}", "-i", f"{MEZZ}/{clip(src)}.mp4",
                    "-vn", "-ac", "2", "-ar", "48000", "-af",
                    "highpass=f=80,afade=t=in:d=0.08,loudnorm=I=-16:TP=-2:LRA=7",
                    "-c:a", "aac", "-b:a", "192k", out], check=True)
    return f"vo/{key}.m4a"


def voice(key, at, src="SPEECH", src_in=None, src_len=None, words=None, sub=True):
    """Place a voice-over line: normalised audio + karaoke subtitle + music duck."""
    if key in VO:
        v = VO[key]
        src_in, src_len, words = v["a"], v["b"] - v["a"], vo_words(key)
    vo_tracks.append(dict(src=vo_file(key, src, src_in, src_len), at=F(at), **{"in": 0}, dur=F(src_len), volume=1.0))
    if not sub:
        return at + src_len
    pos = pick(at, at + src_len, SUB_OPTS)
    ov(at, at + src_len + 0.35, type="sub", pos=pos, words=words)
    ducks.append([F(at) - 3, F(at + src_len)])
    return at + src_len


# 1. MC announces his arrival over the cold open
VO_AT = 2.6
mc_words = [("Mengumumkan", 0.0), ("ketibaan", 0.88), ("Yang", 1.58), ("Berusaha", 1.86), ("Tuan", 2.38),
            ("Haji", 2.72), ("Abang", 3.0), ("Ahmad", 3.26), ("Kerdee", 3.6), ("bin", 4.16), ("Abang", 4.36),
            ("Masagus,", 4.66), ("Pengerusi", 5.64), ("FAMA", 6.04)]
voice("mc", VO_AT, src="0013_D", src_in=0.0, src_len=6.5, words=[dict(w=w, s=s) for w, s in mc_words])

# 2. Title over the look-to-camera
T0 = sum(d for *_, d in pre[:3])
side = pick(T0, T0 + 6.0, {"left": (80, 280, 1000, 800), "right": (920, 280, 1840, 800), "center": (300, 330, 1620, 750)})
ov(T0 + 0.1, T0 + 6.1, type="title", side=side, kicker="MENGENALI", title="PENGERUSI FAMA")

# 3. Name card over the meeting shot
N0 = T0 + pre[3][2]
nside = pick(N0, N0 + 5.4, {"left": (100, 560, 1060, 980), "right": (860, 560, 1820, 980)})
nside, npos = "left", "bottom"  # checked by eye: lower-left is clear of his face on this shot
ov(N0 + 0.3, N0 + 5.3, type="name", side=nside, pos=npos, honor="YBRS. TUAN HAJI",
   name="Abang Ahmad Kerdee\nbin Abang Masagus", role="PENGERUSI FAMA", note="Berkhidmat sejak 1 Ogos 2026")


def chapter(t0, t1, num, title, sub, avoid_sub=False):
    opts = {"tl": (60, 60, 900, 360), "tr": (1020, 60, 1860, 360), "bl": (60, 760, 900, 1040), "br": (1020, 760, 1860, 1040)}
    if avoid_sub:  # a subtitle runs along the bottom: keep the chapter card at the top
        opts = {k: v for k, v in opts.items() if k[0] == "t"}
    k = pick(t0, t1, opts)
    ov(t0 + 0.15, t1, type="chapter", side="right" if k[1] == "r" else "left", pos="bottom" if k[0] == "b" else "top",
       num=num, title=title, sub=sub)


def stat(t0, t1, value, label, sub, force=None):
    if force:
        ov(t0, t1, type="stat", side=force, value=value, label=label, sub=sub)
        return
    opts = {"right": (1100, 360, 1840, 720), "left": (80, 360, 820, 720),
            "right-top": (1100, 120, 1840, 480), "left-top": (80, 120, 820, 480)}
    k = pick(t0, t1, opts)
    ov(t0, t1, type="stat", side=k, value=value, label=label, sub=sub)


# 01 Day one + "bulan pertama saya berada di pejabat… task force"
C1 = N0 + pre[4][2]
chapter(C1, C1 + 3.6, "01", "Hari Pertama di FAMA", "4 Ogos 2026  ·  Ibu Pejabat FAMA", avoid_sub=True)
voice("taskforce", C1 + 0.5)

# 02 MAHA 2026 + Agro Madani sales
chapter(DROP, DROP + 3.4, "02", "MAHA 2026", "Pameran Pertanian, Hortikultur & Agro-Pelancongan Malaysia", avoid_sub=True)
s_at = DROP + 4.2
voice("sales", s_at)
w79 = next(w["s"] for w in W0545 if w["w"].startswith("79")) - VO["sales"]["a"]
stat(s_at + w79 - 0.3, s_at + w79 + 4.6, "RM79.77 JUTA", "NILAI JUALAN AGRO MADANI", "Seluruh negara · setakat November 2026")

# 03 Bersama Rakyat + 39,841 usahawan
m_t = beat(marks["MELAKA"])
chapter(m_t, m_t + 3.2, "03", "Bersama Rakyat", "Program Jualan Pertanian  ·  Melaka", avoid_sub=True)
u_at = m_t + 3.3
voice("usahawan", u_at)
w39 = next(w["s"] for w in W0545 if w["w"].startswith("39")) - VO["usahawan"]["a"]
stat(u_at + w39 - 0.3, u_at + w39 + 4.2, "39,841", "USAHAWAN TERLIBAT", "Jualan Agro Madani · seluruh negara",
     force="left-bottom")  # his hat hides the face from the detector; lower-left sits on the bag, not on him

# 04 Bidara + food supply readiness
b_t = beat(marks["BIDARA"])
chapter(b_t, b_t + 3.2, "04", "Memperkasa Industri", "Lawatan ke Bidara Flour Mill", avoid_sub=True)
voice("bekalan", b_t + 2.0)

# 05 Warga FAMA (music only)
w_t = beat(marks["WARGA"])
chapter(w_t, w_t + 3.6, "05", "Ilmu & Kesejahteraan", "Majlis Watikah Sahabat Ilmuwan  ·  Program Kecergasan FAMA")

# Breakdown: on-camera media statement (sync sound from the shot itself)
sp = next(s for s in shots if s["kind"] == "talk")
sp_voice_at = sp["t0"] + (VO["sara"]["a"] - sp["in"])
ov(sp["t0"] + 0.3, sp["t1"] - 0.2, type="talklabel", kicker="KENYATAAN MEDIA", title="Pengerusi FAMA",
   sub="Pasar Tani Kekal Simpang 4, Perlis  ·  10 November 2026")
L = VO["sara"]["b"] - VO["sara"]["a"]
ov(sp_voice_at, sp_voice_at + L + 0.35, type="sub", pos="talk", words=vo_words("sara"))
voice("sara", sp_voice_at, sub=False)  # the talk shot itself is muted; its line plays normalised
ducks.append([F(sp["t0"]) - 3, F(sp_voice_at + L)])

# End title
ENDT = END_MUSIC - 6.5
ov(ENDT, MAIN_END, type="end", kicker="SELAMAT DATANG KE", title="FAMA", sub="LEMBAGA PEMASARAN PERTANIAN PERSEKUTUAN")

# --------------------------------------------------------------------------------------------
# SFX (Mixkit, public/sfx) and white flashes on section hits
# --------------------------------------------------------------------------------------------
fx("whoosh_cine", T0 - 0.35, 0.35)
fx("impact_big", T0, 0.42)
fx("swoosh_accent", N0 + 0.2, 0.3)
fx("whoosh_air", C1 - 0.3, 0.22)
fx("riser", DROP - 2.6, 0.4)
fx("impact_whoosh", DROP, 0.45)
fx("pop_long", s_at + w79 - 0.3, 0.3)
fx("whoosh_cine", m_t - 0.3, 0.3)
fx("pop_long", u_at + w39 - 0.3, 0.3)
fx("whoosh_cine", b_t - 0.3, 0.3)
fx("whoosh_cine", w_t - 0.3, 0.28)
fx("shutter", w_t + 0.2, 0.2)
fx("whoosh_air", BREAK - 0.4, 0.22)
fx("riser", PEAK2 - 2.6, 0.32)
fx("impact_big", PEAK2, 0.36)
fx("whoosh_cine", ENDT - 0.3, 0.3)
fx("impact_whoosh", ENDT, 0.32)

flashes = [F(DROP), F(m_t), F(b_t), F(w_t), F(PEAK2), F(ENDT)]

# --------------------------------------------------------------------------------------------
os.makedirs(f"{ROOT}/public/mz", exist_ok=True)
used = sorted({s["src"] for s in shots})
for f in os.listdir(f"{ROOT}/public/mz"):
    if f not in used:
        os.remove(f"{ROOT}/public/mz/{f}")
for f in used:
    dst = f"{ROOT}/public/mz/{f}"
    if not os.path.exists(dst):
        shutil.copy(f"{MEZZ}/{f}", dst)

out = dict(
    durationInFrames=F(MAIN_END),
    music=dict(src=MUSIC, offset=OFFSET, volume=0.55, duck=0.16),
    shots=[dict(src=s["src"], **{"from": F(s["t0"])}, dur=F(s["t1"]) - F(s["t0"]), **{"in": s["in"]}, vol=s["vol"],
                z0=s["z"][0], z1=s["z"][1], ox=s["ox"], oy=s["oy"], fadeIn=s["fadeIn"], kind=s["kind"]) for s in shots],
    overlays=[{("from" if k == "from_" else k): v for k, v in o.items()} for o in overlays],
    sfx=sorted(sfx, key=lambda x: x["at"]),
    flashes=flashes,
    vo=vo_tracks,
    ducks=ducks,
)
json.dump(out, open(f"{ROOT}/src/montage/montage.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(shots)} shots (all unique), {MAIN_END:.1f}s main, {len(used)} clips")
for o in out["overlays"]:
    print(f"{o['from'] / FPS:6.2f} {o['dur'] / FPS:5.2f} {o['type']:9s} {o.get('side') or ''} {o.get('pos') or ''} "
          f"{o.get('title') or o.get('value') or ''}")
