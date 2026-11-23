# Crème-objecten (ogen + kransbolletjes): vanaf crème (2, clusters >=3) max 2 stappen door 4/5/6, stopt aan 7/8/K/rood.
import numpy as np, sys; sys.path.insert(0,'.')
from cc import label
def cremeMasker(S,stappen=2):
    L,n=label(S==2); sz=np.bincount(L.ravel()); seed=(S==2)&(sz[L]>=3)
    M=seed.copy(); front=seed.copy(); H,W=S.shape
    for _ in range(stappen):
        nf=np.zeros_like(M)
        for y,x in zip(*np.where(front)):
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                a,b=y+dy,x+dx
                if 0<=a<H and 0<=b<W and not M[a,b] and S[a,b] in (2,4,5,6): nf[a,b]=True
        M|=nf; front=nf
    return M
if __name__=='__main__':
    S=np.load('sprite.npy'); M=cremeMasker(S)
    for y in range(64): print('%2d '%y+''.join(('C' if S[y,x]==2 else ('c' if M[y,x] else '.123456789KrRD'[S[y,x]])) for x in range(64)))
