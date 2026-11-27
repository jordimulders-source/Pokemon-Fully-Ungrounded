# r2 stap 1: sneeuwkap + creme zijkanten per spritepixel opnieuw gemeten (meerderheid van de 9 modelpixels per klasse).
# Bouwt vanaf r1/pachamama_r1.png. Raakt omlijning (1), rand en gezicht niet aan.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
from collections import deque
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); L=lum(a)
o=np.asarray(Image.open('../r1/pachamama_r1.png')).astype(int).copy(); r1=o.copy()
def blok(y,x): return (slice(3*y-9,3*y-6),slice(3*x+3,3*x+6))
med=np.zeros((64,64))
for y in range(4,64):
  for x in range(64): med[y,x]=np.median(L[blok(y,x)])
# gezichtsmasker (zelfde als r1/gezicht.py)
gez=np.zeros((64,64),bool); q=deque([(21,28)]); gez[21,28]=1
while q:
  y,x=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    yy,xx=y+dy,x+dx
    if 13<=yy<29 and 22<=xx<=34 and med[yy,xx]<200 and o[yy,xx]>0 and not gez[yy,xx]: gez[yy,xx]=1; q.append((yy,xx))
np.save('gezmasker.npy',gez)
m=o>0; pd=np.pad(m,1); rand=m&~(pd[:-2,1:-1]&pd[2:,1:-1]&pd[1:-1,:-2]&pd[1:-1,2:])
def klasse(px):
  l=lum(px); r,g,b=px
  if l<120: return 2
  if l<195: return 3
  if l<233: return 4
  return 6 if b>=r-2 else 5
OOG={(18,24),(18,25),(19,24),(19,25),(18,29),(18,30),(18,31),(19,29),(19,30),(19,31)}
n=0
for y in range(9,27):
  for x in range(17,44):
    if o[y,x] not in (3,4,5,6) or rand[y,x] or gez[y,x]: continue
    if (y,x) in OOG: continue
    ks=[klasse(p) for p in a[blok(y,x)].reshape(-1,3)]
    v=np.bincount(ks,minlength=7).argmax()
    if v!=o[y,x]: o[y,x]=v; n+=1
print('kap: gewijzigd',n)
np.save('kap.npy',o)
