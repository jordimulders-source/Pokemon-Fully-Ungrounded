# Meet het model per spritepixel: DF = fractie zwarte lijn (L<50), ML = mediaan helderheid zonder lijn, RG = mediaan r-g (rood/kaak).
import sys; sys.path.insert(0,'sprite_v2_r5')
import warnings; warnings.filterwarnings('ignore')
from kijk import *; from kijk import _A
L=(0.299*_A[...,0]+0.587*_A[...,1]+0.114*_A[...,2])
DF=np.full((64,64),-1.0);ML=np.zeros((64,64));RG=np.zeros((64,64))
for y in range(64):
  for x in range(64):
    a=sprite2model(x,y);b=sprite2model(x+1,y+1)
    sl=(slice(max(0,round(a[1])),round(b[1])),slice(max(0,round(a[0])),round(b[0])))
    l=L[sl];f=FG[sl]
    if f.size==0 or f.mean()<0.25: continue
    DF[y,x]=((l<50)&f).sum()/f.sum()
    m=(l>=50)&f; nl=l[m]; ML[y,x]=np.median(nl) if nl.size else 0
    c=_A[sl][m]; RG[y,x]=np.median(c[:,0]-c[:,1]) if c.size else 0
np.save('sprite_v2_r5/DF.npy',DF);np.save('sprite_v2_r5/ML.npy',ML);np.save('sprite_v2_r5/RG.npy',RG)
