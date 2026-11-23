# maak.py (Grass): gedeelde reductie (zone.npy, lijnkans.npy uit reductie.py) -> technisch opgeschoond -> red.png
# NIET TEKENEN: silhouet, onderdelen, vlakken (bladeren, houtplaten, schijven) en lijnen komen uit het model:
#   - silhouet = kale reductie (+ dunne delen op drempel 0,35, zie reductie.py)
#   - lijnen = buitenlijn 1 px + onderdeelgrens (op het voorste onderdeel) + modellijnen waar de zwarte modellijn >= T van de
#     spritepixel dekt en dwars op de lijn een lokaal maximum is (gemeten plekken; houtnerf zonder zwarte lijn telt niet: geen zebra)
#   - vlakken = samenhangende stukken tussen die lijnen
# Kleur mag afwijken (Gen 3-volume, Jordi): per onderdeel 2 tinten (licht linksboven, schaduw als sikkel rechts/onder,
# per stuk de onder/rechterrand een tint donkerder), roze hooglicht 15 alleen op de ronde delen.
import numpy as np; from scipy import ndimage as nd
from gemeen import *
zone=np.load('zone.npy'); kl=np.load('lijnkans.npy')
fg=zone>0; rank={p:i for i,p in enumerate(PRIO)}
# onderdeelkaart opschonen: eilandjes van <= 3 px van een onderdeel (randruis van de meerderheidsstem, bv. mutsrand tussen
# neus en haar R) gaan naar het onderdeel dat er het meest omheen ligt (twijgblaadjes en knoesten uitgezonderd: die zijn echt klein)
OPGESCHOOND=[]
for z in list(ZNAAM):
    if z in (16,17): continue
    lab,n=nd.label(zone==z)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()>3: continue
        r=nd.binary_dilation(m)&~m&fg; t=zone[r]
        if len(t):
            nz=np.bincount(t).argmax(); zone[m]=nz; OPGESCHOOND+=[(int(X),int(Y),ZNAAM[z],ZNAAM[nz]) for Y,X in zip(*np.where(m))]
print('onderdeelkaart opgeschoond',len(OPGESCHOOND),OPGESCHOOND)
N4=((1,0),(-1,0),(0,1),(0,-1))
def binnen(Y,X): return 0<=Y<64 and 0<=X<64
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not binnen(Y+dy,X+dx) or not fg[Y+dy,X+dx] for dy,dx in N4): OUT[Y,X]=True
BIN=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg&~OUT)):
    if any(zone[Y+dy,X+dx]!=zone[Y,X] and rank[zone[Y+dy,X+dx]]>rank[zone[Y,X]] and fg[Y+dy,X+dx] for dy,dx in N4): BIN[Y,X]=True
# modellijnen: skelet van de modellijnen (skel.py), >= 3 skeletpunten in de spritepixel -> lijn van 1 px op de gemeten plek
SK=np.load('skel.npy')
NAAD=fg&~OUT&(SK>=3)
# onderdeelgrens zonder modellijn ernaast: lijn op het voorste onderdeel; ligt er binnen 1 px al een modellijn, dan niet (geen dubbele lijn)
for Y,X in zip(*np.where(BIN)):
    if any(binnen(Y+dy,X+dx) and NAAD[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1)): BIN[Y,X]=False
LIN=BIN|NAAD
# losse lijnstipjes (< 3 px, raken geen buitenlijn): weg
lab,n=nd.label(LIN,structure=np.ones((3,3))); weg=0
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3 and not (nd.binary_dilation(m,structure=np.ones((3,3)))&OUT).any(): LIN[m]=False; weg+=m.sum()
# dubbele lijnen: een binnenlijnpixel waarvan de onder- of rechterbuur ook lijn is en die zelf een vlakbuur aan de overkant mist -> vlak
LIN=BIN|NAAD
print('binnenlijn',LIN.sum(),'(grens',BIN.sum(),', modellijn',NAAD.sum(),'), stipjes weg',weg)
# vlakken en volume
o=np.zeros((64,64),int)
TWEE={}   # zone -> (licht, schaduw)
for z,r in RAMP.items():
    TWEE[z]=(8,7) if r==ROZE else (r[1],r[0])
# bollen voor het volume: elk onderdeel een bol, de broek als twee benen (split bij het kruis, kolom 34, zoals Rock r2)
BOL=zone.copy(); BOL[(zone==12)&(np.arange(64)[None,:]>=34)]=99
cz={z:np.array(np.where(BOL==z)).mean(1) for z in set(BOL[fg].ravel())}
sz={z:np.array(np.where(BOL==z)).std(1).mean()+1 for z in cz}
stuk=np.zeros((64,64),int); ns=0
for z in cz:
    l,k=nd.label((zone==z)&fg&~LIN&~OUT); stuk[l>0]=l[l>0]+ns; ns+=k
vlak=np.load('vlak.npy'); GEM=np.load('gem.npy')    # meerderheidsstem van de modeltonen per spritepixel (reductie.py), al op de 2 tinten van het onderdeel
psz=np.bincount(stuk.ravel())
for Y,X in zip(*np.where(fg)):
    z=zone[Y,X]; li,sch=TWEE[z]
    if RAMP[z] in (ROZE,BLAUW):   # roze en blauw hout: Gen 3-volume (model is daar vlak)
        b=BOL[Y,X]; g=((cz[b][1]-X)*0.6+(cz[b][0]-Y)*0.8)/sz[b]          # licht van linksboven over de hele bol
        o[Y,X]=li if g>-0.45 else sch
        if z==6 and binnen(Y-1,X) and zone[Y-1,X] in (1,2,3,4,5): o[Y,X]=sch   # slagschaduw onder muts, haar, baard en neus
    else:                         # blad en schors: toon uit het model (lichte/donkere bladhelften, schors)
        o[Y,X]=vlak[Y,X] if vlak[Y,X] in (li,sch) else (li if lum(PAL[vlak[Y,X]])>lum(PAL[sch]) else sch)
# bladeren (baard, haar, twijgblaadjes): elk blad in zijn geheel licht of schaduw, naar de meerderheid van het model in dat blad
# (grote duidelijke bladvormen, geen groene ruis); een blad >= 12 px krijgt de schaduw als sikkel langs zijn onder-/rechterrand
for s_ in range(1,ns+1):
    m=stuk==s_
    if not m.any(): continue
    z=zone[m][0]
    if RAMP[z]!=BLAD_L: continue
    li,sch=TWEE[z]; licht=np.mean([lum(c) for c in GEM[m]])>=145   # gemiddelde modeltoon van het blad (lichtgroen ~150-190, schaduwkant ~130-150)
    o[m]=li if licht else sch
    if licht and m.sum()>=12:
        for Y,X in zip(*np.where(m)):
            if all(binnen(Y+dy,X+dx) and not m[Y+dy,X+dx] for dy,dx in ((1,0),(0,1))): o[Y,X]=sch
# ruis: 3x3-meerderheid binnen hetzelfde stuk (lijnen blijven), 2 rondes
for _ in range(2):
    o2=o.copy()
    for Y,X in zip(*np.where(fg&~LIN&~OUT)):
        t=[o[y,x] for y in range(Y-1,Y+2) for x in range(X-1,X+2) if stuk[y,x]==stuk[Y,X]]
        c=np.bincount(t,minlength=16)
        if c[o[Y,X]]<=1 and c.max()>=3: o2[Y,X]=c.argmax()
    o=o2
# tintvlekjes < 3 px binnen een stuk -> meest voorkomende buurtint van hetzelfde stuk (ruis); kleine stukken zelf (twijgblaadjes, knoesten) blijven
for _ in range(2):
    for k in (3,4,7,8,10,11,12,13,14):
        lab,n=nd.label((o==k)&fg&~LIN&~OUT,structure=np.ones((3,3)))
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            ys,xs=np.where(m); st=stuk[ys[0],xs[0]]
            if psz[st]<=4 or zone[ys[0],xs[0]] in (16,17): continue
            r=nd.binary_dilation(m,structure=np.ones((3,3)))&~m&(stuk==st); t=o[r]; t=t[t!=k]
            if len(t): o[m]=np.bincount(t).argmax()
# ronde delen (neus, hand R, vuist L, elleboog- en schouderschijf R): rand rondom outline base 6, zwart als boog linksmidden-linksonder-ondermidden (Gnomini r10);
# hooglicht 15: 2 px linksboven in het stuk
for zz in (5,9,19):
    m=zone==zz; yy,xx=np.where(m); cy,cx=yy.mean(),xx.mean(); rad=np.sqrt(m.sum()/np.pi)
    hy,hx=int(round(cy-0.45*rad)),int(round(cx-0.4*rad))
    for Y,X in ((hy,hx),(hy,hx+1)):
        if m[Y,X] and not OUT[Y,X] and not LIN[Y,X]: o[Y,X]=15
# lijnen kleuren: binnen = outline base van het eigen onderdeel; buiten = DC (outline base aan de lichtkant, zwart aan de schaduwkant)
for Y,X in zip(*np.where(LIN)): o[Y,X]=BASIS[zone[Y,X]]
LICHT=np.array([-0.6,-0.8])
def normaal(Y,X):
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and (not binnen(Y+dy,X+dx) or not fg[Y+dy,X+dx]): v+=(dx,dy)
    n=np.linalg.norm(v); return v/n if n else v
for Y,X in zip(*np.where(OUT)): o[Y,X]=BASIS[zone[Y,X]] if normaal(Y,X)@LICHT>0.35 else 1
for zz in (5,9,19,8,18):
    m=zone==zz; yy,xx=np.where(m); cy,cx=yy.mean(),xx.mean()
    rand=m&nd.binary_dilation(~m,structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    for Y,X in zip(*np.where(rand)):
        h=np.degrees(np.arctan2(Y-cy,X-cx)); o[Y,X]=1 if 80<=h<=190 else 6
np.save('zone_af.npy',zone); np.save('lin.npy',LIN)
opslaan(o,'red.png')
