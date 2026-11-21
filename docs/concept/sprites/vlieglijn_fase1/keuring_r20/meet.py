import sys
from PIL import Image
from collections import Counter
f=sys.argv[1]
im=Image.open(f); px=im.load(); W,H=im.size
H8='0123456789ABCDEF'
print('    '+''.join(str(x//10) for x in range(6,56)))
print('    '+''.join(str(x%10) for x in range(6,56)))
for y in range(16,62): print('%2d  '%y+''.join('.' if px[x,y]==0 else H8[px[x,y]] for x in range(6,56)))
print('count',sorted(Counter(px[x,y] for x in range(W) for y in range(H) if px[x,y]).items()))
# rand
edge=Counter(); bad=[]
for y in range(H):
  for x in range(W):
    c=px[x,y]
    if not c: continue
    if any(not(0<=x+dx<W and 0<=y+dy<H) or px[x+dx,y+dy]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
      edge[c]+=1
      if c not in (1,2,8,9,15,12,3): bad.append((x,y,H8[c]))
print('randindex',sorted(edge.items())); print('lichte randpixels',bad)
# kleine clusters per index (4-buur)
seen=set(); small=[]
for y in range(H):
  for x in range(W):
    c=px[x,y]
    if not c or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
      a,b=st.pop(); comp.append((a,b))
      for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        n=(a+dx,b+dy)
        if 0<=n[0]<W and 0<=n[1]<H and n not in seen and px[n]==c: seen.add(n); st.append(n)
    if len(comp)<3: small.append((H8[c],comp))
print('clusters<3:',len(small))
for s in small: print(' ',s)
# losse zwarte pixels binnen vlak: index1 met 4 niet-1 niet-0 buren
lone=[(x,y) for y in range(1,H-1) for x in range(1,W-1) if px[x,y]==1 and all(px[x+dx,y+dy] not in (0,1) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('losse zwarte pixels in vlak',lone)
