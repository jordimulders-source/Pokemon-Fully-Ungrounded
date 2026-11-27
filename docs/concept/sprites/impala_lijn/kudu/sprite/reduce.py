# Kale reductie van een (eventueel bewerkt) 1024-model naar spritecellen, zoals impala/sprite/reduce.py:
# voorgrond = alles behalve wit verbonden met de rand (floodfill); per cel alpha >= 0.45; cel met >= 50% zwarte
# modellijn (lum < 70) = lijn (drempel LT=0.25: de modellijn is 1 natief px = ±5 modelpx, ±31% van een cel van 16) (donkerste modelkleur), anders vlakgemiddelde van de niet-lijnpixels -> dichtstbijzijnde
# kleur uit het modelpalet (k-means K=15 op de voorgrond van r3b, vast voor alle varianten).
import numpy as np
from PIL import Image
from scipy import ndimage as nd
def fgmask(a):
    wit=a.min(2)>=232; lab,_=nd.label(wit)
    rand=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
    return ~np.isin(lab,list(rand))
def palet(a,fg,K=15,seed=3):
    nat=a[fg][::7].astype(float); rng=np.random.default_rng(seed); C=nat[rng.choice(len(nat),K,replace=False)]
    for _ in range(60):
        lab=((nat[:,None]-C[None])**2).sum(2).argmin(1)
        C=np.array([nat[lab==k].mean(0) if (lab==k).any() else C[k] for k in range(K)])
    return C[np.argsort((C*[.299,.587,.114]).sum(1))]
def reduceer(a,fg,C,y0,x0,p,H,W,LT=0.25):
    a=a.astype(float); lum=(a*[.299,.587,.114]).sum(2); lijn=fg&(lum<70)
    out=-np.ones((H,W),int)
    for j in range(H):
        for i in range(W):
            xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
            f=fg[ya:yb,xa:xb]
            if f.size==0 or f.mean()<0.45: continue
            l=lijn[ya:yb,xa:xb][f]
            if l.mean()>=LT: out[j,i]=0; continue
            m=a[ya:yb,xa:xb][f][~l].mean(0); out[j,i]=((C-m)**2).sum(1).argmin()
    return out
def opslaan(L,C,pad,ox=None,oy=None):
    H,W=L.shape; ox=(64-W)//2 if ox is None else ox; oy=64-H if oy is None else oy
    img=np.zeros((64,64),'uint8')
    for j in range(H):
        for i in range(W):
            if L[j,i]>=0: img[oy+j,ox+i]=L[j,i]+1
    pal=[0,0,0]+[int(v) for c in C for v in c]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0); return img

def buitenlijn(L):
    """technisch: buitenlijn dicht (opake cel met een transparante 4-buur -> lijnkleur 0). Geeft (nieuw, aantal)."""
    H,W=L.shape; o=L.copy(); n=0
    for j in range(H):
        for i in range(W):
            if L[j,i]<=0: continue
            if any(not(0<=j+dy<H and 0<=i+dx<W) or L[j+dy,i+dx]<0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): o[j,i]=0; n+=1
    return o,n
