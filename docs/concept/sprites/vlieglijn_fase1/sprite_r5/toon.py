# canvas (64x64) als hex-tekens met x-liniaal; python3 toon.py BESTAND y0 y1 x0 x1
import numpy as np, sys
f=np.loadtxt(sys.argv[1],dtype=int); y0,y1,x0,x1=map(int,sys.argv[2:6])
print('    '+''.join(str((x//10)%10) for x in range(x0,x1))); print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%3d '%y+''.join('.' if v==0 else '%X'%v for v in f[y,x0:x1]))
