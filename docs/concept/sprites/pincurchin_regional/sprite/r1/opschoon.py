# technisch opschonen van kaal.npy -> schoon.npy (geen vormen tekenen):
# 1. buitenrand: lichtkant (alleen links/boven open) -> gekleurde selout (rood r / bruin D), anders zwart K
# 2. vultintvlakjes < 3 px -> grootste buurtint binnen dezelfde kleurgroep
import numpy as np
from scipy import ndimage
o=np.load('kaal.npy').copy(); H,W=o.shape
K,D,S,M,Lb,r,R,L=range(8)
RED={r,R,L}; BRN={D,S,M,Lb}
def op(y,x): return 0<=y<H and 0<=x<W and o[y,x]>=0
orig=o.copy()
for y in range(H):
    for x in range(W):
        v=orig[y,x]
        if v<0: continue
        lft=not op(y,x-1); top=not op(y-1,x); rgt=not op(y,x+1); bot=not op(y+1,x)
        if not(lft or top or rgt or bot): continue
        if rgt or bot:
            o[y,x]=K; continue
        if v==K:
            # zwarte modellijn aan de lichtkant -> selout van de groep ernaast
            nb=[orig[yy,xx] for yy,xx in ((y,x+1),(y+1,x),(y,x-1),(y-1,x)) if op(yy,xx) and orig[yy,xx]!=K]
            if not nb: continue
            o[y,x]=r if sum(n in RED for n in nb)>=sum(n in BRN for n in nb) else D
        else: o[y,x]=r if v in RED else D
# vlakjes
for grp in ([S,M,Lb],[R,L]):
    for it in range(3):
        for t in grp:
            lab,n=ndimage.label(o==t)
            for k in range(1,n+1):
                z=lab==k
                if z.sum()>=3: continue
                rand=ndimage.binary_dilation(z)&~z
                buren=[v for v in o[rand] if v in grp and v!=t]
                if buren: o[z]=max(set(buren),key=buren.count)
# zwarte binnenlijn in het bruin (geen rood ernaast, niet op de buitenrand) -> donkerbruine lijn (Gen 3: binnenlijn in de donkerste vlaktint)
o2=o.copy()
for y in range(1,H-1):
    for x in range(1,W-1):
        if o[y,x]!=K: continue
        if any(not op(y+dy,x+dx) for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))): continue
        if any(o[y+dy,x+dx] in RED for dy in (-1,0,1) for dx in (-1,0,1)): continue
        o2[y,x]=D
o=o2
# benoemde reparaties naar het model (rij,kolom)
REP={(24,41):K,(44,43):Lb,(46,36):Lb,(46,37):Lb,(22,25):D,(22,26):D,(22,27):r}
for x in range(30,35): REP[(47,x)]=Lb
for (y,x),v in REP.items(): o[y,x]=v
np.save('schoon.npy',o)
