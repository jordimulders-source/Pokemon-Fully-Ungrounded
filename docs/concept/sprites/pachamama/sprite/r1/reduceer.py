# natief (199x199) -> exacte 3x3-reductie. Niets getekend: elke spritepixel = meerderheid van zijn 3x3 modelpixels.
# Gebruik: python3 reduceer.py OY OX UIT
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
OY,OX=int(sys.argv[1]),int(sys.argv[2]); UIT=sys.argv[3]
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float)
L=lum(a)
# achtergrond = vrijwel wit en vanaf de rand bereikbaar (sneeuw f0fbfe is omsloten door omlijning)
from collections import deque
wit=a.min(2)>=246; bg=np.zeros(wit.shape,bool); q=deque()
for y in range(199):
  for x in (0,198):
    if wit[y,x]: bg[y,x]=1; q.append((y,x))
for x in range(199):
  for y in (0,198):
    if wit[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
while q:
  y,x=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    yy,xx=y+dy,x+dx
    if 0<=yy<199 and 0<=xx<199 and wit[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
dk=(L<55)&~bg
near=nearest(a)
gr=a[...,1]-a[...,0]
grijs=gr<8; near[grijs&(near>=13)]=nearest(a[grijs&(near>=13)],range(2,13))                      # per modelpixel dichtstbijzijnde paletkleur
H=(199-OY)//3; W=(199-OX)//3; o=np.zeros((H,W),int); deel=np.zeros((H,W)); ndk=np.zeros((H,W),int)
for j in range(H):
  for i in range(W):
    sl=(slice(OY+3*j,OY+3*j+3),slice(OX+3*i,OX+3*i+3))
    if bg[sl].sum()>=5: continue
    nd=dk[sl].sum(); ndk[j,i]=nd
    if nd>=3: o[j,i]=1; continue
    v=near[sl][~bg[sl]&~dk[sl]]
    if len(v): bc=np.bincount(v,minlength=16); o[j,i]=bc.argmax(); deel[j,i]=bc.max()/len(v)
    else: o[j,i]=1
ys,xs=np.where(o>0); Y0,X0=ys.min(),xs.min(); o=o[Y0:ys.max()+1,X0:xs.max()+1]; deel=deel[Y0:ys.max()+1,X0:xs.max()+1]; h,w=o.shape
full=np.zeros((64,64),int); x0=(64-w)//2; full[63-h:63,x0:x0+w]=o
np.save(UIT.replace('.png','.npy'),full)
dl=np.zeros((64,64)); dl[63-h:63,x0:x0+w]=deel; np.save(UIT.replace('.png','_deel.npy'),dl)
# rand-score: hoeveel buitenrandpixels al omlijning zijn
m=full>0; pd=np.pad(m,1); rand=m&~(pd[:-2,1:-1]&pd[2:,1:-1]&pd[1:-1,:-2]&pd[1:-1,2:])
open('/dev/stderr','w').write('rand %d van %d omlijnd; oorsprong natief y=%d x=%d -> sprite y=%d x=%d\n'%((full[rand]==1).sum(),rand.sum(),OY+3*Y0,OX+3*X0,63-h,x0))
p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save(UIT,transparency=0)
print(UIT,w,h,'px',(full>0).sum(),'zwart',(full==1).sum())
