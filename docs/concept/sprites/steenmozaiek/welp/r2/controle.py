# Controle: kleine clusters (<3 px, 4-buren) per index, losse omlijningspixels in het binnenste, kleurenaantal.
import sys,numpy as np
from palet import CH
rows=[l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
g=np.array([[CH.index(c) for c in r] for r in rows])
H,W=g.shape; seen=np.zeros_like(g,bool); small=[]
for y in range(H):
  for x in range(W):
    if g[y,x]==0 or seen[y,x]: continue
    v=g[y,x]; st=[(y,x)]; seen[y,x]=1; comp=[]
    while st:
      cy,cx=st.pop(); comp.append((cx,cy))
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=cy+dy,cx+dx
        if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and g[ny,nx]==v: seen[ny,nx]=1; st.append((ny,nx))
    if len(comp)<3 and v not in (1,): small.append((CH[v],comp))
print('kleine clusters (<3 px):',len(small))
for v,c in small: print(' ',v,c)
m=g>0; p=np.pad(m,1); inner=m&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
lone=[(x,y) for y,x in zip(*np.where(inner&(g==1))) if sum(g[y+dy,x+dx]==1 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))==0]
print('losse zwarte pixels binnenin:',lone)
print('indexen gebruikt:',sorted(set(CH[v] for v in g.ravel())), 'aantal incl. transparant', len(set(g.ravel())))
