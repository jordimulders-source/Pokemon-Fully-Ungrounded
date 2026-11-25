import sys
from PIL import Image
import numpy as np
a=np.array(Image.open(sys.argv[1]).convert('RGBA')).astype(int)
H,W=64,64
cols=sorted({tuple(c[:3]) for c in a.reshape(-1,4) if c[3]},key=lambda c:sum(c))
L='0123456789ABCDEF'
idx=np.full((H,W),-1)
for y in range(H):
  for x in range(W):
    if a[y,x,3]: idx[y,x]=cols.index(tuple(a[y,x,:3]))
seen=np.zeros((H,W),bool); small=[]
for y in range(H):
  for x in range(W):
    if idx[y,x]<0 or seen[y,x]: continue
    st=[(x,y)];seen[y,x]=True;comp=[]
    while st:
      cx,cy=st.pop();comp.append((cx,cy))
      for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny=cx+dx,cy+dy
        if 0<=nx<W and 0<=ny<H and not seen[ny,nx] and idx[ny,nx]==idx[y,x]:
          seen[ny,nx]=True;st.append((nx,ny))
    if len(comp)<3: small.append((L[idx[y,x]],comp))
print('kleine vlakjes (<3px):')
for s in small: print(' ',s)
# dambord 2x2
print('dambord:')
for y in range(H-1):
  for x in range(W-1):
    p=idx[y,x];q=idx[y,x+1];r=idx[y+1,x];s=idx[y+1,x+1]
    if min(p,q,r,s)>=0 and p==s and q==r and p!=q: print(' ',(x,y),L[p],L[q])
