# reductie.py: kale 2x-reductie van natief.png -> kaal_{fase}.png (P, 64x64) + klassenkaart natief_klas.npy
# klasse per natieve pixel = dichtstbijzijnde modelkleur (k-means op het model, zaden per kleurgroep);
# spritepixel = figuur als >=2 van de 4 natieve pixels figuur zijn; kleur = meest voorkomende klasse (gelijk: donkerste)
import sys, numpy as np; from PIL import Image
from collections import deque
n=np.asarray(Image.open('natief.png')).astype(float)
PAL=[(0,0,0),(3,1,1),(27,26,25),(51,50,50),(72,72,71),(108,19,20),(162,41,41),(242,113,57),(252,208,89),
     (76,51,36),(101,69,52),(139,102,75),(198,98,92),(248,246,236),(127,56,50),(236,162,66)]
# 15 = amber (tussen oranje en geel) alleen voor de klassenkaart; wordt na de reductie op oranje/geel gezet
# achtergrond = licht en verbonden met de rand (oogwit blijft figuur)
licht=n.min(2)>=215
bg=np.zeros_like(licht); H_,W_=licht.shape
q=deque([(y,x) for y in range(H_) for x in (0,W_-1)]+[(y,x) for x in range(W_) for y in (0,H_-1)])
while q:
    y,x=q.popleft()
    if 0<=y<H_ and 0<=x<W_ and licht[y,x] and not bg[y,x]:
        bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
C=np.array(PAL[1:],float)
d=((n[:,:,None,:]-C[None,None])**2).sum(3); K=d.argmin(2)+1; K[bg]=0
np.save('natief_klas.npy',K)
# vuur: amber telt als geel (lichte punten); zalmkleurige randpixels in het haar boven de hoorns tellen als oranje
K=K.copy(); K[K==15]=8
ys,xs=np.where(K==12)
for y,x in zip(ys,xs):
    if y<15+(21-13)*2: K[y,x]=7
helder=[sum(c) for c in PAL]
def red(px,py,ox=0,oy=0):
    yy,xx=np.where(K>0); x0=xx.min()-px; y0=yy.min()-py
    W=(xx.max()-x0)//2+1; H=(yy.max()-y0)//2+1
    out=np.zeros((64,64),'uint8')
    X0=(64-W)//2+ox; Y0=63-H+oy
    for j in range(H):
        for i in range(W):
            b=K[y0+2*j:y0+2*j+2, x0+2*i:x0+2*i+2].ravel()
            f=b[b>0]
            vuur=len(f)>=1 and all(k in (5,6,7,8,15) for k in f) and Y0+j<30
            if len(f)>=2 or vuur:
                if (f==1).sum()>=2: out[Y0+j,X0+i]=1; continue
                g=f[f!=1]
                v,c=np.unique(g,return_counts=True); best=v[c==c.max()]
                vuurcel=all(k in (5,6,7,8) for k in best)
                out[Y0+j,X0+i]=(max if vuurcel else min)(best,key=lambda k:helder[k])
    return out,(W,H,X0,Y0,x0,y0)
def save(o,fn):
    im=Image.fromarray(o,'P'); p=[c for t in PAL for c in t]; p+= [0]*(768-len(p)); im.putpalette(p); im.save(fn,transparency=0)
if __name__=='__main__':
    for px in (0,1):
        for py in (0,1):
            o,info=red(px,py); save(o,'kaal_%d%d.png'%(px,py)); print(px,py,info)
