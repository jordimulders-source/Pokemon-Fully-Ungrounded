import sys,numpy as np
N=np.load('naad.npy'); G=[l.rstrip('\n') for l in open('grid.txt') if l.strip()]
x0,y0,x1,y1=map(int,sys.argv[1:5])
h=''.join(str(x%10) for x in range(x0,x1))
print('    '+h+'   '+h)
for y in range(y0,y1):
    print('%2d  '%y+G[y][x0:x1]+'   '+''.join('.' if G[y][x]=='.' else ('#' if N[y,x]>=4 else '+' if N[y,x]>=2 else ' ') for x in range(x0,x1)))
