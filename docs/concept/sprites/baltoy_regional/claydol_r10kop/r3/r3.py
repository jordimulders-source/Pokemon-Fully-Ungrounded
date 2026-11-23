# Ronde 3 (basis r2 A): nieuwe tint 10 (warm, lichtheid ~110) tussen 5 en 6; kop-toonstructuur van r10 terug in de onderkop,
# meerstaps tintbanden (2-3-4-5-10, 6 als rand), barsten uit r10; linkeroog rond (buitenste ringkolom + 1 binnenkolom geschrapt);
# neus + rechteroog als in g3r5 (oogring = neusschaduw, x 27-28). Silhouet/krans/punt/staven diff 0, lijf alleen tinten.
import os, sys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'..')); sys.path.insert(0,os.path.join(H,'../r2'))
from lagen import masks, G as G3, PAL as PAL0
import r2
from r2 import oog_asset, NEUS, banden, LIJF, ontspikkel, R1, KIN
NIEUW=(120,108,90)                       # tint 10: lichtheid 109,6 (5 = 136, 6 = 83)
PAL=list(PAL0[:30])+list(NIEUW)+list(PAL0[33:])
yy,xx=np.mgrid[0:64,0:64]
DONKER=[1,2,3,4,5,10,6,7]                 # licht -> donker
rang={t:i for i,t in enumerate(DONKER)}
def donkerst(a,b): return np.where(np.vectorize(rang.get)(a)>=np.vectorize(rang.get)(b),a,b)

# r10-kop zoals in ronde 1 op ons raster gelegd (modeltonen), voor de toonstructuur van de onderkop en de barsten
import maak
_S,_b,_info=maak.bouw(maak.RZ,maak.CZ,ox=12,oy=7)
RM=np.full((64,64),'.'); _R=_info[0]
RM[7:7+_R.shape[0],12:12+_R.shape[1]]=_R
RTOON={'h':2,'l':3,'m':4,'d':5}

def plak(S,A,x0,y0,mag,M):
    for j in range(A.shape[0]):
        for i in range(A.shape[1]):
            y,x=y0+j,x0+i
            if A[j,i]>=0 and mag[y,x]: S[y,x]=A[j,i]; M[y,x]=True

def rode_golf():
    top={}
    for x,t in {12:17,13:16,14:15,15:14,16:13,17:13,18:13,19:14,20:15,21:16,22:17,23:18}.items(): top[x]=t   # boog om oogmidden 17
    top[24]=19; top[25]=19                                                                                    # V om neusmidden 24.5
    for x,t in {26:18,27:17,28:16,29:15,30:14,31:13,32:13,33:13,34:13,35:13,36:14,37:15}.items(): top[x]=t    # boog om oogmidden 33
    band={38:16,39:16,40:16,41:17,42:17,43:17,44:17,45:18,46:18,47:18,48:18,49:19,50:19,51:19,52:19,53:20}
    P={}
    for x,t in top.items():
        for d in range(3): P[(t+d,x)]=8 if (d==0 and x<=36) else 9
    for x,t in band.items():
        for d in range(3): P[(t+d,x)]=9
    return P

KG=[0.42,0.85,1.12,1.42,1.66]; KT=[2,3,4,5,10,6]
BARSTEN=[(10,28),(11,27),(12,27),(13,26),            # linksboven (r10)
         (31,44),(32,45),(33,46),(34,47),(34,48),     # rechtsonder (r10: x 45-49, y 32-35)
         (26,48),(27,49)]                             # rechts naast de band (r10 'g' op y 26)
def bouw():
    S=R1.copy(); M={k:np.zeros((64,64),bool) for k in ('neus','oog','rood','barst')}
    # 1. kopsteen: meerstaps banden (licht linksboven); onderkop (y>=26): donkerste van banden en r10-structuur
    K=banden(31.5,23.5,22.6,16.5,-0.45,-0.6,KG,KT)
    R=np.vectorize(lambda c: RTOON.get(c,0))(RM)
    onder=(yy>=30)&(R>0)
    # onderkop: r10-tonen (3/4/5 in banden met de bolling mee); alleen de rand (10, 6) komt uit de banden
    K=np.where(onder&~np.isin(K,(10,6)),np.where(R==2,3,R),K)
    S[KIN]=K[KIN]
    # 2. barsten: heldere lijn, een stap donkerder (2->4, 3->5, 4->5, 5->10, 10->6)
    for (y,x) in BARSTEN:
        if KIN[y,x]: S[y,x]={2:4,3:5,4:10,5:10,10:6,6:6}[S[y,x]]; M['barst'][y,x]=True
    # 3. neus en rechteroog als blok uit g3r5 (zelfde onderlinge plek: oogring x 27-28 = neusschaduw)
    plak(S,NEUS,22,22,KIN,M['neus'])
    plak(S,oog_asset(),27,18,KIN,M['oog'])
    # 4. linkeroog: buitenste kolom van de dubbele ring (x27) + binnenkolom x35 geschrapt -> 11 breed, ring rond
    plak(S,oog_asset(weg_k=(27,35)),12,17,KIN,M['oog'])
    # 5. rode golf
    for (y,x),c in rode_golf().items():
        if KIN[y,x]: S[y,x]=c; M['rood'][y,x]=True
    # 6. lijf: banden met de nieuwe tint in de sikkel
    vlak=LIJF&np.isin(R1,(3,4,5))&(yy<=60)
    torso=banden(32,50,13,10.5,-0.55,-0.55,[0.35,1.0,1.3,1.62],[2,3,5,10,6])
    armL=banden(19,46.5,4.5,4.2,-0.5,-0.6,[0.45,1.05,1.4,1.7],[2,3,5,10,6])
    armR=banden(46.5,46.5,4.5,4.2,-0.6,-0.6,[0.95,1.35,1.6],[5,10,10,6])
    T=torso.copy()
    T[(xx<=21)&(yy<=51)]=armL[(xx<=21)&(yy<=51)]
    T[(xx>=44)&(yy<=51)]=armR[(xx>=44)&(yy<=51)]
    hals=(yy<=42); T[hals]=np.where(xx[hals]>=40,10,5)
    S[vlak]=T[vlak]
    # 7. spikkels (< 3 px) uit de banden weg
    steen=KIN&~(M['neus']|M['oog']|M['rood']|M['barst'])
    ontspikkel(S,steen|vlak)
    return S,vlak

def check(S,vlak):
    assert ((S>0)==(G3>0)).all(),'silhouet'
    assert not ((S!=R1)&~KIN&~vlak).any(),'buiten kop/lijfvlak'
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    S,v=bouw(); check(S,v); save(S,os.path.join(H,'claydol_r10kop_r3'))
    print('   '+''.join(str(x%10) for x in range(8,56)))
    for y in range(6,61): print('%2d '%y+''.join('.' if q==0 else ('X' if q==10 else str(q)) for q in S[y,8:56]))
