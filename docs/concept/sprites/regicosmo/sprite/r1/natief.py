# Haalt het eigen pixelraster van het model terug -> sprite/r1/natief.png (gekopieerd van regiaqua/sprite/r1/natief.py)
# pitch.py: kam 11,72 (sterk) en 5,86 (de echte kleinste cel: trapjes van de Mars-rand zijn 1 cel van 5,86 px).
import numpy as np; from PIL import Image
IN='model.png'; OUT='sprite/r1/natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); g=a.mean(2)
H,W=g.shape
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
def fit(e):
    best=(0,0,0)
    for p in np.arange(5.84,5.89,0.001):
        for ph in np.arange(0,p,0.05):
            idx=np.round(np.arange(ph,len(e),p)).astype(int); idx=idx[idx<len(e)]
            s=e[idx].mean()
            if s>best[0]: best=(s,p,ph)
    return best
_,px,phx=fit(dx); _,py,phy=fit(dy)
print('pitch x %.3f fase %.2f | pitch y %.3f fase %.2f'%(px,phx,py,phy))
xs=np.arange(phx+0.5+px/2,W,px); ys=np.arange(phy+0.5+py/2,H,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(H,y+2)); x0,x1=int(max(0,x-1)),int(min(W,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
np.save('sprite/r1/natief_rooster.npy',np.array([px,phx,py,phy]))
m=out.min(2)<225; yy,xx=np.where(m); print('natief',out.shape[1],out.shape[0],'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
