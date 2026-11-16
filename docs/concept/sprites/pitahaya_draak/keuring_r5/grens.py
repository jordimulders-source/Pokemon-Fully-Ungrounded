import sys; from PIL import Image; import numpy as np
from collections import Counter
for f in sys.argv[1:]:
    im=Image.open(f); im=im if im.mode=='P' else im.convert('P')
    a=np.array(im)[:64,:64]; P=np.array(im.getpalette()[:768]).reshape(-1,3).astype(int); L=(P*[.299,.587,.114]).sum(1)
    tot=0; zw=0; c=Counter()
    for y in range(63):
        for x in range(63):
            for yy,xx in((y+1,x),(y,x+1)):
                p,q=a[y,x],a[yy,xx]
                if p and q and p!=q:
                    tot+=1
                    d=np.sqrt(((P[p]-P[q])**2).sum())
                    if d<60: zw+=1; c[tuple(sorted((int(p),int(q))))]+=1
    print(f.split('/')[-2] if 'graphics' in f else f.split('/')[-1], 'tintgrenzen',tot,'zwak (RGB-afstand<60) %.1f%%'%(100*zw/tot), c.most_common(5) if 'pitahaya' in f else '')
    if 'pitahaya' in f:
        for (p,q),n in c.most_common(6): print('  ',p,tuple(P[p]),q,tuple(P[q]),'afstand %.0f'%np.sqrt(((P[p]-P[q])**2).sum()),'dL %.0f'%abs(L[p]-L[q]))
