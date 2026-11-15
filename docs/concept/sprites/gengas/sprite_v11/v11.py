# v11 = v10a + (15 nov):
#  1) Jordi: "de stormvlek is niet mooi zo, als die niet goed immersed toont, heb ik liever dat je het reguliere
#     golfpatroon aanhoudt, die is erg mooi gelukt" -> geen vlek, geen spiraal: de lichte strook (l) links van de plek
#     loopt met een schuine, golvende rechterrand door, de rest wordt de middenband m zoals ernaast.
#  2) Gezicht 125% (Jordi: ogen en mond groter, netjes vergroot, niet from scratch): gezicht_groter/gezicht_1.25.npy
#     (Gengars gezicht per kleurlaag geschaald), zelfde middelpunt als het huidige gezicht (Gengar-blok x-6, y+5),
#     kleuren zoals v6/v7; daarna per pixel nagelopen tegen Gengar (zie FIX). Oud gezicht weg, gaten met de buurtint;
#     voorhoofdband opnieuw net boven de grotere ogen (onderrand golvend, volgt de wenkbrauwen).
# Diff buiten x 4-48, y 22-48 = 0 (gemeten).
import os
import numpy as np
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))+'/'
V10=[l.rstrip('\n') for l in open(D+'../sprite_v10/raster_v10a.txt')][:64]
R=[list(r) for r in V10]; log=[]
def zone(x,y): return 4<=x<=48 and 22<=y<=48
def zet(x,y,c,reden):
    assert zone(x,y),(x,y)
    if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
# 1) stormvlek weg: lichte strook loopt door (laatste l-kolom per rij), rechts daarvan m
rand={30:35,31:35,32:35,33:36,34:36,35:37,36:37,37:38,38:38,39:39,40:39,41:37}
for y,xe in rand.items():
    for x in range(36,48):
        if R[y][x] in 'lvbm': zet(x,y,'l' if x<=xe else 'm','bandpatroon loopt door (geen vlek/spiraal)')
# 2a) oud gezicht (Gengar-blok x-6,y+5 zonder d) weg, vullen met de buurtint
g=np.array(Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png'))[:64].astype(int)
FACE={1,2,3,4,5,6,7,14,15}
gat=set()
for x0,x1,y0,y1,nm in ((18,23,28,32,'l'),(28,36,26,31,'r'),(18,38,32,40,'g')):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if g[y,x] in FACE and not (nm=='g' and y==32 and x<30): gat.add((x-6,y+5))
open_=set(gat)
while open_:
    nieuw={}
    for (x,y) in open_:
        b=[R[y+dy][x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) not in open_ and R[y+dy][x+dx] in 'mbl']
        if b: nieuw[(x,y)]=max(set(b),key=lambda c:(b.count(c),c=='m'))
    for (x,y),c in nieuw.items(): zet(x,y,c,'oud gezicht weg, buurtint'); open_.discard((x,y))
# 2b) voorhoofdband: onderrand (laatste b-rij) per kolom net boven de grotere ogen (1 rij ruimte), golvend
lo={9:30,10:29,11:29,12:29,13:30,14:30,15:31,16:31,**{x:32 for x in range(17,23)},23:31,24:31,25:30,26:30,27:30,
    28:29,29:29,30:27,31:27,32:27,33:28,34:28,35:28}
hi={9:25,10:25,11:25,12:25,13:28,**{x:28 for x in range(14,18)},**{x:29 for x in range(18,24)}}
for x in range(9,36):
    for y in range(hi.get(x,28),lo[x]+1):
        if R[y][x] in 'mlb' and not (x in (12,13) and y<28): zet(x,y,'b','voorhoofdband')
    for y in range(lo[x]+1,41):
        if R[y][x]=='b': zet(x,y,'m','lichtere band onder de voorhoofdband')
# 2c) gezicht 1.25 met nalooppunten (FIX, coördinaten in het npy-raster i,j)
F=np.load(D+'../gezicht_groter/gezicht_1.25.npy').copy()
FIX=[((7,15),1,'tandscheiding links 1 px (Gengar x21)'),((7,16),1,'idem'),((8,17),1,'idem'),((8,18),1,'idem'),
     ((13,18),1,'tandschaduw 1 px (Gengar 7-2)'),
     ((13,19),1,'onderste tandscheiding 1 px (Gengar x25)'),((13,20),1,'idem'),
     ((17,16),1,'tandscheiding 1 px (Gengar x29)'),
     ((23,14),1,'tandscheiding 1 px (Gengar x33)'),((23,15),1,'idem'),((23,16),2,'Gengar 7-2'),((24,16),1,'idem'),
     ((27,14),1,'rechtermondhoek 1 px zoals Gengar'),((27,15),1,'idem'),((26,16),1,'idem'),((25,17),1,'idem'),
     ((8,9),5,'linkerpupil 2-2-1 zoals de rechter (gespiegeld)')]
for (i,j),v,r in FIX: F[j,i]=v
MAP={1:'W',2:'H',3:'u',5:'R',6:'E',7:'H',14:'a',15:'K'}
DX,DY=6,27
fixset={(i,j):r for (i,j),v,r in FIX}
for j in range(F.shape[0]):
    for i in range(F.shape[1]):
        v=int(F[j,i])
        if v: zet(i+DX,j+DY,MAP[v],'gezicht 1.25'+(' + '+fixset[(i,j)] if (i,j) in fixset else ''))
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
print(len(log),'wijzigingen; buiten x4-48,y22-48:',sum(1 for y in range(64) for x in range(64) if V10[y][x]!=R[y][x] and not zone(x,y)))
