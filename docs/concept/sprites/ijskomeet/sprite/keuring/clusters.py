# tintvlakjes < 3 px (4-buren) per kleur, en dambord (2x2 om en om)
import numpy as np
t=open('../r1.txt').read().split()[:64]; g=np.array([list(r) for r in t])
H,W=g.shape; seen=np.zeros_like(g,bool); kl=[]
for y in range(H):
  for x in range(W):
    if g[y,x]=='.' or seen[y,x]: continue
    st=[(y,x)]; seen[y,x]=1; c=[]
    while st:
      a,b=st.pop(); c.append((b,a))
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        q,r=a+dy,b+dx
        if 0<=q<H and 0<=r<W and not seen[q,r] and g[q,r]==g[y,x]: seen[q,r]=1; st.append((q,r))
    if len(c)<3: kl.append((g[y,x],c))
from collections import Counter
print('vlakjes<3px:',len(kl),Counter(k for k,_ in kl))
for k,c in kl: print(k,c)
d=0
for y in range(H-1):
  for x in range(W-1):
    a,b,c2,e=g[y,x],g[y,x+1],g[y+1,x],g[y+1,x+1]
    if '.' not in (a,b) and a==e and b==c2 and a!=b: d+=1
print('dambord 2x2:',d)
