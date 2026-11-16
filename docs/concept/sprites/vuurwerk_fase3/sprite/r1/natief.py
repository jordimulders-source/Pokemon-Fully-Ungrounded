# Haalt het eigen pixelraster van het Gemini-model terug (pitch 5,12 px; 10,24 is de harmonische) -> natief.png (200x200)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    best=None
    for p in np.arange(5.05,5.2,0.005):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); s=g[idx].mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
bx=fit(gx); by=fit(gy); print('x',bx,'y',by)
px,phx=bx[1],bx[2]; py,phy=by[1],by[2]
xs=np.arange(phx+1+px/2,1024,px); ys=np.arange(phy+1+py/2,1024,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(1024,y+2)); x0,x1=int(max(0,x-1)),int(min(1024,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save('natief.png'); print(out.shape)
g=np.asarray(im.convert('L')); yy,xx=np.where(g<225); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
im.resize((out.shape[1]*4,out.shape[0]*4),Image.NEAREST).save('natief_4x.png')
