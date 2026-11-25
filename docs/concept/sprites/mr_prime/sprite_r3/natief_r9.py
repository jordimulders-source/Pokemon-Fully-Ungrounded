# Natief raster van gemini/r9.png terughalen (pitch 5.12 = 1024/200), mediaan per blokje -> natief.png
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../gemini/r9.png').convert('RGB')).astype(int)
p=5.12
def ph(g):
    best=None
    for f in np.arange(0,p,0.05):
        idx=np.round(np.arange(f,len(g)-1,p)).astype(int); s=g[idx].mean()
        if best is None or s>best[0]: best=(s,f)
    return best[1]
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0); gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1)
fx,fy=ph(gx),ph(gy); print('fase',fx,fy)
xs=np.arange(fx+1+p/2-0.5,1024,p); ys=np.arange(fy+1+p/2-0.5,1024,p)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(1024,y+2)); x0,x1=int(max(0,x-1)),int(min(1024,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(out.shape)
g=out.mean(axis=2); yy,xx=np.where(g<230); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
