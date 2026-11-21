import sys, numpy as np
H='.123456789abcdef'
a=np.load(sys.argv[1]); open(sys.argv[2],'w').write(''.join('%02d '%y+''.join(H[v] for v in a[y])+'\n' for y in range(64)))
