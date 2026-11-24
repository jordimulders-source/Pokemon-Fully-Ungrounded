# Herbelichting (alleen tintwissel, silhouet blijft): gekleurde selout aan de lichtkant (boven/linksboven) van het witte lijf:
# omlijningspixel met transparant erboven/links en wit lijf (2/3) eronder/rechts -> lavendelschaduw 5.
import numpy as np, sys
from cfg import oudrij, TOP
JMAX=oudrij(17)
o=np.load(sys.argv[1]).copy(); H,W=o.shape; ch=[]
for j in range(H):
    for i in range(W):
        if o[j,i]!=1: continue
        boven=(j==0 or o[j-1,i]==0); links=(i==0 or o[j,i-1]==0)
        onder=j+1<H and o[j+1,i] in (2,3); rechts=i+1<W and o[j,i+1] in (2,3)
        if j<JMAX and ((boven and onder) or (links and rechts)): o[j,i]=5; ch.append((i,j+TOP))
np.save(sys.argv[2],o); print('selout ->5 (x,y volle 64):',ch)
