# zet.py bron doel "x,y,c" ... : losse handmatige pixelwijzigingen in een 64-rijen raster (meldt silhouetafwijking)
import sys
from tl import SIL
R=[list(l.rstrip('\n')) for l in open(sys.argv[1])][:64]
for a in sys.argv[3:]:
    x,y,c=a.split(','); x,y=int(x),int(y)
    if (c=='.')!=(not SIL[y,x]): print('SILHOUET-afwijking',x,y,c)
    R[y][x]=c
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
