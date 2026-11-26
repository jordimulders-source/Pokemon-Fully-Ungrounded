# Sneeuwmonster r2: r1 (bevroren basis) + vier benoemde reparaties, alles uit het model (niets getekend).
#   1 ogen opnieuw gemeten op het 1024-model (dekking per spritepixel), tinten uit de modelhelderheid
#   2 sneeuwpluk: binnenlijnen tussen de bolletjes uit het model, randen van de bolletjes in de modeltint
#   3 armstompje rechts: binnenlijn doorlopend op de gemapte modelpixels
#   4 volume: lichttint per vlak (kop/lijf) uit de modelhelderheid, verzacht over het vlak (zie NOTITIES)
# Gebruik: cd sneeuwmonster && python3 sprite_r2/bouw.py [oogvariant links rechts], bv. "LA RA" (standaard LB RB)
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
UIT='sprite_r2'
r1=np.asarray(Image.open('sprite_r1/sneeuwmonster_r1.png')).astype(int)
o=r1.copy()
tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())

# modelhelderheid van de sneeuw per spritepixel (oppervlakgewogen over het natieve raster, alleen sneeuwklasse)
mw=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        fw=lw=0
        for u,v_,w in overlap(X,Y):
            if c[v_,u]==4: fw+=w; lw+=w*L[v_,u]
        mw[Y,X]=lw/fw if fw>0.2 else np.nan
def tw(l): return 3 if l<212 else 4 if l<236 else 5

# ---------- 4. VOLUME (eerst, op de sneeuwvlakken van r1) ----------
# Gemeten: de lichte sneeuw in het model is vlak (L 240-245, ruis +-2); de enige helderheidsinformatie is de schaduw (L +-200) en
# de smalle overgang ertussen. Schaduw blijft precies waar het model hem heeft (L < 212). Voor licht/midden binnen het verlichte
# deel: de modelhelderheid per pixel, verzacht over het eigen vlak (genormaliseerde gauss, sigma SIG, alleen sneeuwpixels van
# hetzelfde vlak; omlijning, steen en achtergrond tellen niet mee). Dicht bij de modelschaduw zakt die waarde -> midden; ver
# ervan (linksboven) blijft hij hoog -> licht. De grens volgt dus de vorm van de modelschaduw (gebogen), niet de buitenrand.
SIG=2.0; DREMPEL={'kop':236.0,'lijf':235.0}
def vlak(Y,X):
    if Y<=17 or Y>=47: return None     # sneeuwpluk en voetjes: eigen kleine vormen, blijven r1 (model)
    return 'kop' if Y<=31 else 'lijf'
v=o.copy()
sneeuw=np.isin(r1,(3,4,5))
yy,xx=np.mgrid[-6:7,-6:7]; G=np.exp(-(xx**2+yy**2)/(2*SIG**2))
zacht=np.full((64,64),np.nan)
for Y,X in zip(*np.where(sneeuw)):
    z=vlak(Y,X)
    if z is None or np.isnan(mw[Y,X]): continue
    s=w_=0
    for dy in range(-6,7):
        for dx in range(-6,7):
            q=(Y+dy,X+dx)
            if 0<=q[0]<64 and 0<=q[1]<64 and sneeuw[q] and vlak(*q)==z and not np.isnan(mw[q]):
                g=G[dy+6,dx+6]; s+=g*mw[q]; w_+=g
    zacht[Y,X]=s/w_
for Y,X in zip(*np.where(sneeuw)):
    z=vlak(Y,X)
    if z is None or np.isnan(zacht[Y,X]): continue
    if mw[Y,X]<212: o[Y,X]=3                       # schaduw = model
    elif mw[Y,X]<236: o[Y,X]=4                     # modelovergang blijft midden (nooit lichter dan het model)
    else: o[Y,X]=5 if zacht[Y,X]>=DREMPEL[z] else 4
# ontkorrelen binnen de vlakken (tintvlekjes < 3 px, licht < 2 -> buurtint)
def ontkorrel(o,mag):
    for k,minim in ((3,3),(4,3),(5,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim or not mag[m].all(): continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (3,4,5) and o[Y+dy,X+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
mag=sneeuw.copy(); mag[:18]=False
ontkorrel(o,mag); ontkorrel(o,mag)
stap('volume',v,o)
if 'zacht' in sys.argv:
    for Y in range(18,47): print('%2d '%Y+' '.join('  .' if np.isnan(zacht[Y,X]) else '%3d'%zacht[Y,X] for X in range(18,46)))
    sys.exit()
for z in ('kop','lijf'):
    m=np.array([[vlak(Y,X)==z for X in range(64)] for Y in range(64)])&sneeuw
    print('volume %s: licht %d, midden %d, schaduw %d'%(z,((o==5)&m).sum(),((o==4)&m).sum(),((o==3)&m).sum()))

# ---------- 2. SNEEUWPLUK ----------
# Binnenlijnen uit het model (natieve sneeuwlijnpixels gemapt naar de sprite), 1 px, doorlopend:
#   A links|midden: model (45,19)K (46,19) (46,20) (47,21) -> (30,13) (31,14)
#   B midden|rechts: model (53,18)K (52,20) (51,21)         -> (34,13) (33,14)
#   C onderkant linkerbolletje: model (41,22-23)K (43,24) (44,25) -> (28,16) (28,17)
# Randen in de modeltint: bovenrand linkerbolletje (28,12) en rechterbolletje (35,13) (36,13) zijn in het model blauw
# (natief (43-44,18) en (54-56,19)); r1 maakte ze zwart (buitenlijnregel / om-en-om) -> sneeuwlijn.
v=o.copy()
for X,Y in ((30,13),(31,14),(34,13),(33,14),(28,16),(28,17)): o[Y,X]=2
for X,Y in ((28,12),(35,13),(36,13)): o[Y,X]=2
stap('sneeuwpluk',v,o)

# ---------- 3. ARMSTOMPJE RECHTS ----------
# Model: binnenboog natief (56,56)->(57,57)(57,58)(58,59)(58,60)(59,61)(59,62)(60,62)(60,63)(61,64)(62,65)(63,65)(63,66)..(66,66)(67,65);
# gemapt (vloer van (u+0,5-27)*S+18) en tot 1 px 8-samenhangend gedund:
ARM=[(36,36),(37,37),(37,38),(38,39),(38,40),(39,41),(40,42),(41,43),(42,43)]
v=o.copy()
for X,Y in ARM: o[Y,X]=2
# oude, gebroken r1-lijnstukjes in het armvak die niet op de modelboog liggen -> sneeuwtint uit het model
for Y in range(36,45):
    for X in range(35,43):
        if o[Y,X]==2 and (X,Y) not in ARM and not any(o[Y+dy,X+dx] in (0,1) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))):
            o[Y,X]=tw(mw[Y,X]) if not np.isnan(mw[Y,X]) else 3
stap('armstompje',v,o)

# ---------- 1. OGEN ----------
# Gemeten op het 1024-model: dekking donker (L<160, verzadiging<45) + wit hooglicht in het oog per spritepixel; tint per pixel uit de
# gemiddelde helderheid van de donkere modelpixels (< 48 zwart, < 76 steen donker, anders steen midden); glans op de modelplek.
# Rechteroog dekking (x30-33, y23-26):  .30 .73 .67 .13 / .79 .72 .98 .36 / .84 1.0 1.0 .32 / .43 .94 .74 .10
# Linkeroog  dekking (x22-24, y22-26):  -- .47 .23 / .39 .38 .96 / .54 .76 1.0 / .39 .98 .80 / -- .29 .12
OGEN={
 # rechteroog A: rond 4x4-steentje (dekking >= .30, hoeken eraf zoals een rond steentje)
 'RA':{(31,23),(32,23),(30,24),(31,24),(32,24),(33,24),(30,25),(31,25),(32,25),(33,25),(31,26),(32,26)},
 # rechteroog B: 3x4 (dekking >= .40, rechterkolom .32-.36 valt weg), linkerhoeken eraf
 'RB':{(31,23),(32,23),(30,24),(31,24),(32,24),(30,25),(31,25),(32,25),(31,26),(32,26)},
 # linkeroog A: smal ovaal 3 breed x 4 hoog (dekking >= .38, hoeken (22,22) (24,22) (22,25) eraf)
 'LA':{(23,22),(22,23),(23,23),(24,23),(22,24),(23,24),(24,24),(23,25),(24,25)},
 # linkeroog B: 2 breed x 4 hoog (dekking >= .45, kolom x22 valt weg; (23,22) .47 blijft als top)
 'LB':{(23,22),(23,23),(24,23),(23,24),(24,24),(23,25),(24,25)},
}
GLANS={'R':(31,24),'L':(22,23)}   # zwaartepunt wit modelhooglicht: rechts (31.0,24.4), links (22.8,23.4)
MG=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); LG=MG@[.299,.587,.114]; SG=MG.max(2)-MG.min(2); DK=(LG<160)&(SG<45)
fr=lambda X,ph,o0,u0: int(round(ph+0.5+10.24*((X-o0)/S+u0)))
def oogtint(X,Y):
    r=np.s_[fr(Y,9.25,Y0,V0):fr(Y+1,9.25,Y0,V0),fr(X,9.05,X0,U0):fr(X+1,9.05,X0,U0)]
    d=DK[r]
    if not d.any(): return 7
    l=LG[r][d].mean(); return 1 if l<48 else 6 if l<76 else 7
kz=sys.argv[1:3] if len(sys.argv)>2 and sys.argv[1] in OGEN else ['LB','RB']
v=o.copy()
for vak in ((21,26,21,27),(29,34,22,28)):     # oogvakken: r1-oogpixels terug naar sneeuw (modeltint), buitenlijn blijft
    for Y in range(vak[2],vak[3]+1):
        for X in range(vak[0],vak[1]+1):
            if (o[Y,X] in (1,6,7,8) or (X,Y) in ((23,23),(31,24))) and not any(o[Y+dy,X+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))):
                o[Y,X]=tw(mw[Y,X]) if not np.isnan(mw[Y,X]) else 5
for k in kz:
    for X,Y in OGEN[k]: o[Y,X]=oogtint(X,Y)
    gx,gy=GLANS[k[0]]
    if (gx,gy) in OGEN[k]: o[gy,gx]=5
    else:   # glans buiten de vorm: dichtstbijzijnde oogpixel met >= 2 oogburen
        kand=[p for p in OGEN[k] if sum((p[0]+dx,p[1]+dy) in OGEN[k] for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)))>=2]
        p=min(kand,key=lambda p:(p[0]-gx)**2+(p[1]-gy)**2); o[p[1],p[0]]=5
stap('ogen',v,o)

naam=UIT+('/sneeuwmonster_r2.png' if kz==['LB','RB'] else '/oog_%s_%s.png'%tuple(kz))
opslaan(o,naam); toon(o,8,56,14,50)
print('stappen',tel,'| totaal anders dan r1: %d px'%(o!=r1).sum(),'| silhouet-diff t.o.v. r1:',int(((o>0)!=(r1>0)).sum()))

# ---------- MONDVARIANTEN (alleen bij de standaardversie; zelfde regel en pixels als r1, zie sprite_r1/NOTITIES.md) ----------
if kz==['LB','RB']:
    MONDEN={'shroomish':[(-1,0,4),(0,0,3),(1,0,4)],   # Shroomish (28,30) 3 · (29,30) 2 · (30,30) 3 op huid 4 -> stappen onder licht
            'chinchou':[(0,0,2),(0,1,2)]}             # Chinchou (31,36) (31,37) donkerrood -> sneeuwlijn
    MX,MY=27,27
    for n,px in MONDEN.items():
        m=o.copy()
        for dx,dy,k in px: m[MY+dy,MX+dx]=k
        opslaan(m,UIT+'/mond_%s.png'%n)
        print('mond',n,[(int(X),int(Y),CH[o[Y,X]]+'>'+CH[m[Y,X]]) for Y,X in zip(*np.where(m!=o))])
