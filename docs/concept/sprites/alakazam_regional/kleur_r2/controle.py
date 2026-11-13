# controle: kleuren, open randen (lichte pixel naast transparant), losse omlijningspixels, tintvlakjes <3 px, alpha-diff met silhouet
import numpy as np
from PIL import Image
R=[l.ljust(64,'.')[:64] for l in open('raster.txt').read().split('\n')[:64]]
A=np.array([list(r) for r in R])
print('kleuren:',sorted(set(A.flatten())), len(set(A.flatten())))
H,W=A.shape
def nb(y,x):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        yield A[yy,xx] if 0<=yy<H and 0<=xx<W else '.'
rand=[(x,y,A[y,x]) for y in range(H) for x in range(W) if A[y,x] not in '.od' and '.' in list(nb(y,x))]
print('open rand (geen o/d naast transparant):',rand)
los=[(x,y) for y in range(H) for x in range(W) if A[y,x]=='o' and '.' not in list(nb(y,x)) and sum(c=='o' for c in nb(y,x))==0]
print('losse o zonder o-buur en niet aan rand:',los)
# clusters
seen=np.zeros((H,W),bool); small=[]
for y in range(H):
  for x in range(W):
    if seen[y,x] or A[y,x] in '.o': continue
    c=A[y,x]; st=[(y,x)]; seen[y,x]=1; pts=[]
    while st:
      p=st.pop(); pts.append(p)
      for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=p[0]+dy,p[1]+dx
        if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and A[yy,xx]==c: seen[yy,xx]=1; st.append((yy,xx))
    if len(pts)<3: small.append((c,[(q[1],q[0]) for q in pts]))
print('vlakjes <3 px:',len(small)); print(small)
sil=np.asarray(Image.open('../silhouet/silhouet.png'))[...,3]>0
m=A!='.'
print('alpha-diff met silhouet: erbij',[(x,y) for y,x in zip(*np.where(m&~sil))],'eraf',[(x,y) for y,x in zip(*np.where(sil&~m))])
