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
N4=((1,0),(-1,0),(0,1),(0,-1))
def binnen(Y,X): return 0<=Y<64 and 0<=X<64
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not binnen(Y+dy,X+dx) or not fg[Y+dy,X+dx] for dy,dx in N4): OUT[Y,X]=True
BIN=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg&~OUT)):
    if any(zone[Y+dy,X+dx]!=zone[Y,X] and rank[zone[Y+dy,X+dx]]>rank[zone[Y,X]] and fg[Y+dy,X+dx] for dy,dx in N4): BIN[Y,X]=True
# modellijnen (drempel per onderdeel; dikke modellijnen tussen bladeren/platen dekken ~0,2-0,4 van een spritepixel)
T={z:0.22 for z in ZNAAM}; T.update({12:0.30,10:0.30})
K=np.pad(kl,1,constant_values=9)
def nms(Y,X):
    c=kl[Y,X]; y,x=Y+1,X+1
    return any(c>=K[y-dy,x-dx] and c>=K[y+dy,x+dx] for dy,dx in ((0,1),(1,0),(1,1),(1,-1)))
NAAD=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg&~OUT&~BIN)):
    if kl[Y,X]>=T[zone[Y,X]] and nms(Y,X): NAAD[Y,X]=True
LIN=BIN|NAAD
# losse lijnstipjes (< 3 px, raken geen buitenlijn): weg
lab,n=nd.label(LIN,structure=np.ones((3,3))); weg=0
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3 and not (nd.binary_dilation(m,structure=np.ones((3,3)))&OUT).any(): LIN[m]=False; weg+=m.sum()
# dubbele lijnen: een binnenlijnpixel waarvan de onder- of rechterbuur ook lijn is en die zelf een vlakbuur aan de overkant mist -> vlak
print('binnenlijn',LIN.sum(),'(grens',BIN.sum(),', modellijn',NAAD.sum(),'), stipjes weg',weg)
# vlakken en volume
o=np.zeros((64,64),int)
TWEE={}   # zone -> (licht, schaduw)
for z,r in RAMP.items():
    TWEE[z]=(8,7) if r==ROZE else (r[1],r[0])
cz={z:np.array(np.where(zone==z)).mean(1) for z in ZNAAM if (zone==z).any()}
sz={z:np.array(np.where(zone==z)).std(1).mean()+1 for z in cz}
stuk=np.zeros((64,64),int); ns=0
for z in cz:
    l,k=nd.label((zone==z)&fg&~LIN&~OUT); stuk[l>0]=l[l>0]+ns; ns+=k
for Y,X in zip(*np.where(fg)):
    z=zone[Y,X]; li,sch=TWEE[z]
    g=((cz[z][1]-X)*0.6+(cz[z][0]-Y)*0.8)/sz[z]          # licht van linksboven over het hele onderdeel
    rand=any(binnen(Y+dy,X+dx) and stuk[Y+dy,X+dx]!=stuk[Y,X] for dy,dx in ((1,0),(0,1),(1,1)))
    o[Y,X]=li if (g>-0.55 and not rand) or g>0.9 else sch
# ronde delen (neus, hand R, vuist L): rand rondom outline base 6, zwart als boog linksmidden-linksonder-ondermidden (Gnomini r10);
# hooglicht 15: 2 px linksboven in het stuk
for zz in (5,9):
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
for zz in (5,9):
    m=zone==zz; yy,xx=np.where(m); cy,cx=yy.mean(),xx.mean()
    rand=m&nd.binary_dilation(~m,structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    for Y,X in zip(*np.where(rand)):
        h=np.degrees(np.arctan2(Y-cy,X-cx)); o[Y,X]=1 if 80<=h<=190 else 6
np.save('zone_af.npy',zone); np.save('lin.npy',LIN)
opslaan(o,'red.png')
