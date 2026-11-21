# schrap.npy (onderlaag: 4->3 schrappen, elke pixel = modelpixel) -> cumbia_kls.npy (klassen) + log per stap.
import numpy as np, json
from collections import Counter
NAMEN=['_','O','B1','B2','B3','N','M','L1','L2','P','K1','K2','R','G','Y','W']
I={n:i for i,n in enumerate(NAMEN)}
o=np.load('schrap.npy').copy(); H,W=o.shape
basis=o.copy(); log={}
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
GR={I['B1']:'b',I['B2']:'b',I['B3']:'b',I['N']:'s',I['M']:'s',I['L1']:'s',I['L2']:'s',I['P']:'s',I['K1']:'k',I['K2']:'k'}
BLOEM=(slice(8,21),slice(31,46))   # bloem: veelkleurig in het model, niet ontkorrelen
def in_bloem(y,x): return 8<=y<21 and 31<=x<46
# 0. k-means-ruis: rood in de poten (rij >= 56) is lichtroze in het model
n=0
for y in range(56,H):
    for x in range(W):
        if o[y,x]==I['R']: o[y,x]=I['K1']; n+=1
log['0_rood_in_poot']=n
# 1. ontkorrelen: vulklusters < 3 px nemen de meest voorkomende buurvulkleur aan (omlijning, accenten R/G/Y en bloem bevroren)
n=0
for it in range(3):
    for k in [I[c] for c in ('B1','B2','B3','N','M','L1','L2','P')]:   # roze (snavel, poten, vingertjes) = modeldetail, bevroren
        for pts in comps(o==k):
            if len(pts)>=3 or any(in_bloem(a,b) for a,b in pts): continue
            if k in (I['K1'],I['K2']) and any(a>=56 for a,b in pts): continue   # poten: model-lijnpatroon K|k houden
            if k==I['P'] and len(pts)==2: continue   # ruchesrandje (lichtste) mag dun zijn
            c=Counter(o[yy,xx] for a,b in pts for yy,xx in nb4(a,b) if yy is not None and o[yy,xx] in GR)
            c.pop(k,None)
            if c:
                v=c.most_common(1)[0][0]
                for a,b in pts: o[a,b]=v; n+=1
log['1_ontkorrelen_vul']=n
# 2. losse omlijningspixels (1 px, geen O-buur, niet aan de buitenrand) -> buurvulkleur
n=0
for pts in comps(o==I['O']):
    if len(pts)>1: continue
    a,b=pts[0]; nbv=[o[yy,xx] if yy is not None else 0 for yy,xx in nb4(a,b)]
    if 0 in nbv or in_bloem(a,b): continue
    c=Counter(v for v in nbv if v in GR)
    if c: o[a,b]=c.most_common(1)[0][0]; n+=1
log['2_losse_omlijning']=n
# 3. buitenrand dicht: dekkende vulpixel met transparante 4-buur -> omlijning (selout volgt in stap 5)
n=0
for y in range(H):
    for x in range(W):
        if o[y,x] and o[y,x]!=I['O'] and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(y,x)):
            if o[y,x] in (I['K1'],I['K2']): continue   # poten/snavel: model heeft daar zelf al een roze selout
            if o[y,x] in (I['R'],I['G'],I['Y']) and in_bloem(y,x): o[y,x]=I['O']; n+=1; continue
            o[y,x]=I['O']; n+=1
log['3_buitenrand_dicht']=n
# 4. oog: model-oog weg (wordt kopvulkleur B1), dan Pa'u-oog (Gen 3 Oricorio) pixel voor pixel. Ankers in de log.
OOGZONE=[(y,x) for y in range(20,24) for x in range(31,37) if o[y,x]==I['O']]
for y,x in OOGZONE: o[y,x]=I['B1']
# r2 (Jordi 21 nov: "ja pom pom oog voor cumbia"): Pom-Pom frame 1, rijen 18-22, kolommen 33-39; 3=zwart, 13=wit, 2=middentint, 7=donkere tint van de kop
POM={18:{34:'O',35:'O',37:'B3',38:'B3'},19:{33:'O',34:'O',35:'O',36:'O',37:'B2',38:'B3'},20:{33:'O',34:'W',35:'O',36:'O',37:'B2',38:'B2',39:'B3'},21:{33:'O',34:'W',35:'O',36:'O',37:'B2',38:'B2',39:'B3'},22:{34:'O',35:'O',37:'B2',38:'B3'}}
DY,DX=1,-3   # schrap-coördinaten (sprite = schrap - 5): oog links op 2 px van de snavelbasis (zoals Pom-Pom), hoogte = model-oog
oog=[]
for r,d in POM.items():
    for c,v in d.items():
        y,x=r+DY,c+DX; o[y,x]=I[v]; oog.append((y,x,v))
# 4b. waar r1 het Pa'u-ooglid had, stond in de onderlaag een losse rokkleur-pixel (N, k-means-ruis) in de kop -> kopkleur (donkere kopschaduw ernaast)
n=0
for y in range(17,25):
    for x in range(29,40):
        if o[y,x]==I['N']: o[y,x]=I['B3']; n+=1
log['4b_ruis_in_kop']=n
log['4_oog_modeloog_gewist']=len(OOGZONE); log['4_oog_pompom_pixels']=len(oog)

# 5. selout: omlijning aan de lichtkant (transparant boven/links, niet onder/rechts) -> donkere tint van de vulgroep
SEL={'b':I['B3'],'s':I['N'],'k':I['K2']}
n=0
for y in range(H):
    for x in range(W):
        if o[y,x]!=I['O'] or in_bloem(y,x): continue
        up=y==0 or o[y-1,x]==0; lf=x==0 or o[y,x-1]==0
        dn=y==H-1 or o[y+1,x]==0; rt=x==W-1 or o[y,x+1]==0
        if not (up or lf) or dn or rt: continue
        inn=[o[y+1,x] if up else None, o[y,x+1] if lf else None]
        g=[GR.get(v) for v in inn if v is not None]
        g=[v for v in g if v]
        if not g: continue
        s=SEL[g[0]]
        if all(v==s for v in inn if v is not None): continue
        o[y,x]=s; n+=1
log['5_selout']=n
# 5b. lichtroze (K1) op de buitenrand van poten/snavel: lichtkant -> K2 (selout), schaduwkant -> zwart
n=0
for y in range(H):
    for x in range(W):
        if o[y,x]!=I['K1']: continue
        up=y==0 or o[y-1,x]==0; lf=x==0 or o[y,x-1]==0; dn=y==H-1 or o[y+1,x]==0; rt=x==W-1 or o[y,x+1]==0
        if dn or rt: o[y,x]=I['O']; n+=1
        elif up or lf: o[y,x]=I['K2']; n+=1
log['5b_roze_buitenrand']=n
# 6. plaatsen in 64x64: onderkant op rij 61, horizontaal gecentreerd
ys,xs=np.where(o>0); crop=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=crop.shape
full=np.zeros((64,64),int); y0=62-h; x0=(64-w)//2; full[y0:y0+h,x0:x0+w]=crop
# 7. snavel (Jordi 21 nov: "controleer ook of de snavel klopt met de 4 bestaande vormen"): de modelsnavel is ±10x8 px,
#    alle Gen 3-vormen hebben dezelfde kleine haaksnavel (±6x7). Modelsnavel weg, Pom-Pom-snavel pixel voor pixel erop
#    (zelfde verschuiving als het Pom-Pom-oog: rij -4, kolom -8), zodat oog en snavel onderling exact als bij Pom-Pom staan.
f=full; n7=0
for y in range(11,22):
    for x in range(10,21):
        if f[y,x] in (I['K1'],I['K2']) or (f[y,x]==I['O'] and y>=13): f[y,x]=0; n7+=1
for y in range(12,19):                      # kopvoorkant achter de oude snavel dichtzetten: kol 20 = selout, 21-23 = kopkleur
    if f[y,20]==0 or f[y,20] in (I['K1'],I['K2']): f[y,20]=I['B3']; n7+=1
    for x in range(21,24):
        if f[y,x] in (I['K1'],I['K2'],I['O']): f[y,x]=I['B1']; n7+=1
POMSNAVEL={19:{28:'D',29:'D',30:'D'},20:{27:'D',28:'k',29:'k',30:'k',31:'D'},21:{26:'D',27:'k',28:'k',29:'k',30:'k',31:'D'},
           22:{25:'D',26:'k',27:'k',28:'k',29:'O',30:'O'},23:{25:'D',26:'k',27:'K',28:'O'},24:{25:'D',26:'k',27:'O'},25:{25:'D',26:'O'}}
MAP={'k':I['K1'],'K':I['K2'],'D':I['K2'],'O':I['O']}
for r,d in POMSNAVEL.items():
    for c,v in d.items(): f[r-4,c-8]=MAP[v]; n7+=1
# 7b. kin onder de snavelpunt dicht (bij Pom-Pom loopt de kop onder de snavel door; r2 had daar een transparant inhamje)
for y,x in ((20,20),(21,19),(21,20)):
    if f[y,x]==0: f[y,x]=I['B3']; n7+=1
log['7_snavel_pompom']=n7
# 8. poten vast aan het lijf (r3, Jordi: "die lijken niet goed vast te zitten"). Model: poot = kolom [roze selout, roze, zwart]
#    die direct uit de rokrand komt (natief r78-81 links, r76-78 rechts); Gen 3 Pa'u tekent de aanzet zo in de rokrandrij zelf
#    (rij 55: '9e4', rij 56: '9a4'). Schrappen had de linkerpoot schuin en 1 rij kort gemaakt en rechts een gat gelaten.
P={'D':I['K2'],'k':I['K1'],'O':I['O'],'.':0}
POOT=[ # links: rokhoek (53,27) -> verticaal 2 rijen, dan 1 naar links in de voet
 (54,27,'D'),(54,28,'k'),(54,29,'O'),
 (55,25,'.'),(55,26,'.'),(55,27,'D'),(55,28,'k'),(55,29,'O'),
 (56,26,'k'),(56,27,'k'),(56,28,'O'),
 (57,27,'k'),(57,28,'O'),
 # rechts: gat tussen poot en rokrand dicht, kolom [D,k,O]
 (52,38,'D'),(52,39,'O'),(53,37,'D'),(53,38,'k'),(53,39,'O'),(54,37,'D'),(54,38,'k'),(54,39,'O'),(55,38,'D'),(55,39,'k')]
n8=0
for y,x,v in POOT:
    if f[y,x]!=P[v]: f[y,x]=P[v]; n8+=1
log['8_poten']=n8
# 9. r4 (Jordi: "de poten zijn denk ik te verschillend van de bestaande oricorio vormen? Vergelijk eens"):
#    poten + voeten van Pa'u (frame 1, rijen 55-60) pixel voor pixel; aanzet tegen de rokrand uit r3 (rij 52-55) blijft.
#    Hele poot verschoven: links kolom +3, rechts kolom +4 (zelfde rijen), zodat de pootkolom onder dezelfde rokpunt zit als in r3.
n9=0
for y in range(55,64):
    for x in range(64):
        if f[y,x]: f[y,x]=0; n9+=1
for x,v in ((27,'D'),(28,'k'),(29,'O')): f[55,x]=P[v]; n9+=1      # linker aanzet r3 (rij 55) terug
PAU_L={56:{20:'D',21:'O',22:'O',23:'K',24:'D',25:'D',26:'O'},57:{18:'D',19:'D',20:'k',21:'k',22:'k',23:'k',24:'K',25:'D'},
       58:{17:'D',18:'k',19:'k',20:'K',21:'O',22:'O',23:'O',24:'O',25:'O',26:'O'},59:{17:'O',18:'O',19:'O',20:'O'}}
PAU_R={55:{34:'D',35:'K',36:'O'},56:{34:'D',35:'k',36:'O'},57:{32:'D',33:'D',34:'k',35:'k',36:'k',37:'O'},
       58:{31:'D',32:'k',33:'D',34:'k',35:'K',36:'k',37:'k',38:'O'},59:{31:'O',32:'O',33:'O',34:'k',35:'O',36:'O',37:'k',38:'O'},60:{33:'O',34:'O',37:'O',38:'O'}}
P2={'D':I['K2'],'K':I['K2'],'k':I['K1'],'O':I['O']}   # Pa'u heeft 3 rozen (D 115,63,72 / K 191,105,120 / k 255,166,181); wij 2: D en K -> K2
for tab,dx in ((PAU_L,3),(PAU_R,4)):
    for r,d in tab.items():
        for c,v in d.items(): f[r,c+dx]=P2[v]; n9+=1
log['9_poten_pau']=n9
np.save('cumbia_kls.npy',full)
diff=(o!=basis); log['totaal_afwijkend_van_onderlaag']=int(diff.sum()); log['bbox']=[w,h,int(y0),int(x0)]
print(json.dumps(log))
np.save('afwijk.npy',diff)
