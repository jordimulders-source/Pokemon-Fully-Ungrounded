# Meting: dominante modelgroep per spritepixel (P roze, C creme/wit, K tan k/t/b, L lijn #/d, E oog, M magenta M/p, Y geel, . leeg)
import sys, numpy as np
from cov import cov
from txt import CH
GR={'P':'smlL','C':'cw','K':'ktb','L':'#d','E':'E','M':'Mp','Y':'Y','.':'.'}
r0,r1,c0,c1=map(int,sys.argv[1:5])
print('    '+''.join(str(c%10) for c in range(c0,c1)))
for j in range(r0,r1):
    s=''
    for i in range(c0,c1):
        w=cov(j,i); g={k:sum(w[CH.index(c)] for c in v) for k,v in GR.items()}
        s+=max(g,key=g.get)
    print('%3d '%j+s)
