# pixeldiff r5 vs r4 per reparatiezone (index-vergelijking). Paletwijziging index 8 (mond/oogkas) telt apart.
import numpy as np
g=np.load('cur.npy'); r=np.load('r4.npy')
Z={'1 ogen hoofd (x16-35 r25-31)':[(16,25,36,32)],
   '2 mond + tanden (x13-42 r26-44)':[(13,32,43,45),(38,26,43,32)],
   '3 linkerkruis (x0-10 r16-26)':[(0,16,11,27)],
   '4 Shuppet-ogen (x4-13 r44-47, x47-56 r50-53)':[(4,44,14,48),(47,50,57,54)],
   '6 belletjes (x5-10 r33-38, x49-54 r17-22)':[(5,33,11,39),(49,17,55,23)],
   '5+9 draden (links x2-6 r26-43, rechts x56-61 r25-55)':[(2,26,7,44),(56,25,62,56)],
   '7+8+12 muts: glans, schaduwgrens, naad (x26-47 r4-24)':[(26,4,48,25)],
   '10 spleet hoofd/arm (x44-45 r21-32)':[(44,21,46,33)],
   '11 lap linksonder (x25-33 r46-49)':[(25,46,34,50)]}
d=(g!=r); used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-58s %4d px'%(n,(d&m).sum()))
print('%-58s %4d px'%('BUITEN de zones',(d&~used).sum()), [tuple(int(v) for v in p[::-1]) for p in np.argwhere(d&~used)])
print('totaal',d.sum())
