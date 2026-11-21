# kaal_11_d1.npy (2x2-blokreductie van het natieve model, elke pixel uit zijn eigen modelblok) -> samba_kls.npy + log per stap.
# Coordinaten hieronder = uitsnede (rij, kolom) van de onderlaag; aan het eind geplaatst in 64x64.
import numpy as np, json
from collections import Counter
from palet import NAMEN, I
o=np.load('kaal_11_d1.npy'); ys,xs=np.where(o>0); o=o[ys.min():ys.max()+1,xs.min():xs.max()+1].copy()
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
GREEN=[I[c] for c in ('G1','G2','G3','G4','G5','G6')]
PINK=[I[c] for c in ('K3','K2','K1','K0')]
# 0. oogglimp: het witte glimpje viel bij de reductie onder 'achtergrond'; ingesloten transparante pixels -> W (model is daar wit)
n=0
for pts in comps(o==0):
    if not any(a in (0,H-1) or b in (0,W-1) for a,b in pts):
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
for pts in comps(o==I['O']):
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
        if o[y,x] and o[y,x]!=I['O'] and o[y,x] not in PINK and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(y,x)):
            o[y,x]=I['O']; n+=1
log['3_buitenrand_dicht']=n
# 4. snavel (Jordi 21 nov: "controleer ook of de snavel klopt met de 4 bestaande vormen"): modelsnavel = 9x5 px, recht naar links met
#    hangende punt; alle 4 Gen 3-vormen hebben een korte haaksnavel (5-6 x 6-7). -> modelsnavel weg, Pom-Pom-snavel pixel voor pixel,
#    verschoven met dezelfde (DY,DX) als het Pom-Pom-oog, zodat oog en snavel onderling exact als bij Pom-Pom staan.
DY,DX=-3,-11
SNAVELZONE=[(y,x) for y in range(15,22) for x in range(12,22) if o[y,x] in PINK or (o[y,x]==I['O'] and 16<=y<=20 and 14<=x<=21)]
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
# 6. selout: omlijning aan de lichtkant (transparant boven/links, niet onder/rechts) -> donkere tint van de vulgroep eronder/rechts
SEL={I['G1']:I['G3'],I['G2']:I['G4'],I['G3']:I['G4'],I['G4']:I['G5'],I['G5']:I['G6'],I['G6']:I['G6'],I['Y1']:I['Y2'],I['Y2']:I['Y2']}
n=0
for y in range(H):
    for x in range(W):
        if o[y,x]!=I['O']: continue
        up=y==0 or o[y-1,x]==0; lf=x==0 or o[y,x-1]==0
        dn=y==H-1 or o[y+1,x]==0; rt=x==W-1 or o[y,x+1]==0
        if not (up or lf) or dn or rt: continue
        inn=[v for v in ((o[y+1,x] if up else None),(o[y,x+1] if lf else None)) if v is not None and v in SEL]
        if not inn: continue
        o[y,x]=SEL[inn[0]]; n+=1
log['6_selout']=n
# 7. plaatsen in 64x64: onderkant op rij 61, horizontaal gecentreerd
full=np.zeros((64,64),int); y0=62-H; x0=(64-W)//2; full[y0:y0+H,x0:x0+W]=o
np.save('samba_kls.npy',full)
log['afwijkend_van_onderlaag']=int((o!=basis).sum()); log['plaats']=[int(y0),int(x0),W,H]
print(json.dumps(log))
np.save('afwijk.npy',o!=basis)
