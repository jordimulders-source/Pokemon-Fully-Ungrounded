# pixeldiff r6 vs r5 per reparatiezone (index-vergelijking)
import numpy as np
g=np.load('cur.npy'); r=np.load('r5.npy')
Z={'1+4 Shuppet-ogen/rand (x4-14 r44-47, x47-58 r50-53)':[(4,44,15,48),(47,50,59,54)],
   '2 linkerbel (x5-10 r33-38)':[(5,33,11,39)],
   '13 rechterbel (x50-53 r18-21)':[(50,18,54,22)],
   '3 kin (x13-17 r33-40)':[(13,33,18,41)],
   '5 steeklijn (x36-42 r6-12)':[(36,6,43,13)],
   '6 krul (x40-51 r5-12)':[(40,4,52,13)],
   '6+8 lijfschaduw + kolom 41 (x30-45 r13-45)':[(30,13,46,46)],
   '7 flap (x46-48 r19-31)':[(46,19,49,32)],
   '9 kruis (x5-9 r23-24)':[(5,23,10,25)],
   '10 gezicht (x15-23 r17-36)':[(15,17,24,37)],
   '12 arm L-Shuppet (x8-11 r53-54)':[(8,53,12,55)]}
d=(g!=r); used=np.zeros_like(d)
for n,bs in Z.items():
    m=np.zeros_like(d)
    for x0,y0,x1,y1 in bs: m[y0:y1,x0:x1]=True
    m&=~used; used|=m; print('%-55s %4d px'%(n,(d&m).sum()))
print('%-55s %4d px'%('BUITEN de zones',(d&~used).sum()), [tuple(int(v) for v in p[::-1]) for p in np.argwhere(d&~used)])
print('totaal',d.sum())
