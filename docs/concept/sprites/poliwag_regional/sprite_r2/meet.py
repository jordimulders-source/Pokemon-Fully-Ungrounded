# Meet de periode en fase van het Gemini-pixelraster (randsterkte per kolom-/rijgrens)
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open('../referenties/gemini_gekozen_v2.png').convert('RGB')).astype(int)
g=a.sum(axis=2); m=g<700
ys,xs=np.where(m); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    res=[]
    for p in np.arange(14,18.01,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            res.append((g[idx].mean(),p,ph))
    res.sort(reverse=True); return res[:5]
print('x',fit(gx)); print('y',fit(gy))
