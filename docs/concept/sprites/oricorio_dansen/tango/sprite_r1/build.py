# basis.npy (schrap-onderlaag 5->3, elke pixel = modelpixel, 3 px marge) -> tango_kls.npy + log per stap.
import numpy as np, json, sys
from collections import Counter
from lib import *
o=np.load('basis.npy').copy(); H,W=o.shape; log={}; nieuw={}   # nieuw: pixels die niet uit het model komen, per zone
D=[I[n] for n in ('D1','D2','D3','D4','D5','D6')]; K=[I['K1'],I['K2'],I['K3']]
def zet(y,x,v,zone):
    if o[y,x]!=v: o[y,x]=v; nieuw.setdefault(zone,set()).add((y,x))
# 0. randruis: lichte pixels (W/D6/D5) tegen de achtergrond zijn anti-aliasing van het witte model -> transparant
n=0
for it in range(2):
    for y in range(H):
        for x in range(W):
            if o[y,x]==I['W'] and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(o,y,x)) and not (8<=y<=13 and 20<=x<=25):
                o[y,x]=0; n+=1
log['0_randruis']=n
# 1. benen weg (Jordi: mensenbenen -> Oricorio-staakpootjes). Roze/wit/omlijning van de benen vanaf rij 30.
#    In de split (rij <= 43, links en rechts jurk op dezelfde rij) -> D1 (binnenkant jurk), eronder -> transparant.
been=np.zeros_like(o,bool)
for y in range(30,H):
    for x in range(W):
        if o[y,x] in K or (o[y,x]==I['W'] and any(yy is not None and o[yy,xx] in K for yy,xx in nb4(o,y,x))): been[y,x]=True
for it in range(1):   # omlijning direct om de benen die geen jurk raakt
    add=[]
    for y in range(30,H):
        for x in range(W):
            if o[y,x]==I['O'] and not been[y,x] and any(yy is not None and been[yy,xx] for yy,xx in nb4(o,y,x)):
                if y>=48 or not any(yy is not None and o[yy,xx] in D for yy,xx in nb4(o,y,x)): add.append((y,x))
    for p in add: been[p]=True
nd=nt=0
for y,x in zip(*np.where(been)):
    row=o[y]; L=[v for v in row[max(0,x-8):x] if v and v not in K]; R=[v for v in row[x+1:x+9] if v and v not in K]
    if y<=43 and L and R and any(v in D for v in L) and any(v in D for v in R): o[y,x]=I['D1']; nieuw.setdefault('split_binnenkant',set()).add((y,x)); nd+=1
    else: o[y,x]=0; nt+=1
log['1_benen_weg_naar_D1']=nd; log['1_benen_weg_naar_transparant']=nt
np.save('na_benen.npy',o)
# 2. snavel en oog (Jordi: "het oog van tango moet ook nog meer oricorio worden"; snavel vergeleken met de 4 Gen 3-vormen):
#    modelsnavel en modeloog weg; Pom-Pom-snavel en -oog pixel voor pixel, onderlinge afstand zoals bij Pom-Pom.
#    Plaatsing: Pom-Pom (rij,kol) + (DY,DX); oog valt dan op het modeloog (kol 21-24, rij 7-11), snavelbasis op de modelsnavelbasis (kol 19).
DY,DX=-11,-12
pp=ori('pom_pom/')
PPMAP={8:'K3',9:'K1',0xb:'K2',3:'O',0xd:'W'}
oud_snavel=[(y,x) for y in range(8,16) for x in range(8,20) if o[y,x] in K or (o[y,x]==I['W'] and x<20)]
for y,x in oud_snavel: o[y,x]=0
oud_oog=[(y,x) for y in range(7,13) for x in range(20,26) if o[y,x] in (I['O'],I['W'],0)]
for y,x in oud_oog: o[y,x]=I['D4']
log['2_modelsnavel_weg']=len(oud_snavel); log['2_modeloog_weg']=len(oud_oog)
snavel=[];oog=[]
for r in range(18,26):
    for c in range(25,37):
        v=pp[r,c]
        if c<=31 and v in (8,9,0xb) or (c<=30 and r>=22 and v==3):
            y,x=r+DY,c+DX; o[y,x]=I[PPMAP[v]]; snavel.append((y,x))
        elif 33<=c<=36 and r<=22 and v in (3,0xd):
            y,x=r+DY,c+DX; o[y,x]=I[PPMAP[v]]; oog.append((y,x))
log['2_pompom_snavel_px']=len(snavel); log['2_pompom_oog_px']=len(oog)
for p in snavel: nieuw.setdefault('snavel_pompom',set()).add(p)
for p in oog: nieuw.setdefault('oog_pompom',set()).add(p)
for p in oud_oog: nieuw.setdefault('kop_achter_oud_oog',set()).add(p)
np.save('na_kop.npy',o)
# 3. losse brokjes (componenten < 4 px die nergens aan vastzitten) -> transparant
n=0
for pts in comps(o>0):
    if len(pts)<4:
        for p in pts: o[p]=0; n+=1
log['3_losse_brokjes']=n
VAST=set(snavel)|set(oog)
# 4. ontkorrelen: tintclusters < 3 px (D1..D6) nemen de meest voorkomende buurtint aan; D6-glans mag 2 px
n=0
for it in range(3):
    for k in D[1:]:   # D1 = model-binnenlijn (18): niet ontkorrelen, telt als lijn
        for pts in comps(o==k):
            if len(pts)>=3 or (k==I['D6'] and len(pts)==2) or any(p in VAST for p in pts): continue
            c=Counter(o[yy,xx] for a,b in pts for yy,xx in nb4(o,a,b) if yy is not None and o[yy,xx] in D)
            c.pop(k,None)
            if c:
                v=c.most_common(1)[0][0]
                for p in pts: o[p]=v; n+=1
log['4_ontkorrelen']=n
# 5. losse omlijningspixels in een vlak (geen O-buur, geen transparante buur) -> buurtint
n=0
LIJN=(I['O'],I['D1'])
for pts in comps(o==I['O']):
    if len(pts)>1 or pts[0] in VAST: continue
    a,b=pts[0]
    if any(o[a+dy,b+dx] in LIJN for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=a+dy<H and 0<=b+dx<W): continue   # deel van een diagonale modellijn
    nbv=[o[yy,xx] if yy is not None else 0 for yy,xx in nb4(o,a,b)]
    if 0 in nbv: continue
    c=Counter(v for v in nbv if v in D)
    if c: o[a,b]=c.most_common(1)[0][0]; n+=1
log['5_losse_omlijning']=n
# 6. buitenrand dicht: vulpixel met transparante 4-buur -> omlijning
n=0
for y in range(H):
    for x in range(W):
        if o[y,x] in D and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(o,y,x)):
            o[y,x]=I['O']; n+=1
log['6_buitenrand_dicht']=n
np.save('na_schoon.npy',o)
# 7. Oricorio-staakpootjes (Jordi: "de benen zijn wel erg menselijk"). Bron: Baile (graphics/pokemon/oricorio/anim_front.png, frame 1),
#    nabije poot rij 48-61 (staak 'b d 3' = lijnroze/roze/zwart, knik op rij 53-56, voet rij 57-61). b->K3, d->K1, e->K2, 3/6->O, 1->K3.
BAILE={48:{30:'b',31:'e',32:'3'},49:{30:'b',31:'d',32:'3'},50:{30:'b',31:'d',32:'3'},51:{30:'b',31:'d',32:'3'},
       52:{29:'b',30:'d',31:'e',32:'3'},53:{29:'b',30:'d',31:'3'},54:{29:'1',30:'d',31:'3'},55:{28:'b',29:'d',30:'3'},
       56:{27:'b',28:'d',29:'d',30:'3'},57:{26:'b',27:'d',28:'d',29:'d',30:'d',31:'3'},
       58:{24:'b',25:'b',26:'d',27:'d',28:'e',29:'d',30:'e',31:'3'},59:{23:'b',24:'d',25:'e',26:'d',27:'d',28:'b',29:'d',30:'3'},
       60:{23:'3',24:'3',25:'1',26:'d',27:'3',28:'6',29:'d',30:'3'},61:{25:'3',26:'3',28:'3',29:'3'}}
BM={'b':'K3','d':'K1','e':'K2','3':'O','6':'O','1':'K3'}
def plak(rows,dy,dx,zone):
    for r in rows:
        for c,v in BAILE[r].items(): zet(r+dy,c+dx,I[BM[v]],zone)
# 7a. standbeen: Baile-staak + knik + voet, onderkant voet op de modelvoet (rij 57), staak op de modelstaak (kol 26-27)
plak(range(48,62),-4,-4,'standbeen_baile')
# 7b. gestrekt been: Baile-voet (rij 57-61) op de modelvoet linksonder; staak = NIEUW, schuin van de split (rij 33, kol 25) naar de voet
plak(range(57,62),-4,-20,'gestrekt_voet_baile')
for r in range(33,53):
    xc=int(round(25-(r-33)*17/19))
    zet(r,xc-1,I['K3'],'gestrekt_staak_nieuw'); zet(r,xc,I['K1'],'gestrekt_staak_nieuw'); zet(r,xc+1,I['O'],'gestrekt_staak_nieuw')
np.save('na_poten.npy',o)
