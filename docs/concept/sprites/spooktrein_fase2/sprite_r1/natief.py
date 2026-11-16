# Stap 1: eigen pixelraster van het Gemini-model terughalen (pitch gemeten) -> natief.png. Niets getekend.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model/model_r5.png').convert('RGB')).astype(int)
def fit(ax):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax).astype(float); best=None
    for p in np.arange(4.9,5.4,0.002):
        for ph in np.arange(0,p,0.1):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); s=g[idx].mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
bx,by=fit(1),fit(0); print('x',bx,'y',by)
def centres(b): p,ph=b[1],b[2]; return np.arange(ph+1+p/2,1024,p)
xs,ys=centres(bx),centres(by); W,H=len(xs),len(ys); out=np.zeros((H,W,3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(1024,y+2)); x0,x1=int(max(0,x-1)),int(min(1024,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(W,H)
Image.fromarray(out).resize((W*5,H*5),Image.NEAREST).save('natief_5x.png')
