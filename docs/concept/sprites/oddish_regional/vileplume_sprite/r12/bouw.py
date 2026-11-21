# Vileplume r12 = r11 (ogen B) + Jordi's punten op r11 (20 nov). Draaien vanuit vileplume_sprite/: python3 r12/bouw.py [dx]
# 1. "het rondje in het midden van de anemoon moet alleen consistenter": alle 5 mondjes dezelfde vorm/maat/opbouw, op de modelplek.
# 2. "ogen van b zijn goed alleen moet je nog met kleurtinten werken, zoals bij de oorspronkelijke vileplume wss met tinten
#    rood gewerkt is": per oog licht/donker zoals de Vileplume uit de game, in de kratertinten.
# 3. "dus ik stel voor dat je die achterste in zijn geheel een beetje naar links schuift" (T, tegen het gaatje met L).
# 4. "wat betreft de voorste anemonen die in de achterste overlopen, kan je ook fixen met kleurtinten".
# Verder pixel voor pixel r11 (assert onderaan).
import sys, io, contextlib, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from gemeen import *; from anemonen import *; from klassen import klassen
DX=int(sys.argv[1]) if len(sys.argv)>1 else 3
im=Image.open('r11/vileplume_r11.png'); o11=np.asarray(im).astype(int); PAL=[tuple(c) for c in np.array(im.getpalette()[:48]).reshape(-1,3)]
assert [o11[Y,X] for X,Y in [(22,32),(23,32),(31,31),(32,31)]]==[15]*4, 'r11 moet met ogen B gebouwd zijn: python3 r11/bouw.py B'
o=o11.copy()
K,R0,R1,R2,R3=1,2,3,4,5; GEEL,ORANJE,ROODOR=15,14,13
LIJF={6,7,8,9,10}; KR={7,11,12,13,14,15}
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=N4+((1,1),(1,-1),(-1,1),(-1,-1))
def buren(X,Y,n=N4): return [(X+dx,Y+dy) for dy,dx in n if 0<=X+dx<64 and 0<=Y+dy<64]
def stil(path,repl):
    src=open(path).read()
    for l in repl: assert l in src, l; src=src.replace(l,'pass')
    ns={'__name__':'x'}; argv=sys.argv; sys.argv=[path,path.split('/')[0]]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,path,'exec'),ns)
    sys.argv=argv; return ns
# eigenaars: achterste anemonen uit r7 (de achterkroon van r10/r11 is r7), voorste uit r3 en de r11-inkepingen
n7=stil('r7/bouw.py',["opslaan(o,PAL,RONDE+'/vileplume_%s.png'%RONDE)","for v in 'AC': opslaan(VAR[v],PAL,RONDE+'/vileplume_%s_gelaat%s.png'%(RONDE,v))","opslaan(kaal_o,PAL,RONDE+'/kaal.png')"])
n3=stil('r3/bouw.py',["opslaan(o,PAL,RONDE+'/vileplume_'+RONDE+'.png')"])
OWN7,MOND7=n7['OWN'],n7['MOND']; OWN3,MOND3=n3['OWN'],n3['MOND']
o10=np.asarray(Image.open('r10/r10_voor_r3.png')).astype(int)
VOOR=np.isin(OWN3,[0,1])&~((o11!=o10)&(o11==R1)&np.isin(OWN3,[0,1]))   # r11-inkepingen (R1) horen bij de achterste anemoon
ACHTER=np.isin(OWN7,[2,3,4])&~VOOR
gewijzigd={}
def zet(zone,X,Y,k):
    if o[Y,X]!=k: o[Y,X]=k
    gewijzigd.setdefault(zone,set()).add((X,Y))
a_,c_,L_=klassen()
def lichtdekking(X,Y):
    F=np.zeros(16)
    for u,v,w in overlap(X,Y): F[c_[v,u]]+=w
    return (F[4]+F[5])/max(F.sum(),1e-9)

# ---- 1. Mondjes: één vorm voor alle vijf ----
# Model (natief, gereedschap/anemonen.py MOND): ringen 12-14 natieve px breed (5,2-6,0 spritepx), 5-7 hoog (2,2-3,0);
# boven en opzij zwart, onder donkerrood, binnen R2, eromheen licht tentakelweefsel. Eén sjabloon van 6x3, hoeken open
# (het ovaal van het model op 64x64), midden op het gemeten modelmidden: x0=round(cx-2,5), y0=round(cy-1,5) met
# cx=4+(u-36)*0,43, cy=1+(v-28)*0,43.
SJABLOON=[' KKKK ','K2222K',' 0000 ']
CK={'K':K,'2':R2,'0':R0}
MONDPLEK={}
for i in range(5):
    cx,cy=4+(MOND[i][0]-36)*S, 1+(MOND[i][1]-28)*S
    MONDPLEK[i]=(int(round(cx-2.5)),int(round(cy-1.5)))
nieuwmond={}
for i,(x0,y0) in MONDPLEK.items():
    for r,rij in enumerate(SJABLOON):
        for k,ch in enumerate(rij):
            if ch!=' ': nieuwmond[(x0+k,y0+r)]=(i,CK[ch])
oudmond={(X,Y) for Y,X in zip(*np.where((MOND7&~VOOR)|(MOND3&VOOR)))}
oudmond|={(X,Y) for X,Y in [(22,21),(23,21),(24,21),(25,21),(22,22),(26,22),(22,23),(23,23),(24,23),(25,23),(23,22),(24,22),(25,22),
                             (40,19),(41,19),(42,19),(43,19),(44,19),(40,20),(44,20),(41,21),(42,21),(43,21),(41,20),(42,20),(43,20)]}  # r11 VL/VR
for X,Y in oudmond-set(nieuwmond): zet('mondjes',X,Y,R3 if lichtdekking(X,Y)>=0.4 else R2)
for (X,Y),(i,k) in nieuwmond.items(): zet('mondjes',X,Y,k)
for (X,Y),(i,k) in nieuwmond.items():      # lichte rand: lijnpixel naast de ring waar het model licht is -> R3
    for x,y in buren(X,Y,N8):
        if (x,y) in nieuwmond or o[y,x] not in (K,R0,R1) or not (VOOR[y,x] or ACHTER[y,x]): continue
        if lichtdekking(x,y)>=0.4: zet('mondjes',x,y,R3)
# losse lijnstipjes die zo naast de ring zijn komen te staan -> modeltint
for (X,Y) in list(gewijzigd['mondjes']):
    for x,y in buren(X,Y,N8):
        if (x,y) in nieuwmond or o[y,x]!=R0 or not (VOOR[y,x] or ACHTER[y,x]): continue
        if not any(o[yy,xx] in (K,R0) for xx,yy in buren(x,y,N8)): zet('mondjes',x,y,R3 if lichtdekking(x,y)>=0.4 else R2)

# ---- 2. Ogen: Vileplume uit de game (graphics/pokemon/vileplume/anim_front.png): elk oog = lichte tint links
# (216,72,88) + donkere tint rechts (112,24,16), linkeroog (24,37)+(25,37), rechteroog (32,38)+(33,38).
# Hier: geel blijft de lichte tint, roodoranje van de krater de donkere. Vorm en plek als r11.
OOG={(22,32):GEEL,(23,32):ROODOR,(31,31):GEEL,(32,31):ROODOR}
for (X,Y),k in OOG.items(): zet('ogen',X,Y,k)

# ---- 3. T als geheel DX px naar links (tentakels, mondje, omlijning), over L heen; krater blijft staan ----
TM=(OWN7==4)&(o>0)
TM[:, :]&=(np.arange(64)[:,None]<=10)
KRATER=np.zeros((64,64),bool)
for Y in range(9,18):
    for X in range(23,40):
        if o11[Y,X] in KR or o11[Y,X]==K and not ACHTER[Y,X]: KRATER[Y,X]=True
KRATER|=np.isin(o11,list(KR))
oud=o.copy(); tpix=[(X,Y,oud[Y,X]) for Y,X in zip(*np.where(TM))]
vrij=set()
for X,Y,k in tpix:
    if not KRATER[Y,X]: vrij.add((X,Y))
nieuwT=set()
for X,Y,k in tpix:
    if KRATER[Y,X]: continue
    x=X-DX
    if KRATER[Y,x]: continue
    nieuwT.add((x,Y))
vrij-=nieuwT
for X,Y in vrij: zet('T',X,Y,0)
for X,Y,k in tpix:
    if KRATER[Y,X] or KRATER[Y,X-DX]: continue
    zet('T',X-DX,Y,k)
# wat rechts vrijkomt: binnen het silhouet (pixel onder een kroonpixel en tussen kroonpixels op de rij) -> R-schaduw R1;
# erbuiten transparant. Daarna buitenlijn: blootgekomen rand van R/T tegen de achtergrond zwart rechts/onder, R0 links/boven.
for ronde in range(3):
    for X,Y in sorted(vrij):
        if o[Y,X]!=0: continue
        links=any(o[Y,x]>0 for x in range(max(0,X-2),X)); rechts=any(o[Y,x]>0 for x in range(X+1,min(64,X+3)))
        if links and rechts and Y>=4: zet('T',X,Y,R1)     # spleet tussen T en R: R loopt door (schaduw)
VRIJR={(X,Y) for X,Y in vrij if o[Y,X]>0}
for Y in range(0,12):
    for X in range(14,60):
        k=o[Y,X]
        if k in (0,K) or k in KR: continue
        nb=lambda dx,dy: o[Y+dy,X+dx]==0 if 0<=Y+dy<64 else True
        if not (nb(1,0) or nb(-1,0) or nb(0,1) or nb(0,-1)): continue
        if (X,Y) not in VRIJR and not any((x,y) in vrij for x,y in buren(X,Y,N8)): continue
        zet('T',X,Y,K if (nb(1,0) or (nb(0,1) and not nb(-1,0))) else R0)

# ---- 4. Overlap voor/achter met kleurtinten (geen zwarte ring) ----
# Achterste anemoon langs de naad in schaduw (R2/R3 -> R1, R1 -> R0), voorste randpixel lichter (R0/R1 -> R2, R2 -> R3).
# Mondjes en krater blijven buiten schot.
naad_a=set(); naad_v=set()
for Y in range(2,31):
    for X in range(2,62):
        if (X,Y) in nieuwmond or o[Y,X]==0: continue
        if ACHTER[Y,X] and any(VOOR[y,x] and (x,y) not in nieuwmond for x,y in buren(X,Y)): naad_a.add((X,Y))
        if VOOR[Y,X] and any(ACHTER[y,x] and o[y,x]>0 for x,y in buren(X,Y)): naad_v.add((X,Y))
pre=o.copy()
for X,Y in naad_a:
    k=pre[Y,X]
    if k in (R2,R3): zet('naad',X,Y,R1)
    elif k==R1: zet('naad',X,Y,R0)
for X,Y in naad_v:
    k=pre[Y,X]
    if k in (R0,R1): zet('naad',X,Y,R2)
    elif k==R2: zet('naad',X,Y,R3)

# ---- controle ----
zone=np.zeros((64,64),bool)
for s in gewijzigd.values():
    for X,Y in s: zone[Y,X]=True
diff=o!=o11
assert not (diff&~zone).any()
assert not diff[33:,:].any(), 'lijf/poten'
assert all((X,Y+31) in OOG for Y,X in zip(*np.where(diff[31:33,:]))), "lijf rij 31-32"
slecht=[(X,Y) for Y,X in zip(*np.where(diff)) if KRATER[Y,X] and (X,Y) not in OOG]
assert not slecht, ('krater',slecht)
assert len(set(o.ravel()))<=16
opslaan(o,PAL,'r12/vileplume_r12.png')
print('DX',DX,'mondjes',MONDPLEK)
print('gewijzigd t.o.v. r11 per zone (px echt anders):')
for z,s in gewijzigd.items(): print('  %-8s %3d'%(z,sum(1 for X,Y in s if o[Y,X]!=o11[Y,X])))
print('  totaal   %3d'%diff.sum())
ch='.K0123abcdeGuomy'
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
