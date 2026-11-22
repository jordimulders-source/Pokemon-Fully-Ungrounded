import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
for ax in (1,0):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax).astype(float)
    best=[]
    for p in np.arange(8,24,0.02):
        for ph in np.arange(0,p,0.5):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int)
            best.append((g[idx].mean()/g.mean(),round(p,2),ph))
    best.sort(reverse=True); print('axis',ax,best[:3])
