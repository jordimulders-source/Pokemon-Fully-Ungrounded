# raster.py uit kaal.npy raster.txt  |  raster.py in raster.txt out.npy : tekstraster <-> indices
import sys, numpy as np
C='.X+abcdemnopz'
if sys.argv[1]=='uit':
    G=np.load(sys.argv[2]); open(sys.argv[3],'w').write('\n'.join(''.join(C[v] for v in r) for r in G)+'\n')
else:
    R=[l.rstrip('\n') for l in open(sys.argv[2])][:64]
    G=np.array([[C.index(ch) for ch in r] for r in R]); np.save(sys.argv[3],G)
