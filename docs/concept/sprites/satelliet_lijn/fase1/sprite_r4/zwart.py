# zwart.py: 2x2 zwart, L-hoeken zwart, K-D-K op een rij/kolom, open randen, losse vultintpixels (8-buren)
import numpy as np, sys
from collections import deque
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'sprite.npy'); K=o==1
b22=[(y,x) for y in range(63) for x in range(63) if K[y:y+2,x:x+2].all()]
L=[]
for y in range(1,63):
    for x in range(1,63):
        if not K[y,x]: continue
        for dy,dx in ((1,1),(1,-1),(-1,1),(-1,-1)):
            if K[y+dy,x] and K[y,x+dx] and not K[y+dy,x+dx]: L.append((y,x))
kdk=[(y,x) for y in range(64) for x in range(1,63) if o[y,x]==2 and K[y,x-1] and K[y,x+1]]+[(y,x) for y in range(1,63) for x in range(64) if o[y,x]==2 and K[y-1,x] and K[y+1,x]]
pad=np.pad(o,1); opn=[(y,x) for y in range(64) for x in range(64) if o[y,x] in (3,4,5,6,7,8,9,10) and 0 in (pad[y,x+1],pad[y+2,x+1],pad[y+1,x],pad[y+1,x+2])]
def small(o):
  res=[]
  for i in (5,6,7,8,9,10):
    seen=np.zeros(o.shape,bool)
    for y,x in zip(*np.where(o==i)):
      if seen[y,x]: continue
      q=deque([(y,x)]); seen[y,x]=1; c=[]
      while q:
        a,b=q.popleft(); c.append((int(a),int(b)))
        for dy in (-1,0,1):
          for dx in (-1,0,1):
            u,v=a+dy,b+dx
            if 0<=u<64 and 0<=v<64 and o[u,v]==i and not seen[u,v]: seen[u,v]=1; q.append((u,v))
      if len(c)<3: res.append(('.#DPpWwlmTt'[i],c))
  return res
print('px',int((o>0).sum()),'zwart',int(K.sum()))
print('2x2 zwart',b22); print('L-hoek (middenpixel)',sorted(set(L))); print('K-D-K',kdk); print('open rand',opn); print('losse vultint',small(o))
