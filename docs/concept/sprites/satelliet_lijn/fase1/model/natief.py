# Haalt het eigen pixelraster van een Gemini-plaatje terug -> natief.png (pitch en fase gefit)
import sys; from PIL import Image; import numpy as np
IN,OUT=sys.argv[1],sys.argv[2]
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    best=None
    for p in np.arange(9.5,12.0,0.01):
        for ph in np.arange(0,p,0.5):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
_,px,phx=fit(gx); _,py,phy=fit(gy); print('pitch',px,py,'fase',phx,phy)
xs=np.arange(phx+1+px/2,a.shape[1]-1,px); ys=np.arange(phy+1+py/2,a.shape[0]-1,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT); print(out.shape)
