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
# 2b. wit (217) buiten het oog = lichte rand/glans in het model tussen strengen -> D5
n=0
for y in range(H):
    for x in range(W):
        if o[y,x]==I['W'] and (y,x) not in set(oog): o[y,x]=I['D5']; n+=1
log['2b_wit_buiten_oog']=n
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
# 5b. losse binnenlijnpixels D1 (1 px, geen O/D1 in de 8-buurt) -> buurtint
n=0
for pts in comps(o==I['D1']):
    if len(pts)>1: continue
    a,b=pts[0]
    if any(o[a+dy,b+dx] in (I['O'],) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=a+dy<H and 0<=b+dx<W): continue
    c=Counter(o[yy,xx] for yy,xx in nb4(o,a,b) if yy is not None and o[yy,xx] in D[1:])
    if c: o[a,b]=c.most_common(1)[0][0]; n+=1
log['5b_losse_D1']=n
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
POOT=set()
def plak(rows,dy,dx,zone):
    for r in rows:
        for c,v in BAILE[r].items(): zet(r+dy,c+dx,I[BM[v]],zone); POOT.add((r+dy,c+dx))
# r2 (Jordi over r1: "het linkerbeen er heel gek uit ziet als een lange streep, is het mogelijk om de jurk daar wat meer overheen te laten vallen,
#     zodat je alleen de onderkant van de poot ziet zoals bij de rechterpoot")
# 7r2a. split dicht: binnenkant -> jurktint D2; alleen een smalle spleet blijft (per rij de meest rechtse splitpixel, tegen de modelrand) in D1
SPLEET=set()
spl=nieuw.get('split_binnenkant',set())
for y in sorted({p[0] for p in spl}):
    xs=sorted(x for yy,x in spl if yy==y)
    SPLEET.add((y,xs[-1]))
    for x in xs[:-1]: zet(y,x,I['D2'],'r2_split_dicht_jurk')
# 7r2b. franjezoom links: blok rij 43-50, kol 28-38 (franje rechts, r1 na opschonen) 18 kolommen naar links gekopieerd (kol 10-20)
blok=o[43:51,28:39].copy()
for r in range(8):
    for c in range(11):
        zet(43+r,10+c,blok[r,c],'r2_franje_kopie_rechts')
# 7r2c. rok valt over de dij: het gat tussen zoom, gekopieerde franje en middenstrengen (waar in r1 de dij zat) -> jurktint D2; omlijning volgt in 8c
for y,xs in ((42,range(17,21)),(43,range(17,21)),(44,range(18,22))):
    for x in xs:
        if o[y,x] in (0,I['O']): zet(y,x,I['D2'],'r2_rok_over_dij')
# 7a. standbeen: Baile-staak + knik + voet (zoals r1)
plak(range(48,62),-4,-4,'standbeen_baile')
# 7b. gestrekt been: Baile-voet (zoals r1); staak alleen het stuk onder de franje (vanaf de eerste rij waaronder alles vrij is), Baile-staakpatroon b d 3
plak(range(57,62),-4,-20,'gestrekt_voet_baile')
rows=list(range(33,53)); cx={r:int(round(25-(r-33)*17/19)) for r in rows}
vrij=[r for r in rows if all(o[rr,cx[rr]+dx]==0 for rr in range(r,53) for dx in (-1,0,1))]
R0=min(vrij); log['r2_staak_vanaf_rij']=R0
for r in range(R0,53):
    for dx,v in ((-1,'K3'),(0,'K1'),(1,'O')): zet(r,cx[r]+dx,I[v],'gestrekt_staak_onder_franje'); POOT.add((r,cx[r]+dx))
np.save('na_poten.npy',o)
# 8a. kop onder de snavel: bij Pom-Pom loopt de wang onder de snavel door (Pom-Pom rij 23-25, kol 27-29); het gat dat de langere modelsnavel achterliet -> kopvulling
for p in [(12,17),(12,18),(13,16),(13,17),(14,15),(14,16),(12,19),(13,18),(14,17)]:
    zet(p[0],p[1],I['D4'],'kop_onder_snavel_pompom')
# 8a2. r2: bovenrand kop ronder (Jordi: "de bovenste lijn van het hoofd bij tango" ... "dat mag wat ronder").
#      r1: rij 3 kol 20-26 recht (7 px). Nieuw: boog 2-1-1-2-4 (kol 17 / 18 / 19 / 20-21 / 22-25), top één rij hoger; knot ongewijzigd.
for x in range(22,26):
    zet(3,x,o[4,x],'r2_kop_boog')      # vulling = de kopvulling eronder (rij 4)
    zet(2,x,I['O'],'r2_kop_boog')      # nieuwe omlijning (wordt selout in stap 9)
# 8b. restanten van de oude beenomlijning (rij >= 44, omlijning zonder jurk-buur, niet van de nieuwe poten) -> transparant
n=0
for it in range(2):
    for y in range(44,H):
        for x in range(W):
            if o[y,x]==I['O'] and been[y,x] and (y,x) not in POOT and not any(yy is not None and o[yy,xx] in D for yy,xx in nb4(o,y,x)) \
               and not any(0<=y+dy<H and 0<=x+dx<W and o[y+dy,x+dx] in D for dy in (-1,0,1) for dx in (-1,0,1)):
                o[y,x]=0; n+=1
log['8b_oude_beenomlijning']=n
# 8c. buitenrand opnieuw dicht (na kop en poten)
n=0
for y in range(H):
    for x in range(W):
        if o[y,x] in D and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(o,y,x)):
            o[y,x]=I['O']; n+=1
log['8c_buitenrand_dicht']=n
np.save('na_poten.npy',o)
# 9. selout: omlijning aan de lichtkant (transparant boven of links, niet onder of rechts) -> één tint donkerder dan de vulling (min. D1)
n=0
for y in range(H):
    for x in range(W):
        if o[y,x]!=I['O'] or (y,x) in POOT or (y,x) in VAST: continue
        up=y==0 or o[y-1,x]==0; lf=x==0 or o[y,x-1]==0; dn=y==H-1 or o[y+1,x]==0; rt=x==W-1 or o[y,x+1]==0
        if not (up or lf) or dn or rt: continue
        inn=[o[y+1,x]] if up else []
        if lf: inn.append(o[y,x+1])
        inn=[v for v in inn if v in D]
        if not inn: continue
        v=I['D2'] if min(inn)>=I['D3'] else I['D1']; o[y,x]=v; n+=1
log['9_selout']=n
np.save('tango_kls.npy',o)
tot=sum(len(v) for v in nieuw.values()); log['nieuw_per_zone']={k:len(v) for k,v in nieuw.items()}
basis=np.load('basis.npy'); log['afwijkend_van_onderlaag_totaal']=int((basis!=o).sum()); log['dekkend']=int((o>0).sum())
print(json.dumps(log))
# maskers voor de roodvarianten (rood.py)
sp=np.zeros_like(o,bool)
for p in SPLEET: sp[p]=True
np.save('split_mask.npy',sp)
kn=np.zeros_like(o,bool)
for p in [(6,28),(7,29),(8,29),(9,29),(10,29),(11,29),(12,29),(13,29)]: kn[p]=True   # binnenlijn kop|knot (modellijn, O/D1)
np.save('knot_mask.npy',kn)
