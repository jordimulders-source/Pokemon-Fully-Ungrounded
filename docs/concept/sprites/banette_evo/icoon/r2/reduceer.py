# Shuppetto-icoon r2: exacte 2x2-reductie van de FRONT (niets getekend).
# Elke icoonpixel komt uit zijn 2x2-blok frontpixels; regels zoals half2.py (Krassault).
# Gebruik: python3 reduceer.py OY OX UIT.txt
import sys; from PIL import Image; import numpy as np
FRONT='docs/concept/sprites/banette_evo/af/shuppetto.png'
a=np.array(Image.open(FRONT)).astype(int)
# weglaten (toegestaan: delen weglaten): Shuppets (5,10,11,12,14 + hun 1/2/3 in hun kaders), draden (13)
weg=np.zeros_like(a,bool)
weg|=(a==13)
for (x0,y0,x1,y1) in ((2,40,17,59),(45,42,63,62)):   # kaders van de twee Shuppets
    weg[y0:y1,x0:x1]=True
# linkerbelletje (x5-10,y33-38) hangt aan een draad onder de punt: weg
weg[33:39,5:11]=True
a=np.where(weg,0,a)
OY,OX=int(sys.argv[1]),int(sys.argv[2])
H,W=a.shape; h=(H-OY)//2; w=(W-OX)//2
K7=int(__import__('os').environ.get('K7','1'))
LIJN={1}; MOND={8}; GEEL={9}
o=np.zeros((h,w),int); nd=np.zeros((h,w),int)
def meest(v):
    v=[x for x in v if x not in (0,1)]
    if not v: return 1
    vals,c=np.unique(v,return_counts=True); return int(vals[c.argmax()])
for j in range(h):
    for i in range(w):
        b=a[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2].ravel()
        t=(b==0).sum(); d=(b==1).sum(); nd[j,i]=d
        if t>=3: continue
        if (b==9).sum()>=1: o[j,i]=9; continue          # oog/bel-geel is klein: altijd houden
        MT=int(__import__("os").environ.get("MT","2"))
        if (b==8).sum()>=MT: o[j,i]=8; continue          # mond (drempel MT)
        if d>=3: o[j,i]=1; continue
        if t==2: o[j,i]=1 if d>=1 else meest(b); continue   # randblok: omlijning als er lijn in zit
        if d==2: o[j,i]=-1; continue
        o[j,i]=meest(b)
        if o[j,i]==7 and (b==7).sum()<K7: o[j,i]=6     # donkerrood alleen als diepe schaduw (>=K7 van 4)
for j in range(h):
    for i in range(w):
        if o[j,i]!=-1: continue
        b=a[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2]; dd=(b==1)
        nb=[(j-1,i),(j+1,i),(j,i-1),(j,i+1)]
        edge=any(not(0<=y<h and 0<=x<w) or o[y,x]==0 for y,x in nb)
        vert=dd[:,0].all() or dd[:,1].all(); hor=dd[0,:].all() or dd[1,:].all()
        thick=False
        if vert: thick=any(0<=x<w and nd[j,x]>=3 for x in (i-1,i+1))
        if hor: thick=thick or any(0<=y<h and nd[y,i]>=3 for y in (j-1,j+1))
        o[j,i]=1 if (edge or not thick) else meest(b.ravel())
np.save(sys.argv[3].replace('.txt','.npy'),o)
ch='0123456789abcdef'
open(sys.argv[3],'w').write('\n'.join(''.join('.' if v==0 else ch[v] for v in r) for r in o)+'\n')
print(open(sys.argv[3]).read())
