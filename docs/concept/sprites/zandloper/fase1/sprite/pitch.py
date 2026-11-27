# Meet het pixelraster van het model (randsterkte per kolom/rij), handen weggelaten.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model.png').convert('RGB')).astype(int)
a=a.copy(); a[380:660,170:330]=255; a[500:660,690:850]=255   # handen eruit (eigen raster)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    res=[]
    for p in np.arange(8,26,0.02):
        best=0
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()
            if s>best: best=s;bph=ph
        res.append((best,p,bph))
    res.sort(reverse=True); return res[:6]
print('x',fit(gx)); print('y',fit(gy))
