# python3 clusters.py raster : tintvlakjes < 3 px (4-samenhang), zonder lijnen/ogen
import sys; from lib import *
R=lees(sys.argv[1]); seen=set(); res=[]
for y in range(64):
  for x in range(64):
    c=R[y][x]
    if c in '.KnYWPD' or (x,y) in seen: continue
    st=[(x,y)]; comp=[]
    while st:
      a,b=st.pop()
      if (a,b) in seen or not(0<=a<64 and 0<=b<64) or R[b][a]!=c: continue
      seen.add((a,b)); comp.append((a,b)); st+=[(a+1,b),(a-1,b),(a,b+1),(a,b-1)]
    if len(comp)<3: res.append((c,comp))
print(len(res))
for c,comp in res: print(c,comp)
