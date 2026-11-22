# Lijnkaart op spriteresolutie met kam-detectie (meting, geen tekenen): lijnscore = aandeel natieve lijnpixels binnen straal R rond het
# spritepixelcentrum; lijn als score >= T en lokaal maximum horizontaal of verticaal of diagonaal (niet-maximum-onderdrukking) -> 1 px lijnen op de modelplek.
# -> lijnscore.npy, lijnkaart.npy (64x64, geplaatst), lijnfam64.npy
import numpy as np, json, sys
from reduce import LIJN, FAM
F,OY,OX=2.9,0,0.97; pl=json.load(open('plaats.json'))
R=float(sys.argv[1]) if len(sys.argv)>1 else 1.6; T=float(sys.argv[2]) if len(sys.argv)>2 else 0.22
yy,xx=np.mgrid[0:200,0:200]
sc=np.zeros((64,64)); fam=-np.ones((64,64),int)
for Y in range(64):
    for X in range(64):
        cy=(Y-pl['dy']+0.5)*F+OY; cx=(X-pl['dx']+0.5)*F+OX
        if not(0<=cy<200 and 0<=cx<200): continue
        y0,y1=int(max(0,cy-R-1)),int(min(200,cy+R+2)); x0,x1=int(max(0,cx-R-1)),int(min(200,cx+R+2))
        m=((yy[y0:y1,x0:x1]+0.5-cy)**2+(xx[y0:y1,x0:x1]+0.5-cx)**2)<=R*R
        if m.sum()==0: continue
        l=LIJN[y0:y1,x0:x1][m]; sc[Y,X]=l.mean()
        if l.any(): ff=FAM[y0:y1,x0:x1][m]; ff=ff[ff>=0]; fam[Y,X]=np.bincount(ff).argmax()
def g(Y,X): return sc[Y,X] if 0<=Y<64 and 0<=X<64 else 0
L=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        s=sc[Y,X]
        if s<T: continue
        for (a,b),(c,d) in (((0,-1),(0,1)),((-1,0),(1,0)),((-1,-1),(1,1)),((-1,1),(1,-1))):
            if s>=g(Y+a,X+b) and s>=g(Y+c,X+d): L[Y,X]=True; break
np.save('lijnscore.npy',sc); np.save('lijnkaart.npy',L); np.save('lijnfam64.npy',fam); print(L.sum())
