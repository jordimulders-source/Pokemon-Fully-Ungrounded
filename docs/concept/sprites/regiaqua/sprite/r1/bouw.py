# Regiaqua r1: kale reductie (kaal.py) -> technisch opschonen. Elke stap telt de pixels die hij verandert.
# Bouwen: cd docs/concept/sprites/regiaqua && python3 sprite/r1/kaal.py && python3 sprite/r1/bouw.py
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import pal, gemeen as g
D=g.D
K=np.load(os.path.join(D,'kaal.npy'))
kaal=pal.k2idx(K)                       # paletindex van de kale reductie
LIJN=11                                 # extra paletkleur: selout/binnenlijn (donkerste eigen tint)
PALET=pal.PAL+[(10,38,68)]
s=kaal.copy(); log=[]
fig=s>0
def stap(naam,nieuw):
    global s
    d=(nieuw!=s).sum(); log.append((naam,int(d),nieuw!=s)); s=nieuw
TONEN=[2,3,4,5,6,7,8]                   # water toon 0..6
# 1. stippen: kale stippixels -> omringende watertoon (meerderheid 8-buren), dan 7 blokjes van 2x2 op de modelplek.
n=s.copy()
for y,x in zip(*np.where(s==9)):
    b=[s[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if s[yy,xx] in TONEN]
    n[y,x]=max(set(b),key=b.count) if b else 3
X0=22; BLOK=[(X0+5,28),(X0,31),(X0+3,31),(X0+6,31),(X0+9,31),(X0+3,34),(X0+8,34)]
for x,y in BLOK:
    n[y:y+2,x:x+2]=9; n[y,x]=10
stap('stippen',n)
# 2. zwart binnen het silhouet (geen buitenrand) -> binnenlijn LIJN (Gen 3: binnenlijnen niet zwart).
p=np.pad(fig,1); bnd=fig&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
n=s.copy(); n[(s==1)&~bnd]=LIJN; stap('zwart binnen -> binnenlijn',n)
# 3. buitenlijn 1 px: schaduwkant (normaal naar rechts/onder) zwart, lichtkant (links/boven) LIJN.
f=fig.astype(float); gy,gx=np.gradient(ndimage.gaussian_filter(f,1.2))
nx,ny=-gx,-gy; nn=np.hypot(nx,ny)+1e-9; nx/=nn; ny/=nn
schaduw=(0.6*nx+0.8*ny)>0.1
# dunne punten (handen): de gladde normaal klopt daar niet; een zuivere zijkant (achtergrond alleen rechts of alleen links)
# volgt de kant: rechts = schaduw, links = licht.
H,W=fig.shape
for y,x in zip(*np.where(bnd)):
    l=not p[y+1,x]; r=not p[y+1,x+2]; u=not p[y,x+1]; d=not p[y+2,x+1]
    if r and not l and not u and not d: schaduw[y,x]=True
    if l and not r and not u and not d: schaduw[y,x]=False
n=s.copy(); n[bnd&schaduw]=1; n[bnd&~schaduw]=LIJN; stap('buitenlijn',n)
# 3b. tussentoon 2 (128 px, vrijwel gelijk aan zijn buren) opgedeeld naar toon 1 of 3 volgens de modelhelderheid
#     van dat spritevlak (gemiddelde natieve L < 98 -> toon 1): een tint minder, hardere grenzen, geen vorm veranderd.
import kaal as kl
a_,fig_,L_,dot_,blk_=g.natief()
n=s.copy()
for y,x in zip(*np.where(s==4)):
    xs=kl.X0+(x-kl.OX+(np.arange(8)+.5)/8)/kl.s; ys=kl.Y0+(y-kl.OY+(np.arange(8)+.5)/8)/kl.s
    n[y,x]=3 if L_[ys.astype(int)[:,None],xs.astype(int)[None,:]].mean()<98 else 5
stap('tussentoon opdelen',n)
TONEN=[2,3,5,6,7,8]
# 4. ontkorrelen: losse pixels (8-samenhangend) van toon 0..4 -> meest voorkomende
#    (alleen losse pixels: 2-px stukjes zijn streepjes uit het model en blijven)
#    watertoon onder de 8-buren (bij gelijkspel de dichtstbijzijnde toon). Glans (toon 5,6) blijft: strepen en lichtvegen
#    van het model worden niet weggepoetst. Lijnen en stippen worden niet aangeraakt.
def ontkorrel(s):
    n=s.copy()
    for t,maxn in ((2,1),(3,1),(5,1),(6,1)):
        lab,k=ndimage.label(s==t,structure=np.ones((3,3)))
        sz=np.bincount(lab.ravel())
        for c in range(1,k+1):
            if sz[c]>maxn: continue
            ys,xs=np.where(lab==c); b=[]
            for y,x in zip(ys,xs):
                b+=[s[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if s[yy,xx] in TONEN and s[yy,xx]!=t]
            if not b: continue
            best=max(set(b),key=lambda v:(b.count(v),-abs(int(v)-int(t))))
            n[lab==c]=best
    return n
for _ in range(3): stap('ontkorrelen',ontkorrel(s))
# 5. dubbele lijn in de vingerinkepingen (modelzwart + buitenlijn = 2 px): binnenste lijnpixel -> watertoon van de buren.
n=s.copy()
for y,x in [(45,8),(45,9),(46,7),(47,7),(48,52)]:
    assert s[y,x]==LIJN,(y,x,s[y,x])
    b=[s[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if s[yy,xx] in TONEN]
    n[y,x]=max(set(b),key=b.count)
stap('lijn 1 px in inkepingen',n)
# zones: verbonden delen van het silhouet (hand links, lijf, hand rechts) + het stippenvak
lab,nz=ndimage.label(fig); zn={}
for c in range(1,nz+1):
    xs=np.where(lab==c)[1]; zn[c]='hand links' if xs.max()<16 else ('hand rechts' if xs.min()>46 else 'lijf')
ZONE=np.full(fig.shape,'',object)
for c,nm in zn.items(): ZONE[lab==c]=nm
ZONE[27:37,21:35]='stippen'
def compact(idx,P):   # ongebruikte paletindexen eruit (index 0 blijft transparant)
    used=[0]+[i for i in range(1,len(P)) if (idx==i).any()]
    m=np.zeros(256,'uint8'); m[used]=np.arange(len(used)); return m[idx],[P[i] for i in used]
if __name__=='__main__':
    pal.opslaan(kaal,os.path.join(D,'kaal.png'),PALET)
    uit,P2=compact(s,PALET)
    pal.opslaan(uit,os.path.join(D,'regiaqua_r1.png'),P2)
    np.save(os.path.join(D,'r1.npy'),s)
    for nm,d,_ in log: print(nm,d)
    print('kleuren (incl. transparant)',len(P2))
    tot=(s!=kaal)
    for z in ['lijf','stippen','hand links','hand rechts']:
        m=ZONE==z; print('zone %-11s afwijkend %3d px |'%(z,(tot&m).sum()),', '.join('%s %d'%(nm,(mk&m).sum()) for nm,_,mk in log if (mk&m).sum()))
    print('totaal afwijkend',tot.sum(),'van',fig.sum())
