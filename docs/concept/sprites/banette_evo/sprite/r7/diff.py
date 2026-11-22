# pixeldiff r7 vs r6 per reparatiezone (index-vergelijking)
import numpy as np
g=np.load('cur.npy'); r=np.load('r6.npy')
Z={'1a oog rood (x25-37 r22-31)':[(25,22,38,32)],'1b oog grijs (x15-23 r25-32)':[(15,25,24,33)],
   '2 bel links (x5-10 r33-38)':[(5,33,11,39)],'2 bel rechts (x49-54 r17-21)':[(49,17,55,22)],
   '3 lap + kaaklijn (x21-33 r43-49)':[(21,43,34,50)],'4 hoedsteken (x36-48 r5-12)':[(36,5,49,13)],
   '5 rode rand (x38-45 r13-23)':[(38,13,46,24)],'6 linkerkruis (x0-11 r16-28)':[(0,16,12,29)],
   '7 mond (x15-44 r32-41)':[(15,32,45,42)],'8 los (15-16,19),(46,22),(46,31),(48,17-18),(33,8)':[(15,19,17,20),(46,22,47,23),(46,31,47,32),(48,17,49,19),(33,8,34,9)]}
d=(g!=r); used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-58s %4d px'%(n,(d&m).sum()))
print('%-58s %4d px'%('BUITEN de zones',(d&~used).sum()), [tuple(int(v) for v in p[::-1]) for p in np.argwhere(d&~used)])
print('totaal',d.sum())
