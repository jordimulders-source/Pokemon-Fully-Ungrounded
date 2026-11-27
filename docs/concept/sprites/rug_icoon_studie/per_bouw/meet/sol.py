import numpy as np,ld,json
from hand import H
from soorten import BOUW
from scipy import ndimage as nd
from scipy.spatial import ConvexHull
def solidity(m):
    ys,xs=np.nonzero(m); pts=np.c_[xs,ys].astype(float)
    pts=np.vstack([pts+[dx,dy] for dx in(0,1) for dy in(0,1)])
    h=ConvexHull(pts); return m.sum()/h.volume
def thin(m,r):
    st=nd.generate_binary_structure(2,1); e=nd.binary_erosion(m,st,iterations=r); o=nd.binary_dilation(e,st,iterations=r)&m
    return 1-o.sum()/m.sum()
rows=[]
for b,L in BOUW.items():
    for s in L:
        fm=ld.front(s)[...,3]>0
        rows.append((b,s,H[s]['pose'],solidity(fm),thin(fm,2),thin(fm,3)))
for r in rows: print('%-10s %-10s %-7s sol%.2f thin2 %.2f thin3 %.2f'%r)
import numpy as np
for p in ('zelfde','wissel','spiegel'):
    a=np.array([r[3:] for r in rows if r[2]==p]); print(p,len(a),np.median(a,0).round(2),np.percentile(a,25,0).round(2),np.percentile(a,75,0).round(2))
