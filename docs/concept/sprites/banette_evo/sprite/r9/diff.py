# pixeldiff r9 vs r8 per reparatiezone (index-vergelijking)
import numpy as np
g=np.load('cur.npy'); r=np.load('r8.npy')
Z={'1 bel links (6-9, 34-37)':[(6,34,10,38)],'1 bel rechts (50-53, 18-21)':[(50,18,54,22)],
   '2 kapflap (12,29)':[(12,29,13,30)],'3 steken kap (36-42, 6-12)':[(36,6,43,13)],
   '4 ogen popL (4-14, 44-47)':[(4,44,15,48)],'4 ogen popR (47-58, 49-53)':[(47,49,59,54)],
   '5 mondhoek (40-42, 27-31)':[(40,27,43,32)],'6 kruis (55, 19-22)':[(55,19,56,23)]}
d=(g!=r); used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-34s %4d px'%(n,(d&m).sum()))
print('%-34s %4d px'%('BUITEN de zones',(d&~used).sum()), [tuple(int(v) for v in p[::-1]) for p in np.argwhere(d&~used)])
print('totaal',d.sum())
