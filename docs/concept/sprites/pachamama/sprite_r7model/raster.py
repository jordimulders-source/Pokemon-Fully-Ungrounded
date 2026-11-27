# zoekt de periode en fase van het (ruwe) pixelraster van het model
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float)
g=a.mean(2)
gx=np.abs(np.diff(g[100:950,60:1040],axis=1)).sum(0)  # grens tussen kolom k en k+1 -> positie k+1
gy=np.abs(np.diff(g[60:950,60:1040],axis=0)).sum(1)
def fit(gr,off):
    best=None
    for p in np.arange(5.4,6.0,0.002):
        for ph in np.arange(0,p,0.05):
            pos=np.arange(ph,len(gr),p); idx=np.round(pos).astype(int); idx=idx[idx<len(gr)]
            s=gr[idx].mean()
            if best is None or s>best[0]: best=(s,p,(ph+off+1)%p)
    return best
bx=fit(gx,60); by=fit(gy,60)
print('x',bx,'mean',gx.mean()); print('y',by,'mean',gy.mean())
