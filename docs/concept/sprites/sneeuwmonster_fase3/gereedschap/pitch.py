# Meet rasterpitch van het model: randsterkte per kolom/rij, breed bereik 4-14 (piek bij p en 2p -> p).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('model.png').convert('RGB')).astype(float); g=a.mean(2)
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
def best(e,lo=4.0,hi=14.0):
    res=[]
    for p in np.arange(lo,hi,0.01):
        sc=0;bp=0
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(e)-1,p)).astype(int); idx=idx[idx<len(e)]
            s=e[idx].mean()/e.mean()
            if s>sc: sc,bp=s,ph
        res.append((sc,p,bp))
    return res
for n,e in (('x',dx),('y',dy)):
    r=best(e); r2=sorted(r,reverse=True)[:8]; print(n,[(round(s,2),round(p,2),ph) for s,p,ph in r2])
