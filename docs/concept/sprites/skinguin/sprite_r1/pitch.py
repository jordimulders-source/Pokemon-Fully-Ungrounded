# Meet de pitch van het Gemini-raster (randsterkte per kolom/rij, autocorrelatie + fase-fit)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../model/model.png').convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    res=[]
    for p in np.arange(4,20,0.01):
        best=(0,0)
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()
            if s>best[0]: best=(s,ph)
        res.append((best[0],p,best[1]))
    res.sort(reverse=True); return res[:8]
print('x',fit(gx)); print('y',fit(gy))
g=gx-np.convolve(gx,np.ones(31)/31,'same'); ac=[np.dot(g[:-k],g[k:]) for k in range(1,40)]
print('acx',sorted(range(1,40),key=lambda k:-ac[k-1])[:6])
