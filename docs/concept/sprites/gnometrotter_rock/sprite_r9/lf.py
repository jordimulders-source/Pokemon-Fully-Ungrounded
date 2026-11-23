import sys,numpy as np
lf=np.load('lijn.npy')
G=[l.rstrip('\n') for l in open('grid.txt') if l.strip()]
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(x0,x1))+'   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    print('%2d  '%y+G[y][x0:x1]+'   '+''.join('.' if G[y][x]=='.' else (str(min(9,int(lf[y,x]*10))) if lf[y,x]>=0.1 else ' ') for x in range(x0,x1)))
