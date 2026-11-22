# Haalt het eigen pixelraster van het Gemini-model terug -> gereedschap/natief.png
# Pitch gemeten met gereedschap/pitch.py (randsterkte per kolom/rij): kam 10,24 px (1024/100), fase 9,20; visueel bevestigd
# (blokjes ±10 px op een uitvergroting van de kop). Natief 99x99, figuur x15-88, y14-83 (74x70).
import numpy as np; from PIL import Image
IN='referenties/gemini_gekozen_r4.png'; OUT='gereedschap/natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); g=a.mean(2)
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
def fit(e):
    best=(0,0,0)
    for p in np.arange(10.20,10.28,0.002):
        for ph in np.arange(0,p,0.05):
            idx=np.round(np.arange(ph,len(e),p)).astype(int); idx=idx[idx<len(e)]
            s=e[idx].mean()
            if s>best[0]: best=(s,p,ph)
    return best
_,px,phx=fit(dx); _,py,phy=fit(dy)
print('pitch x %.3f fase %.2f | pitch y %.3f fase %.2f'%(px,phx,py,phy))
# rand ligt tussen kolom idx en idx+1 -> celmidden = rand + 0.5 + p/2
xs=np.arange(phx+0.5+px/2,1024,px); ys=np.arange(phy+0.5+py/2,1024,py)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1.5)),int(min(1024,y+2.5)); x0,x1=int(max(0,x-1.5)),int(min(1024,x+2.5))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
m=out.min(2)<215; yy,xx=np.where(m); print('natief',out.shape[1],out.shape[0],'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
