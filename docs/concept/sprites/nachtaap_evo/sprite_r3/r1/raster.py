# Zoekt pitch en fase van het natieve Gemini-raster (randsterkte per kolom-/rijgrens)
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open('referenties/gemini_gekozen_r3.png').convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    res=[]
    for p in np.arange(15.0,17.5,0.01):
        for ph in np.arange(0,p,0.5):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            res.append((g[idx].mean(),p,ph))
    res.sort(reverse=True); return res[:5]
print('x',fit(gx)); print('y',fit(gy))
