# ed.py bron.txt doel.txt edits.txt : handmatige rijsegmenten "y: x=tekens ..." over een raster leggen ('=' = laten staan); meldt silhouetafwijkingen
import sys
from tl import *
R=[list(l) for l in raster(sys.argv[1])]
for l in open(sys.argv[3]):
    l=l.split('#')[0]
    if not l.strip(): continue
    y,rest=l.split(':',1); y=int(y)
    for t in rest.split():
        x,s_=t.split('=',1); x=int(x)
        for k,c in enumerate(s_):
            if c=='=': continue
            if (c=='.')!=(not SIL[y,x+k]): print('SILHOUET-afwijking',x+k,y,c)
            R[y][x+k]=c
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
