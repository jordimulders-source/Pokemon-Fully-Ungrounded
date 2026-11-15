# v7 = v6 + opdracht (15 nov): Jordi koos "van jouw versie de positionering" = plek uit sprite_r3 (Gengar-gezicht als
# één blok op Gengar-coördinaat x-6, y+5). Ogen én grijns samen als één blok op die verschuiving (onderlinge afstand
# oog-grijns = exact Gengar). Vrijgekomen plekken: omliggende lijftinten van v6. Losse l (31,43),(30,44) opgenomen.
# Bandrand boven het rechteroog rond gemaakt (geen rechte naad). Alleen in de zone x 8-33, y 28-47.
import os
import numpy as np
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))+'/'
R=[list(l.rstrip('\n')) for l in open(D+'../sprite_v6/raster.txt')][:64]
V6=[r[:] for r in R]
log=[]
def inzone(x,y): return 8<=x<=33 and 28<=y<=47
def zet(x,y,c,reden):
    assert inzone(x,y),(x,y)
    if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
g=np.array(Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png'))[:64]
MAP={1:'W',2:'H',3:'G',5:'R',6:'E',7:'H',13:'b',14:'a',15:'K'}
FACE={1,2,3,4,5,6,7,14,15}
delen=[('linkeroog',18,23,28,32),('rechteroog',28,36,26,31),('grijns',18,38,32,40)]
def gezicht():
    for nm,x0,x1,y0,y1 in delen:
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                v=int(g[y,x]); nb=g[y-1:y+2,x-1:x+2].flatten()
                if v in FACE or (v==13 and any(int(n) in {1,2,3,4,5,6,7} for n in nb)):
                    if nm=='grijns' and y==32 and x<30: continue
                    yield nm,x,y,MAP[v]
# 1) v6-gezicht weg (ogen dx-5,dy+3; grijns dx-5,dy+6), gaten vullen met de lijftint van de buren
gat=set()
for nm,x,y,c in gezicht():
    dy=6 if nm=='grijns' else 3
    gat.add((x-5,y+dy))
open_=set(gat)
while open_:
    nieuw={}
    for (x,y) in open_:
        buren=[R[y+dy][x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) not in open_ and R[y+dy][x+dx] in 'mblu']
        if buren: nieuw[(x,y)]=max(set(buren),key=lambda c:(buren.count(c),c=='m'))
    assert nieuw
    for (x,y),c in nieuw.items(): zet(x,y,c,'v6-gezicht weg, lijftint van de buren'); open_.discard((x,y))
# 2) losse l-pixels opnemen in het omliggende vlak
for (x,y) in ((31,43),(30,44)):
    buren=[R[y+dy][x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and R[y+dy][x+dx] in 'mblu']
    zet(x,y,max(set(buren),key=buren.count),'losse l opgenomen in het vlak eromheen')
# 3) bandrand boven het rechteroog: onderrand loopt rond (27 bij x24-25, 28 bij x26-27, 29 bij x28-34, 28 bij x35,
#    27 vanaf x36) i.p.v. 8 px recht op rij 28; (34,29) was al b (buiten de zone)
for x in range(28,34): zet(x,29,'b','bandrand rond: onderrand op rij 29 aansluitend op (34,29)')
for x in range(8,34):
    if R[30][x]=='b': zet(x,30,'m','geen bandpunt naar het oog (vulling uit v6-oogrand)')
# 4) Gengar-gezicht als één blok op (x-6, y+5) = plek uit sprite_r3
for nm,x,y,c in gezicht(): zet(x-6,y+5,c,f'Gengar {nm} ({x},{y}) -> blok x-6,y+5')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
buiten=[(x,y) for y in range(64) for x in range(64) if V6[y][x]!=R[y][x] and not inzone(x,y)]
print(len(log),'wijzigingen; pixels anders dan v6 buiten de zone x8-33,y28-47:',len(buiten))
