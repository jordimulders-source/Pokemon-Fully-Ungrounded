# Meet natieve pitch/fase van het Gemini-model via randsterkte per kolom/rij
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../MODEL.png').convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(2).sum(0).astype(float); gy=np.abs(np.diff(a,axis=0)).sum(2).sum(1).astype(float)
def fit(g,lo,hi):
    best=[]
    for p in np.arange(lo,hi,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            best.append((g[idx].mean()/g.mean(),p,ph))
    best.sort(reverse=True); return best[:5]
for lo,hi in [(4.9,5.3),(10.0,10.5)]:
    print('x',fit(gx,lo,hi)); print('y',fit(gy,lo,hi))
