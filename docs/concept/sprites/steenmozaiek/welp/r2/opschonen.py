# Stap 3: alleen technisch opschonen op de onderlaag (red2_TW): eindpalet = deelverzameling van het modelpalet,
# bruin max 3 tinten (overige bruintinten -> dichtstbijzijnde bewaarde tint), ruis < 3 px in bruin naar buurtint,
# buitenlijn 1 px dicht (zwart waar de achtergrond onder/rechts ligt, selout 59,34,36 boven/links).
import sys; from PIL import Image; import numpy as np
from reduceer import PAL
TW=int(sys.argv[1]) if len(sys.argv)>1 else 50
FIN=[(0,0,0),(22,11,17),(59,34,36),(99,62,57),(148,99,86),(186,141,126),(113,86,97),(148,121,142),(172,152,177),(195,190,192),(248,249,249),(217,204,174),(230,140,134)]
FIN=np.array(FIN); BR=[3,4,5]
def fin_of(c):
    c=np.array(c); d=((FIN[1:]-c)**2).sum(1); k=int(np.argmin(d))+1
    return k
# modelpaletindex -> eindindex (bruin alleen naar bruin)
from reduceer2 import G
M={0:0}
for k,p in enumerate(PAL):
    if G[k]=='bruin': M[k+1]=BR[int(np.argmin(((FIN[BR]-p)**2).sum(1)))]
    else: M[k+1]=fin_of(p)
r=np.load(f'red2_{TW}.npy'); base=np.vectorize(M.get)(r); a=base.copy()
np.save(f'kaal_{TW}.npy',base)
BRUIN=set(BR); H,W=a.shape
def nb4(j,i):
    for dj,di in ((-1,0),(1,0),(0,-1),(0,1)):
        y,x=j+dj,i+di
        if 0<=y<H and 0<=x<W: yield y,x
o=a.copy()
for j in range(H):
    for i in range(W):
        if a[j,i]==0 or a[j,i] in (1,10,12): continue   # zwart, tandwit, tong blijven
        bgdir=[(dj,di) for dj,di in ((-1,0),(1,0),(0,-1),(0,1)) if not(0<=j+dj<H and 0<=i+di<W) or a[j+dj,i+di]==0]
        if not bgdir: continue
        o[j,i]=1 if any(d in ((1,0),(0,1)) for d in bgdir) else 2
a=o
for it in range(3):
    seen=np.zeros_like(a,bool)
    for j in range(H):
        for i in range(W):
            if seen[j,i] or a[j,i] not in BRUIN: continue
            c=a[j,i]; st=[(j,i)]; cl=[]; seen[j,i]=True
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in nb4(y,x):
                    if not seen[yy,xx] and a[yy,xx]==c: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)<3:
                cnt={}
                for y,x in cl:
                    for yy,xx in nb4(y,x):
                        v=a[yy,xx]
                        if v in BRUIN and v!=c: cnt[v]=cnt.get(v,0)+1
                if cnt:
                    v=max(cnt,key=cnt.get)
                    for y,x in cl: a[y,x]=v
np.save(f'onderlaag_{TW}.npy',a); np.save('FIN.npy',FIN)
def save(a,fn):
    im=np.zeros(a.shape+(4,),'uint8'); m=a>0; im[m,:3]=FIN[a[m]]; im[m,3]=255; Image.fromarray(im).save(fn)
save(base,f'kaal_{TW}.png'); save(a,f'onderlaag_{TW}.png')
print('gewijzigd t.o.v. kale reductie:',(a!=base).sum())
