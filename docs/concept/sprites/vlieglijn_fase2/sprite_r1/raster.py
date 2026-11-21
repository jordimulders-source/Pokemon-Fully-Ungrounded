# Controle natief raster: pitch/fase zoeken en celhomogeniteit meten.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/gemini_gekozen_r1.png').convert('RGB')).astype(int)
g=a.sum(-1)
gx=np.abs(np.diff(g,axis=1)).sum(0).astype(float); gy=np.abs(np.diff(g,axis=0)).sum(1).astype(float)
def fit(gr,lo,hi):
    best=None
    for p in np.arange(lo,hi,0.002):
        for ph in np.arange(0,p,0.1):
            idx=np.round(np.arange(ph,len(gr),p)).astype(int); idx=idx[idx<len(gr)]
            s=gr[idx].sum()/ (len(gr)/p)
            if best is None or s>best[0]: best=(s,p,ph)
    return best
print('x',fit(gx,6.7,6.95)); print('y',fit(gy,6.7,6.95))
