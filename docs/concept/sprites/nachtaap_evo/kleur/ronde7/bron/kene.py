# Kene ronde 7: met de hand gekozen blokken (x0,x1,y0,y1) voor de rugband en 3 getrapte dwarsbanden,
# overgenomen van de lichte patroonpixels in het poppetje (onderlaag 4:1). Elke band 3 px dik, treden van 3.
# Kleur: band in idx6 (m) met eigen schaduwrand idx5 (l) op de basis; op het hooglicht een tint lichter (n, rand m), in de lijfschaduw l.
import sys
# per rij: (y, x0, x1), met de hand overgenomen van de onderlaag (4:1) en verdikt tot 3 px, treden van 2-3 px
ROWS=[(27,20,25),(28,20,30),(29,20,30),(30,17,20),(31,17,20),(32,17,20),          # rugband: van achter de kop over de rug in band A
      (30,26,30),(31,28,32),(32,28,32),(33,28,32)]+[(y,30,32) for y in range(34,41)]   # band A: trede, daarna recht omlaag
ROWS+=[(28,33,37),(29,33,37),(30,35,38),(31,35,38),(32,35,38)]+[(y,37,39) for y in range(33,40)]  # band B
ROWS+=[(34,42,44),(35,42,44),(36,42,44),(37,44,46),(38,44,46),(39,44,46)]          # band C (achterlijf, kort, donker)
RUG=[];A=[];B=[]
C=[(42,44,34,36),(44,46,37,39)]
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
# ondergrond = het raster van ronde 7 zonder kene (dus de vacht van ronde 1, zonder oude lijnen of meander)
g=[['.']*64 for _ in range(64)]
for line in open(os.path.join(H,'raster.txt')):
    if line.startswith('# ---- ronde 7: kene dik'): break
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,st=line.split()
    for i,ch in enumerate(st): g[int(y)][int(x)+i]=ch
IDX={'.':0,'k':1,'d':2,'s':3,'b':4,'l':5}
base=np.array([[IDX.get(c,9) for c in r] for r in g])
P=set()
for (y,x0,x1) in ROWS:
    P|={(x,y) for x in range(x0,x1+1)}
Cset={(x,y) for (x0,x1,y0,y1) in C for x in range(x0,x1+1) for y in range(y0,y1+1)}
rug={(x,y) for (y,x0,x1) in ROWS[:6] for x in range(x0,x1+1)}
out={}
P={p for p in P if base[p[1],p[0]] not in (1,2)}   # omlijning (k/d) blijft staan
for (x,y) in sorted(P,key=lambda p:(p[1],p[0])):
    below=(x,y+1) not in P; right=(x+1,y) not in P; top=(x,y-1) not in P; left=(x-1,y) not in P
    # band: kern m (idx6), schaduwrand rechts/onder l (idx5), lichtere rand linksboven n (alleen aan de lichtkant, x<=31)
    ch='m'
    if (top or left) and x<=30: ch='n'
    if below or right: ch='l'
    if base[y,x]==3: ch='l'
    out.setdefault(y,{})[x]=ch
# de vacht rond de rugband: het hooglicht wijkt (b), zodat de band zelf het lichtste is en niet in het hooglicht overloopt
for y in range(26,34):
    for x in range(17,32):
        if (x,y) not in P and base[y,x]==5 and not (y==26): out.setdefault(y,{})[x]='b'
lines=[]
for y in sorted(out):
    xs=sorted(out[y]); run=[xs[0]]
    for x in xs[1:]+[None]:
        if x is not None and x==run[-1]+1: run.append(x); continue
        lines.append('%d %d %s'%(y,run[0],''.join(out[y][i] for i in run)))
        if x is not None: run=[x]
print('# ---- ronde 7: kene dik (rugband + 3 getrapte dwarsbanden, uit het poppetje; m licht/basis, l schaduwkant, n rand linksboven) ----')
print('\n'.join(lines))
print('# kene-pixels:',len(P))
