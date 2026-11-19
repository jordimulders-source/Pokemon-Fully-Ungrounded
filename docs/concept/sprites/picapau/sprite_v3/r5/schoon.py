# Technisch opschonen van de kale reductie: buitenlijn 1 px op de bestaande silhouetrand (silhouet blijft gelijk).
# geel aan de lichtkant (achtergrond boven/links) -> selout 17 (98 49 8), anders zwart. Grijs (poten/snavel) en zwart blijven.
import numpy as np
o=np.load('kaal_11.npy').copy(); H,W=o.shape
GEEL={2,3,4}
ring=np.zeros_like(o)
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v==0 or v in (1,10,11): continue
        up=y==0 or o[y-1,x]==0; dn=y==H-1 or o[y+1,x]==0; lf=x==0 or o[y,x-1]==0; rt=x==W-1 or o[y,x+1]==0
        if not(up or dn or lf or rt): continue
        SEL={2:17,3:17,4:17,5:6,6:6,7:9,8:9,9:9,12:13,13:13,14:13}
        if (up or lf) and not (dn or rt): ring[y,x]=SEL[v]
        else: ring[y,x]=1
n=(ring>0).sum(); o[ring>0]=ring[ring>0]
np.save('schoon.npy',o); print('ringpixels',n)
