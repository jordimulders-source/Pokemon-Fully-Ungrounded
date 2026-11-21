# bewijs r7: verschil met r5 B alleen in het potengebied; losse pixels; open randen; pootlijst
import numpy as np
r5=np.loadtxt('../sprite_r5/vlieg_r5_B.txt',dtype=int)
POOT={7,8,9,10,11,12,14,15}
for n in 'AB':
    f=np.loadtxt(f'vlieg_r7_{n}.txt',dtype=int); d=[(x,y) for y,x in zip(*np.where(f!=r5))]
    buiten=[p for p in d if p[1]<41 or r5[p[1],p[0]] not in POOT|{0,1}]
    los=[(x,y) for y in range(41,63) for x in range(1,63) if f[y,x] and not any(f[y+a,x+b] for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
    op=[(x,y) for y in range(41,63) for x in range(1,63) if f[y,x]>1 and any(f[y+a,x+b]==0 for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
    print(f'{n}: anders dan r5 B {len(d)} px; buiten potengebied {len(buiten)}; losse px {los}; open rand {op}; kleuren {len(set(f.ravel()))-1}')
