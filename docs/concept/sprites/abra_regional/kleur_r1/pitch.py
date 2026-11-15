# Meet pitch/fase van het Gemini-pixelraster per as (randsterkte per kolom-/rijgrens)
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    res=[]
    for p in np.arange(8,18,0.01):
        best=None
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()/g.mean()
            if best is None or s>best[0]: best=(s,p,ph)
        res.append(best)
    res.sort(reverse=True); return res[:6]
for n,g in (('x',gx),('y',gy)):
    print(n,[('%.2f'%s,'%.2f'%p,ph) for s,p,ph in fit(g)])
