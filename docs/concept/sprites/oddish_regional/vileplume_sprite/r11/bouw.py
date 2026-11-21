# Vileplume r11 = r10_voor_r3 + Jordi's punten op r10 (20 nov). Draaien vanuit vileplume_sprite/: python3 r11/bouw.py
# "wat er bij de voorste 2 foutgaat is niet zo zeer de vorm van de anemonen, maar meer de ronde vorm erom heen die er
# niet goed bij past, daarnaast zijn de cirkels erin ook nog niet goed. De linkerpoot mag nog iets meer een knievorm
# hebben, ogen moeten we een andere kleur geven zodat het niet samenvoegt met de anemonen"
# Keuzes: omtrek voorste 2 = zoals het model; mondjes voorste 2 = zoals het model; ogen = "een kleur die goed contrast geeft".
# Alles buiten de zones VL/VR (+ hun rand), linkerpoot en de 4 ooppixels blijft pixel voor pixel r10 (assert onderaan).
import sys, io, contextlib, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from gemeen import *; from anemonen import *; from klassen import klassen

BASIS='r10/r10_voor_r3.png'
im=Image.open(BASIS); o10=np.asarray(im).astype(int); PAL=[tuple(c) for c in np.array(im.getpalette()[:48]).reshape(-1,3)]
o=o10.copy()
K,R0,R1,R2,R3,W0=1,2,3,4,5,6
LIJF={6,7,8,9,10}; KR={7,11,12,13,14,15}

# ---- r3-indeling (de voorste anemonen VL/VR in r10 zijn 1-op-1 r3): eigenaar per pixel, klonten (tentakels), mondjes ----
src=open('r3/bouw.py').read().replace("opslaan(o,PAL,RONDE+'/vileplume_'+RONDE+'.png')","pass")
ns={'__name__':'r3bouw'}; argv=sys.argv; sys.argv=['r3/bouw.py','r3']
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,'r3/bouw.py','exec'),ns)
sys.argv=argv
OWN,KL,MOND3=ns['OWN'],ns['KL'],ns['MOND']
r3=np.asarray(Image.open('r3/vileplume_r3.png')).astype(int)
VOOR=np.isin(OWN,[0,1]); assert (o10[VOOR]!=r3[VOOR]).sum()==6, 'VL/VR in r10 = r3 op de 6 naadpixels van r10 na'
KRATERBOX=lambda X,Y: 23<=X<=39 and 9<=Y<=17
def mondmidden(i):
    cx,cy=MOND[i][:2]; return 4+(cx-36)*S, 1+(cy-28)*S
def ctr(X,Y): return U0+(X+0.5-X0)/S, V0+(Y+0.5-Y0)/S
gewijzigd={}   # zone -> set van pixels
def zet(zone,X,Y,k):
    if o[Y,X]!=k: o[Y,X]=k; gewijzigd.setdefault(zone,set()).add((X,Y))

# ---- 1. Omtrek VL/VR zoals het model ----
# Gemeten (NOTITIES): de buitenmaat van VL/VR (r3-ellipsen, gemeten op het model) en de onderrand (lobben, zwarte lijn,
# R1-voetschaduw; onderste kroonrij per kolom r10 = kale reductie, x8-55: 0 verschil) kloppen al met het model.
# Wat niet bij het model past is de gesloten ZWARTE RING boven/opzij, waar VL/VR over L, T, R en de krater liggen, en de
# gladde ronde bovenrand. In het model:
#  - onderste helft (de "voet"/schijf die over L en R valt): donkerrode rand (R0), geen zwart;
#  - bovenste helft: de tentakels steken als losse vingers uit, met inkepingen ertussen, tegen de donkerdere (beschaduwde)
#    achterste anemoon. Geen lijn om de vingers; de achterste anemoon ligt er in schaduw (R1) achter.
N4=((1,0),(-1,0),(0,1),(0,-1))
def buren(X,Y,n=N4): return [(X+dx,Y+dy) for dy,dx in n if 0<=X+dx<64 and 0<=Y+dy<64]
def boven(i,X,Y):
    u,v=ctr(X,Y); return np.sin(hoek(i,u,v))<-0.20
def eigen_voor(X,Y):
    b=[OWN[y,x] for x,y in buren(X,Y) if OWN[y,x] in (0,1)]; return max(set(b),key=b.count) if b else -1
def is_achter(X,Y): return not VOOR[Y,X] and o10[Y,X] not in KR and not KRATERBOX(X,Y) and o10[Y,X]!=0 and o10[Y,X] not in LIJF
# a) ring: zwarte pixels van de achterste anemonen die aan VL/VR grenzen (niet krater, niet tegen achtergrond/lijf)
ring=[]
for Y in range(2,31):
    for X in range(2,62):
        if o10[Y,X]!=K or not is_achter(X,Y): continue
        if any(VOOR[y,x] for x,y in buren(X,Y)) and not any(o10[y,x]==0 or o10[y,x] in LIJF for x,y in buren(X,Y)):
            ring.append((X,Y))
# b) inkepingen tussen de vingers (bovenste helft): randpixels van VL/VR die geen tentakel zijn (tussenlijn/schijf) en aan
#    de achterste anemoon grenzen worden achterste anemoon in schaduw (R1), en hun buur naar het mondje toe ook als dat
#    geen tentakel is (inkeping 2 px diep, zoals het model ±1-2 spritepx). Tentakels worden niet verlengd.
def naar_mond(i,X,Y):
    cx,cy=MOND[i][:2]; mx,my=4+(cx-36)*S,1+(cy-28)*S; dx,dy=mx-(X+.5),my-(Y+.5)
    return (X+int(np.sign(dx)) if abs(dx)>=abs(dy) else X, Y+int(np.sign(dy)) if abs(dy)>abs(dx) else Y)
gat=[]
for Y in range(2,31):
    for X in range(2,62):
        i=OWN[Y,X]
        if i not in (0,1) or KL[Y,X] or MOND3[Y,X] or not boven(i,X,Y): continue
        if any(is_achter(x,y) for x,y in buren(X,Y)):
            gat.append((X,Y)); x,y=naar_mond(i,X,Y)
            if OWN[y,x]==i and not KL[y,x] and not MOND3[y,x]: gat.append((x,y))
for X,Y in gat: zet('vingers',X,Y,R1)
GAT=np.zeros((64,64),bool)
for X,Y in gat: GAT[Y,X]=True
VOOR2=VOOR&~GAT
# c) ringpixels: onderste helft (schijf over L/R) donkerrode rand R0 zoals het model; bovenste helft R0 alleen direct
#    tegen een vingertop (de lijn volgt de vingers), anders schaduw R1 (de inkeping loopt door, geen gesloten boog).
for X,Y in ring:
    i=eigen_voor(X,Y)
    if not boven(i,X,Y): zet('ring',X,Y,R0)
    else: zet('ring',X,Y,R0 if any(VOOR2[y,x] and KL[y,x] for x,y in buren(X,Y)) else R1)
# een R0-ringpixel zonder lijnbuur (8 buren) is een los lijnstipje midden in een vlak (toets.py) -> schaduw R1
N8=N4+((1,1),(1,-1),(-1,1),(-1,-1))
for X,Y in ring:
    if o[Y,X]==R0 and not any(o[y,x] in (K,R0) for x,y in buren(X,Y,N8)): zet('ring',X,Y,R1)

# ---- 2. Mondjes VL en VR uit het model (dekking natief raster, gereedschap/anemonen.py MOND; rapport in NOTITIES) ----
# VL: rij 21 x22-25 donker 0,5-0,6 (zwart); rij 22 x22 0,5 en x26 0,8 donker, x23-25 licht 0,8-0,9; rij 23 x22-25 donker 0,3-0,4 (R0 in het model)
# VR: rij 19 x40-44 donker 0,4-0,7 (zwart); rij 20 x40 0,6 en x44 0,5 donker, x41-43 licht; rij 21 x41-43 donker 0,4-0,6 (R0)
# Binnen: R2 zoals het model. Rondom ligt in het model licht tentakelweefsel (R3, dekking licht >= 0,4): een lijnpixel
# (R0/zwart/R1) direct naast de ring wordt daar R3, zodat de ring niet in de tentakellijnen opgaat.
MONDNIEUW={0:{'K':[(22,21),(23,21),(24,21),(25,21),(22,22),(26,22)],'R0':[(22,23),(23,23),(24,23),(25,23)],'R2':[(23,22),(24,22),(25,22)]},
           1:{'K':[(40,19),(41,19),(42,19),(43,19),(44,19),(40,20),(44,20)],'R0':[(41,21),(42,21),(43,21)],'R2':[(41,20),(42,20),(43,20)]}}
a_,c_,L_=klassen()
def lichtdekking(X,Y):
    F=np.zeros(16)
    for u,v,w in overlap(X,Y): F[c_[v,u]]+=w
    return (F[4]+F[5])/F.sum()
oudmond={(X,Y) for Y,X in zip(*np.where(MOND3&VOOR))}
nieuwmond=set()
for i,m in MONDNIEUW.items():
    for kl,pts in m.items():
        for X,Y in pts: zet('mondjes',X,Y,{'K':K,'R0':R0,'R2':R2}[kl]); nieuwmond.add((X,Y))
for X,Y in oudmond-nieuwmond:          # oude ringpixels buiten de nieuwe ring: tint van het model rondom
    zet('mondjes',X,Y,R3 if lichtdekking(X,Y)>=0.4 else R2)
for X,Y in list(nieuwmond):
    for x,y in buren(X,Y,N4+((1,1),(1,-1),(-1,1),(-1,-1))):
        if (x,y) in nieuwmond or not VOOR2[y,x]: continue
        if o[y,x] in (K,R0,R1) and lichtdekking(x,y)>=0.4: zet('mondjes',x,y,R3)
# een R0-stipje dat zo los is komen te staan (tentakellijn die op de ring uitkwam) volgt het model eromheen
for X,Y in [(X,Y) for Y in range(15,27) for X in range(18,50) if VOOR2[Y,X] and o[Y,X]==R0]:
    if any(abs(X-a)<=2 and abs(Y-b)<=2 for a,b in nieuwmond) and (X,Y) not in nieuwmond \
       and not any(o[y,x] in (K,R0) for x,y in buren(X,Y,N4+((1,1),(1,-1),(-1,1),(-1,-1)))):
        zet('mondjes',X,Y,R3 if lichtdekking(X,Y)>=0.4 else R2)

# ---- 3. Linkerpoot (links op het scherm): knie uit het model ----
# Model natief (uitsnede 3x): heup u84-89 (v120-128), knie steekt naar voren (links) tot u80 bij v130-140, daaronder
# u82 (v140-155), scheen u84-90 (v155-165), kap v164-165. Omgerekend (X=4+(u-36)*0,43, Y=1+(v-28)*0,43) linkerkant per rij:
# r43-44 x24 | r45-48 x23 (knie) | r49-55 x24 | r56-59 x25. Rechterkant: r45-50 x25, r51-58 x26/27.
# r10 had x23 t/m r50 en x24 vanaf r51 tot de voet: één verspringing, geen knie. Opbouw per rij lijn (W0) - vulling - zwart.
POOT={45:(23,'aeeK'),46:(23,'aea'),47:(23,'ada'),48:(23,'ada'),
      49:(24,'adK'),50:(24,'adK'),51:(24,'adK'),52:(24,'adK'),53:(24,'adK'),54:(24,'acK'),55:(24,'acK'),
      56:(25,'acK'),57:(25,'acK'),58:(25,'acK'),59:(25,'KK')}
CH={'a':6,'c':8,'d':9,'e':10,'K':1}
for Y in range(45,61):
    for X in range(20,30): zet('linkerpoot',X,Y,0)
    if Y in POOT:
        x0,s=POOT[Y]
        for j,ch in enumerate(s): zet('linkerpoot',x0+j,Y,CH[ch])

# ---- 4. Ogen: zelfde 4 pixels als r10, andere kleur (opties op vel_ogen.png) ----
OOG=[(22,32),(23,32),(31,31),(32,31)]       # per oog: linkerpixel (r10 R2) + rechterpixel (r10 kraterbruin)
OPTIES={'A':(W0,W0),'B':(15,15),'C':(15,K)}   # A leisteen (lijnkleur lijf, = mond) | B kratergeel | C kratergeel + zwart
KEUZE=sys.argv[1] if len(sys.argv)>1 and sys.argv[1] in 'ABC' else 'B'
def ogen(a,keuze):
    a=a.copy(); l,r=OPTIES[keuze]
    for j,(X,Y) in enumerate(OOG): a[Y,X]=l if j%2==0 else r
    return a
basis=o.copy()
o=ogen(o,KEUZE)
for X,Y in OOG: gewijzigd.setdefault('ogen',set()).add((X,Y))

# ---- controle: buiten de zones identiek aan r10 ----
zone=np.zeros((64,64),bool)
for s in gewijzigd.values():
    for X,Y in s: zone[Y,X]=True
assert ((o!=o10)&~zone).sum()==0
# rechterpoot, lijf, armen, krater, gezicht (behalve ogen) ongewijzigd
diff=o!=o10
assert not diff[41:63,30:64].any(), 'rechterpoot'
toegestaan=set(OOG)|gewijzigd.get('linkerpoot',set())
assert all((X,Y) in toegestaan for Y,X in zip(*np.where(diff)) if Y>=31), 'lijf/armen/gezicht'
slecht=[(X,Y,o10[Y,X],o[Y,X]) for Y,X in zip(*np.where(diff)) if (X,Y) not in OOG and (o10[Y,X] in KR or (KRATERBOX(X,Y) and not VOOR[Y,X]))]
assert not slecht, slecht
opslaan(o,PAL,'r11/vileplume_r11.png')
for k in OPTIES: opslaan(ogen(basis,k),PAL,'r11/vileplume_r11_ogen%s.png'%k)
print('gewijzigd t.o.v. r10 per zone:')
for z,s in gewijzigd.items(): print('  %-11s %3d px'%(z,sum(1 for X,Y in s if o[Y,X]!=o10[Y,X])))
print('  totaal      %3d px'%(o!=o10).sum())
ch='.K0123abcdeGuomy'
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
if '--diag' in sys.argv:
    for Y in range(2,31):
        s=''
        for X in range(4,60):
            i=OWN[Y,X]
            if (X,Y) in set(ring): s+='#'
            elif GAT[Y,X]: s+='g'
            elif i in (0,1): s+= 'm' if MOND3[Y,X] else ('T' if KL[Y,X] else ('l' if o10[Y,X] in (1,2) else 'b'))
            else: s+=' ' if o10[Y,X]==0 else '.'
        print('%2d %s'%(Y,s))
