# kaal_11.npy (2x2-blokreductie van het natieve model, elke pixel uit zijn eigen modelblok) -> samba_kls.npy + log per stap.
# Coordinaten hieronder = uitsnede (rij, kolom) van de onderlaag; aan het eind geplaatst in 64x64.
import numpy as np, json
from collections import Counter
from palet import NAMEN, I
import sys
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'kaal_11geel.npy'); ys,xs=np.where(o>0); o=o[ys.min():ys.max()+1,xs.min():xs.max()+1].copy()
H,W=o.shape; basis=o.copy(); log={}
def nb4(y,x):
    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx
        yield (yy,xx) if (0<=yy<H and 0<=xx<W) else (None,None)
def comps(mask):
    seen=np.zeros(mask.shape,bool); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for yy,xx in nb4(a,b):
                        if yy is not None and mask[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
                out.append(pts)
    return out
GREEN=[I[c] for c in ('G1','G2','G3','G4','G5')]
LINE=[I['O'],I['L']]
PINK=[I[c] for c in ('K3','K2','K1','K0')]
# 0. oogglimp: het witte glimpje viel bij de reductie onder 'achtergrond'; ingesloten transparante pixels in de oogzone -> W (model is daar wit)
n=0
for pts in comps(o==0):
    if not any(a in (0,H-1) or b in (0,W-1) for a,b in pts) and all(14<=a<=20 and 20<=b<=26 for a,b in pts):
        for a,b in pts: o[a,b]=I['W']; n+=1
log['0_ingesloten_wit']=n
# 1. ontkorrelen: groene vulklusters < 3 px -> meest voorkomende groene buur (geel, roze, omlijning bevroren: modeldetail)
n=0
for it in range(3):
    for k in GREEN+[I['Y2']]:
        for pts in comps(o==k):
            if len(pts)>=3: continue
            c=Counter(o[yy,xx] for a,b in pts for yy,xx in nb4(a,b) if yy is not None and o[yy,xx] in GREEN+[I['Y1']])
            c.pop(k,None)
            if c:
                v=c.most_common(1)[0][0]
                for a,b in pts: o[a,b]=v; n+=1
log['1_ontkorrelen']=n
# 2. losse omlijningspixels (1 px, geen O-buur, niet aan de buitenrand) -> buurvulkleur
n=0
for pts in comps(np.isin(o,LINE)):
    if len(pts)>1: continue
    a,b=pts[0]; nbv=[o[yy,xx] if yy is not None else 0 for yy,xx in nb4(a,b)]
    if 0 in nbv: continue
    c=Counter(v for v in nbv if v in GREEN)
    if c: o[a,b]=c.most_common(1)[0][0]; n+=1
log['2_losse_omlijning']=n
# 3. buitenrand dicht: dekkende vulpixel met transparante 4-buur -> omlijning (roze poten hebben in het model zelf een roze/donkere rand: blijven)
n=0
for y in range(H):
    for x in range(W):
        if o[y,x] and o[y,x] not in LINE and o[y,x] not in PINK and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(y,x)):
            o[y,x]=I['O']; n+=1
log['3_buitenrand_dicht']=n
# 3a. binnenlijnen dunner (pixel-perfect): de 2x2-reductie maakt van een schuine 1-px modellijn hoekjes (L-vormen) en klonten.
#     Een binnenlijnpixel (niet aan transparant) die alleen een hoek tussen twee loodrechte lijnburen vormt, of in een 2x2-lijnblok zit
#     zonder de lijn te breken, wordt de meest voorkomende vulkleur eromheen. Oog/snavel/poten niet.
def islin(y,x): return 0<=y<H and 0<=x<W and o[y,x] in LINE
def tr(y,x): return not(0<=y<H and 0<=x<W) or o[y,x]==0
n=0
DUN=False   # r1: uitgezet (brak de schuine lijnen in stippels)
for it in range(3 if DUN else 0):
    for y in range(H):
        for x in range(W):
            if o[y,x] not in LINE or y>=38 or (12<=y<=22 and 10<=x<=27): continue
            if any(tr(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1)): continue
            N,S,Wn,E=islin(y-1,x),islin(y+1,x),islin(y,x-1),islin(y,x+1)
            k=sum((N,S,Wn,E))
            elbow=(k==2 and ((N and E and islin(y-1,x+1)==False) or (N and Wn and not islin(y-1,x-1)) or (S and E and not islin(y+1,x+1)) or (S and Wn and not islin(y+1,x-1))))
            if not elbow: continue
            f=Counter(o[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if o[y+dy,x+dx] not in LINE and o[y+dy,x+dx]!=0)
            if f: o[y,x]=f.most_common(1)[0][0]; n+=1
log['3a_lijnhoekjes_dunner']=n
# 3c. dikke binnenlijnen dunner (Zhang-Suen-verdunning op het lijnmasker): waar de 2x2-reductie twee dicht bij elkaar liggende
#     modellijnen of een schuine lijn tot een 2 px dikke klont maakte, blijft 1 px lijn over (de modellijn), de rest wordt de
#     meest voorkomende vulkleur eromheen. Buitenrand (lijnpixel naast transparant), oog/snavel en poten blijven.
def zs():
    m=np.isin(o,LINE)
    prot=np.zeros_like(m)
    for y in range(H):
        for x in range(W):
            if not m[y,x]: continue
            if y>=38 or (12<=y<=22 and 10<=x<=27): prot[y,x]=True
            elif any(not(0<=y+dy<H and 0<=x+dx<W) or o[y+dy,x+dx]==0 for dy in(-1,0,1) for dx in(-1,0,1)): prot[y,x]=True
    weg=[]
    changed=True
    while changed:
        changed=False
        for step in (0,1):
            rm=[]
            for y in range(1,H-1):
                for x in range(1,W-1):
                    if not m[y,x] or prot[y,x]: continue
                    P=[m[y-1,x],m[y-1,x+1],m[y,x+1],m[y+1,x+1],m[y+1,x],m[y+1,x-1],m[y,x-1],m[y-1,x-1]]
                    B=sum(P); A=sum((not P[i]) and P[(i+1)%8] for i in range(8))
                    if not(2<=B<=6 and A==1): continue
                    if step==0 and (P[0] and P[2] and P[4] or P[2] and P[4] and P[6]): continue
                    if step==1 and (P[0] and P[2] and P[6] or P[0] and P[4] and P[6]): continue
                    rm.append((y,x))
            for y,x in rm: m[y,x]=False; weg.append((y,x)); changed=True
    return weg
n=0
weg=zs()
for y,x in weg: o[y,x]=-7
for it in range(4):
    for y,x in weg:
        if o[y,x]!=-7: continue
        f=Counter(o[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if 0<=y+dy<H and 0<=x+dx<W and o[y+dy,x+dx]>0 and o[y+dy,x+dx] not in LINE)
        if f: o[y,x]=f.most_common(1)[0][0]; n+=1
o[o==-7]=I['L']
log['3c_dikke_lijnen_verdund']=n
# 3b. binnenlijnen in de waaier: zwarte lijnpixel die nergens aan transparant grenst en alleen tussen donkere waaiertinten (G4/G5) ligt
#     -> donkergroene lijn L (Gen 3: binnenlijn in een donkere tint van het vlak; het lijf houdt zijn zwarte omlijning en springt naar voren)
n=0; DONKER={I['G4'],I['G5']}
for y in range(H):
    for x in range(W):
        if o[y,x]!=I['O']: continue
        nb8=[o[y+dy,x+dx] if 0<=y+dy<H and 0<=x+dx<W else 0 for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
        if 0 in nb8: continue
        f=[v for v in nb8 if v not in LINE]
        if f and all(v in DONKER for v in f): o[y,x]=-5; n+=1
o[o==-5]=I['L']
log['3b_waaierlijn_donkergroen']=n
# 4. snavel (Jordi 21 nov: "controleer ook of de snavel klopt met de 4 bestaande vormen"): modelsnavel = 9x5 px, recht naar links met
#    hangende punt; alle 4 Gen 3-vormen hebben een korte haaksnavel (5-6 x 6-7). -> modelsnavel weg, Pom-Pom-snavel pixel voor pixel,
#    verschoven met dezelfde (DY,DX) als het Pom-Pom-oog, zodat oog en snavel onderling exact als bij Pom-Pom staan.
DY,DX=-3,-11
SNAVELZONE=[(y,x) for y in range(15,22) for x in range(11,22) if o[y,x] in PINK+[I['Y2']] or (o[y,x]==I['O'] and 16<=y<=20 and 14<=x<=20 and not (y==16 and x>=21))]
n4=0
for y,x in SNAVELZONE:
    # wat erachter ligt: links van de kop = verre vleugel (meest voorkomende groene buur), in de kop = kopkleur G1
    o[y,x]=-1
for it in range(4):
    for y,x in SNAVELZONE:
        if o[y,x]!=-1: continue
        c=Counter(o[yy,xx] for yy,xx in nb4(y,x) if yy is not None and o[yy,xx] in GREEN)
        if c: o[y,x]=c.most_common(1)[0][0]; n4+=1
for y,x in SNAVELZONE:
    if o[y,x]==-1: o[y,x]=I['G2']; n4+=1
POMSNAVEL={19:{28:'8',29:'8',30:'8'},20:{27:'8',28:'9',29:'9',30:'9',31:'8'},21:{26:'8',27:'9',28:'9',29:'9',30:'9',31:'8'},
           22:{25:'8',26:'9',27:'9',28:'9',29:'3',30:'3'},23:{25:'8',26:'9',27:'b',28:'3'},24:{25:'8',26:'9',27:'3'},25:{25:'8',26:'3'}}
PM={'8':I['K3'],'9':I['K1'],'b':I['K2'],'3':I['O']}
for r,d in POMSNAVEL.items():
    for c,v in d.items(): o[r+DY,c+DX]=PM[v]; n4+=1
log['4_snavel_pompom']=n4; log['4_snavel_zone_gevuld']=len(SNAVELZONE)
# 5. oog: modeloog weg (kopkleur G1), Pom-Pom-oog (frame 1, rij 18-22, kol 33-39) pixel voor pixel; 3=zwart, 13=wit, 2/7 = kopschaduw naast het oog
OOGZONE=[(y,x) for y in range(15,20) for x in range(21,26) if o[y,x] in (I['O'],I['W'])]
for y,x in OOGZONE: o[y,x]=I['G1']
POM={18:{34:'O',35:'O',37:'G3',38:'G3'},19:{33:'O',34:'O',35:'O',36:'O',37:'G2',38:'G3'},20:{33:'O',34:'W',35:'O',36:'O',37:'G2',38:'G2',39:'G3'},
     21:{33:'O',34:'W',35:'O',36:'O',37:'G2',38:'G2',39:'G3'},22:{34:'O',35:'O',37:'G2',38:'G3'}}
n5=0
for r,d in POM.items():
    for c,v in d.items(): o[r+DY,c+DX]=I[v]; n5+=1
log['5_oog_model_gewist']=len(OOGZONE); log['5_oog_pompom']=n5
np.save('voor_selout.npy',o)
# 5b. tweede ontkorrelronde na verdunnen/snavel: groene vulklusters < 3 px -> meest voorkomende groene buur (oogzone uit)
n=0
for it in range(3):
    for k in GREEN:
        for pts in comps(o==k):
            if len(pts)>=3 or any(14<=a<=20 and 20<=b<=29 for a,b in pts): continue
            c=Counter(o[yy,xx] for a,b in pts for yy,xx in nb4(a,b) if yy is not None and o[yy,xx] in GREEN)
            c.pop(k,None)
            if c:
                v=c.most_common(1)[0][0]
                for a,b in pts: o[a,b]=v; n+=1
log['5b_ontkorrelen_2']=n
# 6. selout: buitenrandpixel (lijn) met transparant boven/links en niet onder/rechts -> gekleurde selout (groen L, geel Y2, roze K3);
#    donkergroene modellijn (L) op de buitenrand aan de schaduwkant (transparant onder/rechts) -> zwart
SEL={**{g:I['L'] for g in GREEN},I['Y1']:I['Y2'],I['Y2']:I['Y2'],I['W']:I['L']}
n=0; n6b=0
for y in range(H):
    for x in range(W):
        if o[y,x] not in LINE: continue
        up=y==0 or o[y-1,x]==0; lf=x==0 or o[y,x-1]==0
        dn=y==H-1 or o[y+1,x]==0; rt=x==W-1 or o[y,x+1]==0
        if not (up or lf or dn or rt): continue
        if dn or rt:
            if o[y,x]==I['L']: o[y,x]=I['O']; n6b+=1
            continue
        inn=[v for v in ((o[y+1,x] if up else None),(o[y,x+1] if lf else None)) if v is not None and v in SEL]
        if not inn: continue
        if o[y,x]!=SEL[inn[0]]: o[y,x]=SEL[inn[0]]; n+=1
log['6_selout']=n; log['6b_L_schaduwkant_zwart']=n6b
# 6c. roze buitenrand (poten, snavel): lichtroze (K1/K0) of donkerroze (K3) aan de lichtkant (transparant boven/links, niet onder/rechts)
#     -> middenroze K2 als effen selout (model wisselt daar K2/K3/K1 door de reductie: om-en-om voorkomen); aan de schaduwkant -> zwart
n=0
for y in range(H):
    for x in range(W):
        if o[y,x] not in PINK: continue
        up=y==0 or o[y-1,x]==0; lf=x==0 or o[y,x-1]==0; dn=y==H-1 or o[y+1,x]==0; rt=x==W-1 or o[y,x+1]==0
        if (dn or rt) and not (up or lf): o[y,x]=I['O']; n+=1
        elif (up or lf) and o[y,x]!=I['K2']: o[y,x]=I['K2']; n+=1
log['6c_roze_buitenrand']=n
# 7. plaatsen in 64x64: onderkant op rij 61, horizontaal gecentreerd
full=np.zeros((64,64),int); y0=62-H; x0=(64-W)//2; full[y0:y0+H,x0:x0+W]=o
np.save('samba_kls.npy',full)
log['afwijkend_van_onderlaag']=int((o!=basis).sum()); log['plaats']=[int(y0),int(x0),W,H]
print(json.dumps(log))
np.save('afwijk.npy',o!=basis)
