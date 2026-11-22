# Overschrijft afzonderlijke pixels/stukken in rijen.txt: regels "y x tekens" in een patchbestand.
# Alleen bestaande (opake) pixels mogen veranderen; het silhouet blijft bevroren.
import sys
rows={}
order=[]
for l in open('rijen.txt'):
    y,x,s=l.split(); rows.setdefault(int(y),[]).append([int(x),s])
def put(y,x,ch):
    for seg in rows[y]:
        a,s=seg
        if a<=x<a+len(s):
            assert s[x-a]!='.'
            seg[1]=s[:x-a]+ch+s[x-a+1:]; return
    raise SystemExit(f'pixel {x},{y} niet in silhouet')
for l in open(sys.argv[1]):
    l=l.split('#')[0].strip()
    if not l: continue
    y,x,s=l.split(); y,x=int(y),int(x)
    for i,ch in enumerate(s): put(y,x+i,ch)
with open('rijen.txt','w') as f:
    for y in sorted(rows):
        for a,s in sorted(rows[y]): f.write(f"{y} {a} {s}\n")
