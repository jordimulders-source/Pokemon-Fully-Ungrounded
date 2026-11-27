# Stap 3: technisch opschonen van de kale reductie (kaal.npy) + oog + nieuwe vleugelharen (Jordi 27 nov).
import numpy as np, sys
from gemeen import *
k=np.load('kaal.npy'); s=k.copy(); Hh,Ww=s.shape
log={}
def zet(y,x,v,why):
    if s[y,x]!=v: s[y,x]=v; log.setdefault(why,[]).append((x,y))
# 1. oog uit het model: grijze ring om een donker oog (model: schijf 136-140, donkere kern); 4x4 op de modelplek
OOG=[[4,9,9,4],[9,1,1,9],[9,1,1,9],[4,9,9,4]]
for dy,r in enumerate(OOG):
    for dx,v in enumerate(r):
        if v is not None: zet(4+dy,8+dx,v,'oog')
# 2. losse ruispixels: een pixel waarvan alle 4 buren dezelfde andere vlakkleur hebben (geen lijn, geen oog)
for y in range(1,Hh-1):
    for x in range(1,Ww-1):
        v=s[y,x]; nb=[s[y-1,x],s[y+1,x],s[y,x-1],s[y,x+1]]
        if v>1 and len(set(nb))==1 and nb[0]>1 and nb[0]!=v and not (4<=y<=7 and 8<=x<=11):
            zet(y,x,nb[0],'ruis')
# (2b 'losse zwarte pixels in grijs weg' geprobeerd en geschrapt: vleugel en staart liepen ineen = pixelblur)
# 3. buitenlijn dicht: randpixel (grenst aan transparant) met een lichte vlakkleur, waar het onderdeel >=3 px dik is -> omlijning
t=lambda y,x: (y<0 or x<0 or y>=Hh or x>=Ww or s[y,x]==0)
for y in range(Hh):
    for x in range(Ww):
        v=s[y,x]
        if v in (0,1) or (4<=y<=7 and 8<=x<=11): continue
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            if t(y+dy,x+dx) and not t(y-dy,x-dx) and not t(y-2*dy,x-2*dx) and s[y-dy,x-dx]!=1:
                zet(y,x,1,'buitenlijn'); break
np.save('schoon.npy',s)
# 4. nieuwe vleugelharen (Jordi: "vervang je door haren die beter passen bij een sprite"): losse 1-px lijntjes
#    in de omlijningskleur, schuin naar achteren-onder zoals de modelharen, vanaf de achterrand van de kale vleugels.
HAAR={'A':[[(8,26),(9,27)],[(10,25),(11,26)],[(12,24),(13,25)],            # links (vleugel uitgestoken)
           [(31,16),(32,17)],[(31,19),(32,20)],[(32,22),(33,23)]],          # rechts (vleugel over het lijf)
      'B':[[(7,28),(8,29),(9,30)],[(8,26),(9,27),(10,28)],[(10,25),(11,26),(12,27)],[(12,24),(13,25),(14,26)],
           [(31,15),(32,16),(33,17)],[(31,18),(32,19),(33,20)],[(31,21),(32,22),(33,23)]]}
for var,strokes in HAAR.items():
    v=s.copy()
    for st in strokes:
        for x,y in st: assert v[y,x]==0,(var,x,y); v[y,x]=1
    np.save(f'haar_{var}.npy',v)
    print('haren',var,sum(len(t) for t in strokes),'px')
for kk,vv in log.items(): print(kk,len(vv))
