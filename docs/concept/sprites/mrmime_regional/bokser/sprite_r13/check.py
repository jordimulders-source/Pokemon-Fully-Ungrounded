# Controle: lichte pixels op de buitenrand, losse pixels (geen buur met dezelfde index), kleurtelling
import numpy as np; from PIL import Image
import sys; g=np.load(sys.argv[1]); H,W=g.shape
rand=[];los=[]
for y in range(H):
    for x in range(W):
        v=g[y,x]
        if v==0: continue
        nb=[g[yy,xx] if 0<=yy<H and 0<=xx<W else 0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
        if 0 in nb and v>=5: rand.append((x,y,int(v)))
        nb8=[g[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x) and 0<=yy<H and 0<=xx<W]
        if v not in nb8 and v not in (1,): los.append((x,y,int(v)))
print('lichte buitenrand (x,y,idx):',rand)
print('losse pixels:',los)
print('kleuren:',sorted(set(g.ravel().tolist())))
