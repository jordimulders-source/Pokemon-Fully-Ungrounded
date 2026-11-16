# Eigen pixelraster van het model terughalen (methode Krassault/fase 1): pitch per as fitten, mediaan per cel.
import sys; from PIL import Image; import numpy as np
IN=sys.argv[1]; OUT=sys.argv[2]
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    best=None
    for p in np.arange(9.0,11.5,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); s=g[idx].mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
_,px,phx=fit(gx); _,py,phy=fit(gy); print('pitch',round(px,3),round(phx,2),round(py,3),round(phy,2))
xs=np.arange(phx+1+px/2,1024,px); ys=np.arange(phy+1+py/2,1024,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
g=out.astype(int).sum(2); yy,xx=np.where(g<735); print('natief',out.shape[1],out.shape[0],'bbox',xx.min(),xx.max(),yy.min(),yy.max(),'maat',xx.max()-xx.min()+1,yy.max()-yy.min()+1)
