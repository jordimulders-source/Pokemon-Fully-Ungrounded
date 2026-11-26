# Natief raster terughalen bij gegeven pitch: beste fase per as, mediaan per cel.
import sys; from PIL import Image; import numpy as np
src,dst,p=sys.argv[1],sys.argv[2],float(sys.argv[3])
a=np.asarray(Image.open(src).convert('RGB')).astype(int)
H,W=a.shape[:2]
def fase(g):
    best=None
    for ph in np.arange(0,p,0.25):
        idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
        s=g[idx].mean()
        if best is None or s>best[0]: best=(s,ph)
    return best[1]
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
phx,phy=fase(gx),fase(gy)
# grens na index ph -> cel begint op ph+1
xs=np.arange(phx+1-p,W,p); ys=np.arange(phy+1-p,H,p)
out=[];spread=[]
for y0 in ys:
    row=[]
    for x0 in xs:
        c=a[int(max(0,np.ceil(y0+1))):int(min(H,np.floor(y0+p-1))), int(max(0,np.ceil(x0+1))):int(min(W,np.floor(x0+p-1)))].reshape(-1,3)
        if len(c)==0: c=np.array([[255,255,255]])
        row.append(np.median(c,axis=0)); spread.append(c.std(axis=0).mean())
    out.append(row)
out=np.array(out).astype('uint8')
Image.fromarray(out).save(dst); print(phx,phy,out.shape,'gem spreiding',np.mean(spread))
