# Meet de pitch van het Gemini-raster in r5 via autocorrelatie van de randsterkte
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/r5.png').convert('RGB')).astype(int)
for ax,name in ((1,'x'),(0,'y')):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax).astype(float)
    best=[]
    for p in np.arange(3.0,16,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            best.append((g[idx].mean()/g.mean(),p,ph))
    best.sort(reverse=True); print(name,[ (round(s,2),round(p,2),ph) for s,p,ph in best[:8]])
