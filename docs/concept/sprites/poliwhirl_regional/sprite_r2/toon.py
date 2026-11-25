# python3 toon.py raster.npy -> tekstraster
import sys,numpy as np
o=np.load(sys.argv[1])
print('   '+''.join(str(i%10) for i in range(o.shape[1])))
for j,r in enumerate(o): print('%2d '%j+''.join('.' if v==0 else '%x'%v for v in r))
