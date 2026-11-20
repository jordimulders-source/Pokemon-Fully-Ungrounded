# Natief raster van Gemini r1 terughalen (pitch ~10.24) -> natief.png (celmediaan van het midden 5x5)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/r1.png').convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(2).sum(0).astype(float); gy=np.abs(np.diff(a,axis=0)).sum(2).sum(1).astype(float)
def fit(g):
    best=None
    for p in np.arange(10.0,10.5,0.005):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g),p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
bx=fit(gx); by=fit(gy); print('x',bx,'y',by)
def cent(b): p,ph=b[1],b[2]; return np.arange(ph+0.5+p/2,1024,p)
xs,ys=cent(bx),cent(by); out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
        out[j,i]=np.median(a[max(0,y0):y1,max(0,x0):x1].reshape(-1,3),0)
Image.fromarray(out).save('natief.png'); Image.fromarray(out).resize((out.shape[1]*8,out.shape[0]*8),Image.NEAREST).save('natief_8x.png')
g=out.min(2); yy,xx=np.where(g<235); print(out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
