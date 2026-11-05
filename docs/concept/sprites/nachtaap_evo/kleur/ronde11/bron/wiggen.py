# Ronde 11: drie lichte tapse wiggen. Loop en richting = de 3D-projectie silhouet/wiggen_64.npy;
# per rij met de hand verdikt langs dezelfde middenlijn: bovenaan >= 4 px, tot ~2/3 >= 3 px, dan taps naar 1 px.
# Kleur vlak: lichtkant f (idx 15, maanzilver), lijfschaduw m (idx 6); 1 px basis b tussen wig en vachthooglicht l.
import os, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
W1=[(26,23,28),(27,21,28),(28,22,29),(29,24,30),(30,26,31),(31,27,32),(32,30,32),(33,30,32),(34,30,32),(35,30,32),(36,30,32),(37,31,32),(38,32,32)]
W2=[(27,31,34),(28,33,36),(29,34,37),(30,35,38),(31,36,38),(32,37,39),(33,37,39),(34,37,39),(35,38,40),(36,38,40),(37,39,40),(38,39,40),(39,39,39),(40,39,39)]
W3=[(34,42,45),(35,43,45),(36,44,46),(37,44,45),(38,45,45)]
WIG={'voor':W1,'midden':W2,'achter':W3}
g=[['.']*64 for _ in range(64)]
for line in open(os.path.join(H,'raster.txt')):
    if line.startswith('# ---- ronde 11'): break
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,st=line.split()
    for i,ch in enumerate(st): g[int(y)][int(x)+i]=ch
P={}
for n,rows in WIG.items():
    for (y,x0,x1) in rows:
        for x in range(x0,x1+1):
            if g[y][x] not in '.kd': P[(x,y)]=n
out={}
for (x,y) in P: out.setdefault(y,{})[x]='m' if g[y][x]=='s' else 'f'
for (x,y) in P:
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            X,Y=x+dx,y+dy
            if (X,Y) not in P and g[Y][X]=='l' and 15<=X<=49 and 24<=Y<=50 and not (X<=24 and Y>=36): out.setdefault(Y,{})[X]='b'
lines=['# ---- ronde 11: drie tapse wiggen (f licht / m schaduw, 1 px basis langs het hooglicht) ----']
for y in sorted(out):
    xs=sorted(out[y]); run=[xs[0]]
    for x in xs[1:]+[None]:
        if x is not None and x==run[-1]+1: run.append(x); continue
        lines.append('%d %d %s'%(y,run[0],''.join(out[y][i] for i in run)))
        if x is not None: run=[x]
print('\n'.join(lines))
K=np.load(os.path.join(H,'../../../silhouet/wiggen_64.npy'))
print('# wigpixels: %d, buiten de projectie: %d'%(len(P),sum(1 for p in P if not K[p[1],p[0]])))
open(os.path.join(H,'wig_pixels.txt'),'w').write('\n'.join('%d %d %s'%(x,y,n) for (x,y),n in sorted(P.items())))
