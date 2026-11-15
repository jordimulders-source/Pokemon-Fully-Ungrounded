# Meet de pitch van het Gemini-pixelraster (randsterkte per kolom/rij)
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
for ax,name in ((1,'x'),(0,'y')):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax).astype(float)
    best=[]
    for p in np.arange(6,20,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            best.append((g[idx].mean()/g.mean(),p,ph))
    best.sort(reverse=True); print(name,[(round(s,2),round(p,2),ph) for s,p,ph in best[:5]])
im=np.asarray(Image.open(sys.argv[1]).convert('L')); yy,xx=np.where(im<200); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
