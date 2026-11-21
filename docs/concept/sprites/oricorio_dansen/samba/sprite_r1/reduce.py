# natief (km_lab) -> 2x2-blokreductie met regels. Elke spritepixel komt uit zijn eigen 2x2-blok modelpixels (niets getekend).
# Gebruik: python3 reduce.py OY OX  -> kaal_OYOX.npy
import sys, numpy as np
from collections import Counter
from palet import KM, I
lab=np.load('km_lab.npy'); H,W=lab.shape
cl=np.zeros(lab.shape,int)
for k,v in KM.items(): cl[lab==k]=I[v]
OY,OX=int(sys.argv[1]),int(sys.argv[2]); MODE=sys.argv[3] if len(sys.argv)>3 else 'd1'
h,w=(H-OY)//2,(W-OX)//2; o=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        b=cl[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2].ravel()
        nbg=(b==0).sum(); nd=(b==I['O']).sum()
        if nbg>=3: continue
        if nd>=2 or (nd>=1 and (nbg>=1 or MODE!='d2')): o[j,i]=I['O']; continue
        if MODE=='d1g6' and (b==I['G6']).sum()>=1: o[j,i]=I['G6']; continue
        f=[v for v in b if v not in (0,I['O'])]
        c=Counter(f).most_common()
        if len(c)>1 and c[0][1]==c[1][1]:   # gelijkspel: de donkerste (hogere index binnen de groene reeks) wint niet automatisch; neem de eerste in het blok
            o[j,i]=c[0][0]
        else: o[j,i]=c[0][0]
np.save('kaal_%d%d_%s.npy'%(OY,OX,MODE),o)
ys,xs=np.where(o>0); print(OY,OX,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(o>0).sum())
