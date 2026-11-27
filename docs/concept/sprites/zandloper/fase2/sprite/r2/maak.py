# Zandloper fase 2, r2: bouwt voort op r1 (zandloper_fase2_r1.png). Alleen de benoemde zones veranderen:
# 1 ogen (1-op-1 op spriteschaal), 2 vulvolume zand uit de modelhelderheid (6/5/4), 3 glas-schaduw + taille, 4 haakuiteinde ?.
import os, sys
import numpy as np; from PIL import Image
from scipy import ndimage as nd
H=os.path.dirname(os.path.abspath(__file__)); R1=os.path.join(H,'../r1')
# r1-hulpdelen (natief raster, klassen, zone, lijnen) zonder bijwerkingen: r1/maak.py tot en met stap 2
src=open(os.path.join(R1,'maak.py')).read().split('# 3) ogen')[0]
src=src.replace("HIER=os.path.dirname(os.path.abspath(__file__))","HIER=%r"%R1)
ns={}; exec(src,ns)
N,NK,LIJN,ZONE,LS,PAL,G=ns['N'],ns['NK'],ns['LIJN'],ns['ZONE'],ns['LS'],ns['PAL'],ns['G']
SPRE=ns['S'].copy()                     # r1 na stap 1-2 (zandtinten + lijnen), vóór ogen/buitenlijn
s2m,m2n,n2s,oogklasse=ns['s2m'],ns['m2n'],ns['n2s'],None
R1IM=np.array(Image.open(os.path.join(R1,'zandloper_fase2_r1.png'))).astype(int)
R=R1IM.copy(); SIL=R>0
rand=SIL&~nd.binary_erosion(SIL,structure=np.ones((3,3)))
NP,NPH=10.24,9.25
lum=N.mean(axis=2)
ZONEN={}

# ---------- 1) OGEN: 1-op-1 op spriteschaal (natieve cellen vooruit afgebeeld, geen vergroting) ----------
def ok(rgb):
    r,g,b=rgb; l=(r+g+b)/3
    if l<85: return 1
    if g>=225 and b>=140: return 14
    if g>=175 and b<85: return 15
    return None
OOGBOX=np.zeros((64,64),bool); OOGBOX[21:28,22:38]=True
OOGBOX&=SIL&~rand
# eerst terug naar de zandtint/lijnen van r1 zonder vergroot oog
R[OOGBOX]=SPRE[OOGBOX]; R[OOGBOX&(R==1)]=4
# natieve rijen/kolommen per oog; per oog één rij/kolom geschrapt (5 natief -> 4 sprite), niets hertekend
OGEN=[dict(rij=[36,38,39,40,41],kol=[39,40,41,42],x=24,y=22),       # linkeroog: rij 37 (= rij 38 zonder 2e geel) en kolom 43 geschrapt
      dict(rij=[36,37,39,40,41],kol=[47,48,49,50,51,53],x=30,y=22)] # rechteroog: rij 38 en kolom 52 (midden van de zwarte massa) geschrapt
for o in OGEN:
    for a_,nj in enumerate(o['rij']):
        for b_,ni in enumerate(o['kol']):
            k=ok(N[nj,ni]); i,j=o['x']+b_,o['y']+a_
            if k is None and N[nj,ni].mean()<120: k=2
            if k is not None and OOGBOX[j,i]: R[j,i]=k
ZONEN['ogen']=OOGBOX.copy()

# ---------- 2) VOLUME ZAND: vultint uit de modelhelderheid ----------
# veld = helderheid van de natieve vulcellen (lijncellen en achtergrond tellen niet: genormaliseerde vervaging)
vul=np.isin(NK,['L','L2','M'])&~LIJN
F=np.where(vul,lum,0.0); W=vul.astype(float)
sig=1.3
Fb=nd.gaussian_filter(F,sig)/np.maximum(nd.gaussian_filter(W,sig),1e-6)
def veld(i,j):
    x0,y0=s2m(i,j); x1,y1=s2m(i+1,j+1); a0,a1,b0,b1=m2n(x0),m2n(x1),m2n(y0),m2n(y1)
    s=w=0.0
    for nj in range(int(np.floor(b0)),int(np.ceil(b1))):
        for ni in range(int(np.floor(a0)),int(np.ceil(a1))):
            ov=(min(a1,ni+1)-max(a0,ni))*(min(b1,nj+1)-max(b0,nj))
            if ov>0 and W[nj,ni]>=0: s+=ov*Fb[nj,ni]; w+=ov
    return s/w
VUL=ZONE&SIL&~rand&~OOGBOX&np.isin(R,[4,5,6])&(LS==0)
V=np.zeros((64,64))
for j,i in zip(*np.where(VUL)): V[j,i]=veld(i,j)
T6,T5=float(sys.argv[1]) if len(sys.argv)>1 else 192, float(sys.argv[2]) if len(sys.argv)>2 else 168
R[VUL]=np.where(V[VUL]>=T6,6,np.where(V[VUL]>=T5,5,4))
ZONEN['volume']=VUL.copy()

# ---------- 3) ZANDLOPER: glas-schaduw en taille uit het model ----------
GA={10:(222,244,250),9:(160,204,224),8:(114,160,186),7:(64,94,122)}
GK=np.array(list(GA)); GV=np.array([GA[k] for k in GK],float)
glasn=((N[...,None,:]-GV)**2).sum(-1); GN=GK[glasn.argmin(-1)]
glasok=glasn.min(-1)<((N[...,None,:]-np.array(list(ns['ANK'].values()),float))**2).sum(-1).min(-1)
def meerderheid(i,j,fn):
    x0,y0=s2m(i,j); x1,y1=s2m(i+1,j+1); a0,a1,b0,b1=m2n(x0),m2n(x1),m2n(y0),m2n(y1); w={}
    for nj in range(int(np.floor(b0)),int(np.ceil(b1))):
        for ni in range(int(np.floor(a0)),int(np.ceil(a1))):
            ov=(min(a1,ni+1)-max(a0,ni))*(min(b1,nj+1)-max(b0,nj))
            t=fn(ni,nj)
            if ov>0 and t is not None: w[t]=w.get(t,0)+ov
    return max(w,key=w.get) if w else None
GLASZ=SIL&~rand&np.isin(R1IM,[8,9,10])
def glasdeel(i,j):
    x0,y0=s2m(i,j); x1,y1=s2m(i+1,j+1); a0,a1,b0,b1=m2n(x0),m2n(x1),m2n(y0),m2n(y1); w={}
    for nj in range(int(np.floor(b0)),int(np.ceil(b1))):
        for ni in range(int(np.floor(a0)),int(np.ceil(a1))):
            ov=(min(a1,ni+1)-max(a0,ni))*(min(b1,nj+1)-max(b0,nj))
            if ov>0 and glasok[nj,ni] and GN[nj,ni]!=7: w[int(GN[nj,ni])]=w.get(int(GN[nj,ni]),0)+ov
    return w
for j,i in zip(*np.where(GLASZ)):
    w=glasdeel(i,j)
    if not w: continue
    tot=sum(w.values())
    # dunne schaduwrand van het model (9/8) blijft: donkerste glastint met >= 30 % dekking wint, anders meerderheid
    donker=[t for t in (8,9) if w.get(t,0)>=0.3*tot]
    R[j,i]=donker[0] if donker else max(w,key=w.get)
# taille (x21-23, y49-51): klasse die het model daar toont
ZTOON={'L':5,'L2':6,'M':4,'B1':3,'B2':2,'K':1}
TAILLE=np.zeros((64,64),bool); TAILLE[49:52,21:24]=True; TAILLE&=SIL
def tfn(ni,nj):
    if NK[nj,ni]=='.': return None
    if glasok[nj,ni]: return int(GN[nj,ni])
    if NK[nj,ni]=='K': return 7          # donkere glasrand in het model; binnenlijn, dus glaslijn i.p.v. zwart
    return ZTOON[NK[nj,ni]]
for j,i in zip(*np.where(TAILLE)):
    t=meerderheid(i,j,tfn)
    if t: R[j,i]=t
ZONEN['zandloper']=GLASZ|TAILLE

# ---------- 4) VRAAGTEKEN: haakuiteinde ----------
HAAK=np.zeros((64,64),bool); HAAK[23:27,6:12]=True; HAAK&=SIL
for j,i in zip(*np.where(HAAK)):
    if R1IM[j,i]!=1: continue
    # buitenlijn volgens de regel; aan de lichtkant (links) selout 2, waar het model bruin toont ook 2
    links=any(not SIL[j+dy,i-1] for dy in (-1,0,1) if 0<=j+dy<64)   # transparante buur met linkercomponent = lichtkant
    t=meerderheid(i,j,lambda ni,nj: NK[nj,ni] if NK[nj,ni]!='.' else None)
    if links or t in ('B1','B2','M'): R[j,i]=2
    if not rand[j,i] and t in ('L','L2','M'): R[j,i]=ZTOON[t]
ZONEN['vraagteken']=HAAK.copy()

# ---------- losse vultintvlakjes < 3 px binnen de gewijzigde zones -> buurtint (zelfde groep) ----------
GR={3:'z',4:'z',5:'z',6:'z',8:'g',9:'g',10:'g'}
ALLE=ZONEN['volume']|ZONEN['zandloper']
for _ in range(3):
    for t in [4,5,6,8,9,10]:
        lab,k=nd.label(R==t)
        for q in range(1,k+1):
            m=lab==q
            if m.sum()>=3 or not (m&ALLE).all(): continue
            for j,i in zip(*np.where(m)):
                b=[R[jj,ii] for jj in range(j-1,j+2) for ii in range(i-1,i+2) if 0<=jj<64 and 0<=ii<64 and R[jj,ii]!=t and GR.get(R[jj,ii])==GR[t]]
                if b: R[j,i]=max(set(b),key=b.count)

assert ((R>0)==SIL).all(), 'silhouet veranderd'
ALLZ=np.zeros((64,64),bool)
for z in ZONEN.values(): ALLZ|=z
assert (R[~ALLZ]==R1IM[~ALLZ]).all(), 'wijziging buiten de zones'
im=Image.fromarray(R.astype('uint8'),'P'); p=[]
for c in PAL: p+=list(c)
im.putpalette(p+[0]*(768-len(p))); im.save(os.path.join(H,'zandloper_fase2_r2.png'),transparency=0)
np.save(os.path.join(H,'r2.npy'),R)
print('kleuren',len(set(R[R>0].ravel())),'telling',np.bincount(R.ravel(),minlength=16)[1:])
for z,m in ZONEN.items(): print('%-11s gewijzigd t.o.v. r1: %d (zone %d px)'%(z,(m&(R!=R1IM)).sum(),m.sum()))
print('totaal gewijzigd',(R!=R1IM).sum())
