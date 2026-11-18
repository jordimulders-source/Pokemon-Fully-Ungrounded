# pixeldiff r8 vs r7 per reparatiezone (index-vergelijking)
import numpy as np
g=np.load('cur.npy'); r=np.load('r7.npy')
Z={'1 lijn popR (57,53)':[(57,53,58,54)],'2 lijn popL (13,56)':[(13,56,14,57)],
   '3 naad muts (35-41, 6-12)':[(35,6,42,13)],'4 voet/lap (24-33, 46-49)':[(24,46,34,50)],
   '5 bel links (6-9, 34-37)':[(6,34,10,38)],'6 bel rechts (50-53, 18-21)':[(50,18,54,22)],
   '7 ogen poppetjes':[(5,45,7,47),(11,45,13,47),(48,51,50,53),(54,51,56,53)],
   '8 los (29,15)':[(29,15,30,16)],'9 glans muts (33-35, 8-10)':[(33,8,36,11)]}
d=(g!=r); used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-34s %4d px'%(n,(d&m).sum()))
print('%-34s %4d px'%('BUITEN de zones',(d&~used).sum()), [tuple(int(v) for v in p[::-1]) for p in np.argwhere(d&~used)])
print('totaal',d.sum())
