import sys; sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image
from p6 import CH,PAL,to_txt,save
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); lum=n.mean(2)
m=np.load('mask_r1.npy'); ox,oy=11,-4
P=np.array(PAL,float); I={c:i for i,c in enumerate(CH)}
o=np.full((64,64),-1)
for j in range(64):
  for i in range(64):
    if not m[j,i]: continue
    y=3*j+oy; x=3*i+ox
    if y<0: o[j,i]=I['W']; continue
    px=n[y:y+3,x:x+3].reshape(-1,3); l=lum[y:y+3,x:x+3].ravel()
    hi=np.sort(l)[-3:].mean()
    kd=(l<75).sum(); km=((l<hi-45)&(l>=75)).sum()
    keep=l>=hi-45
    med=np.median(px[keep],0) if keep.sum()>=3 else np.median(px,0)
    if kd>=2: o[j,i]=I['K']; continue
    if kd+km>=3 and hi>150: o[j,i]=I['S']; continue
    cand='WLMDabcdG'
    d=[((med-P[I[c]])**2).sum() for c in cand]
    o[j,i]=I[cand[int(np.argmin(d))]]
to_txt(o,'r6w/onder2.txt'); save(o,'r6w/onder2')
