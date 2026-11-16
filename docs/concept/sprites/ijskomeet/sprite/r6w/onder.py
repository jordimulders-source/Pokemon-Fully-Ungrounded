# r6 onderlaag: model (natief raster) per spritepixel 3x3-blok -> palet, binnen het bevroren silhouet.
import sys; sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image
from p6 import CH,PAL,to_txt,save
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
m=np.load('mask_r1.npy'); ox,oy=11,-4
P=np.array(PAL,float); I={c:i for i,c in enumerate(CH)}
lum=n.mean(2)
o=np.full((64,64),-1); F=np.zeros((64,64))
def blk(j,i):
    y=3*j+oy; x=3*i+ox
    if y<0 or x<0 or y+3>200 or x+3>200: return None
    return n[y:y+3,x:x+3].reshape(-1,3), lum[y:y+3,x:x+3].ravel()
for j in range(64):
    for i in range(64):
        if not m[j,i]: continue
        b=blk(j,i)
        if b is None: o[j,i]=I['W']; continue
        px,l=b
        F[j,i]=(l<60).mean()
        fg=px[l<248] if (l<248).sum()>=3 else px
        med=np.median(fg,0)
        cand='WLMDabcdGg' 
        d=[((med-P[I[c]])**2).sum() for c in cand]
        o[j,i]=I[cand[int(np.argmin(d))]]
np.save('r6w/F.npy',F)
to_txt(o,'r6w/onder.txt'); save(o,'r6w/onder')
