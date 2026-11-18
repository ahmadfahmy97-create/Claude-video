import re, subprocess, sys, json
def ls(fid):
    h = subprocess.run(["curl","-sSL",f"https://drive.google.com/embeddedfolderview?id={fid}"],capture_output=True,text=True).stdout
    out=[]
    for m in re.finditer(r'id="entry-([^"]+)".*?<a href="([^"]+)".*?flip-entry-title">([^<]+)',h,re.S):
        out.append((m.group(1), m.group(3), 'folders' in m.group(2)))
    return out
res=[]
def walk(fid, path):
    for i,n,isdir in ls(fid):
        if isdir: walk(i, path+"/"+n)
        else: res.append({"id":i,"name":n,"folder":path})
walk(sys.argv[1], "")
json.dump(res, open(sys.argv[2],"w"), indent=0)
from collections import Counter
for k,v in Counter(r["folder"] for r in res).items(): print(v, k)
