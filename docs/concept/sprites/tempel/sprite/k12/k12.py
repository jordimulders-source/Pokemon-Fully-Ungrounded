# k12 = k11 + rechterstijl schuin (trapje), geen parallelle voeg naast de stijl
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a11,pal=laad('../k11/tempel.png'); a=a11.copy()
Z={
 # buitenrand rechterstijl: x25 (y49-52) -> x26 (y53-56) -> x27 (y57-60), zwart; stijlvlak schuift mee (5)
 (25,53):5,(25,54):5,(25,55):5,(25,56):5,(25,57):5,
 (26,53):1,(26,54):1,(26,55):1,(26,56):1,
 (26,57):5,(26,58):5,(26,59):5,(26,60):5,
 (27,57):1,(27,58):1,(27,59):1,(27,60):1,
 # voeg naast de stijl (x27, y49-52) weg; muur loopt door
 (27,49):3,(27,50):3,(27,51):5,(27,52):5,
 # verticale voeg x29 onderaan (y57-59) weg, anders weer een lijn vlak naast de stijl
 (29,57):5,(29,58):5,(29,59):5,
 (27,56):5,
}
for (x,y),c in Z.items(): a[y,x]=c
# binnenlijnen van de poort niet zwart: zwart (1) binnen het silhouet -> donkerste eigen tint (14)
a8,_=laad("../k8/tempel.png"); dm=deurmasker(a8)   # oorspronkelijk deurgat (62 px)
H,W=a.shape
omgezet=[]
for y in range(44,61):
    for x in range(12,28):
        if a[y,x]!=1 or dm[y,x]: continue
        rand=any(not(0<=x+dx<W and 0<=y+dy<H) or a[y+dy,x+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
        if rand: continue
        a[y,x]=14; omgezet.append((x,y))
print('zwart -> 14:',len(omgezet),omgezet)
bewaar(a,pal,'tempel.png')
