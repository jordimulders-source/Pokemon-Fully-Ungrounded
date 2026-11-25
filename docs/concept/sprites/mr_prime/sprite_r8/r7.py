# r7 (op de r6-uitvoer r6_uit.png): stok, linkeroog, linkerhaar/aansluiting (Mr. Rime 1-op-1), ronde kop,
# omlijning + schaduw volgens Dragonfly Cave. Niets nieuw getekend: pixels uit Mr. Rime / Mr. Mime / de sprite zelf,
# verschoven of omgekleurd. PNG-indexen: 0 transparant, 1=16 (lijn/zwart) 2=40 3=66 4=100 5=128 6=164 7=200 8=248,
# 9=224 (wit midden, nieuw in het palet).
import numpy as np; from PIL import Image
G='../../../../../graphics/pokemon/%s.png'
PAL=[(152,208,160),(16,16,24),(40,40,54),(66,70,92),(100,106,132),(128,124,146),(164,162,178),(200,200,212),(248,248,248),
     (224,224,234)]
RIME=np.asarray(Image.open(G%'mr_rime/front')).astype(int)
C=np.asarray(Image.open('r6_uit.png')).astype(int).copy(); R6=C.copy()
LOG={}
def zet(zone,y,x,v):
    if C[y,x]!=v: C[y,x]=v; LOG[zone]=LOG.get(zone,0)+1
def P(zone,y,x0,s):
    """rij y vanaf x0: tekens 0-9a-f of '.'=transparant, '-'=laten"""
    for i,ch in enumerate(s):
        if ch=='-': continue
        zet(zone,y,x0+i,0 if ch=='.' else int(ch,16))

# ---- 3. LINKERHAAR: Mr. Rime-linkervleugel + aansluiting op rand/zijhaar 1-op-1, in de Rime-stand t.o.v. de hoed
# (de hoed is Rime x19-44 r6-15 op (+7,-3), hoed.py). Zelfde verschuiving voor vleugel, zijhaar en gezichtsrand,
# zodat vleugel, rand en zijhaar liggen zoals bij Rime. Omkleuring = die van de hoed (hoed.py + palet.py):
# Rime 3,1 -> 1 (16), 4 -> 2 (40), 2 -> 3 (66); Rime-gezichtsrand c -> 5 (gezichtsselout).
DX,DY=7,-3
MAPR={3:1,1:1,4:2,2:3}
K=set((y+DY,x+DX) for y in range(6,16) for x in range(19,45) if RIME[y,x] in MAPR)
W={}
for y in range(9,22):
    for x in range(5,24):
        if y>=16 and x>=24: continue
        v=RIME[y,x]
        if v in MAPR and (x<=18 or y>=16): W[(y+DY,x+DX)]=MAPR[v]
for x in range(24,27): W[(16+DY,x+DX)]=MAPR[RIME[16,x]]   # Rime r16 x24-26: zwarte rand haar/gezicht
for y in range(5,18):           # oude (verschoven) r6-vleugel en het losse zijhaarstompje weg
    for x in range(12,28):
        if (y,x) not in K and (y,x) not in W and 1<=C[y,x]<=5 and not (y>=15 and x<=12):
            zet('linkerhaar: oude r6-vleugel/stompje weg',y,x,0)
for (y,x),v in W.items():
    if (y,x) not in K: zet('linkerhaar: Rime-vleugel + aansluiting 1-op-1',y,x,v)

# ---- 6. RONDE KOP. Links: de Rime-gezichtsrand onder het zijhaar (Rime r16-22: x24-26, 22-23, 21, 21, 21, 21, 22) in
# dezelfde stand als het haar; de 2 extra voorhoofdrijen van r2 rekken de verticale rij x21 met 2 rijen op.
# Rechts: de bovenboog van de Gen 3 Mr. Mime-kop (anim_front_gba r15-18: linkerrand x25, 24, 23, 22 = inspringing
# 3, 2, 1, 0) gespiegeld: lijn r13 x45, r14 x46, r15 x47, r16+ x48 (waar hij al stond). Wit doortrekken/wegknippen.
Z='kop rond'
P(Z,15,28,'1888')           # onder het zijhaar: lijn (overlap) + gezichtswit tot het verre oog
for y in (16,17,18,19): P(Z,y,26,'..58')
P(Z,20,27,'158')            # rij 20: snorkrul raakt het gezicht (overlap -> zwart)
P(Z,13,45,'1..'); P(Z,14,46,'1.'); P(Z,15,47,'1.')
P(Z,12,46,'11')             # hoedrand rechts: onderkant ligt nu vrij -> lijn
# ---- 2. LINKEROOG: zelfde ring als het nabije oog (bovenhoeken 7) en onderhoeken ook 7 -> gesloten ring, bij beide
P('linkeroog',16,30,'767'); P('linkeroog',20,30,'767'); P('nabije oog (onderhoeken als bovenhoeken)',19,38,'767')

# ---- 1. STOK. Zelfde stok (r6-maat, haak, schacht, hand), pixels verschoven tot regelmatige lijnen:
# schacht: linkerlijn x per rij 7,7,8,9,10,10,11,12,13,13,... (trap 2-1-1 over de hele lengte, rij 21-39), overal 4 breed:
# lichte-kantlijn 2 (outline base, links) | hooglicht 4 | basis 3 | zwart 1 (schaduwkant rechts); over de hand beide lijnen
# zwart (overlap). Haak: buitenboog 3-1-1 bovenop, dan verticaal links; hooglicht (6/5) linksboven, doorlopend in de
# hooglichtlijn van de schacht; binnenkant boog (onder) donker 2. Hand: dezelfde witte vlakken naast de schacht.
OUD=[(y,x) for y in range(15,42) for x in range(0,24) if C[y,x]>0 and (x<=18 and y<=33 or (y>=33 and x<=23 and not (y>=35 and x>=24)))
     and not (y<=17 and x>=19) and not (28<=y<=33 and x>=19)]
STOKRIJEN={
15:(0,'...222'),
16:(0,'..25662'),
17:(0,'.2566542'),
18:(0,'25644531'),
19:(0,'254322531'),
20:(0,'2433211431'),
21:(0,'24321..2431'),
22:(0,'23321..2431'),
23:(0,'.13221..2431'),
24:(0,'..111....2431'),
25:(10,'2431'),
26:(10,'2431.44'),
27:(10,'414318844'),          # hand: linksboven-hoek, schacht (lijnen zwart: overlap), vingers rechts
28:(10,'4814318481'),
29:(10,'488143178111'),
30:(10,'4881431711'),
31:(10,'1888143171'),
32:(11,'17771431111'),
33:(12,'11111431'),
34:(16,'2431'),
35:(17,'2431'),
36:(18,'2431'),
37:(19,'2431'),
38:(19,'2431'),
39:(20,'1431'),
40:(21,'11'),
}
NIEUW=set()
for y,(x0,s) in STOKRIJEN.items():
    for i,ch in enumerate(s):
        if ch not in '.-': NIEUW.add((y,x0+i))
for (y,x) in OUD:
    if (y,x) not in NIEUW: zet('stok: oude pixels weg (verschoven)',y,x,0)
for y,(x0,s) in STOKRIJEN.items(): P('stok + hand',y,x0,s)

# ---- 4. KLEUR, SCHADUW, LIJNEN (Dragonfly Cave)
import licht
# 4a. volume per vorm: lichtbron linksboven-voor, per onderdeel (licht.py); tinten 2 (40) .. 5 (128), Alphyena-stappen.
ARM_L={29:46,30:47,31:47,32:48,33:49,34:52,35:53,36:52,37:53,38:53}
DELEN=[
 ('hoedkruin',lambda y,x: 3<=y<=7 and 30<=x<=46),
 ('hoedrand',lambda y,x: 9<=y<=12 and 26<=x<=48),
 ('rechtervleugel',lambda y,x: (y<=11 and x>=49) or (y<=8 and x>=47)),
 ('linkervleugel',lambda y,x: 5<=y<=17 and 12<=x<=30 and not (y==12 and x>=26) and not (y>=15 and x>=28)),
 ('linkermouw',lambda y,x: 28<=y<=33 and 19<=x<=27),
 ('linkerpand',lambda y,x: 29<=y<=44 and 23<=x<=32),
 ('rechterpand',lambda y,x: 28<=y<=45 and 33<=x<=53 and not (y in ARM_L and x>=ARM_L[y])),
 ('rechterarm',lambda y,x: y in ARM_L and x>=ARM_L[y] and x<=58),
 ('voorbeen',lambda y,x: 45<=y<=57 and 21<=x<=34),
 ('achterbeen',lambda y,x: 46<=y<=56 and 35<=x<=54),
]
AANDEEL=(0.24,0.42,0.25,0.09)
DONKER=np.isin(C,[2,3,4,5])
for naam,f in DELEN:
    M=np.zeros(C.shape,bool)
    for y,x in zip(*np.where(DONKER)):
        if f(y,x): M[y,x]=True
    licht.schaduw(C,M,AANDEEL,(2,3,4,5),'schaduw '+naam,zet,macht=1.0,L=(-0.55,-0.6,1.0),glad=2)
# 4b. omlijning (DC: "take the base outlining shade for every color and color all of the outline except the shadows in
# that color"; "outline shadows are always black"): buitenrand aan de schaduwkant (rand wijst naar rechts/onder) zwart 1,
# aan de lichtkant (links/boven) de outline base van het onderdeel: donker 2 (40), wit 4 (100, zoals Mr. Mime 90-115). Stok is al zo gezet.
WIT=(6,7,8,9)
def stok_of_oog(y,x): return (x<=23 and 15<=y<=41 and not (y<=17 and x>=19)) or (14<=y<=21 and 29<=x<=43)
B0=C.copy()
for y in range(64):
    for x in range(64):
        v=B0[y,x]
        if v==0 or stok_of_oog(y,x): continue
        nx=ny=0; open4=False
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if (dy or dx) and (not(0<=yy<64 and 0<=xx<64) or B0[yy,xx]==0):
                    nx+=dx; ny+=dy
                    if dy==0 or dx==0: open4=True
        if not open4: continue
        binnen=[B0[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))
                if 0<=y+dy<64 and 0<=x+dx<64 and B0[y+dy,x+dx] not in (0,1)]
        basis=4 if (v in WIT or (v in (1,5) and any(b in WIT for b in binnen))) else 2
        zw=nx+ny>0 or (nx+ny==0 and nx>0)
        zet('omlijning: '+('zwart (schaduwkant)' if zw else 'outline base lichtkant'),y,x,1 if zw else basis)

# 4c. wit (gezicht, V, buikband): zelfde belichting, hoogteveld van de hele vorm (gaten van ogen/snor dicht), alleen de
# witte pixels omgekleurd: 8 (248) licht, 9 (224) midden, 7 (200) schaduw, 6 (164) diepste schaduw rechtsonder.
def wit_deel(naam,f,aandeel,toon=(6,7,9,8),gat=lambda y,x: False):
    vorm=np.zeros(C.shape,bool); kleur=np.zeros(C.shape,bool)
    for y in range(64):
        for x in range(64):
            if (f(y,x) or gat(y,x)) and C[y,x]!=0:
                vorm[y,x]=True
                if C[y,x] in (7,8,9) and not gat(y,x): kleur[y,x]=True
    licht.schaduw(C,kleur,aandeel,toon,'schaduw '+naam,zet,vorm=vorm,macht=1.0,L=(-0.55,-0.6,1.0),glad=2)
OOG=lambda y,x: (14<=y<=20 and 36<=x<=42) or (16<=y<=20 and 30<=x<=32) or (18<=y<=21 and 33<=x<=35)
wit_deel('V',lambda y,x: 29<=y<=45 and 30<=x<=38,(0.0,0.10,0.18,0.72))
wit_deel('buikband',lambda y,x: 46<=y<=48 and 30<=x<=47,(0.0,0.12,0.25,0.63))

# 4d. opschonen: losse pixels (geen enkele 4-buur met dezelfde tint) binnen een donker onderdeel -> meest voorkomende buurtint
for naam,f in DELEN:
    D=C.copy()
    for y in range(1,63):
        for x in range(1,63):
            v=D[y,x]
            if not f(y,x) or v not in (2,3,4,5): continue
            nb=[D[y-1,x],D[y+1,x],D[y,x-1],D[y,x+1]]
            if 0 in nb or v in nb: continue
            nn=[t for t in nb if t in (2,3,4,5)]
            if nn: zet('opschonen: losse pixel -> buurtint',y,x,max(set(nn),key=nn.count))
P('kop rond',20,27,'48')    # rij 20: snorkrul/gezicht: 1 omlijningspixel (geen dubbele selout)
# 4e. gezicht: wit 8 met een schaduwsikkel rechts (9 = 224, 7 = 200), naar onder breder (bol), links geen grijs
GZ='schaduw gezicht (sikkel rechts)'
for y in range(13,21):
    for x in range(29,48):
        if C[y,x] in (7,9) and not OOG(y,x): zet(GZ,y,x,8)
for y,x0,s_ in ((15,46,'9'),(16,47,'9'),(17,46,'97'),(18,46,'97'),(19,45,'977'),(20,45,'977'),(21,45,'977'),(22,44,'977')):
    P(GZ,y,x0,s_)
# 4f. geen om-en-om op een rand: een omlijningspixel (buitenrand) waarvan geen enkele rand-buur (8-buren op de rand)
# dezelfde lijnkleur heeft, krijgt de lijnkleur van zijn randburen (zwart of outline base).
def rand(y,x):
    if C[y,x]==0: return False
    return any(not(0<=y+dy<64 and 0<=x+dx<64) or C[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
for _ in range(2):
    D=C.copy()
    for y in range(64):
        for x in range(64):
            if not rand(y,x) or D[y,x] not in (1,2,4) or stok_of_oog(y,x): continue
            bur=[D[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64 and rand(y+dy,x+dx)]
            lijn=[b for b in bur if b in (1,2,4)]
            if len(lijn)>=2 and D[y,x] not in lijn:
                zet('omlijning: om-en-om weg',y,x,max(set(lijn),key=lijn.count))
# 4g. tintvlakjes < 3 px binnen een donker onderdeel (niet op de buitenrand, geen glans 5) -> omringende tint
from collections import deque
def in_deel(y,x): return any(f(y,x) for _,f in DELEN)
for _ in range(2):
    D=C.copy(); seen=np.zeros(C.shape,bool)
    for y in range(64):
        for x in range(64):
            v=D[y,x]
            if v not in (2,3,4) or seen[y,x]: continue
            q=deque([(y,x)]); seen[y,x]=1; comp=[(y,x)]
            while q:
                a,b=q.popleft()
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=a+dy,b+dx
                    if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and D[yy,xx]==v: seen[yy,xx]=1; q.append((yy,xx)); comp.append((yy,xx))
            if len(comp)>=3 or not all(in_deel(*p) and not rand(*p) and not stok_of_oog(*p) for p in comp): continue
            nb=[D[a+dy,b+dx] for a,b in comp for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if (a+dy,b+dx) not in comp and D[a+dy,b+dx] in (2,3,4,5)]
            if nb:
                t=max(set(nb),key=nb.count)
                for a,b in comp: zet('opschonen: tintvlakje < 3 px -> omringende tint',a,b,t)
