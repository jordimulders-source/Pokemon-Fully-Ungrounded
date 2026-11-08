# ronde 3: oude kop (af/olinguito.png) 1-op-1 op r2-lijf, verschuiving +2,+3 (oog op oog)
import numpy as np
from PIL import Image
old=np.array(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/af/olinguito.png'))
g=[list(l.rstrip('\n')) for l in open('raster_r2.txt')]
hb={**{y:32 for y in range(20,38)},38:30,39:30,40:29,41:28,42:27,43:24,44:21,45:17}
was=set()
for y,b in hb.items():
    for x in range(0,b+1):
        if g[y][x]!='.': was.add((x,y)); g[y][x]='.'
Bo={17:27,**{y:29 for y in range(18,29)},29:28,30:28,31:28,32:28,33:28,34:27,35:25,36:24,37:24,38:22,39:21,40:18,41:17}
DX,DY=2,3; kop=set()
for y,b in Bo.items():
    for x in range(0,b+1):
        v=old[y,x]
        if v: g[y+DY][x+DX]='%x'%v; kop.add((x+DX,y+DY))
gap=sorted(was-kop,key=lambda p:(p[1],p[0])); extra=sorted(kop-was,key=lambda p:(p[1],p[0]))
print('kop px oud',len(kop),'r2-kop px',len(was),'gat',len(gap),'buiten r2',len(extra))
print('gat',gap); print('extra',extra)
for p in gap: g[p[1]][p[0]]='?'
open('stappen/r3_basis.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
