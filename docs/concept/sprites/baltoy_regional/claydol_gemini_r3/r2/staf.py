# Rechterstaf apart opnieuw schrappen (de staf is los): zelfde rijen als de hele sprite, eigen kolommen buiten de stafkop.
import sys, itertools, numpy as np; sys.path.insert(0,'.')
from schrap3 import k
from kaal3 import RIJEN
from cc import label
L,n=label(k>0,diag=True); M=L==L[55,83]
K=np.where(M,k,0)
def staf(cols):
    kk=np.delete(np.delete(K,RIJEN,0),cols,1); ys,xs=np.where(kk>0); return kk[ys.min():ys.max()+1,xs.min():xs.max()+1]
def kost(cols):
    c=0
    for i in cols:
        A=K[:,i]; B=K[:,i-1]; C=K[:,i+1]; c+=((A!=B)&(A!=C)).sum()+0.2*(A!=B).sum()
    return c
if __name__=='__main__':
    res=[]
    for cols in itertools.combinations(range(69,85),3):
        if any(b-a<2 for a,b in zip(cols,cols[1:])): continue
        if staf(list(cols)).shape[1]!=15: continue
        res.append((round(kost(cols),1),cols))
    res.sort(); print(res[:15])

def staf2(cols,extra):
    rows=sorted(set(RIJEN)|set(extra))
    kk=np.delete(np.delete(K,rows,0),cols,1); ys,xs=np.where(kk>0); return kk[ys.min():ys.max()+1,xs.min():xs.max()+1]
def plaats(st,S,rest):
    h,w=st.shape; y0=64-h; x0=64-w; P=np.argwhere(st>0)+[y0,x0]; Q=np.argwhere(rest)
    return np.abs(P[:,None,:]-Q[None]).max(2).min(),y0,x0
