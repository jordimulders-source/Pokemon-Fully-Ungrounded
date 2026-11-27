# Meet de rasterpitch/fase van het model (randsterkte per kolom/rij, kamscore). Gekopieerd van regiaqua/sprite/r1.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('model.png').convert('RGB')).astype(float)
g=a.mean(2)
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
def best(e,lo,hi):
    res=[]
    for p in np.arange(lo,hi,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(e)-1,p)).astype(int); idx=idx[idx<len(e)]
            res.append((e[idx].mean()/e.mean(),p,ph))
    res.sort(reverse=True); return res[:6]
for n,e in (('x',dx),('y',dy)):
    print(n,[(round(s,2),round(p,2),ph) for s,p,ph in best(e,4.5,8)])
