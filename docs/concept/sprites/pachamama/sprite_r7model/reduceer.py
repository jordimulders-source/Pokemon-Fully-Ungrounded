# natief (188x173) -> exacte 3x3-reductie. Elke spritepixel = meerderheid van zijn 3x3 modelpixels (niets getekend).
# Gebruik: python3 reduceer.py OY OX UIT
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
from collections import deque
OY,OX=int(sys.argv[1]),int(sys.argv[2]); UIT=sys.argv[3]
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); NH,NW=a.shape[:2]
L=lum(a)
wit=a.min(2)>=240; bg=np.zeros(wit.shape,bool); q=deque()
for y in range(NH):
  for x in range(NW):
    if (y in(0,NH-1) or x in(0,NW-1)) and wit[y,x]: bg[y,x]=1; q.append((y,x))
while q:
  y,x=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    yy,xx=y+dy,x+dx
    if 0<=yy<NH and 0<=xx<NW and wit[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
np.save('bg.npy',bg)
dk=(L<55)&~bg
near=nearest(a)
gr=a[...,1]-a[...,0]
grijs=gr<8; near[grijs&(near>=13)]=nearest(a[grijs&(near>=13)],range(2,13))
H=(NH-OY)//3; W=(NW-OX)//3; o=np.zeros((H,W),int); deel=np.zeros((H,W))
for j in range(H):
  for i in range(W):
    sl=(slice(OY+3*j,OY+3*j+3),slice(OX+3*i,OX+3*i+3))
    if bg[sl].sum()>=5: continue
    if dk[sl].sum()>=3: o[j,i]=1; continue
    v=near[sl][~bg[sl]&~dk[sl]]
    if len(v): bc=np.bincount(v,minlength=16); o[j,i]=bc.argmax(); deel[j,i]=bc.max()/len(v)
    else: o[j,i]=1
ys,xs=np.where(o>0); Y0,X0=ys.min(),xs.min(); o=o[Y0:ys.max()+1,X0:xs.max()+1]; deel=deel[Y0:ys.max()+1,X0:xs.max()+1]; h,w=o.shape
full=np.zeros((64,64),int); x0=(64-w)//2; y0=63-h; full[y0:63,x0:x0+w]=o
np.save(UIT.replace('.png','.npy'),full)
# koppeling sprite <-> natief: spritepixel (sy,sx) = natief rijen OY+3*(sy-y0+Y0).. kolommen OX+3*(sx-x0+X0)..
np.save(UIT.replace('.png','_map.npy'),np.array([OY+3*Y0-3*y0, OX+3*X0-3*x0]))
m=full>0; pd=np.pad(m,1); rand=m&~(pd[:-2,1:-1]&pd[2:,1:-1]&pd[1:-1,:-2]&pd[1:-1,2:])
sys.stderr.write('OY%d OX%d rand %d/%d omlijnd; %dx%d\n'%(OY,OX,(full[rand]==1).sum(),rand.sum(),w,h))
p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save(UIT,transparency=0)
