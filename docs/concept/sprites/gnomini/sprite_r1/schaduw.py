# schaduw.py A|B : toonkaart (licht linksboven) per onderdeel als gids -> sh_X.png. Kleurfamilie per pixel blijft die van de reductie (model);
# alleen de toon (licht/midden/schaduw) en de kant van de omlijning (selout linksboven, zwart rechtsonder) veranderen. Muts: modeltonen blijven.
import sys, numpy as np
from PIL import Image
from gemeen import *
var=sys.argv[1]
o=np.asarray(Image.open('red_%s.png'%var)).astype(int).copy()
zone=np.load('zone_%s.npy'%var); L=np.load('lijn_%s.npy'%var)
ROZE=[6,7,8,9]; BLAUW=[10,11,12,13]   # donker, schaduw, midden, licht
l=np.array([-0.5,-0.5,0.71]); l/=np.linalg.norm(l)
def ell(zz):
    yy,xx=np.where(zone==zz); return (xx.min()+xx.max())/2,(yy.min()+yy.max())/2,(xx.max()-xx.min()+1)/2,(yy.max()-yy.min()+1)/2
# bollen: (cx, cy, rx, ry)
B={k:ell(k) for k in (2,4,5,6,7)}
yy,xx=np.where(zone==3); B[3]=((xx.min()+xx.max())/2, 45.0 if True else 0, (xx.max()-xx.min()+1)/2, 11.0)
# drempels (licht, schaduw) per onderdeel
DR={3:(0.90,0.62),2:(0.82,0.45),4:(0.80,0.42),5:(0.85,0.50),6:(0.85,0.45),7:(0.85,0.45)}
fg=zone>0
for Y,X in zip(*np.where(fg&~L)):
    zz=zone[Y,X]
    if zz!=3: continue   # muts, neus, armpjes, voetjes: modeltonen (al bol met licht linksboven)
    cx,cy,rx,ry=B[zz]; nx=(X+0.5-cx-0.5)/rx; ny=(Y+0.5-cy-0.5)/ry; r2=nx*nx+ny*ny
    nz=np.sqrt(max(0.05,1-min(r2,0.98))); n=np.array([nx,ny,nz]); n/=np.linalg.norm(n)
    I=float(n@l)*0.5+0.5
    fam=ROZE if o[Y,X] in ROZE else BLAUW
    hi,lo=DR[zz]
    if fam==ROZE: hi=0.975
    else: hi=0.93
    t=3 if I>=hi else (2 if I>=lo else 1)
    o[Y,X]=fam[t]
# slagschaduw van de mutsrand op het lijf: 1 rij onder de mutslijn, 2 rijen in de rechterhelft
for Y,X in zip(*np.where((zone==3)&~L)):
    boven=[zone[Y-k,X]==1 for k in (1,2)]
    fam=ROZE if o[Y,X] in ROZE else BLAUW
    if boven[0] or (boven[1] and X>B[3][0]-2): o[Y,X]=fam[1]
# omlijning: buitenrand aan de lichtkant (achtergrond links/boven, niet rechts/onder) -> selout (donkerste zonetint), anders zwart.
for Y,X in zip(*np.where(L)):
    zz=zone[Y,X]
    nb={(dy,dx):fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))}
    buiten=not all(nb.values())
    if not buiten: continue
    licht=(not nb[(0,-1)] or not nb[(-1,0)]) and nb[(0,1)] and nb[(1,0)]
    if zz!=3: continue   # alleen het lijf; muts: lijnkleur van het model (selout zit er al in)
    if licht and Y<B[zz][1]+2:
        fam=ROZE if zz in (2,4,5) or (zz==3 and Y<47) else BLAUW
        o[Y,X]=fam[0]
    else: o[Y,X]=1
opslaan(o,'sh_%s.png'%var)
