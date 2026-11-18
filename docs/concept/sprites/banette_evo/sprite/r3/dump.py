# tekstraster van een zone: python3 dump.py npy x0 y0 x1 y1  (index als hex)
import sys,numpy as np
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]
print('    '+''.join('%x'%(i%16) for i in range(x0,x1)))
for j in range(y0,y1): print('%3d '%j+''.join('.' if g[j,i]==0 else '%x'%g[j,i] for i in range(x0,x1)))
