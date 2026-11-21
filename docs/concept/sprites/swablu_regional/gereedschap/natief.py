# Haalt het eigen pixelraster van het Swablu-model terug -> gereedschap/natief.png
# Pitch gemeten met gereedschap/pitch.py: kammen op 8,53 en 12,81 (verhouding 2:3) -> gemeenschappelijke cel 4,27 px (1024/240);
# visueel bevestigd (oog, snavelranden: ±4,3 px per modelpixel).
import numpy as np; from PIL import Image
IN='model/swablu_model.png'; OUT='gereedschap/natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); g=a.mean(2)
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
def fit(e):
    best=(0,0,0)
    for p in np.arange(4.22,4.32,0.001):
        for ph in np.arange(0,p,0.05):
            idx=np.round(np.arange(ph,len(e)-1,p)).astype(int); idx=idx[idx<len(e)]
            s=e[idx].mean()
            if s>best[0]: best=(s,p,ph)
    return best
sx,px,phx=fit(dx); sy,py,phy=fit(dy)
print('pitch x %.3f fase %.2f (score %.1f) | pitch y %.3f fase %.2f (score %.1f)'%(px,phx,sx/dx.mean(),py,phy,sy/dy.mean()))
H,W=g.shape
xs=np.arange(phx+0.5+px/2,W,px); ys=np.arange(phy+0.5+py/2,H,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,round(y-1))),int(min(H,round(y+1)+1)); x0,x1=int(max(0,round(x-1))),int(min(W,round(x+1)+1))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
np.save('gereedschap/raster.npy',np.array([px,phx,py,phy]))
m=out.min(2)<215; yy,xx=np.where(m); print('natief',out.shape[1],out.shape[0],'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'figuur',m.sum())
