import numpy as np
r5=np.loadtxt('../sprite_r5/vlieg_r5_B.txt',dtype=int); f=np.loadtxt('vlieg_r8.txt',dtype=int); POOT={7,8,9,10,11,12,14,15}
d=[(x,y) for y,x in zip(*np.where(f!=r5))]
buiten=[p for p in d if p[1]<41 or r5[p[1],p[0]] not in POOT|{0,1}]
N=((1,0),(-1,0),(0,1),(0,-1))
los=[(x,y) for y in range(41,63) for x in range(1,63) if f[y,x] and not any(f[y+a,x+b] for a,b in N)]
op=[(x,y) for y in range(41,63) for x in range(1,63) if f[y,x]>1 and any(f[y+a,x+b]==0 for a,b in N)]
print(f'r8: anders dan r5 B {len(d)} px; buiten potengebied {len(buiten)}; losse px {los}; open rand {op}; kleuren {len(set(f.ravel()))-1}')
print('geel-pixels nu:',[(x,y,f[y,x]) for x,y in [(28,y) for y in range(49,55)]+[(29,y) for y in range(51,55)]])
