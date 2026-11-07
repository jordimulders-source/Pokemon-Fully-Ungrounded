# controle.py raster : losse pixels/kleine vlakjes (8-verbonden clusters < 3 px per kleur) + kleurtelling + silhouet
import sys
from tl import *
R=raster(sys.argv[1]); H=64
seen=set(); small=[]
for y in range(H):
  for x in range(64):
    c=R[y][x]
    if c=='.' or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
      a,b=st.pop(); comp.append((a,b))
      for dy in (-1,0,1):
        for dx in (-1,0,1):
          aa,bb=a+dx,b+dy
          if 0<=aa<64 and 0<=bb<H and (aa,bb) not in seen and R[bb][aa]==c: seen.add((aa,bb)); st.append((aa,bb))
    if len(comp)<3: small.append((c,comp))
for c,comp in sorted(small): print(c,comp)
m=np.array([[ch!='.' for ch in r] for r in R])
print('px',m.sum(),'silhouet-diff',int((m!=SIL).sum()))
from collections import Counter; print(sorted(Counter(ch for r in R for ch in r if ch!='.').items()))
