# Gezicht per spritepixel uit het model gemeten (mediaan-helderheid per 3x3-blok -> 3 gezichtstinten; modellijnen -> 2,
# lijnen tegen de kap -> 1). Ogen: per modelpixel uitgelezen (zie verslag), niet uit een andere sprite.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); L=lum(a)
o=np.load('stap3.npy'); oud=o.copy()
Y0,Y1,X0,X1=13,29,22,37
med=np.zeros((64,64)); nd=np.zeros((64,64),int)
for sy in range(Y0,Y1):
  for sx in range(X0,X1):
    b=L[3*sy-9:3*sy-6,3*sx+3:3*sx+6]; med[sy,sx]=np.median(b); nd[sy,sx]=(b<70).sum()
gez=np.zeros((64,64),bool)
for sy in range(Y0,Y1):
  for sx in range(X0,X1):
    gez[sy,sx]= med[sy,sx]<200 and o[sy,sx]!=0
# alleen het samenhangende stuk rond het midden van het gezicht (niet de kapschaduw rechts)
from collections import deque
seen=np.zeros_like(gez); q=deque([(21,28)]); seen[21,28]=1
while q:
  y,x=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    yy,xx=y+dy,x+dx
    if Y0<=yy<Y1 and X0<=xx<X1 and gez[yy,xx] and not seen[yy,xx] and xx<=34: seen[yy,xx]=1; q.append((yy,xx))
gez=seen
for sy in range(Y0,Y1):
  for sx in range(X0,X1):
    if not gez[sy,sx]: continue
    hood=any(0<=sy+dy<64 and med[sy+dy,sx+dx]>=200 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
    m=med[sy,sx]
    if nd[sy,sx]>=3 or m<70: o[sy,sx]=1 if (hood or m<45) else 2
    else: o[sy,sx]=2 if m<112 else (3 if m<166 else 4)
# ogen (modelpixels uitgelezen, zie verslag): lid zwart, wit, pupil, iris
OGEN={(18,24):1,(18,25):1,(19,24):6,(19,25):1,
      (18,29):1,(18,30):1,(18,31):1,(19,29):6,(19,30):1,(19,31):6}
for p,v in OGEN.items(): o[p]=v
np.save('gezicht.npy',o)
print('gewijzigd t.o.v. stap3:',int((o!=oud).sum()))
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('gezicht.png',transparency=0)
for y in range(12,30): print('%2d '%y+''.join('.123456789ABCDEF'[v] if v else ' ' for v in o[y,20:40]))
