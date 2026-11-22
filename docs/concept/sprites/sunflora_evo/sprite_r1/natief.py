# Haalt het eigen pixelraster van Gemini-r5 terug (pitch ~4.27 px = 1024/240) -> natief.png. Niets getekend.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/r5.png').convert('RGB')).astype(int)
def fit(ax):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax).astype(float)
    best=None
    for p in np.arange(4.24,4.30,0.001):
        for ph in np.arange(0,p,0.1):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()
            s=s/g.mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
bx,by=fit(1),fit(0); print('x',bx,'y',by)
H,W=a.shape[:2]
xs=np.arange(bx[2]+1+bx[1]/2,W-1,bx[1]); ys=np.arange(by[2]+1+by[1]/2,H-1,by[1])
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,round(y)-1)),int(min(H,round(y)+1)); x0,x1=int(max(0,round(x)-1)),int(min(W,round(x)+1))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(out.shape)
Image.fromarray(out).resize((out.shape[1]*6,out.shape[0]*6),Image.NEAREST).save('natief_6x.png')
