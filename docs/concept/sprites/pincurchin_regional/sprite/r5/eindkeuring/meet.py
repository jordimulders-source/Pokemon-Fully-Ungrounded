# Meet: kleine tintclusters, randpixels (buitenomtrek) per index, zwart/donker-wissels op de rand
import sys
from PIL import Image
from collections import Counter
P='/home/user/Pokemon-Fully-Ungrounded/'+(sys.argv[1] if len(sys.argv)>1 else 'docs/concept/sprites/pincurchin_regional/sprite/r5/V1_oog4x5_mond+1+2.png')
im=Image.open(P); W,H=64,64; g=[[im.getpixel((x,y)) for x in range(W)] for y in range(H)]
seen=set(); small=[]
for y in range(H):
  for x in range(W):
    v=g[y][x]
    if v==0 or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
      a,b=st.pop(); comp.append((a,b))
      for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        c,d=a+dx,b+dy
        if 0<=c<W and 0<=d<H and (c,d) not in seen and g[d][c]==v: seen.add((c,d)); st.append((c,d))
    if len(comp)<3: small.append((v,comp))
print('clusters <3 px per index:',Counter(v for v,c in small))
for v,c in small: print(' idx',v,c)
# buitenrand
edge=Counter(); 
for y in range(H):
  for x in range(W):
    if g[y][x]==0: continue
    if any(g[y+dy][x+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<W and 0<=y+dy<H):
      edge[g[y][x]]+=1
print('buitenrand per index:',dict(edge))
