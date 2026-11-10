# controle: kleuren, alpha-diff met silhouet, open randen (lichte kleur naast transparant), losse o, clusters <3 px
import sys,numpy as np, pal
R=pal.load(sys.argv[1] if len(sys.argv)>1 else 'raster.txt'); A=np.array([list(r) for r in R]); H,W=A.shape
GLANS={(33,16),(33,17),(35,17),(40,18)}   # oogwit/glans mag klein
print('kleuren:',''.join(sorted(set(A.flatten())-{'.'})),len(set(A.flatten())-{'.'}),'+ transparant')
def nb(y,x):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx; yield A[yy,xx] if 0<=yy<H and 0<=xx<W else '.'
rand=[(x,y,A[y,x]) for y in range(H) for x in range(W) if A[y,x] not in '.od' and '.' in list(nb(y,x))]
print('open rand:',rand)
def nb8(y,x):
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            if dy or dx:
                yy,xx=y+dy,x+dx; yield A[yy,xx] if 0<=yy<H and 0<=xx<W else '.'
los=[(x,y) for y in range(H) for x in range(W) if A[y,x]=='o' and '.' not in list(nb(y,x)) and not any(c=='o' for c in nb8(y,x))]
print('losse o:',los)
seen=np.zeros((H,W),bool); small=[]
for y in range(H):
  for x in range(W):
    if seen[y,x] or A[y,x] in '.o': continue
    c=A[y,x]; st=[(y,x)]; seen[y,x]=1; pts=[]
    while st:
      p=st.pop(); pts.append(p)
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        yy,xx=p[0]+dy,p[1]+dx
        if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and A[yy,xx]==c: seen[yy,xx]=1; st.append((yy,xx))
    if len(pts)<3 and not all((q[1],q[0]) in GLANS for q in pts): small.append((c,[(q[1],q[0]) for q in pts]))
print('clusters <3 px:',len(small)); 
for s in small: print('  ',s)
sil=np.load('meet5.npz')['sil']; m=A!='.'
print('alpha-diff: erbij',[(x,y) for y,x in zip(*np.where(m&~sil))],'eraf',[(x,y) for y,x in zip(*np.where(sil&~m))])
