# controle.py sprite.png : (1) kleuren, (2) silhouetverschil met het model (alpha>=0.45) buiten de toegestane zones,
# (3) kleine tintvlakjes (<3 px, 4-buren) per index, (4) losse omlijningspixels (index 1) zonder contact met rand of andere lijn,
# (5) randpixels van het silhouet die geen donkere rand zijn.
import sys,json,numpy as np; from PIL import Image; from collections import deque
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
a=np.asarray(Image.open(sys.argv[1])); dy=int(sys.argv[2]) if len(sys.argv)>2 else 0
print('kleuren gebruikt:',len(np.unique(a)),'(incl. transparant)')
c=np.asarray(Image.open(G+k['model'])).astype(float); H,W=c.shape[:2]
A=np.zeros((64,64))
for y in range(64):
  for x in range(64):
    ya,yb=max(int(Y0+y*s),0),min(int(Y0+(y+1)*s),H); xa,xb=max(int(X0+x*s),0),min(int(X0+(x+1)*s),W)
    if ya<yb and xa<xb: A[y,x]=(c[ya:yb,xa:xb,3]>0).mean()
m=A>=0.45; sp=a>0
zone=np.zeros((64,64),bool); zone[41:64,26:38]=True   # steunarm: koordband, polsband, ronde hand (toegestaan)
d=(m!=sp)&~zone
print('silhouetverschil buiten toegestane zone:',d.sum(),'px  (sprite extra:',(sp&~m&~zone).sum(),', sprite mist:',(m&~sp&~zone).sum(),')')
for y,x in zip(*np.where(d)): print('   ',(x,y),'sprite' if sp[y,x] else 'model', 'alpha',round(A[y,x],2))
# kleine vlakjes
seen=np.zeros((64,64),bool); klein=[]
for y in range(64):
  for x in range(64):
    if a[y,x]==0 or seen[y,x]: continue
    v=a[y,x]; q=deque([(y,x)]); seen[y,x]=1; pts=[(y,x)]
    while q:
      yy,xx=q.popleft()
      for ddy,ddx in ((1,0),(-1,0),(0,1),(0,-1)):
        Y,Xx=yy+ddy,xx+ddx
        if 0<=Y<64 and 0<=Xx<64 and not seen[Y,Xx] and a[Y,Xx]==v: seen[Y,Xx]=1; q.append((Y,Xx)); pts.append((Y,Xx))
    if len(pts)<3 and v not in (1,): klein.append((v,[(p[1],p[0]) for p in pts]))
print('vlakjes < 3 px (index, pixels):',len(klein))
for v,p in klein: print('   ',v,p)
# losse omlijning
los=[]
for y in range(64):
  for x in range(64):
    if a[y,x]!=1: continue
    nb=[a[y+dy2,x+dx] if 0<=y+dy2<64 and 0<=x+dx<64 else 0 for dy2 in (-1,0,1) for dx in (-1,0,1) if (dy2,dx)!=(0,0)]
    if 0 not in nb and sum(1 for n in nb if n==1)==0: los.append((x,y))
print('losse omlijningspixels midden in een vlak:',los)
# rand
rand=[]
for y in range(64):
  for x in range(64):
    if a[y,x]==0: continue
    if any((a[y+dy2,x+dx]==0 if 0<=y+dy2<64 and 0<=x+dx<64 else True) for dy2,dx in ((1,0),(-1,0),(0,1),(0,-1))):
      if a[y,x] not in (1,5,13,15): rand.append((x,y,'.123456789ABCDEF'[a[y,x]]))
print('randpixels zonder donkere rand:',len(rand)); print('   ',rand)
