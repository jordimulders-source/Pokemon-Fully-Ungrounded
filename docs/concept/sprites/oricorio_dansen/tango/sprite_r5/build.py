# basis.npy (kale onderlaag: schrap 2->1, fase 1 0, geplaatst in 64x64, elke pixel = modelpixel) -> tango_kls.npy + log per stap.
import numpy as np, json
from collections import Counter
NAMEN=['_','O','D0','D1','D2','D3','D4','R1','R2','R3','K1','K2','K3','W']
I={n:i for i,n in enumerate(NAMEN)}
_,O,D0,D1,D2,D3,D4,R1,R2,R3,K1,K2,K3,W=range(14)
o=np.load('basis.npy').copy(); H,W_=o.shape; basis=o.copy(); log={}
def nb4(y,x): return [(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<H and 0<=x+dx<W_]
def tr(y,x): return not(0<=y<H and 0<=x<W_) or o[y,x]==0
def comps(mask):
    seen=np.zeros(mask.shape,bool); out=[]
    for y in range(H):
        for x in range(W_):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for yy,xx in nb4(a,b):
                        if mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
                out.append(pts)
    return out
def tel(k,n=1): log[k]=log.get(k,0)+n
DONK=(D0,D1,D2,D3,D4); ROOD=(R1,R2,R3); ROZE=(K1,K2,K3)
# 0. R1 (k-means 15, 158,78,93) is een roze middentint in poten/snavel; in de franje (rij>=40, buiten de poten) -> R2
for y in range(40,H):
    for x in range(W_):
        if o[y,x]==R1 and not ((x>=38 and y>=48) or (28<=x<=34 and y>=53)): o[y,x]=R2; tel('0_R1_franje_naar_R2')
# 1. oog uit het model weg (oog + wimpers, rij 11-17, kol 29-37: zwart en het glimpje dat als achtergrond meetelde) -> kopvulkleur van de buren
for it in range(3):
    for y in range(11,18):
        for x in range(29,37):
            if o[y,x]==O or (o[y,x]==0 and 12<=y<=15 and 30<=x<=34):
                c=Counter(o[a,b] for a,b in nb4(y,x) if o[a,b] in DONK)
                if c: o[y,x]=c.most_common(1)[0][0]; tel('1_modeloog_weg')
# 2. snavel uit het model weg (roze/rood en zwart in kop-voorkant rij 11-20, kol 16-29) -> transparant
for y in range(11,21):
    for x in range(16,30):
        if o[y,x] in ROZE+ROOD+(W,) or (o[y,x]==O and x<=28 and y>=12): o[y,x]=0; tel('2_modelsnavel_weg')
# 2b. kopvoorkant dichtzetten: per rij 12-19 van de eerste kopvulpixel naar links tot kol 24 kopkleur (D1), kol 23 omlijning
for y in range(12,20):
    xs=[x for x in range(23,32) if o[y,x] in DONK]
    if not xs: continue
    for x in range(24,min(xs)):
        if o[y,x]!=D1: o[y,x]=D1; tel('2b_kop_dicht')
    if o[y,23]==0: o[y,23]=O; tel('2b_kop_dicht')
# 3. Pom-Pom-oog + -snavel pixel voor pixel (frame 1; oog rij 18-22 kol 33-36, snavel rij 19-25 kol 25-31), verschoven DY=-6, DX=-3:
#    oog op de hoogte/plek van het modeloog, snavel op dezelfde afstand van het oog als bij Pom-Pom.
DY,DX=-6,-3
POM={18:{34:O,35:O},19:{33:O,34:O,35:O,36:O},20:{33:O,34:W,35:O,36:O},21:{33:O,34:W,35:O,36:O},22:{34:O,35:O}}
SNAVEL={19:{28:K3,29:K3,30:K3},20:{27:K3,28:K1,29:K1,30:K1,31:K3},21:{26:K3,27:K1,28:K1,29:K1,30:K1,31:K3},
        22:{25:K3,26:K1,27:K1,28:K1,29:O,30:O},23:{25:K3,26:K1,27:K2,28:O},24:{25:K3,26:K1,27:O},25:{25:K3,26:O}}
for tab,k in ((POM,'3_pompom_oog'),(SNAVEL,'3_pompom_snavel')):
    for r,d in tab.items():
        for c,v in d.items(): o[r+DY,c+DX]=v; tel(k)
# 3b. links van de snavel (rij 13-19) niets: alles links van de snavel transparant
for y in range(13,20):
    xs=[x for x in range(16,32) if o[y,x] in ROZE]
    for x in range(16,min(xs) if xs else 16):
        if o[y,x]: o[y,x]=0; tel('3b_links_van_snavel')
# 3a. kopomlijning boven de snavel zoals Pom-Pom (rij 18-20 kol 26-27 = omlijning/kop)
for y,x,v in ((13,23,O),(13,24,D1),(14,23,O)):
    if o[y,x]!=v: o[y,x]=v; tel('3a_kop_boven_snavel_pompom')
np.save('na_kop.npy',o)
# 4. poten: modelpootjes (onder de franje) weg, dan Baile-voet (frame 1, rij 56-61, kol 23-31) links (DX=+1), gespiegeld rechts;
#    het zichtbare onderbeen als Gen 3-staakje [donkerroze, roze, zwart] op de modelplek (links kol 29-31, rechts de modeldiagonaal).
for y in range(48,H):
    for x in range(36,64):
        if o[y,x] and not (y==48 and x in (40,41,43,44)): o[y,x]=0; tel('4_modelpoot_weg')
for y in range(53,H):
    for x in range(22,35):
        if o[y,x] in ROZE+(R1,) or (y>=56 and x>=28) or y>=58: 
            if o[y,x]: o[y,x]=0; tel('4_modelpoot_weg')
BAILE=['.......bdd3....','......bdddd3...','....bbddede3...','...bdeddbd3....','...331d36d3....','.....33.33.....']  # rij 56-61, kol 20-34
BM={'b':K3,'d':K1,'e':K2,'3':O,'1':K3,'6':O}
voet_l=[];voet_r=[]
for i,row in enumerate(BAILE):
    for j,ch in enumerate(row):
        if ch=='.': continue
        y,x=56+i,20+j
        voet_l.append((y,x+1,BM[ch]))
        voet_r.append((y-1,41+(31-x),BM[ch]))       # gespiegeld: kol 31->41 ... 23->49, 1 rij hoger
for y,x,v in voet_l: o[y,x]=v; tel('4_baile_voet_links')
for y,x,v in voet_r: o[y,x]=v; tel('4_baile_voet_rechts_gespiegeld')
BEEN=[(53,29,K3),(53,30,K1),(53,31,O),(54,29,K3),(54,30,K1),(54,31,O),(55,29,K3),(55,30,K1),(55,31,O)]+\
     [(48,38,K3),(48,39,K1),(49,39,K3),(49,40,K1),(49,41,O),(50,39,K3),(50,40,K1),(50,41,O),(51,40,K3),(51,41,K1),(51,42,O),
      (52,41,K3),(52,42,K1),(52,43,O),(53,41,K3),(53,42,K1),(53,43,O),(54,42,K3),(54,43,K1),(54,44,O)]
for y,x,v in BEEN:
    if o[y,x]!=v: o[y,x]=v; tel('4_onderbeen')
# 4b. herbelichting gespiegelde voet: roze/zwart op de buitenrand: lichtkant (transparant links/boven) donkerroze, schaduwkant (rechts/onder) zwart
for y,x,v in voet_r:
    if o[y,x] in ROZE+(O,):
        lf=tr(y,x-1); up=tr(y-1,x); rt=tr(y,x+1); dn=tr(y+1,x)
        nv=O if (rt or dn) else (K3 if (lf or up) else o[y,x])
        if nv!=o[y,x]: o[y,x]=nv; tel('4b_herbelicht_rechtervoet')
np.save('na_poten.npy',o)
# 5. ontkorrelen: vulklusters < 3 px (donker/rood) nemen de meest voorkomende buurvulkleur aan; oog/snavel/poten bevroren
VUL=DONK+(R2,R3)
for it in range(3):
    for k in DONK:   # rood (franjeveren + naden) = modeltekening, niet ontkorrelen
        for pts in comps(o==k):
            if len(pts)>=3: continue
            c=Counter(o[yy,xx] for a,b in pts for yy,xx in nb4(a,b) if o[yy,xx] in VUL); c.pop(k,None)
            if c:
                v=c.most_common(1)[0][0]
                for a,b in pts: o[a,b]=v; tel('5_ontkorrelen')
# 6. losse omlijningspixels (1 px, geen zwarte buur, niet aan de buitenrand) -> buurvulkleur
for pts in comps(o==O):
    if len(pts)>1: continue
    a,b=pts[0]
    if any(tr(yy,xx) for yy,xx in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]) or (8<=a<=22 and 18<=b<=36): continue
    c=Counter(o[yy,xx] for yy,xx in nb4(a,b) if o[yy,xx] in VUL)
    if c: o[a,b]=c.most_common(1)[0][0]; tel('6_losse_omlijning')
# 7. buitenrand dicht: dekkende vulpixel (donker/rood) met transparante 4-buur -> omlijning
for y in range(H):
    for x in range(W_):
        if o[y,x] in VUL and any(tr(yy,xx) for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]): o[y,x]=O; tel('7_buitenrand_dicht')
np.save('tango_kls.npy',o)
d=(o!=basis); log['totaal_afwijkend_van_kale_onderlaag']=int(d.sum()); log['dekkend']=int((o>0).sum())
ys,xs=np.where(o>0); log['bbox']=[int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)]
np.save('afwijk.npy',d); json.dump(log,open('log.json','w'),indent=0); print(log)
