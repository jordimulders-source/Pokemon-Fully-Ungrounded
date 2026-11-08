# losse-pixelscan: tintclusters < 3 px, en omlijning (1) zonder contact met rand/andere lijn
import sys,numpy as np
g=[l.rstrip('\n') for l in open(sys.argv[1])]
a=np.array([[c for c in r] for r in g])
H,W=a.shape
seen=np.zeros(a.shape,bool)
for y in range(H):
  for x in range(W):
    if a[y,x]=='.' or seen[y,x]: continue
    st=[(y,x)]; seen[y,x]=1; comp=[]
    while st:
        cy,cx=st.pop(); comp.append((cy,cx))
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=cy+dy,cx+dx
            if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==a[y,x]: seen[yy,xx]=1; st.append((yy,xx))
    if len(comp)<3: print('cluster',a[y,x],len(comp),[(cx,cy) for cy,cx in comp])
for y in range(H):
  for x in range(W):
    if a[y,x]=='1':
      nb=[a[y+dy,x+dx] if 0<=y+dy<H and 0<=x+dx<W else '.' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))]
      if '.' not in nb and nb[:4].count('1')+nb[:4].count('2')==0: print('losse 1 in vlak',(x,y))
