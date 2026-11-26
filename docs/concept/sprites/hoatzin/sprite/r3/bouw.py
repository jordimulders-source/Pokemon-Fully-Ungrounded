# Hoatzin fase 2 r1: model overnemen. Kale reductie (kaal.py) -> alleen technische opschoning en reparaties naar het model; elke stap geteld.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from kaal import reduceer
o,info=reduceer(); kaal=o.copy(); np.save(HIER+'/kaal.npy',kaal); opslaan(kaal,HIER+'/kaal.png')
a,c,L=laad()
GRP={}
for k in LIJF: GRP[k]=LIJF
for k in GG: GRP[k]=GG
for k in BL: GRP[k]=BL
for k in RO: GRP[k]=RO
SEL={2:2,3:2,4:2,5:5,6:5,7:5,8:8,9:8,10:10,11:10}
N4=((-1,0),(1,0),(0,-1),(0,1))
def frac(X,Yy):
    cc,ll,w,_=vak(X,Yy,c,L); return np.array([w[cc==k].sum() for k in range(7)])
# ===== r2 stap T: toon opnieuw verdeeld naar de modelhelderheid per pixel (alleen de lijfpixels van het model, zonder zwart):
#   < 50 donker (= de basis, het grootste vlak; model-piek 36-40), 50-63 midden (bolling hals/borst, vleugelranden, snavelrug),
#   >= 64 licht (alleen hooglicht; model-piek 60-68 toppen). ---
def tlijf2(l): return 2 if l<42 else 3 if l<62 else 4   # r3: grenzen 42/62 -> tinten ongeveer gelijk verdeeld (Murkrow-ramp)
def lD(cc,ll,w): m=cc==D; return (w[m]*ll[m]).sum()/w[m].sum() if m.any() else None
tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
v=o.copy()
for Yy,X in zip(*np.where(np.isin(o,[2,3,4]))):
    cc,ll,w,_=vak(X,Yy,c,L); l=lD(cc,ll,w)
    if l is not None: o[Yy,X]=tlijf2(l)
stap('toon (r2)',v,o)
# ===== reparaties naar het model (op de kale reductie, vóór de buitenlijn) =====
def kuifzone(X,Yy): return (Yy<=8 and 10<=X<=33) or (27<=X<=33 and Yy<=17 and not (X>=33 and Yy>=15)) or (9<=X<=12 and Yy<=10)
# --- A. kuifpunten: de stekels zijn in het model ±1,5 spritepixel breed en breken bij 45 %. In de kuifzone: figuur vanaf 30 %
#        modeldekking, geelgroen wint vanaf 20 % (de punten), zwart vanaf 33 %; tint uit de modelhelderheid zoals kaal.py. ---
from kaal import tgg,tlijf
def lm(cc,ll,w,k): m=cc==k; return (w[m]*ll[m]).sum()/max(w[m].sum(),1e-9)
def lkd(cc,ll,w): m=(cc==K)|(cc==D); return (w[m]*ll[m]).sum()/max(w[m].sum(),1e-9)
v=o.copy()
for Yy in range(0,20):
    for X in range(8,36):
        if not kuifzone(X,Yy): continue
        cc,ll,w,_=vak(X,Yy,c,L); f=np.array([w[cc==k].sum() for k in range(7)])
        if 1-f[0]<0.30: continue
        if f[Y]>=0.20:   # tint van de punt: p75 van de geelgroene modelhelderheid (de punt is in het model fel, de rand olijf)
            m=cc==Y; o[Yy,X]=tgg(np.percentile(ll[m],75))
        elif o[Yy,X]==0: o[Yy,X]=1 if f[K]>=0.33 else (tlijf2(lD(cc,ll,w)) if lD(cc,ll,w) is not None else 2)
#    tint per punt (Gen 3-leesbaarheid op 1x; vorm blijft): per samenhangende geelgroene punt in de kuifzone is de buitenste
#    pixel (verst van het kopmidden 21,12) licht, de rest midden, bij >= 4 px de binnenste olijf (verloop naar binnen, zoals het model).
km=np.zeros((64,64),bool)
for Yy in range(0,20):
    for X in range(8,36):
        if kuifzone(X,Yy) and o[Yy,X] in GG: km[Yy,X]=True
lab_,n_=label(km)
for i in range(1,n_+1):
    pts=sorted(zip(*np.where(lab_==i)),key=lambda p:-((p[1]-21)**2+(p[0]-12)**2))
    for j,(Yy,X) in enumerate(pts):
        o[Yy,X]=7 if j==0 else (5 if (len(pts)>=4 and j==len(pts)-1) else 6)
stap('kuifpunten',v,o)
# --- B. poten en tenen: in het model ±1,9 spritepixel breed; bij 45 % breken knie en tenen. Onder y46: figuur vanaf 33 %. ---
v=o.copy()
for Yy in range(46,64):
    for X in range(10,50):
        if o[Yy,X]: continue
        cc,ll,w,_=vak(X,Yy,c,L); f=np.array([w[cc==k].sum() for k in range(7)])
        if 1-f[0]<(0.45 if (24<=X<=29 and Yy>=58) else 0.33): continue   # r3: tussen de tenen van de verre voet de gewone drempel (model 40 %: gat)
        o[Yy,X]=1 if f[K]>=0.33 else (tlijf2(lD(cc,ll,w)) if lD(cc,ll,w) is not None else 2)
stap('poten',v,o)
# --- C. oog (gezicht = belangrijkste). Kale reductie houdt ring (x17-21, y13-17) en rood (x18-20) al op de modelplek, tinten
#        uit het model. Reparaties naar het model: (17,15) rood->blauw (model: ring rondom dicht, daar R45/B38 %); pupil = het
#        zwarte spleetje (model K 25 % + 23 % in (18,15)/(19,15)) als 1 px zwart op (19,15), midden van het rood;
#        glans = het witte stipje links van de spleet in het model (W 8 % in (18,15)). ---
v=o.copy()
o[15,17]=8
o[15,19]=1
# glans: in het model een wit stipje links van de spleet (W 8 %). Op 3 px iris maakt een witte pixel het oog op 1x wit i.p.v. rood
# (Jordi: "Belangrijk is het rode oog"), dus weggelaten: (18,15) wordt rood (licht, zoals de rest van de iris). Variant met glans in vel_oog.png.
GLANS=(15,18)
o[GLANS]=11
stap('oog',v,o)
# --- D. stralingsteken: alleen de 3 bladen + stip, geelgroen. Uit het model: pixel = teken waar >= 50 % geelgroen
#        modeldekking (zelfde vak als kaal.py, alleen een hogere drempel zodat bladen en stip niet samenklonteren). Waar het
#        model tussen blad en stip een smalle donkere spleet heeft (< 1 spritepixel) worden de raakpixels lijf, zodat de
#        4 delen los lezen: stip = (24,38) (88 %); weg: (25,38) 55 %, (24,39) 60 %, (25,39) 75 %, (23,38) 73 %, (23,39) 53 %.
#        Tint: licht (7) op het vlak, midden (6) aan de onder-/rechterrand van elk blad (licht linksboven). Lijf eromheen = kaal. ---
TEKZ=(20,33,29,44)   # x0,y0,x1,y1
def tekenpixels():
    P=set()
    for Yy in range(TEKZ[1],TEKZ[3]):
        for X in range(TEKZ[0],TEKZ[2]):
            cc,ll,w,_=vak(X,Yy,c,L); fy=w[cc==Y].sum()
            if fy>=0.50: P.add((X,Yy))
    return P-SPLEET
SPLEET={(25,38),(23,39),(25,39),(23,38),(24,39)}   # spleten tussen bladen en stip; stip = (24,38), het sterkste stippixel (88 %)
TP=tekenpixels()
v=o.copy()
for Yy in range(TEKZ[1],TEKZ[3]):
    for X in range(TEKZ[0],TEKZ[2]):
        if X<=20: continue          # linkerrand = verre vleugel (eigen geelgroen), niet aankomen
        if (X,Yy) in TP: o[Yy,X]=6 if ((X,Yy+1) not in TP and (X,Yy-1) in TP) else 7
        elif o[Yy,X] in GG:      # geelgroene reductierestjes rond het teken -> lijftint uit het model
            cc,ll,w,_=vak(X,Yy,c,L); o[Yy,X]=(tlijf2(lD(cc,ll,w)) if lD(cc,ll,w) is not None else 2)
stap('teken',v,o)
# --- E (r2). veerlijnen uit het model: modelpixels met L < 10 (de echte zwarte lijnen; de schaduw is 15-35) die verder dan 12 modelpx van de achtergrond liggen (binnenlijnen,
#        niet de buitenlijn) worden punt voor punt naar het spriteraster gemapt; een spritepixel in de opgeheven vleugel, de verre
#        vleugel of de staart wordt lijn als er >= NV van die punten in vallen (de lijnen zijn in het model ±0,4 spritepx dik en
#        zouden bij de gewone 33 %-drempel verdwijnen). Op lijf -> zwart; in het geelgroen -> olijf (binnenlijn in de eigen donkerste tint). ---
from PIL import ImageFilter
NV=30
bgm=Image.fromarray(((c==0)*255).astype('uint8'))
for _ in range(6): bgm=bgm.filter(ImageFilter.MaxFilter(5))
ver=np.array(bgm)>0
lijnm=(L<10)&(c!=0)&~ver
cnt=np.zeros((64,64),int)
vy,vx=np.where(lijnm)
SXs=np.floor((vx-MX0)*S+SX0).astype(int); SYs=np.floor((vy-MY0)*S+SY0).astype(int)
for X,Yy in zip(SXs,SYs):
    if 0<=X<64 and 0<=Yy<64: cnt[Yy,X]+=1
def vleugelzone(X,Yy): return (X>=33 and 8<=Yy<=31) or (X>=37 and Yy>=31 and Yy<=45) or (X<=20 and 28<=Yy<=48)
v=o.copy()
for Yy,X in zip(*np.where(o>0)):
    if not vleugelzone(X,Yy) or o[Yy,X]==1: continue
    if cnt[Yy,X]>=NV: o[Yy,X]=2 if o[Yy,X] in LIJF else 5   # r3: binnenlijn in de donkerste eigen tint, niet zwart
VEER=(v!=o)
#    veerlichamen: in het model hebben de veren in het donkere vleugeldeel een lichtere grijze bovenrand (L 55-68) die in het
#    vakgemiddelde wegvalt. In de vleugelzones komt de lijftint daarom uit de p75 van de lijfhelderheid in het vak (niet het gemiddelde),
#    zodat die randen middentint worden en de lijnen ertussen lezen. Buitenrand volgt in stap 1.
for Yy,X in zip(*np.where(np.isin(o,[2,3,4]))):
    if not vleugelzone(X,Yy): continue
    cc,ll,w,_=vak(X,Yy,c,L); m=cc==D
    if m.sum()>=20: o[Yy,X]=tlijf2(np.percentile(ll[m],75))
VEER=(cnt>=NV)&(v>0)
stap('veerlijnen',v,o)
# --- F (r2). snavel/masker: in het model loopt een lichte rugrand diagonaal van (12,17) naar (7,22) (L 73-92) en is de
#        onderkant/kaak donker (L 37-48). In de snavelzone (x4-17, y16-25) komt de lijftint uit de modelhelderheid met de
#        snavelgrenzen >= 70 licht, >= 50 midden, anders donker, en de lichte rug wordt beschermd tegen ontkorrelen. ---
def snavelzone(X,Yy): return 4<=X<=17 and 16<=Yy<=25 and not (16<=X and Yy>=21)
SNAVEL=np.zeros((64,64),bool)
v=o.copy()
for Yy,X in zip(*np.where(np.isin(o,[2,3,4]))):
    if not snavelzone(X,Yy): continue
    cc,ll,w,_=vak(X,Yy,c,L); l=lD(cc,ll,w)
    if l is None: continue
    o[Yy,X]=4 if l>=70 else 3 if l>=50 else 2; SNAVEL[Yy,X]=True
stap('snavel',v,o)
# --- 1. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder (schaduwkant): zwart. Lichtkant: selout van de groep. Dunne punten (1 px breed,
#        achtergrond aan beide kanten) houden hun kleur als middentint, zodat geelgroene punten blijven lezen. ---
def rand(o):
    fg=o>0; uit=[]
    for Yy,X in zip(*np.where(fg)):
        k=o[Yy,X]
        if k in (1,12): continue
        bg=[not (0<=Yy+dy<64 and 0<=X+dx<64 and fg[Yy+dy,X+dx]) for dy,dx in N4]   # boven, onder, links, rechts
        if not any(bg): continue
        if k in GG and ((bg[2] and bg[3]) or (bg[0] and bg[1]) or sum(bg)>=3):   # dunne geelgroene punt houdt zijn kleur
            n=k
        elif k in GG and not (bg[1] or bg[3]): n=5 if not ((bg[2] and not (0<=X+2<64 and fg[Yy,X+2])) or (bg[0] and not (Yy+2<64 and fg[Yy+2,X]))) else k
        elif bg[1] or bg[3]: n=1
        elif (bg[2] and not (0<=X+2<64 and fg[Yy,X+2])) or (bg[0] and not (Yy+2<64 and fg[Yy+2,X])): n=min(k,3) if k in LIJF else k   # 2 px breed deel (poten): lichtkant houdt de vulling, hooguit middentint
        else: n=1 if k in LIJF else SEL[k]   # r2: lijf is zo donker dat een selout in de basistint wegvalt; lijn rondom zwart (zoals Murkrow gba)
        if n!=k: uit.append((Yy,X,n))
    for Yy,X,k in uit: o[Yy,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 2. ontkorrelen: tintvlekjes < 3 px (licht < 2) in het lijf nemen de meest voorkomende buurtint van dezelfde groep aan.
#        Niet in oog, teken en kuifpunten (die staan op modelplekken). ---
BESCHERM=np.zeros((64,64),bool); BESCHERM[12:19,16:23]=True
for (X,Yy) in TP: BESCHERM[Yy,X]=True
BESCHERM|=km
BESCHERM|=VEER
BESCHERM|=SNAVEL&(o==4)
fg_=o>0
RAND=np.zeros((64,64),bool)
for Yy,X in zip(*np.where(fg_)):
    RAND[Yy,X]=any(not (0<=Yy+dy<64 and 0<=X+dx<64 and fg_[Yy+dy,X+dx]) for dy,dx in N4)
def ontkorrel(o):
    for k,minim in ((2,3),(3,3),(4,2),(5,2),(6,2)):
        lab_,n_=label(o==k,acht=False)
        for i in range(1,n_+1):
            m=lab_==i
            if m.sum()>=minim or (m&BESCHERM).any() or (m&RAND).any(): continue   # buitenlijn/selout blijft
            buur=[o[Yy+dy,X+dx] for Yy,X in zip(*np.where(m)) for dy,dx in N4 if 0<=Yy+dy<64 and 0<=X+dx<64 and o[Yy+dy,X+dx] in GRP[k] and o[Yy+dy,X+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 3. losse zwarte pixel midden in een vlak (geen zwarte 8-buur, geen achtergrond in de 8-buurt) -> meest voorkomende buurtint ---
v=o.copy()
for Yy,X in zip(*np.where(o==1)):
    if BESCHERM[Yy,X]: continue
    nb8=[o[Yy+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=Yy+dy<64 and 0<=X+dx<64]
    if 0 not in nb8 and 1 not in nb8 and len(nb8)==8:
        nb=[o[Yy+dy,X+dx] for dy,dx in N4]; o[Yy,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)
# ===== r3: benoemde reparaties (keurder) =====
# --- G. zuur verre vleugel (x7-19, y37-47): tint per pixel uit de geelgroene modelhelderheid met harde grenzen
#        < 115 olijf, < 165 midden, anders licht (verloop van binnen naar de punt per veervinger); buitenrand en veerlijnen blijven. ---
v=o.copy()
for Yy in range(37,48):
    for X in range(7,20):
        if o[Yy,X] not in GG or RAND[Yy,X]: continue
        cc,ll,w,_=vak(X,Yy,c,L); m=cc==Y
        if w[m].sum()<0.2: continue
        l=(w[m]*ll[m]).sum()/w[m].sum(); o[Yy,X]=5 if l<115 else 6 if l<165 else 7
#    verloop per vinger van binnen (boven) naar de punt (onder): in een kolom wordt de tint naar beneden nooit weer donkerder
#    (olijf -> midden -> licht, harde grenzen); zwarte lijnen en de buitenrand onderbreken de kolom.
for X in range(7,20):
    hoogst=5
    for Yy in range(37,48):
        k=o[Yy,X]
        if k not in GG: hoogst=5; continue
        if RAND[Yy,X]: continue
        if k<hoogst: o[Yy,X]=hoogst
        hoogst=max(hoogst,o[Yy,X])
stap('zuur verre vleugel',v,o)
# --- F. tenen nabije voet eindigen in zwart (Skarmory gba): lichte tinten aan onder-/rechterrand -> lijn ---
v=o.copy()
for X,Yy in ((30,60),(31,60),(32,59),(33,59),(34,61),(34,62),(37,60)): o[Yy,X]=1
stap('tenen nabije voet',v,o)
# --- H. losse tintvlekjes kop/kuif -> tint van de omringende vlakken (meest voorkomende lijftint van de 8 buren) ---
v=o.copy()
for X,Yy in ((21,17),(13,7),(16,16),(11,18)):
    if o[Yy,X] in LIJF:
        nb=[o[Yy+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and o[Yy+dy,X+dx] in LIJF]
        if nb: o[Yy,X]=max(set(nb),key=nb.count)
stap('tintvlekjes kop',v,o)
# --- D. oog uit het model (keurder r2): rood 3x3 x18-20,y14-16; pupil verticaal (19,14)-(19,15); blauw: links x17, boven y13,
#        onder y17, rechts 2 px (x21 licht, x22 donker; model: blauw tot x22,2); donkere rand (zwart) om het blauw zoals in het model.
#        Rood: bovenrij donker (schaduw onder de rand), rest licht. Geen glans. ---
v=o.copy()
for X in range(18,21):
    for Yy in range(14,17): o[Yy,X]=11
o[14,18]=10; o[14,20]=10
o[14,19]=1; o[15,19]=1
for Yy in range(14,17): o[Yy,17]=8; o[Yy,21]=9; o[Yy,22]=8
for X in range(18,22): o[13,X]=8; o[17,X]=8
o[17,21]=9
for X in range(18,22): o[12,X]=1; o[18,X]=1
for Yy in range(14,17): o[Yy,16]=1; o[Yy,23]=1
for X,Yy in ((17,13),(22,13),(17,17),(22,17)): o[Yy,X]=1
stap('oog (r3)',v,o)
# --- zones: afwijkingen t.o.v. de kale reductie ---
def zone(X,Yy):
    if 16<=X<=22 and 12<=Yy<=18: return 'oog'
    if kuifzone(X,Yy): return 'kuif'
    if TEKZ[0]<=X<TEKZ[2] and TEKZ[1]<=Yy<TEKZ[3] and X>20: return 'teken'
    if X<=32 and Yy<=24 and not (X>=21 and Yy>=21): return 'kop+snavel'
    if Yy>=46: return 'poten'
    if X>=33 and Yy<=31: return 'vleugel rechts (opgeheven)'
    if X>=37 and Yy>=31: return 'staart'
    if X<=20 and Yy>=28: return 'vleugel links (verre)'
    return 'hals+lijf'
ZT={}
for Yy,X in zip(*np.where(o!=kaal)): z=zone(X,Yy); ZT[z]=ZT.get(z,0)+1
print('per zone',ZT)
NAAM=HIER+'/hoatzin_r3.png'
np.save(HIER+'/r3.npy',o); opslaan(o,NAAM)
print('stappen',tel); print('anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren',len(set(o.ravel()))-1,'| figuur',(o>0).sum())

# ===== variant: teken iets naar de buikrand (voorrand linksonder), deels achter de ronding =====
# Dezelfde tekenpixels (geen nieuwe), verschoven met (-2,+1) = langs de modelnormaal van de buikrand (0,78/-0,63, teken2.py) naar buiten.
# Waar een verschoven pixel op de buitenlijn, de verre vleugel of de achtergrond valt, valt hij weg (achter de ronding).
DX,DY=-2,1
ov=o.copy()
for (X,Yy) in TP:   # oude plek: meest voorkomende lijftint van de buren buiten het teken (het model heeft daar teken, geen lijf)
    nb=[o[Yy+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (X+dx,Yy+dy) not in TP and o[Yy+dy,X+dx] in LIJF]
    ov[Yy,X]=max(set(nb),key=nb.count) if nb else 4
for (X,Yy) in TP:
    X2,Y2=X+DX,Yy+DY
    if o[Y2,X2] in LIJF and not RAND[Y2,X2] and (X2,Y2) not in TP or ((X2,Y2) in TP): 
        if ov[Y2,X2] in LIJF or (X2,Y2) in TP: ov[Y2,X2]=o[Yy,X]
weg=sum(1 for (X,Yy) in TP if ov[Yy+DY,X+DX] not in GG)
ontkorrel(ov)
opslaan(ov,HIER+'/hoatzin_r3_variant_teken.png'); np.save(HIER+'/variant.npy',ov)
print('variant: teken %d px, waarvan %d weggevallen achter de rand; anders dan hoofdversie %d px'%(len(TP),weg,(ov!=o).sum()))
