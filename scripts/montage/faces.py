# face boxes per clip at 2.5 fps (1920x1080 coords) -> /home/user/work/faces/<clip>.json
import cv2, numpy as np, subprocess, json, os, sys
from concurrent.futures import ProcessPoolExecutor
M='/home/user/mezz'; O='/home/user/work/faces'; os.makedirs(O,exist_ok=True)
W,H=960,540
def run(c):
    out=f"{O}/{c[:-4]}.json"
    if os.path.exists(out): return
    det=cv2.FaceDetectorYN.create('/home/user/models/yunet.onnx','',(W,H),0.6)
    p=subprocess.Popen(["ffmpeg","-v","error","-i",f"{M}/{c}","-vf",f"fps=2.5,scale={W}:{H}","-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    res=[];n=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        _,f=det.detect(np.frombuffer(b,np.uint8).reshape(H,W,3))
        boxes=[[round(float(v)*2) for v in r[:4]]+[round(float(r[-1]),2)] for r in (f if f is not None else []) if r[2]*r[3]*4>2500]
        res.append({"t":round(n/2.5,2),"b":boxes}); n+=1
    json.dump(res,open(out,"w"))
if __name__=='__main__':
    clips=[c for c in sorted(os.listdir(M)) if c.endswith('.mp4') and '.tmp' not in c]
    with ProcessPoolExecutor(4) as ex: list(ex.map(run,clips))
    print("faces done",len(clips))
