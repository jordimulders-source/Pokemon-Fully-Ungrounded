# herkomst per natieve modelcel: 4=r4, 6=r6 (stekel -4,-1 / strepen), 3=r3_3 (staart -2,+3), ?=geen bron (gevuld/getekend)
import sys; sys.path.insert(0,'../gereedschap')
import numpy as np
from natief import natief
D='../gemini/'
m=np.load('model_nat.npy').astype(int)
r4=natief(D+'r4.png').astype(int); r6=natief(D+'r6.png').astype(int); r3=natief(D+'r3_3_Y_A.png').astype(int)
np.save('r4_nat.npy',r4); np.save('r6_nat.npy',r6); np.save('r3_nat.npy',r3)
def sh(a,dx,dy):
    o=np.full_like(a,-999); 
    for y in range(100):
        for x in range(100):
            Y,X=y-dy,x-dx
            if 0<=Y<100 and 0<=X<100: o[y,x]=a[Y,X]
    return o
src={'4':r4,'6':sh(r6,-4,-1),'3':sh(r3,-2,3),'s':sh(r6,0,1)}
H=np.full((100,100),'?')
for y in range(100):
    for x in range(100):
        if m[y,x].sum()>740: H[y,x]='.'; continue
        for k,a in src.items():
            if np.abs(a[y,x]-m[y,x]).max()<=3: H[y,x]=k; break
np.save('herkomst.npy',H)
print('    '+''.join(str(x%10) for x in range(3,97)))
for y in range(5,90): print(f'{y:3d} '+''.join(H[y,3:97]))
