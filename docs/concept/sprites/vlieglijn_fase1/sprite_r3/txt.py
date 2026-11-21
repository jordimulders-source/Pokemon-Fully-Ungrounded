# raster <-> tekens. python3 txt.py naar IN.txt UIT.chr | python3 txt.py terug IN.chr UIT.txt
import numpy as np, sys
CH='.#kdgGLcChWwvpor'
if sys.argv[1]=='naar':
    o=np.loadtxt(sys.argv[2],dtype=int)
    open(sys.argv[3],'w').write('\n'.join(''.join(CH[v] for v in r) for r in o)+'\n')
else:
    L=[l.rstrip('\n') for l in open(sys.argv[2]) if l.strip()]
    o=np.array([[CH.index(c) for c in l] for l in L]); np.savetxt(sys.argv[3],o,fmt='%2d')
