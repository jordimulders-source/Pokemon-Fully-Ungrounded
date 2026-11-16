# r8: opschoonpunten keuring r7b. Basis r7b; silhouet en tinten volgens het model (modelstats gem); rest diff 0.
import numpy as np; from PIL import Image
src=Image.open('r7b.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r=o.copy()
MG=np.load('../sprite_r6/modelstats.npy')[0]
log={}
def mark(pt,x,y,v):
    if o[y,x]!=v: log.setdefault(pt,[]).append((x,y,int(o[y,x]),int(v))); o[y,x]=v
def fg(y,x): return 0<=y<64 and 0<=x<64 and o[y,x]>0
def edge(y,x): return any(not fg(y+dy,x+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
# 1: staartpunt x55-63 y49-57. Model rij 54 gevuld t/m x62 (195), punt x63 rij 53-57 (144-170): inham dicht.
for x in (61,62,63): mark('1 staartpunt',x,54,4)
Z1=[(x,y) for y in range(49,58) for x in range(55,64) if o[y,x]>0]
for x,y in Z1:
    if edge(y,x):
        top = y<=53                                 # bovenrand tot en met de punt: selout 5
        mark('1 staartpunt',x,y,5 if top else 1)    # vanaf de punt (x63 rij 54) en onderrand: zwart
    elif o[y,x] in (1,5) and MG[y,x]>=120:   # model <120 = donkere lijn, blijft 5
        mark('1 staartpunt',x,y,4)                  # vulling (model 139-163)
# 2: onderrand links x14-18 y55-57. Model rij 57 gevuld vanaf x18 (126); (16,57)=179 hoort er niet bij.
mark('2 onderrand links',16,57,0)
for x,y in [(14,55),(14,56),(15,56),(16,56),(17,56),(18,57)]:
    mark('2 onderrand links',x,y,1)
# 3: rij y46 x23-27 één tint 3 (model ±170)
for x in range(23,28): mark('3 rij y46',x,46,3)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
Z=np.zeros((64,64),bool); Z[49:58,55:64]=True; Z[55:58,14:19]=True; Z[46,23:28]=True
FACE=np.zeros((64,64),bool); FACE[9:27,25:42]=True
d=o!=r
with open('telling.txt','w') as f:
    for k in sorted(log): s='%s: %d %s'%(k,len(log[k]),log[k]); print(s); f.write(s+'\n')
    s='diff totaal %d, buiten de drie zones %d, gezicht %d'%(d.sum(),(d&~Z).sum(),(d&FACE).sum()); print(s); f.write(s+'\n')
