# r9 DC-eindkeuring: analyse op een sprite (randen, zwarte binnenlijnen naast groen, kleine tintvlekjes)
import sys,numpy as np
from PIL import Image
def label(m):
  lab=np.zeros(m.shape,int);n=0
  for y in range(64):
    for x in range(64):
      if m[y,x] and not lab[y,x]:
        n+=1;st=[(y,x)];lab[y,x]=n
        while st:
          p,q=st.pop()
          for i,j in ((-1,0),(1,0),(0,-1),(0,1)):
            r,c=p+i,q+j
            if 0<=r<64 and 0<=c<64 and m[r,c] and not lab[r,c]: lab[r,c]=n;st.append((r,c))
  return lab,n
a=np.array(Image.open(sys.argv[1])); ch='.KDMLolgbBxRW'
G=lambda v:'L' if v in(2,3,4) else 'G' if v in(5,6,7) else 'B' if v in(8,9) else 'R' if v in(10,11) else 'K' if v==1 else None
def tr(y,x): return y<0 or x<0 or y>63 or x>63 or a[y,x]==0
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(i,j) for i in(-1,0,1) for j in(-1,0,1) if (i,j)!=(0,0)]
print('-- randpixels in lichte tint (niet K, niet donkerste groepstint):')
for y in range(64):
  for x in range(64):
    v=a[y,x]
    if v and any(tr(y+i,x+j) for i,j in N4) and v not in(1,2,5,8,10):
      ny=sum(i for i,j in N8 if tr(y+i,x+j)); nx=sum(j for i,j in N8 if tr(y+i,x+j))
      print(' ',y,x,ch[v],'licht' if nx+ny<0 or (nx+ny==0 and ny<0) else 'schaduw')
print('-- K binnen (geen transparante 4-buur) met groene buur:')
for y in range(64):
  for x in range(64):
    if a[y,x]==1 and not any(tr(y+i,x+j) for i,j in N4):
      b=[ch[a[y+i,x+j]] for i,j in N4]
      if any(c in 'olg' for c in b): print(' ',y,x,''.join(b))
print('-- clusters < 3 px (per index, 4-samenhang, niet K):')
for v in range(2,12):
  lab,n=label(a==v)
  for k in range(1,n+1):
    s=np.argwhere(lab==k)
    if len(s)<3: print(' ',ch[v],[tuple(p) for p in s])
