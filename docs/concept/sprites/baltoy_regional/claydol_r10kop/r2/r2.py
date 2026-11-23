# Ronde 2: neus + ogen uit g3r5 palet B als asset (1-op-1), rode golf netjes (8/9-opbouw),
# kop en lijf opnieuw getint met harde, vormvolgende tintvlakken (licht linksboven, sikkel rechtsonder).
# Silhouet, krans, punt, staven diff 0; lijf alleen tinten van vlakpixels (3/4/5), tekening (6/7/9) blijft.
import os, sys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'..'))
from lagen import masks, G as G3, PAL
R1=np.array(Image.open(os.path.join(H,'../claydol_r10kop.png'))).astype(int)
kop,KIN,bol,punt=masks()
yy,xx=np.mgrid[0:64,0:64]

# ---------- assets uit g3r5 palet B ----------
OOG_RIJEN={21:(32,36),22:(31,37),23:(30,38),24:(29,39),25:(28,39),26:(27,39),27:(27,39),28:(27,39),29:(27,39),30:(27,38),31:(28,37),32:(32,35)}
def oog_asset(weg_k=(),dubbel_k=(),dubbel_r=()):
    """middelste oog van g3r5 (x 27-39, y 21-32) als array (-1 = geen asset); kolommen schrappen/herhalen, rijen herhalen"""
    A=-np.ones((12,13),int)
    for y,(a,b) in OOG_RIJEN.items():
        for x in range(a,b+1): A[y-21,x-27]=G3[y,x]
    cols=[]
    for x in range(27,40):
        if x in weg_k: continue
        cols.append(x-27)
        if x in dubbel_k: cols.append(x-27)
    rows=[]
    for y in range(21,33):
        rows.append(y-21)
        if y in dubbel_r: rows.append(y-21)
    return A[np.ix_(rows,cols)]
NEUS=G3[22:32,22:28]          # neus g3r5 x 22-27, y 22-31

NEUSM=np.zeros((64,64),bool); OOGM=np.zeros((64,64),bool); ROODM=np.zeros((64,64),bool); BARSTM=np.zeros((64,64),bool)
def plak(S,A,x0,y0,mag,M=None):
    for j in range(A.shape[0]):
        for i in range(A.shape[1]):
            y,x=y0+j,x0+i
            if A[j,i]>=0 and mag[y,x]:
                S[y,x]=A[j,i]
                if M is not None: M[y,x]=True

# ---------- tintvlakken ----------
def banden(cx,cy,rx,ry,lx,ly,grenzen,tonen):
    """s = afstand tot het lichtpunt (lx,ly) in genormaliseerde ellips-coördinaten; harde grenzen"""
    u=(xx-cx)/rx; v=(yy-cy)/ry; s=np.sqrt((u-lx)**2+(v-ly)**2)
    T=np.full((64,64),tonen[-1])
    for g,t in reversed(list(zip(grenzen,tonen[:-1]))): T[s<g]=t
    return T

DIK=3
def rode_golf(oog='A'):
    """bovenste rij per kolom (top) en dikte; symmetrische V om neusmidden x=24.5 (neus x 22-27)"""
    top={}
    # linkerboog boven het linkeroog (oog x 12-22, midden 17): symmetrisch om 17
    for x,t in {12:17,13:16,14:15,15:14,16:13,17:13,18:13,19:14,20:15,21:16,22:17,23:18}.items(): top[x]=t
    # V: punt x 24-25, symmetrisch om het neusmidden 24.5 (benen 23/26, 22/27, ...)
    top[24]=19; top[25]=19
    # rechterboog boven het rechteroog (oog x 28-40, midden 34.5): symmetrisch om 34.5
    for x,t in {26:18,27:17,28:16,29:15,30:14,31:14,32:13,33:13,34:13,35:13,36:13,37:13,38:14,39:14,40:15,41:16}.items(): top[x]=t
    # band om de zijkant: loopt vloeiend uit de boog, 3 dik, licht dalend
    band={42:17,43:17,44:17,45:18,46:18,47:18,48:18,49:19,50:19,51:19,52:19,53:20}
    P={}
    for x,t in top.items():
        for d in range(DIK): P[(t+d,x)]=8 if (d==0 and x<=38) else 9
    for x,t in band.items():
        for d in range(3): P[(t+d,x)]=9
    return P

def _comp(M,start):
    out=np.zeros(M.shape,bool); st=[start]; out[start]=True
    while st:
        a,b=st.pop()
        for c,d in ((a+1,b),(a-1,b),(a,b+1),(a,b-1),(a+1,b+1),(a-1,b-1),(a+1,b-1),(a-1,b+1)):
            if 0<=c<64 and 0<=d<64 and M[c,d] and not out[c,d]: out[c,d]=True; st.append((c,d))
    return out
LIJF=_comp(G3>0,(50,30))&(yy>=40)          # lijf = hoofdcomponent onder de kop; staven zijn losse componenten
def lijf_tinten(S):
    """alleen vlakpixels (3,4,5) van het lijf krijgen een nieuwe tint; 6/7/9 (trapjes, haken, lijn) blijven"""
    vlak=LIJF&np.isin(R1,(3,4,5))&(yy<=60)
    torso=banden(32,50,13,10.5,-0.55,-0.55,[0.35,1.0,1.55],[2,3,5,6])
    armL=banden(19,46.5,4.5,4.2,-0.5,-0.6,[0.45,1.1,1.6],[2,3,5,6])
    armR=banden(46.5,46.5,4.5,4.2,-0.6,-0.6,[1.25],[5,6])
    T=torso.copy()
    T[(xx<=21)&(yy<=51)]=armL[(xx<=21)&(yy<=51)]
    T[(xx>=44)&(yy<=51)]=armR[(xx>=44)&(yy<=51)]
    hals=(yy<=42); T[hals]=np.where(xx[hals]>=40,6,5)      # hals in de schaduw van de kop
    S[vlak]=T[vlak]
    return vlak

KG=[0.62,1.12,1.55]
def bouw(oog='A'):
    for M in (NEUSM,OOGM,ROODM,BARSTM): M[:]=False
    S=R1.copy()
    # 1. kopsteen opnieuw: ellips van de kop, licht linksboven
    K=banden(31.5,23.5,22.6,16.5,-0.45,-0.6,KG,[2,3,5,6])
    S[KIN]=K[KIN]
    STEEN=KIN.copy()
    # 2. barsten (posities uit r10/r1), als heldere lijn een tint donkerder dan de steen eronder
    for (y,x) in [(10,28),(11,27),(12,27),(13,26),(31,44),(32,45),(33,46)]:
        if KIN[y,x]: S[y,x]={2:4,3:5,5:6,6:6}[S[y,x]]; BARSTM[y,x]=True
    # 3. neus
    plak(S,NEUS,22,22,KIN,NEUSM)
    # 4. ogen
    if oog=='A':
        plak(S,oog_asset(),28,18,KIN,OOGM)                         # rechts 13x12 (x 28-40); linkerring valt op de neusschaduw zoals in g3r5
        plak(S,oog_asset(weg_k=(34,35)),12,17,KIN,OOGM)            # links 2 binnenkolommen smaller: 11x12 (x 12-22); rechterring = neuslijn
    else:
        plak(S,oog_asset(dubbel_k=(33,),dubbel_r=(24,25,28)),28,17,KIN,OOGM)   # rechts 14x15
        plak(S,oog_asset(weg_k=(34,35),dubbel_r=(24,)),12,17,KIN,OOGM)        # links 11x13
    # 5. rode golf
    for (y,x),c in rode_golf(oog).items():
        if KIN[y,x]: S[y,x]=c; ROODM[y,x]=True
    # 6. lijf
    vlak=lijf_tinten(S)
    # 7. spikkels uit de tintbanden weg (alleen steen/lijfvlak, niet ogen/neus/rood/barsten)
    STEEN&=~(NEUSM|OOGM|ROODM|BARSTM)
    ontspikkel(S,STEEN|vlak)
    return S,vlak

def ontspikkel(S,toegewezen):
    """tintvlakjes < 3 px die door de tintbanden ontstaan (alleen toegewezen pixels) -> meest voorkomende toegewezen buurtint"""
    seen=np.zeros(S.shape,bool); log=[]
    for y,x in zip(*np.where(toegewezen)):
        if seen[y,x]: continue
        v=S[y,x]; st=[(y,x)]; comp=[]; seen[y,x]=True
        while st:
            a,b=st.pop(); comp.append((a,b))
            for c,d in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if 0<=c<64 and 0<=d<64 and not seen[c,d] and S[c,d]==v and toegewezen[c,d]: seen[c,d]=True; st.append((c,d))
        if len(comp)<3:
            for a,b in comp:
                nb=[S[c,d] for c,d in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)) if toegewezen[c,d] and S[c,d]!=v]
                if nb: S[a,b]=max(set(nb),key=nb.count); log.append((a,b))
    return log
def check(S,vlak):
    assert ((S>0)==(G3>0)).all(),'silhouet'
    assert not ((S!=R1)&~KIN&~vlak).any(),'buiten kop/lijfvlak'
    assert set(np.unique(S))<=set(range(10))
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    for o in 'AB':
        S,v=bouw(o); check(S,v); save(S,os.path.join(H,'proef_'+o))

def lever():
    out={}
    for o,naam in (('A','claydol_r10kop_r2'),('B','claydol_r10kop_r2_B_grote_ogen')):
        S,v=bouw(o); check(S,v); save(S,os.path.join(H,naam)); out[o]=(S,v)
    return out
