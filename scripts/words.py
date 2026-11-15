import json,sys
clip=sys.argv[1]; a=float(sys.argv[2]); b=float(sys.argv[3])
d=json.load(open(f'transcripts/{clip}.json'))
out=[]
for s in d['segments']:
    for w in s['words']:
        if w['s']>=a-0.01 and w['e']<=b+0.01: out.append(f"{w['w'].strip()}[{w['s']:.2f}-{w['e']:.2f}]")
print(' '.join(out))
