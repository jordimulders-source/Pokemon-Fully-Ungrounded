# reductie.py: kale 2x-reductie van natief.png -> kaal_{px}{py}.png (P, 64x64) + klassenkaart natief_klas.npy
# klasse per natieve pixel = dichtstbijzijnde modelkleur (palet gemeten op het model, k-means + regio-histogrammen);
# spritepixel = figuur als >=2 van de 4 natieve pixels figuur zijn (vuur: al vanaf 1); kleur: zwart als >=2 zwart,
# anders meest voorkomende klasse (gelijk: donkerste, in vuur: lichtste)
import numpy as np; from PIL import Image
from collections import deque
n=np.asarray(Image.open('natief.png')).astype(float)
PAL=[(0,0,0),(3,1,1),(22,22,22),(40,40,40),(50,40,34),(80,64,52),(124,97,77),(218,184,134),(240,229,186),
     (105,20,22),(138,30,34),(205,75,50),(240,135,62),(250,205,110),(172,52,43)]
# 14 = middenrood alleen voor de klassenkaart (wordt rood/oranjerood in schoon.py)
FIRE=(9,10,11,12,13,14)
H_,W_=n.shape[:2]
licht=n.min(2)>=215
# achtergrond: licht en verbonden met de rand, plus ingesloten witte modelgaten (hoornkrul, staartkrul) van >=4 px
# die echt wit zijn (zonder gele zweem); oogglans/crème blijft figuur
wit=(n.min(2)>=225)&((n.max(2)-n.min(2))<18)
def comp(m):
    seen=np.zeros_like(m); out=[]
    for y,x in zip(*np.where(m)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=1; c=[]
        while st:
            a,b=st.pop(); c.append((a,b))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                p,q=a+dy,b+dx
                if 0<=p<H_ and 0<=q<W_ and m[p,q] and not seen[p,q]: seen[p,q]=1; st.append((p,q))
        out.append(c)
    return out
bg=np.zeros_like(licht)
for c in comp(licht):
    if any(a in (0,H_-1) or b in (0,W_-1) for a,b in c): 
        for a,b in c: bg[a,b]=True
gaten=[]
for c in comp(wit&~bg):
    if len(c)>=4:
        gaten.append((len(c),min(b for a,b in c),min(a for a,b in c)))
        for a,b in c: bg[a,b]=True
print('ingesloten modelgaten (px, x, y):',gaten)
C=np.array(PAL[1:],float)
d=((n[:,:,None,:]-C[None,None])**2).sum(3); K=d.argmin(2)+1; K[bg]=0
np.save('natief_klas.npy',K)
helder=[sum(c) for c in PAL]
def red(px,py):
    yy,xx=np.where(K>0); x0=xx.min()-px; y0=yy.min()-py
    W=(xx.max()-x0)//2+1; H=(yy.max()-y0)//2+1
    out=np.zeros((64,64),'uint8')
    X0=(64-W)//2; Y0=63-H
    for j in range(H):
        for i in range(W):
            b=K[max(y0+2*j,0):y0+2*j+2, max(x0+2*i,0):x0+2*i+2].ravel()
            f=b[b>0]
            vuur=len(f)>=1 and all(k in FIRE for k in f)
            if len(f)>=2 or vuur:
                if (f==1).sum()>=2: out[Y0+j,X0+i]=1; continue
                g=f[f!=1] if (f!=1).any() else f
                v,c=np.unique(g,return_counts=True); best=v[c==c.max()]
                vuurcel=all(k in FIRE for k in best)
                out[Y0+j,X0+i]=(max if vuurcel else min)(best,key=lambda k:helder[k])
    return out,(W,H,X0,Y0,x0,y0)
def save(o,fn):
    im=Image.fromarray(o,'P'); p=[c for t in PAL for c in t]; p+= [0]*(768-len(p)); im.putpalette(p); im.save(fn,transparency=0)
if __name__=='__main__':
    for px in (0,1):
        for py in (0,1):
            o,info=red(px,py); save(o,'kaal_%d%d.png'%(px,py)); print(px,py,info)
