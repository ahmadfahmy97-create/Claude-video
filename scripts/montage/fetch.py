import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
r = json.load(open('/home/user/work/cm_files.json'))
seen=set(); jobs=[]
for x in r:
    if x['folder']=='/Program Kecergasan': continue  # identical to /FX3
    key=x['name']
    if key in seen: continue
    seen.add(key); jobs.append(x)
OUT='/home/user/mezz'; DL='/home/user/dl'; os.makedirs(OUT,exist_ok=True)
def tag(f): return f.strip('/').replace(' ','_')[:20]
def run(x):
    stem=f"{tag(x['folder'])}__{x['name'].rsplit('.',1)[0]}"
    out=f"{OUT}/{stem}.mp4"
    if os.path.exists(out): return
    src=f"{DL}/{x['id']}.mp4"
    for _ in range(4):
        p=subprocess.run(["curl","-sSL","--retry","3","-o",src,f"https://drive.usercontent.google.com/download?id={x['id']}&export=download&confirm=t"])
        if p.returncode==0 and os.path.getsize(src)>100000: break
    p=subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-map","0:v:0","-map","0:a:0?","-vf","scale=1920:1080:flags=lanczos,format=yuv420p","-r","25",
        "-c:v","libx264","-preset","veryfast","-crf","18","-g","25","-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",out+".tmp.mp4"])
    if p.returncode==0: os.rename(out+".tmp.mp4", out)
    else: print("FAIL", stem, flush=True)
    os.remove(src)
    print("ok", stem, flush=True)
json.dump(jobs, open('/home/user/work/jobs.json','w'))
print(len(jobs),"jobs",flush=True)
with ThreadPoolExecutor(3) as ex: list(ex.map(run, jobs))
print("DONE",flush=True)
