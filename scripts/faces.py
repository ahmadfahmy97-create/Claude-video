"""Detect faces in public/footage/base.mp4 and place captions / graphics / zoom origins
so nothing sits on top of a face. Updates src/timeline.json in place.

Usage: python3 scripts/faces.py
"""
import json
import os
import subprocess

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.environ.get("YUNET", "/home/user/models/yunet.onnx")
CACHE = f"{ROOT}/src/faces.json"
W, H, STEP = 540, 960, 3  # analyse at half res, every 3rd frame (10 fps)

tl = json.load(open(f"{ROOT}/src/timeline.json"))
FPS = tl["fps"]

if not os.path.exists(CACHE) or os.path.getmtime(CACHE) < os.path.getmtime(f"{ROOT}/public/footage/base.mp4"):
    det = cv2.FaceDetectorYN.create(MODEL, "", (W, H), 0.55)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{ROOT}/public/footage/base.mp4", "-vf",
                             f"select='not(mod(n\\,{STEP}))',scale={W}:{H}", "-vsync", "0", "-f", "rawvideo",
                             "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    faces = []
    n = 0
    while True:
        buf = proc.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        _, f = det.detect(img)
        boxes = []
        if f is not None:
            for r in f:
                x, y, w, h = (float(v) * 2 for v in r[:4])  # back to 1080x1920
                if w * h > 1500:  # ignore tiny background faces
                    boxes.append([round(x), round(y), round(w), round(h)])
        faces.append(dict(frame=n * STEP, boxes=boxes))
        n += 1
    json.dump(faces, open(CACHE, "w"))
faces = json.load(open(CACHE))
print("face samples:", len(faces))


def faces_between(t0, t1):
    f0, f1 = int(t0 * FPS), int(t1 * FPS)
    return [s for s in faces if f0 <= s["frame"] <= f1]


# ------------------------------------------------------------------ zoom origins
for z in tl["zooms"]:
    ss = faces_between(z["start"], z["start"] + 1.0)
    best = None
    for s in ss:
        for (x, y, w, h) in s["boxes"]:
            if best is None or w * h > best[2] * best[3]:
                best = (x, y, w, h)
    if best:
        x, y, w, h = best
        z["ox"] = round(min(max((x + w / 2) / 1080, 0.2), 0.8), 3)
        z["oy"] = round(min(max((y + h / 2) / 1920, 0.15), 0.7), 3)
    else:
        z["ox"], z["oy"] = 0.5, 0.4


def zoom_at(t):
    cur = None
    for z in tl["zooms"]:
        if z["start"] <= t + 1e-6:
            cur = z
    return cur or dict(scale=1, ox=0.5, oy=0.4)


def screen_boxes(s):
    """Face boxes as they appear on screen after the punch-in zoom."""
    z = zoom_at(s["frame"] / FPS)
    sc, ox, oy = z["scale"], z["ox"] * 1080, z["oy"] * 1920
    out = []
    for (x, y, w, h) in s["boxes"]:
        nx, ny = ox + (x - ox) * sc, oy + (y - oy) * sc
        # pad: hair above the detected box, chin below
        out.append((nx - 0.15 * w * sc, ny - 0.35 * h * sc, w * sc * 1.3, h * sc * 1.5))
    return out


def overlap(t0, t1, y0, y1, x0=60, x1=940):
    """Face area covered by the band, weighted so the main (largest) face counts most."""
    tot = 0.0
    for s in faces_between(t0, t1):
        bx = screen_boxes(s)
        if not bx:
            continue
        amax = max(w * h for (_, _, w, h) in bx)
        for (x, y, w, h) in bx:
            ix = max(0, min(x1, x + w) - max(x0, x))
            iy = max(0, min(y1, y + h) - max(y0, y))
            tot += ix * iy * ((w * h) / amax) ** 2
    return tot


# ------------------------------------------------------------------ graphics slots (faces only)
SIZES = {  # height, candidate centre ys (inside the 230..1480 safe band)
    "headline": (360, [960, 410, 1060]),
    "bigstat": (390, [960, 430, 1040]),
    "combo": (400, [960, 440, 1040]),
    "stamp": (190, [420, 980, 1100]),
    "price": (280, [980, 420, 1100]),
    "calendar": (340, [960, 420, 1060]),
    "sara": (240, [980, 400, 1100]),
    "checklist": (150, [1060, 380, 980]),
    "warning": (290, [980, 410, 1080]),
    "question": (240, [400, 980]),
    "endcard": (420, [1000, 1080, 440]),
    "location": (110, [300, 1080]),
    "tag": (80, [290, 1080]),
}
placed = []
for g in tl["gfx"]:
    if g["type"] not in SIZES:
        continue
    h, ys = SIZES[g["type"]]
    if g.get("over"):
        base = next(q for q in reversed(placed) if q["type"] == "combo")
        g["y"] = base["y"] + 150
    else:
        best = None
        for i, y in enumerate(ys):
            o = overlap(g["start"], g["start"] + g["dur"], y - h / 2, y + h / 2) + i * 2000  # prefer earlier slots
            # don't sit on another graphic that is still on screen
            for q in placed:
                if q["start"] + q["dur"] > g["start"] and abs(q["y"] - y) < (SIZES[q["type"]][0] + h) / 2:
                    o += 1e9
            if best is None or o < best[0]:
                best = (o, y)
        g["y"] = best[1]
    g["h"] = h
    placed.append(g)
    print(f"  {g['type']:9s} @{g['start']:6.2f}s +{g['dur']:.1f} -> y={g['y']}")

# ------------------------------------------------------------------ captions (avoid graphics hard, faces soft)
moved = 0
for p in tl["captions"]:
    nchar = sum(len(w["text"]) + 1 for w in p["words"])
    cap_h = 95 if nchar <= 18 else 175
    best = None
    for i, y in enumerate((1300, 1200, 1400, 1100, 760)):
        o = overlap(p["start"], p["end"], y - cap_h / 2, y + cap_h / 2) + i * 3000
        for g in placed:
            if g["type"] == "heat":
                continue
            if g["start"] < p["end"] and g["start"] + g["dur"] > p["start"]:
                gy0, gy1 = g["y"] - g["h"] / 2, g["y"] + g["h"] / 2
                if g["type"] in ("location", "tag"):
                    gy0, gy1 = g["y"] - g["h"] / 2, g["y"] + g["h"] / 2
                if y + cap_h / 2 > gy0 - 20 and y - cap_h / 2 < gy1 + 20:
                    o += 1e9
        if best is None or o < best[0]:
            best = (o, y)
    p["y"] = best[1]
    moved += best[1] != 1300
print("captions moved:", moved)

json.dump(tl, open(f"{ROOT}/src/timeline.json", "w"), ensure_ascii=False, indent=1)
print("updated src/timeline.json")
