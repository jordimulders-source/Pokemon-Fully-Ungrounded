import numpy as np
from mcov import a,L,S
from scipy import ndimage as nd
sat=a.max(2)-a.min(2)
def blk(i,j):
    xa,ya=24+(i-1)*S,1+(j-4)*S; return (slice(max(0,int(round(ya))),int(round(ya+S))),slice(max(0,int(round(xa))),int(round(xa+S))))
K=np.zeros((64,64)); B=np.zeros((64,64))
for j in range(64):
    for i in range(64):
        sl=blk(i,j); l=L[sl]
        if l.size==0: continue
        K[j,i]=(l<38).mean(); B[j,i]=((l>=38)&(l<95)&(sat[sl]<40)).mean()
np.save('mKB.npy',np.stack([K,B]))
