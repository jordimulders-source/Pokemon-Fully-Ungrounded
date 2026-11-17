# pixeldiff r10 vs r9 per reparatiezone (index-vergelijking)
import numpy as np
g=np.load('cur.npy'); r=np.load('r9.npy')
Z={'1 mondband (15-41, 32-42)':[(15,32,42,43)],'7 kinrand (15-28, 36-44)':[(15,36,29,45)],
   '2 bel links (5-10, 33-38)':[(5,33,11,39)],'2 bel rechts (49-54, 17-22)':[(49,17,55,23)],
   '3+4 Shuppet links (0-17, 37-57)':[(0,37,18,58)],'3+4 Shuppet rechts (44-63, 42-62)':[(44,42,64,63)],
   '6 mutstop (31-43, 5-12)':[(31,5,44,13)],'8 naad (21-28, 12-31)':[(21,12,29,32)],
   '9 rood gezicht (26-40, 13-31)':[(26,13,41,32)],'10 linkerkruis (0-11, 16-27)':[(0,16,12,28)],
   '5 touwtjes (rest)':[(0,0,64,64)]}
d=(g!=r); used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-38s %4d px'%(n,(d&m).sum()))
print('totaal',d.sum())
# touwtjes: alleen hertint (14->13), geen vormwijziging
t=(r==14)&(g==13); print('waarvan touwpixels alleen hertint (marine -> draad):',t.sum())
