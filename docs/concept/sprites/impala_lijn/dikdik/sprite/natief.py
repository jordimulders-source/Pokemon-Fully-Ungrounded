# Haalt het eigen pixelraster van het Gemini-model terug (pitch ~10.24 px) -> natief.png (+ natief_12x.png)
import sys; from PIL import Image; import numpy as np
IN=sys.argv[1] if len(sys.argv)>1 else '../referenties/model_r3b.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
def fit(g):
    best=None
    for p in np.arange(9.8,10.7,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()-g.mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
bx=fit(gx); by=fit(gy); print('x',bx[1:],'y',by[1:])
px,phx=bx[1],bx[2]; py,phy=by[1],by[2]
xs=np.arange(phx+1+px/2,1024,px); ys=np.arange(phy+1+py/2,1024,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save(OUT); im.resize((out.shape[1]*8,out.shape[0]*8),Image.NEAREST).save(OUT.replace('.png','_8x.png'))
g=np.asarray(im.convert('L')); yy,xx=np.where(g<225); print(out.shape,'bbox',xx.min(),xx.max(),yy.min(),yy.max())
