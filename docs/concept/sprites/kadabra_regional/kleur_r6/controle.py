# controle: kleuren, alpha-diff met het bevroren silhouet, open randen, losse o, clusters < 3 px
import sys,numpy as np, pal
from PIL import Image
R=pal.load(sys.argv[1] if len(sys.argv)>1 else 'raster.txt'); A=np.array([list(r) for r in R]); H,W=A.shape
KLEIN={(29,22),(30,22),(23,23)}   # oogwit mag klein
kl=set(A.flatten())-{'.'}; idx={pal.CH[c] for c in kl}
print('letters:',''.join(sorted(kl)),'-> kleuren',len(idx),'+ transparant')
def nb(y,x):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx; yield A[yy,xx] if 0<=yy<H and 0<=xx<W else '.'
print('open rand (o, d en k mogen aan de rand):',[(x,y,A[y,x]) for y in range(H) for x in range(W) if A[y,x] not in '.odk' and '.' in list(nb(y,x))])
def nb8(y,x):
    for dy in(-1,0,1):
        for dx in(-1,0,1):
            if dy or dx:
                yy,xx=y+dy,x+dx; yield A[yy,xx] if 0<=yy<H and 0<=xx<W else '.'
print('losse o (zonder o/d/k-buur):',[(x,y) for y in range(H) for x in range(W) if A[y,x]=='o' and not any(c in 'odk' for c in nb8(y,x))])
seen=np.zeros((H,W),bool); small=[]
for y in range(H):
  for x in range(W):
    if seen[y,x] or A[y,x] in '.odwtrs': continue   # d = lijn/selout, w = klauw/oogwit, rood = klaver
    c=A[y,x]; st=[(y,x)]; seen[y,x]=1; pts=[]
    while st:
      p=st.pop(); pts.append(p)
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        yy,xx=p[0]+dy,p[1]+dx
        if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and A[yy,xx]==c: seen[yy,xx]=1; st.append((yy,xx))
    if len(pts)<3 and not (c=='k' and all('.' in list(nb(q[0],q[1])) for q in pts)) and not all((q[1],q[0]) in KLEIN for q in pts): small.append((c,[(q[1],q[0]) for q in pts]))
print('clusters <3 px:',len(small))
for s in small: print('  ',s)
sil=np.asarray(Image.open('../silhouet/silhouet.png').convert('L'))>0; m=A!='.'
print('alpha-diff: erbij',[(x,y) for y,x in zip(*np.where(m&~sil))],'eraf',[(x,y) for y,x in zip(*np.where(sil&~m))])
ys,xs=np.where(m); print('box',xs.min(),xs.max(),ys.min(),ys.max(),'=',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'px',m.sum())
