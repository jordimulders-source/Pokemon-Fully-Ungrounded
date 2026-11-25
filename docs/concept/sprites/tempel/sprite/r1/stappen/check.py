# check.py raster.txt: kleuren, kleine tintclusters (<3 px), dikke lijnklonten (2x2 lijn), losse lijnpixels
import sys, numpy as np
C='.X+abcdemnopz'
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]; G=np.array([[C.index(ch) for ch in r] for r in R])
print('kleuren gebruikt:',sorted(set(G.ravel())),'aantal (incl transp):',len(set(G.ravel())))
seen=np.zeros_like(G,bool); small=[]
for y in range(64):
  for x in range(64):
    if G[y,x]>=3 and G[y,x] not in (10,11,12) and not seen[y,x]:
      q=[(y,x)]; seen[y,x]=1; comp=[]
      while q:
        p=q.pop(); comp.append(p)
        for yy,xx in ((p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)):
          if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and G[yy,xx]==G[y,x]: seen[yy,xx]=1; q.append((yy,xx))
      if len(comp)<3: small.append((C[G[y,x]],[(b,a) for a,b in comp]))
print('kleine clusters:',len(small)); print(small)
ln=(G==2)
blk=[(x,y) for y in range(63) for x in range(63) if ln[y,x] and ln[y+1,x] and ln[y,x+1] and ln[y+1,x+1]]
print('2x2 lijnklonten:',blk)
P=np.pad((G==1)|(G==2),1)
lone=[(x,y) for y in range(64) for x in range(64) if G[y,x]==2 and P[y:y+3,x:x+3].sum()==1]
print('losse lijnpixels:',lone)
