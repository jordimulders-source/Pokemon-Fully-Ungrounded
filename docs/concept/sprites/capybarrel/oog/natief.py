import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
def fit(g):
    best=None
    for p in np.arange(8,24,0.02):
        for ph in np.arange(0,p,0.5):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()-g.mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
bx=fit(gx); by=fit(gy); print(bx,by)
px,phx=bx[1],bx[2]; py,phy=by[1],by[2]
xs=np.arange(phx+1+px/2,1024,px); ys=np.arange(phy+1+py/2,1024,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(sys.argv[2]); print(out.shape)
