# Zandloper fase 2, r1: kale reductie 0,80 (maten/kaal_0.80.png) + reparaties per pixel uit het natieve modelraster.
# Niets getekend: tinten/lijnen komen uit het natieve raster (pitch 10,24), ogen 1-op-1 uit het model (125 %),
# buitenlijn = bestaande randpixels omgekleurd (silhouet = kale reductie).
import os, sys, json
import numpy as np; from PIL import Image
from scipy import ndimage as nd
HIER=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HIER,'..'))
import gemeen
PAL=list(gemeen.PAL)
PAL[7]=(64,94,122); PAL[9]=(160,204,224)          # glaslijn/-midden zoals fase 1 en fase 3
PAL[14]=(248,240,176); PAL[15]=(232,184,48)       # 14 = oog-licht, 15 = oog-geel (eigen oogtinten)
ZAND=[2,3,4,5,6]; GLAS=[7,8,9,10]; KAP=[11,12,13]; OOG=[14,15]
G=json.load(open(os.path.join(HIER,'geo_0.80.json')))
NP,NPH=10.24,9.25

kaal=np.array(Image.open(os.path.join(HIER,'../maten/kaal_0.80.png'))).astype(int)
kaal[kaal==14]=10                                  # enige witte pixel (glasglans) -> glas-licht
S=kaal.copy(); SIL=kaal>0

# ---------- natief raster ----------
m=np.asarray(Image.open(os.path.join(HIER,'../../model.png')).convert('RGB')).astype(int)
n=99; N=np.zeros((n,n,3),int)
for j in range(n):
    for i in range(n):
        x=int(NPH%NP+i*NP+NP/2); y=int(NPH%NP+j*NP+NP/2)
        N[j,i]=np.median(m[y-2:y+3,x-2:x+3].reshape(-1,3),axis=0)
BG=N.min(axis=2)>238
# zandklassen op het natieve raster (gemeten modeltinten)
ANK={'L':(248,218,132),'L2':(252,236,175),'M':(208,160,72),'B1':(136,88,32),'B2':(112,64,24),'K':(30,25,20)}
nam=list(ANK); A=np.array([ANK[k] for k in nam],float)
d=((N[...,None,:]-A)**2).sum(-1); NK=np.array(nam)[d.argmin(-1)]; NK[BG]='.'
# lijncel = M/B/K die niet in een 2x2-blok van dezelfde klasse ligt (dunne lijn), B/K altijd lijn
def vlak(cl):
    b=(NK==cl); v=np.zeros_like(b)
    for dy in (0,1):
        for dx in (0,1):
            blk=b[:-1,:-1]&b[1:,:-1]&b[:-1,1:]&b[1:,1:]
            v[dy:dy+n-1,dx:dx+n-1]|=blk
    return v
LIJN=np.zeros((n,n),bool)
LIJN|=(NK=='M')&~vlak('M'); LIJN|=np.isin(NK,['B1','B2','K'])
# natieve randcellen (grenzen aan achtergrond) zijn de buitenlijn: die doet stap 4, niet als binnenlijn afbeelden
RANDN=nd.binary_dilation(BG,structure=np.ones((3,3)))&~BG
LIJN&=~RANDN
TOON={'L':5,'L2':6,'M':4,'B1':3,'B2':3,'K':2}     # vlaktint per klasse
LTOON={'M':3,'B1':2,'B2':2,'K':2}                  # binnenlijntint per klasse (geen zwart binnenin)

def s2m(i,j): return ((i-G['ox'])*G['T']+G['cx'], (j-G['oy'])*G['T']+G['cy'])
def m2n(x): return (x-NPH%NP)/NP

# zandzone: alles boven de zandloper (rij <= 47) dat in de kale reductie zand of lijn is
ZONE=np.zeros((64,64),bool)
for j in range(64):
    for i in range(64):
        if SIL[j,i] and j<=47 and kaal[j,i] in [1]+ZAND: ZONE[j,i]=True
# glasbuik rechts begint op rij 45-47: daar geen herbouw
for j in range(45,48):
    for i in range(64):
        if any(kaal[jj,ii] in GLAS+KAP for jj in range(j,min(64,j+3)) for ii in range(max(0,i-1),min(64,i+2))): ZONE[j,i]=False

# 1) vlaktint: oppervlaktegewogen meerderheid van de natieve VLAK-cellen onder de spritecel
for j,i in zip(*np.where(ZONE)):
    x0,y0=s2m(i,j); x1,y1=s2m(i+1,j+1)
    a0,a1=m2n(x0),m2n(x1); b0,b1=m2n(y0),m2n(y1); w={}
    for nj in range(int(np.floor(b0)),int(np.ceil(b1))):
        for ni in range(int(np.floor(a0)),int(np.ceil(a1))):
            ov=(min(a1,ni+1)-max(a0,ni))*(min(b1,nj+1)-max(b0,nj))
            if ov<=0 or NK[nj,ni]=='.' or LIJN[nj,ni]: continue
            t=TOON[NK[nj,ni]]; w[t]=w.get(t,0)+ov
    if w: S[j,i]=max(w,key=w.get)
    else:   # alleen lijncellen: tint van de buren in het model
        S[j,i]=-1
# lege cellen: meerderheid van de zone-buren
for _ in range(3):
    for j,i in zip(*np.where(S==-1)):
        b=[S[jj,ii] for jj in range(j-1,j+2) for ii in range(i-1,i+2) if 0<=jj<64 and 0<=ii<64 and S[jj,ii]>1 and ZONE[jj,ii]]
        if b: S[j,i]=max(set(b),key=b.count)
S[S==-1]=5
# 2) lijnen vooruit afbeelden: elke natieve lijncel -> precies 1 spritecel (celmidden); dunne lijnen blijven 1 px en doorlopend
def n2s(ni,nj):
    x=NPH%NP+(ni+.5)*NP; y=NPH%NP+(nj+.5)*NP
    return int(np.floor((x-G['cx'])/G['T']+G['ox'])), int(np.floor((y-G['cy'])/G['T']+G['oy']))
LS=np.zeros((64,64),int)
for nj,ni in zip(*np.where(LIJN)):
    i,j=n2s(ni,nj)
    if 0<=i<64 and 0<=j<64 and ZONE[j,i]:
        t=LTOON[NK[nj,ni]]; LS[j,i]=t if LS[j,i]==0 else min(LS[j,i],t)
S[LS>0]=LS[LS>0]

# 3) ogen 1-op-1 uit het natieve model (125 %), per oog op het eigen middelpunt
def oogklasse(rgb):
    r,g,b=rgb; lum=(r+g+b)/3
    if lum<85: return 1
    if g>=225 and b>=140: return 14
    if g>=175 and b<85: return 15
    return None
OGEN=[((39,36),(43,41)),((46,36),(53,41))]   # natieve kolommen/rijen (incl. wenkbrauw rechts)
OOGZONE=np.zeros((64,64),bool)
for (c0,r0),(c1,r1) in OGEN:
    mx=(c0+c1)/2; my=(r0+r1)/2
    si,sj=n2s(mx,my) if False else (None,None)
    x=NPH%NP+(mx+.5)*NP; y=NPH%NP+(my+.5)*NP
    sx=(x-G['cx'])/G['T']+G['ox']; sy=(y-G['cy'])/G['T']+G['oy']
    ox=int(round(sx-(c1-c0+1)/2)); oy=int(round(sy-(r1-r0+1)/2))
    for nj in range(r0,r1+1):
        for ni in range(c0,c1+1):
            k=oogklasse(N[nj,ni]); i,j=ox+ni-c0, oy+nj-r0
            OOGZONE[j,i]=True
            if k is not None: S[j,i]=k
            elif NK[nj,ni] in ('B1','B2'): S[j,i]=2
            elif S[j,i]==1: S[j,i]=TOON.get(NK[nj,ni],4)
    print('oog',(c0,r0),'-> sprite',ox,oy)

# 4) buitenlijn: randpixels van het (bevroren) silhouet; zwart aan de schaduwkant, eigen donkerste tint aan de lichtkant
def groep(v):
    if v in GLAS: return 'g'
    if v in KAP: return 'k'
    if v in ZAND or v in OOG: return 'z'
    return None
SELOUT={'z':2,'g':7,'k':11}
P=np.pad(SIL,1)
T=S.copy()
for j,i in zip(*np.where(SIL)):
    dx=dy=0
    for yy in (-1,0,1):
        for xx in (-1,0,1):
            if (yy or xx) and not P[j+1+yy,i+1+xx]: dx+=xx; dy+=yy
    if dx==0 and dy==0: continue
    if OOGZONE[j,i] and S[j,i] in OOG: continue
    nrm=np.hypot(dx,dy); lit=(-0.6*dx-0.8*dy)/nrm>0.05
    g=groep(S[j,i])
    if g is None:  # al lijn: groep van de binnenburen
        b=[groep(S[jj,ii]) for jj in range(j-1,j+2) for ii in range(i-1,i+2) if 0<=jj<64 and 0<=ii<64 and groep(S[jj,ii])]
        g=max(set(b),key=b.count) if b else 'z'
    T[j,i]=SELOUT[g] if lit else 1
S=T

# 5) losse tintvlakjes < 3 px (vultinten, niet lijnen/ogen) -> meerderheid van de buren in dezelfde groep
for _ in range(2):
    for t in [3,4,5,6,8,9,10,12,13]:
        lab,k=nd.label(S==t)
        for q in range(1,k+1):
            ys,xs=np.where(lab==q)
            if len(ys)>=3: continue
            for j,i in zip(ys,xs):
                b=[S[jj,ii] for jj in range(j-1,j+2) for ii in range(i-1,i+2) if 0<=jj<64 and 0<=ii<64 and S[jj,ii]!=t and groep(S[jj,ii])==groep(t) and S[jj,ii] not in (2,7,11)]
                if b and not (t==3 and LS[j,i]): S[j,i]=max(set(b),key=b.count)

assert ((S>0)==SIL).all(), 'silhouet veranderd'
im=Image.fromarray(S.astype('uint8'),'P'); p=[]
for c in PAL: p+=list(c)
im.putpalette(p+[0]*(768-len(p))); im.save(os.path.join(HIER,'zandloper_fase2_r1.png'),transparency=0)
np.save(os.path.join(HIER,'r1.npy'),S)
print('kleuren',len(set(S[S>0].ravel())))

# ---------- rapport: afwijking t.o.v. de kale reductie per zone ----------
rand=SIL&~nd.binary_erosion(SIL,structure=np.ones((3,3)))
Z=np.full(S.shape,'lijf/armen/staart',object); Z[48:,:]='zandloper'
Z[43:48][np.isin(kaal[43:48],GLAS+KAP)]='zandloper'
Z[7:21,19:46]='brein'; Z[15:31,5:20]='vraagteken'; Z[17:32,48:57]='uitroepteken'; Z[OOGZONE]='ogen'
for z in ['ogen','brein','vraagteken','uitroepteken','lijf/armen/staart','zandloper']:
    mm=(Z==z)&SIL; dd=mm&(kaal!=S)
    print('%-18s %4d px, afwijkend %3d (%2.0f%%): buitenlijn %3d, binnen %3d'%(z,mm.sum(),dd.sum(),100*dd.sum()/mm.sum(),(dd&rand).sum(),(dd&~rand).sum()))
print('totaal afwijkend',(kaal!=S).sum(),'van',SIL.sum())
