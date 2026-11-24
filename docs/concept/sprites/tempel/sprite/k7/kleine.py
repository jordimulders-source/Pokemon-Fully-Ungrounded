import sys,numpy as np; sys.path.insert(0,'../k5')
from clusters import tel
from PIL import Image
p=sys.argv[1]
_,l0=tel('../k6/tempel.png',0); _,l1=tel(p,0)
s0={(c,tuple(sorted(cp))) for c,cp in l0}
for c,cp in l1:
    if (c,tuple(sorted(cp))) not in s0: print('nieuw', c, sorted(cp))
s1={(c,tuple(sorted(cp))) for c,cp in l1}
print('verdwenen', sum(1 for k in s0 if k not in s1))
