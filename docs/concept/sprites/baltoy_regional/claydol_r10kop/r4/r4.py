# Ronde 4 (basis r3): ogen + neus als blok d px omlaag (d=1/2), golf zakt mee en loopt rechts eerst omlaag om het rechteroog;
# neus 1-op-1 uit g3r5 incl. lengte en punt (y 22-34); kop en lijf: sikkels (verschoven ellipsen) in 2/3/5/10/6, harde grenzen.
import os, sys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
for p in ('..','../r2','../r3'): sys.path.insert(0,os.path.join(H,p))
from lagen import G as G3
from r2 import oog_asset, LIJF, ontspikkel, R1, KIN
from r3 import PAL
yy,xx=np.mgrid[0:64,0:64]

# neus g3r5: per rij de kolommen (lijn x22, neusrug-licht x23, lijf 24-26, schaduw 27; punt smaller tot y 34)
NEUS_RIJEN={22:(22,27),23:(22,27),24:(22,27),25:(22,27),26:(22,27),27:(22,27),28:(22,27),29:(22,27),30:(22,27),
            31:(23,27),32:(23,26),33:(24,26),34:(24,26)}
def plak(S,A,x0,y0,M):
    for j in range(A.shape[0]):
        for i in range(A.shape[1]):
            y,x=y0+j,x0+i
            if A[j,i]>=0 and KIN[y,x]: S[y,x]=A[j,i]; M[y,x]=True

def ellips_buiten(cx,cy,rx,ry): return ((xx-cx)/rx)**2+((yy-cy)/ry)**2>1
def sikkels(cx,cy,rx,ry,basis,stappen,licht=None):
    """basis-tint; per stap (sx,sy,tint): alles BUITEN de vorm-ellips verschoven naar het licht = die tint (sikkel rechtsonder);
       licht=(cx,cy,rx,ry,tint): hooglicht-ellips linksboven"""
    T=np.full((64,64),basis)
    for sx,sy,t in stappen: T[ellips_buiten(cx+sx,cy+sy,rx,ry)]=t
    if licht: T[~ellips_buiten(*licht[:4])]=licht[4]
    return T

def golf_pixels(d):
    """middellijn van de golf (d=0), penseel straal 1 -> 3 px dik; 8 = bovenste pixel per kolom aan de lichtkant (x<=36)"""
    P=[(11,18),(12,18),(13,17),(14,16),(15,15),(16,14),(18,14),(19,15),(20,16),(21,17),(22,18),(23,19),(24,20),(25,20),
       (26,19),(27,18),(28,17),(29,16),(30,15),(31,14),(35,14),(36,15),(37,16),(38,17),(39,18),
       (40,19),(41,20),(41.5,21),(41.5,22),(42,23),(43,24),(44,24.6),(46,25),(48,25.3),(53,25.8)]
    P=[(x,y+d) for x,y in P]
    M=np.zeros((64,64),bool)
    for (x0,y0),(x1,y1) in zip(P[:-1],P[1:]):
        vx,vy=x1-x0,y1-y0; L2=vx*vx+vy*vy
        t=np.clip(((xx-x0)*vx+(yy-y0)*vy)/L2,0,1)
        M|=((xx-(x0+t*vx))**2+(yy-(y0+t*vy))**2)<=1.0001
    C=np.where(M,9,0)
    for x in range(64):
        ys=np.where(M[:,x])[0]
        if len(ys) and x<=36: C[ys[0],x]=8
    return C

BARSTEN=[(10,28),(11,27),(12,27),(13,26),(31,44),(32,45),(33,46),(34,47),(34,48)]
STAP={2:3,3:5,5:10,10:6,6:6,4:5}

def kop(S,d,M):
    T=sikkels(31.5,23.5,22.6,16.5,3,[(-7,-5,5),(-3.5,-2.5,10),(-1.2,-0.8,6)],licht=(21,11,13,6.5,2))
    S[KIN]=T[KIN]
    for y,x in BARSTEN:
        if KIN[y,x]: S[y,x]=STAP[S[y,x]]; M['barst'][y,x]=True

def lijf(S):
    vlak=LIJF&np.isin(R1,(3,4,5))&(yy<=61)
    torso=sikkels(32.5,49.5,12.5,7.5,3,[(-8,-5,5),(-4,-2.5,10),(-1.5,-1,6)],licht=(26,45,5,2.5,2))
    armL=sikkels(18.5,46.5,4,4,3,[(-2.5,-2,5),(-1.2,-1,10)],licht=(17,44.5,2.2,1.5,2))
    armR=sikkels(47,46.5,4,4,3,[(-3,-2.5,5),(-1.5,-1.2,10)])
    voetL=sikkels(26,57,4.5,2.5,5,[(-1.5,-1.2,10)],licht=(24.5,55.5,2.5,1,3))
    voetR=sikkels(37,57.5,7,3,5,[(-2,-1.5,10)],licht=(34,55.5,3.5,1,3))
    T=torso.copy()
    for m,A in (((xx<=21)&(yy<=51),armL),((xx>=44)&(yy<=51),armR),((yy>=55)&(xx<=30),voetL),((yy>=55)&(xx>=31),voetR)):
        T[m]=A[m]
    hals=(yy<=42); T[hals]=np.where(xx[hals]>=38,10,5)
    S[vlak]=T[vlak]
    # selout: lijnpixels (7) op de silhouetrand aan de lichtkant (transparant links of boven, niet rechts/onder) -> 6
    sel=np.zeros((64,64),bool)
    for y,x in zip(*np.where(LIJF&(R1==7)&(yy>=40))):
        tl=(G3[y,x-1]==0) or (G3[y-1,x]==0); br=(G3[y,x+1]==0) or (G3[y+1,x]==0)
        if tl and not br and x<=32: sel[y,x]=True
    S[sel]=6
    return vlak,sel

def bouw(d=1):
    S=R1.copy(); M={k:np.zeros((64,64),bool) for k in ('neus','oog','rood','barst')}
    kop(S,d,M)
    N=-np.ones((13,6),int)
    for y,(a,b) in NEUS_RIJEN.items():
        for x in range(a,b+1): N[y-22,x-22]=G3[y,x]
    plak(S,N,22,22+d,M['neus'])
    plak(S,oog_asset(),27,18+d,M['oog'])
    plak(S,oog_asset(weg_k=(27,35)),12,17+d,M['oog'])
    C=golf_pixels(d)
    for y,x in zip(*np.where((C>0)&KIN)): S[y,x]=C[y,x]; M['rood'][y,x]=True
    vlak,sel=lijf(S)
    steen=KIN&~(M['neus']|M['oog']|M['rood']|M['barst'])
    ontspikkel(S,steen|vlak)
    return S,vlak|sel

def check(S,v):
    assert ((S>0)==(G3>0)).all(),'silhouet'
    assert not ((S!=R1)&~KIN&~v).any(),'buiten kop/lijf'
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    for d in (1,2):
        S,v=bouw(d); check(S,v); save(S,os.path.join(H,'proef_d%d'%d))

def lever():
    for d,naam in ((1,'claydol_r10kop_r4'),(2,'claydol_r10kop_r4_ogen2px')):
        S,v=bouw(d); check(S,v); save(S,os.path.join(H,naam))
