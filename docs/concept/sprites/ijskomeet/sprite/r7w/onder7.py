# r6-methode, maar op de r5-uitlijning (natief 3i+15, 3j-6)
import sys; sys.path.insert(0,'r6w'); sys.path.insert(0,'.')
import numpy as np; from PIL import Image
from p6 import CH,PAL,to_txt
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); lum=n.mean(2)
m=np.load('mask_r1.npy'); ox,oy=15,-6
P=np.array(PAL,float); I={c:i for i,c in enumerate(CH)}
o=np.full((64,64),-1); kd=np.zeros((64,64),int); med=np.zeros((64,64,3))
CAND='WLMDabcdG'
for j in range(64):
  for i in range(64):
    if not m[j,i]: continue
    y=3*j+oy; x=3*i+ox
    if y<0: o[j,i]=I['W']; continue
    px=n[y:y+3,x:x+3].reshape(-1,3); l=lum[y:y+3,x:x+3].ravel()
    if len(l)==0: o[j,i]=I['W']; continue
    kd[j,i]=(l<70).sum()
    keep=l>=70
    md=np.median(px[keep],0) if keep.sum()>=2 else np.median(px,0)
    med[j,i]=md
    o[j,i]=I[CAND[int(np.argmin([((md-P[I[c]])**2).sum() for c in CAND]))]]
np.save('r7w/O.npy',o); np.save('r7w/kd.npy',kd); np.save('r7w/med.npy',med)
to_txt(o,'r7w/O.txt')
