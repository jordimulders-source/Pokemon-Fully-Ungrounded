# Meet rasterpitch van het model (stenenzone uitgesloten): randsterkte per kolom/rij, breed bereik 4-12.
# Uitkomst 26 nov: 8,53 en 4,27 scoren vrijwel gelijk -> echte cel = 4,27 (1024/240), visueel bevestigd (mondlijn 1 cel).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('model.png').convert('RGB')).astype(float); g=a.mean(2)
dx=np.abs(np.diff(g,axis=1)); dy=np.abs(np.diff(g,axis=0)); dx[290:470,390:495]=0; dy[290:470,390:495]=0
dx=dx.sum(0); dy=dy.sum(1)
def best(e):
    res=[]
    for p in np.arange(4.0,12.0,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(e)-1,p)).astype(int); idx=idx[idx<len(e)]
            res.append((e[idx].mean()/e.mean(),p,ph))
    res.sort(reverse=True); return res[:6]
for n,e in (('x',dx),('y',dy)): print(n,[(round(s,2),round(p,2),ph) for s,p,ph in best(e)])
