# Zandloper fase 2, r3: zes benoemde reparaties op r2, alles uit het natieve modelraster.
import os, sys
import numpy as np; from PIL import Image
from scipy import ndimage as nd
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from basis import *
R=R2.copy(); SIL0=R2>0
ZONEN={}
TOON={'L':5,'L2':6,'M':4,'B1':3,'B2':2,'K':1}
def nkl(a,b): return NK[b,a]
def meerd(i,j,fn=nkl,zonder=('.',)):
    w=dekking(i,j,fn); w={k:v for k,v in w.items() if k not in zonder}
    return max(w,key=w.get) if w else None
def groep(v):
    return 'g' if v in (7,8,9,10) else 'k' if v in (11,12,13) else 'z' if v in (2,3,4,5,6,14,15) else None
SELOUT={'z':2,'g':7,'k':11}
def buitenlijn(R,mask):
    """r1-regel: randpixel -> zwart aan de schaduwkant, eigen donkerste tint aan de lichtkant (alleen binnen mask)"""
    S=R>0; P=np.pad(S,1); T=R.copy()
    for j,i in zip(*np.where(mask&S)):
        dx=dy=0
        for yy in (-1,0,1):
            for xx in (-1,0,1):
                if (yy or xx) and not P[j+1+yy,i+1+xx]: dx+=xx; dy+=yy
        if dx==0 and dy==0: continue
        lit=(-0.6*dx-0.8*dy)/np.hypot(dx,dy)>0.05
        g=groep(R[j,i])
        if g is None:
            b=[groep(R[jj,ii]) for jj in range(j-1,j+2) for ii in range(i-1,i+2) if 0<=jj<64 and 0<=ii<64 and groep(R[jj,ii])]
            g=max(set(b),key=b.count) if b else 'z'
        T[j,i]=SELOUT[g] if lit else 1
    return T
def rand(S): return S&~nd.binary_erosion(S,structure=np.ones((3,3)))

# ---------- 1) lichte zone onder het gezicht: modellicht (L) direct onder de ogen -> 6, één vlek ----------
Z1=np.zeros((64,64),bool); Z1[26:32,22:38]=True
for j,i in zip(*np.where(Z1)):
    if R[j,i] in (5,6) and meerd(i,j)=='L': R[j,i]=6
ZONEN['1 lichte zone']=Z1

# ---------- 2) onderrand glas: losse 9/8 weg, binnenrand van het model vooruit afgebeeld ----------
Z2=np.zeros((64,64),bool); Z2[46:57,12:37]=True
GA={10:(222,244,250),9:(160,204,224),8:(114,160,186),7:(64,94,122)}
def glas(a,b):
    v=N[b,a]
    if NK[b,a]=='.' or v[2]<=v[0]+15: return None
    return min(GA,key=lambda k:((v-np.array(GA[k]))**2).sum())
RD=rand(SIL0)
for j,i in zip(*np.where(Z2&np.isin(R,[8,9]))):      # eerst de losse modelpixels terug naar de buurtint
    w=dekking(i,j,lambda a,b: 'g' if glas(a,b) in (9,10) else ('z' if NK[b,a] in ('L','L2','M') else None))
    b=[R[jj,ii] for jj in range(j-1,j+2) for ii in range(i-1,i+2) if R[jj,ii] in (4,5,6,10)]
    R[j,i]=max(set(b),key=b.count) if b else 10
for nj in range(62,82):
    for ni in range(10,60):
        if glas(ni,nj) in (8,9):
            i,j=n2s(ni,nj)
            # valt de modelrandcel op de buitenlijn (0,8-compressie), dan 1 px naar binnen (boven/rechtsboven), anders gaat de boog stuk
            for di,dj in ((0,0),(0,-1),(1,-1),(1,0)):
                ii,jj=i+di,j+dj
                if Z2[jj,ii] and SIL0[jj,ii] and not RD[jj,ii] and R[jj,ii] in (4,5,6,8,9,10): R[jj,ii]=9; break
ZONEN['2 onderrand glas']=Z2

# ---------- 3) hals: onderrand één kleur; aansluiten op de zwarte onderkant van de bollen ----------
Z3=np.zeros((64,64),bool); Z3[50:56,19:26]=True
for j,i in zip(*np.where(Z3&RD)):
    if R[j,i]==7: R[j,i]=1
ZONEN['3 hals']=Z3

# ---------- 4) haakuiteinde ?: lichte vulling uit het model, rond afgesloten ----------
Z4=np.zeros((64,64),bool); Z4[23:27,7:11]=True
for j,i in zip(*np.where(Z4&SIL0&~RD)):
    t=meerd(i,j)
    if t in ('L','L2'): R[j,i]=6 if R[j-1,i]==6 else 5
    elif t=='M': R[j,i]=4
ZONEN['4 haak ?']=Z4

# ---------- 5) linkerarm en rechtervuist: silhouet en vulling uit het model ----------
def herbouw(Z,drempel):
    S=R>0
    for j,i in zip(*np.where(Z)):
        w=dekking(i,j,lambda a,b: 'bg' if NK[b,a]=='.' else 'f'); tot=sum(w.values())
        dek=w.get('f',0)/tot
        if dek>=drempel:
            t=meerd(i,j); R[j,i]=TOON[t] if t else 5
            if R[j,i]==1: R[j,i]=2          # binnenin geen zwart
        else: R[j,i]=0
    # vulling: 5 -> 6 waar het r2-veld 6 gaf (zelfde helderheidsverdeling)
    for j,i in zip(*np.where(Z&(R==5)&(R2==6))): R[j,i]=6
Z5a=np.zeros((64,64),bool); Z5a[31:34,15:23]=True
Z5b=np.zeros((64,64),bool); Z5b[32:39,44:54]=True
herbouw(Z5a,0.45); herbouw(Z5b,0.5)
Z5=Z5a|Z5b
# buitenlijn in deze zone: alleen pixels met een transparante 4-buur (een pixel die alleen schuin aan de achtergrond
# grenst is binnenkant en houdt de modeltint; dat waren de zwarte 'vingerpunten'); naar linksonder telt als lichtkant
S5=R>0; P4=np.pad(S5,1)
rand4=S5&~(P4[:-2,1:-1]&P4[2:,1:-1]&P4[1:-1,:-2]&P4[1:-1,2:])
def buitenlijn5(R,mask):
    S=R>0; P=np.pad(S,1); T=R.copy()
    for j,i in zip(*np.where(mask)):
        dx=dy=0
        for yy in (-1,0,1):
            for xx in (-1,0,1):
                if (yy or xx) and not P[j+1+yy,i+1+xx]: dx+=xx; dy+=yy
        if dx==0 and dy==0: continue
        lit=(-0.6*dx-0.8*dy)/np.hypot(dx,dy)>-0.2
        T[j,i]=2 if lit else 1
    return T
R=buitenlijn5(R,Z5&rand4)
ZONEN['5 arm/vuist']=Z5

# ---------- 6) houten kappen: lichte roodbruine strook uit het model (12, lichtste cellen 13) ----------
Z6=np.zeros((64,64),bool); Z6[42:58,11:16]=True; Z6[46:58,28:37]=True
Z6&=np.isin(R,[11,12,13])
for j,i in zip(*np.where(Z6)):
    if R[j,i] in (12,13): R[j,i]=11
for nj in range(60,82):
    for ni in range(15,60):
        v=N[nj,ni]; l=v.mean()
        if v[0]>v[2]+50 and 90<=l<130 and v[0]>150:      # lichte roodbruine strook (b07040-tinten)
            i,j=n2s(ni,nj)
            if Z6[j,i] and not (RD[j,i] and R[j,i]==1): R[j,i]=13 if l>=117 else 12     # lichtste strookcellen (bovenaan, lichtkant) 13
ZONEN['6 kappen']=Z6

# ---------- controle en opslaan ----------
ALL=np.zeros((64,64),bool)
for z in ZONEN.values(): ALL|=z
assert (R[~ALL]==R2[~ALL]).all(), 'wijziging buiten de zones'
assert ((R>0)==SIL0)[~(Z5a|Z5b)].all(), 'silhouet buiten zone 5 veranderd'
im=Image.fromarray(R.astype('uint8'),'P'); p=[]
for c in PAL: p+=list(c)
im.putpalette(p+[0]*(768-len(p))); im.save(os.path.join(H,'zandloper_fase2_r3.png'),transparency=0)
np.save(os.path.join(H,'r3.npy'),R)
print('kleuren',len(set(R[R>0].ravel())),'telling',np.bincount(R.ravel(),minlength=16)[1:])
for z,m in ZONEN.items(): print('%-16s gewijzigd t.o.v. r2: %d'%(z,(m&(R!=R2)).sum()))
print('silhouet gewijzigd',((R>0)!=SIL0).sum(),'totaal gewijzigd',(R!=R2).sum())
