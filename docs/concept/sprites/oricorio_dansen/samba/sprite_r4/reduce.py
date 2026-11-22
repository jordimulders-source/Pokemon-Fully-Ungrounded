# natief (200x200) -> sprite, schaal f (niet-geheel), geen gemiddelden: elke spritepixel = een modelklasse of een modellijn.
#  1. lijnen: elke natieve lijnpixel (k-means 0 zwart / 1,3 donkergroen / 2,8 donkergeel / 4 donkerroze) valt in één spritepixel;
#     spritepixels met >= nl lijnpixels = lijnkandidaat; daarna verdund tot 1 px (skimage thin) -> de modellijnen op hun plek.
#  2. dekking: aandeel dekkende natieve pixels >= td, of lijn.
#  3. vulling: meest voorkomende vulklasse (zonder lijnpixels) in het blok; gelijkspel: donkerste.
#  4. lijnfamilie per lijnpixel (meest voorkomend in het blok): 0 zwart, 1 donkergroen, 2 donkergeel, 3 donkerroze.
import numpy as np, sys
from skimage.morphology import thin
from palet import NAMEN, KL
lab=np.load('km_lab.npy'); I={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=I[v]
LIJN=np.isin(lab,[0,1,2,3,4,8])
FAM=np.full(lab.shape,-1); FAM[lab==0]=0; FAM[np.isin(lab,[1,3])]=1; FAM[np.isin(lab,[2,8])]=2; FAM[lab==4]=3
RANG={'O':9,'G4':8,'Y3':7,'K3':7,'B2':7,'G3':5,'B1':5,'K2':4,'Y2':4,'G2':3,'G1':1,'Y1':1,'K1':1,'W':0}
def grenzen(n,f,o):
    g=np.floor(o+np.arange(0,int((n-o)/f)+1)*f).astype(int); return g[g<=n]
def red(f,oy,ox,nl=1,td=0.45,dun=True):
    gy=grenzen(cl.shape[0],f,oy); gx=grenzen(cl.shape[1],f,ox)
    H,W=len(gy)-1,len(gx)-1
    o=np.zeros((H,W),int); fam=-np.ones((H,W),int); lc=np.zeros((H,W),int); cov=np.zeros((H,W))
    for j in range(H):
        for i in range(W):
            sl=(slice(gy[j],gy[j+1]),slice(gx[i],gx[i+1]))
            b=cl[sl].ravel(); l=LIJN[sl].ravel(); n=len(b)
            cov[j,i]=(b>0).sum()/n; lc[j,i]=l.sum()
            if l.sum(): ff=FAM[sl].ravel(); ff=ff[ff>=0]; fam[j,i]=np.bincount(ff).argmax()
            v=b[(b>0)&~l]
            if len(v):
                u,c=np.unique(v,return_counts=True); m=c.max()
                o[j,i]=max([x for x,cc in zip(u,c) if cc==m],key=lambda x:RANG[NAMEN[x]])
    lijn=thin(lc>=nl) if dun else (lc>=nl)
    dek=(cov>=td)|lijn
    # vulpixel zonder eigen vulkleur (blok was alleen lijn): kleur van de meest voorkomende vulbuur
    uit=np.zeros((H,W),int)
    for j in range(H):
        for i in range(W):
            if not dek[j,i]: continue
            if lijn[j,i]: uit[j,i]=I['O']; continue
            if o[j,i]: uit[j,i]=o[j,i]; continue
            nb=[o[y,x] for y,x in ((j-1,i),(j+1,i),(j,i-1),(j,i+1)) if 0<=y<H and 0<=x<W and o[y,x]]
            uit[j,i]=max(set(nb),key=nb.count) if nb else I['O']
    return uit,fam,lijn
if __name__=='__main__':
    f,oy,ox=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])
    o,fam,l=red(f,oy,ox); np.save('reductie.npy',o); np.save('lijnfam.npy',fam); ys,xs=np.where(o>0)
    print(o.shape,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(o>0).sum())
