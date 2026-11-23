# volume.py: red.png -> vol.png. Gen 3-volume (licht linksboven) op lijf en broek zoals bij Gnomini (midden als basis, schaduwsikkel rechts,
# slagschaduw onder snor/mutsrand), selout aan de lichtkant van de buitenlijn. Muts, neus, snor, handen, benen: modeltonen.
import numpy as np
from gemeen import *
o=lees('red.png'); zone=np.load('zone.npy'); L=np.load('lijn.npy')
fg=zone>0
lijf=np.isin(zone,(5,8))&~L
# lijf+broek als bol: middelpunt en stralen uit de zone (incl. lijnen)
yy,xx=np.where(np.isin(zone,(5,8))); cx,cy=27.0,45.5; rx,ry=14.0,8.5
l=np.array([-0.55,-0.6,0.58]); l/=np.linalg.norm(l)
for Y,X in zip(*np.where(lijf)):
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r2=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r2,0.96)))]); n/=np.linalg.norm(n); I=float(n@l)
    if zone[Y,X]==5: o[Y,X]=8 if I>=0.30 else 7
    else: o[Y,X]=11 if I>=0.25 else (10 if I>=-0.25 else 9)
# slagschaduw: 1 rij lijf direct onder snor/neus/muts (vlak, niet de lijn) -> schaduwtint
for Y,X in zip(*np.where(lijf&(zone==5))):
    if zone[Y-1,X] in (1,2,3,4) or (L[Y-1,X] and zone[Y-2,X] in (1,2,3,4)): o[Y,X]=7
# selout: buitenlijn waarvan de achtergrond links/boven ligt (lichtkant) -> donkerste vlaktint van het onderdeel
SEL={1:2,2:6,3:14,4:14,5:6,6:6,7:6,8:9,9:9,10:9}
for Y,X in zip(*np.where(L&fg)):
    if o[Y,X]!=1: continue
    v=np.zeros(2)
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        if not fg[Y+dy,X+dx]: v+=(dx,dy)
    if not v.any(): continue
    v/=np.linalg.norm(v)
    if v@np.array([-0.6,-0.8])>0.35: o[Y,X]=SEL[zone[Y,X]]
opslaan(o,'vol.png')
