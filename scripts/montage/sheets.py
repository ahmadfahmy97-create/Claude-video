# contact sheets: one mid frame per clip (two for clips >12s), labelled
import os, subprocess, json, sys
from PIL import Image, ImageDraw, ImageFont
M='/home/user/mezz'; O='/home/user/work/sheets'; os.makedirs(O,exist_ok=True)
clips=sorted(f for f in os.listdir(M) if f.endswith('.mp4') and '.tmp' not in f)
info={}
tiles=[]
for c in clips:
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{M}/{c}'],capture_output=True,text=True).stdout.strip() or 0)
    info[c]=d
    ts=[d*0.5] if d<12 else [d*0.25,d*0.75]
    for k,t in enumerate(ts):
        p=f'/home/user/work/thumbs/{c}_{k}.jpg'; os.makedirs(os.path.dirname(p),exist_ok=True)
        if not os.path.exists(p):
            subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',f'{M}/{c}','-frames:v','1','-vf','scale=384:216',p])
        tiles.append((c,k,d,p))
json.dump(info,open('/home/user/work/durations.json','w'),indent=0)
W,H,COLS,ROWS=384,216,6,6
for s in range(0,len(tiles),COLS*ROWS):
    im=Image.new('RGB',(W*COLS,H*ROWS),'black'); dr=ImageDraw.Draw(im)
    for i,(c,k,d,p) in enumerate(tiles[s:s+COLS*ROWS]):
        x,y=(i%COLS)*W,(i//COLS)*H
        try: im.paste(Image.open(p),(x,y))
        except Exception: pass
        lab=c.replace('.mp4','').split('__'); lab=f"{lab[0][:10]} {lab[1][-6:]}{'b' if k else ''} {d:.0f}s"
        dr.rectangle([x,y,x+len(lab)*7+6,y+14],fill='black'); dr.text((x+3,y+1),lab,fill='yellow')
    im.save(f'{O}/sheet_{s//(COLS*ROWS):02d}.jpg',quality=80)
print(len(clips),'clips',sum(info.values())/60,'min')
