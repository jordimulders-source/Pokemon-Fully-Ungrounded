# Kene ronde 8: middenlijn van 3 px op de ruggengraat + getrapte, schuine zijbanden van 3 px (treden 2 px),
# met de hand per rij (y, x0, x1). Kleur vlak per band: lichtkant LICHT, in de lijfschaduw SCHADUW; geen bevel.
# Rond de banden 1 px basis (b) waar het vachthooglicht (l) ze zou raken.
import os, sys, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
LICHT=sys.argv[1] if len(sys.argv)>1 else 'n'; SCHADUW=sys.argv[2] if len(sys.argv)>2 else 'm'
M=[(y,17,19) for y in (31,32,33)]+[(y,20,22) for y in (29,30,31)]+[(y,23,32) for y in (27,28,29)]+[(y,33,34) for y in (28,29,30)] \
 +[(y,35,36) for y in (29,30,31)]+[(y,37,39) for y in (31,32,33)]+[(y,40,42) for y in (32,33,34)]
B1=[(30,24,26),(31,24,26),(32,25,27),(33,25,27)]+[(y,26,28) for y in range(34,38)]+[(y,27,29) for y in range(38,42)]
B2=[(y,31,33) for y in range(30,34)]+[(y,32,34) for y in range(34,38)]+[(y,33,35) for y in range(38,44)]
BC=[(y,41,43) for y in range(35,41)]+[(y,42,44) for y in range(41,46)]
ROWS=M+B1+B2+BC
g=[['.']*64 for _ in range(64)]
for line in open(os.path.join(H,'raster.txt')):
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,st=line.split()
    for i,ch in enumerate(st): g[int(y)][int(x)+i]=ch
P={(x,y) for (y,x0,x1) in ROWS for x in range(x0,x1+1) if g[y][x] not in '.kd'}

out={}
for (x,y) in P: out.setdefault(y,{})[x]=SCHADUW if g[y][x]=='s' else LICHT
for (x,y) in P:
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            X,Y=x+dx,y+dy
            if (X,Y) not in P and g[Y][X]=='l' and 17<=X<=49 and 24<=Y<=50 and not (X<=24 and Y>=36): out.setdefault(Y,{})[X]='b'
# losse vachtpixeltjes tussen omlijning en middenlijn (met de hand nagelopen) -> basis
for (x,y) in ((21,27),(18,29)): out.setdefault(y,{})[x]='b'

out.setdefault(30,{})[38]='d'   # los schaduwpixeltje tussen omlijning en trede: hoekje van de omlijning
lines=['# ---- ronde 8: kene vlak (middenlijn + 3 getrapte zijbanden, %s licht / %s schaduw, 1 px basis eromheen) ----'%(LICHT,SCHADUW)]
for y in sorted(out):
    xs=sorted(out[y]); run=[xs[0]]
    for x in xs[1:]+[None]:
        if x is not None and x==run[-1]+1: run.append(x); continue
        lines.append('%d %d %s'%(y,run[0],''.join(out[y][i] for i in run)))
        if x is not None: run=[x]
print('\n'.join(lines)); print('# kene-pixels: %d'%len(P))
open(os.path.join(H,'kene_pixels.txt'),'w').write('\n'.join('%d %d'%p for p in sorted(P)))
