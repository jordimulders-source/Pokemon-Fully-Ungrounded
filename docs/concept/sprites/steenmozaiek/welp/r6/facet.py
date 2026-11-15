# Facetkaart uit het model: per natieve modelpixel de toonklasse (0 donker, 1 mid, 2 licht, 3 hooglicht) van het bruin,
# gemeten op helderheid (dalen in het histogram: 78 / 119 / 150), 3x3-modusfilter tegen ruis, dan per spritepixel de
# meerderheidsklasse van zijn vlak modelpixels (zelfde afbeelding als lever.py: offset 2, schaal 3,3).
import numpy as np
from PIL import Image
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
Lm=n@np.array([0.299,0.587,0.114]); r,g,b=n[...,0],n[...,1],n[...,2]
brown=(r>g+12)&(r>b+8)&(Lm>45)&(Lm<200)&~((r>205)&(g<160))
T=(78,119,150)
cls=np.full(Lm.shape,-1); cls[brown]=np.digitize(Lm[brown],T)
def modus(c,it=2):
    for _ in range(it):
        o=c.copy()
        for y in range(1,c.shape[0]-1):
            for x in range(1,c.shape[1]-1):
                if c[y,x]<0: continue
                w=c[y-1:y+2,x-1:x+2].ravel(); w=w[w>=0]
                v=np.bincount(w,minlength=4)
                if v.max()>=5: o[y,x]=v.argmax()
        c=o
    return c
cls=modus(cls)
X0=Y0=2; s=3.3; H,W=45,50
def facetkaart():
    out=np.full((H,W),-1); lum=np.zeros((H,W))
    for j in range(H):
        for i in range(W):
            y0,y1=int(round(Y0+j*s)),int(round(Y0+(j+1)*s)); x0,x1=int(round(X0+i*s)),int(round(X0+(i+1)*s))
            w=cls[y0:y1,x0:x1].ravel(); w=w[w>=0]
            if len(w): out[j,i]=np.bincount(w,minlength=4).argmax(); lum[j,i]=Lm[y0:y1,x0:x1][cls[y0:y1,x0:x1]>=0].mean()
    return out,lum
if __name__=='__main__':
    f,l=facetkaart(); np.save('facet.npy',f); np.save('facetlum.npy',l)
    for row in f: print(''.join('.SMLH'[v+1] for v in row))
    for k in range(4): print(k,(f==k).sum())
