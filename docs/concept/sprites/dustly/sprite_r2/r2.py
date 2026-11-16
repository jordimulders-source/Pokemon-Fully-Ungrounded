# r2 = r1 A + (1) mond/tanden, (2) mondhoek links, (3) perzikrand dunner. Diff per zone, 0 erbuiten.
import numpy as np
r1=np.load('sprite_r2/r1_idx.npy'); o=r1.copy(); log={}
def put(z,x,y,v):
    if o[y,x]!=v: o[y,x]=v; log[z]=log.get(z,0)+1
# 1. mond: model natief rij 57-58 valt in spriterij 34 -> één rechte lijn x14-23 (dip van r1 weg, rij 35 x17-19 lijftint 3)
for x in range(14,24): put('mond',x,34,1)
for x in (17,18,19): put('mond',x,35,3)
# tanden: links model x25 (1 breed) -> sprite x14; rechts model x35-36 boven, punt x36 -> sprite x21-22 boven, punt x22
put('mond',14,35,9); put('mond',14,36,9); put('mond',15,35,1); put('mond',15,36,1); put('mond',13,35,3); put('mond',16,35,3)
put('mond',20,35,1); put('mond',21,35,9); put('mond',22,35,9); put('mond',23,35,1)
put('mond',21,36,1); put('mond',22,36,9); put('mond',23,36,1)
# 2. mondhoek links: model rij 57 x21-23 is '+' (lijnkleur, 35-58), geen lijftint -> sprite x12-13 index 2 i.p.v. zwart
put('mondhoek',12,34,2); put('mondhoek',13,34,2)
# 3. perzikrand: tweede laag zonder perzik in het model (aandeel 0,00) terug naar de buurtint
for x,y in [(25,12),(21,13),(20,15),(17,16),(15,17),(13,25)]:
    nb=[o[y+dy,x+dx] for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)) if o[y+dy,x+dx] in (3,4,5,6)]
    put('perzik',x,y,max(set(nb),key=nb.count))
np.save('sprite_r2/r2_idx.npy',o)
d=o!=r1; print('diff totaal',d.sum(),log)
zones={'mond':(11,24,33,37),'perzik':(9,30,8,26)}
out=d.copy()
for (x0,x1,y0,y1) in zones.values(): out[y0:y1+1,x0:x1+1]=False
print('diff buiten de zones:',out.sum())
