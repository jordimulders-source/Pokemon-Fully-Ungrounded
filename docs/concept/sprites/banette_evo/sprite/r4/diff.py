# pixeldiff r4 vs r3 per zone (index-vergelijking; ring 5->6 telt apart als paletsamenvoeging)
import numpy as np
g=np.load('cur.npy'); r=np.load('r3.npy')
Z={'1 mond (x13-44 r31-44, wangarm x38-41 r26-30)':[(13,31,45,45),(38,26,42,31)],'4 rechteroog (x30-33 r25-29)':[(30,25,34,30)],
   '3 linkerkruis (x0-9 r16-27)':[(0,16,10,28)],'2+5 Shuppet links (x2-17 r38-57)':[(2,38,18,58)],'2+5 Shuppet rechts (x44-62 r40-62)':[(44,40,63,63)]}
d=(g!=r); ring=(r==5)&(g==6); d2=d&~ring
used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-48s %4d px'%(n,(d2&m).sum()))
print('%-48s %4d px'%('oogring 5->6 (paletsamenvoeging, beide hoofdogen)',ring.sum()))
print('%-48s %4d px'%('BUITEN de zones',(d2&~used).sum()), [tuple(p[::-1]) for p in np.argwhere(d2&~used)])
