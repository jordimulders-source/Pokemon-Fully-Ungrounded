# Ruis-scan: pixels zonder gelijke 8-buur (los), en zwarte pixels die nergens aan achtergrond of andere zwarte pixel grenzen.
import sys; import numpy as np
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'r1.npy'); H,W=o.shape
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v==0: continue
        nb=[o[a,b] for a in range(y-1,y+2) for b in range(x-1,x+2) if (a,b)!=(y,x) and 0<=a<H and 0<=b<W]
        if v not in nb and v not in (14,): print('los', x,y,v, 'buren',sorted(set(nb)))
