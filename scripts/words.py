"""Print word timings in a source range: python3 scripts/words.py <project> <clip> <from> <to>"""
import json, sys
proj, clip, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
d = json.load(open(f'projects/{proj}/transcripts/{clip}.json'))
out = []
for s in d['segments']:
    for w in s['words']:
        if w['s'] >= a - 0.01 and w['e'] <= b + 0.01:
            out.append(f"{w['w'].strip()}[{w['s']:.2f}-{w['e']:.2f}]")
print(' '.join(out))
