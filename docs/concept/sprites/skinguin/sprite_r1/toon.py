import sys,numpy as np
s=np.loadtxt(sys.argv[1],dtype=int); r0,r1,c0,c1=map(int,sys.argv[2:6])
ch='.KrSMLWgdYoyb'
print('   '+''.join(str(i%10) for i in range(c0,c1)))
for y in range(r0,r1): print('%2d '%y+''.join(ch[v] for v in s[y,c0:c1]))
