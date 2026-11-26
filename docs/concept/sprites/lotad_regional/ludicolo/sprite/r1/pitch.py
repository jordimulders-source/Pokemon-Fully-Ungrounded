# Meet de natieve pitch van het model (kamscore op de randsterkte, breed bereik).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../r6/gemini_r6.png').convert('RGB')).astype(int); g=a.mean(2)
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
for nm,e in (('x',dx),('y',dy)):
    res=[]
    for p in np.arange(3.0,14.0,0.01):
        best=(0,0)
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(e)-1,p)).astype(int); s=e[idx].mean()
            if s>best[0]: best=(s,ph)
        res.append((best[0],p,best[1]))
    res.sort(reverse=True); print(nm,[('%.2f'%p,'%.2f'%ph,int(s)) for s,p,ph in res[:8]])
