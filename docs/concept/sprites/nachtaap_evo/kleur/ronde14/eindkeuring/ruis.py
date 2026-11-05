# dambord (2x2 a b / b a) en 1-px harken (a b a b a op een rij) (alleen lezen)
import numpy as np, sys
from PIL import Image
a=np.array(Image.open(sys.argv[1]))[:64]
H,W=a.shape; d=[]; h=[]
for y in range(H-1):
  for x in range(W-1):
    p,q,r,s=a[y,x],a[y,x+1],a[y+1,x],a[y+1,x+1]
    if 0 not in (p,q,r,s) and p==s and q==r and p!=q: d.append((x,y,int(p),int(q)))
for y in range(H):
  for x in range(W-4):
    v=a[y,x:x+5]
    if 0 not in v and v[0]==v[2]==v[4] and v[1]==v[3] and v[0]!=v[1]: h.append(('h',x,y,list(map(int,v))))
for x in range(W):
  for y in range(H-4):
    v=a[y:y+5,x]
    if 0 not in v and v[0]==v[2]==v[4] and v[1]==v[3] and v[0]!=v[1]: h.append(('v',x,y,list(map(int,v))))
print('dambord 2x2:',len(d),d); print('harken 5px:',len(h),h)
