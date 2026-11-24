import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
import k7b
a0,pal=laad('../k6/tempel.png'); H,W=a0.shape; k7b.a0=a0
a=np.load('auto.npy')
STAP=[3,4,5,6,15]   # toonladder licht->donker
idx={c:i for i,c in enumerate(STAP)}
# gezichtsveld ongemoeid
a[37:44,13:30]=a0[37:44,13:30]
# vlakbasis = meest voorkomende steentint in 7x7 rond de pixel (k6)
for y in range(H):
    for x in range(W):
        if a[y,x]==a0[y,x]: continue
        blok=a0[max(0,y-3):y+4,max(0,x-3):x+4].ravel()
        blok=[c for c in blok if c in idx]
        base=np.bincount(blok,minlength=16).argmax()
        if abs(idx[a[y,x]]-idx[base])>1: a[y,x]=a0[y,x]
a=k7b.filt(a)
np.save('stap2.npy',a)
