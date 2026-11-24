# Kleine tintvlakjes (<3 px, 4-buren) per index in de te keuren sprite
import sys
from PIL import Image
im=Image.open(sys.argv[1]); px=im.load(); W,H=im.size
seen=set()
for y in range(H):
  for x in range(W):
    i=px[x,y]
    if i in (0,1) or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
      a,b=st.pop(); comp.append((a,b))
      for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(a+dx,b+dy)
        if 0<=n[0]<W and 0<=n[1]<H and n not in seen and px[n]==i: seen.add(n); st.append(n)
    if len(comp)<3: print(i,comp)
