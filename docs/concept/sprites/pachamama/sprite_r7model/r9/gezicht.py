# r9: r4 v1 + gezicht van Gemini r10, alleen binnen het gezichtsmasker van r4 (rest pixel-identiek).
# Meting: r10 terug naar het natieve raster (5,12 px, fase x 4,6 / y 4,5), elke natieve pixel -> paletklasse,
# dan exact 3x3 natief -> 1 spritepixel (gelijke schaal x/y = 15,36 modelpx per spritepx).
# Gebruik: python3 r9/gezicht.py A B UIT.npy   (spritekolom = (i+A)//3, spriterij = (j-B)//3)
import sys, numpy as np
from PIL import Image
from collections import deque
D='docs/concept/sprites/pachamama/'
A=int(sys.argv[1]); B=int(sys.argv[2]); UIT=sys.argv[3]
r4=np.array(Image.open(D+'sprite_r7model/r4/pachamama_r4.png'))
M=np.asarray(Image.open(D+'gemini/r10.png').convert('RGB')).astype(int)
# --- gezichtsmasker r4 (definitie r4/hoofd.py 'gez') + ingesloten gaten (oogwit, lijnen)
z2=np.load(D+'sprite_r7model/r4/natief_g2_gez.npy'); MY,MX=-21,-2
def bl(y,x): return (slice(max(MY+3*y,0),max(MY+3*y+3,0)),slice(max(MX+3*x,0),MX+3*x+3))
gez=np.zeros((64,64),bool)
for y in range(5,40):
  for x in range(10,50): gez[y,x]=z2[bl(y,x)].sum()>=5
out=np.zeros((64,64),bool); q=deque([(0,0)]); out[0,0]=1
while q:
  r,c=q.popleft()
  for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
    R,C=r+dr,c+dc
    if 0<=R<64 and 0<=C<64 and not out[R,C] and not gez[R,C]: out[R,C]=1; q.append((R,C))
mask=~out
# --- natief raster
P=5.12; OX,OY=4.6,4.5; NY=NX=199
N=np.zeros((NY,NX,3),int)
for j in range(NY):
  for i in range(NX):
    cx=int(OX+P*i+P/2); cy=int(OY+P*j+P/2); N[j,i]=np.median(M[cy-1:cy+2,cx-1:cx+2].reshape(-1,3),0)
L=N.mean(2); red=(N[:,:,0]-N[:,:,1])>60
# tintniveaus van het model (gemeten medianen: neus 236/230/200, wangvlak 184/173/155, voorhoofd 172/157/141,
# ondergezicht 166/152/135, schaduw rechts 118/106/90, oogkas ~97, lijnen 60-80, pupil/lid ~10-40) -> paletindex
K=np.select([L<55,L<85,L<130,L<164,L<205],[1,2,3,4,13],5)   # oogkas L 96-99 -> 3 (palet 3 = L 103)
oog=np.zeros((NY,NX),bool); oog[63:70,65:77]=1; oog[63:70,86:100]=1   # gemeten oogvakken (natief)
K[(L>200)&oog]=10                   # oogwit
K[red]=-1
K[:47]=-1                       # boven de kapschaduw: kap, niet gezicht
K[:, :64]=-1; K[:,108:]=-1      # crème haar naast het gezicht
np.save(D+'sprite_r7model/r9/natief_klasse.npy',K)
o=r4.copy(); leeg=[]
for y,x in zip(*np.where(mask)):
  i0=3*x-A; j0=3*y+B
  c=K[j0:j0+3,i0:i0+3].ravel(); f=c[c>=0]
  if len(f)<4: o[y,x]=0; leeg.append((y,x)); continue
  n={k:(f==k).sum() for k in (1,2,3,4,13,10,5)}
  if n[1]>=3: v=1
  elif n[10]>=3: v=10
  elif n[2]>=3 or n[1]+n[2]>=4: v=2
  else:
    best=max(n[3],n[4],n[13],n[5]); kk=[k for k in (3,4,13,5) if n[k]==best]
    v=K[j0+1,i0+1] if K[j0+1,i0+1] in kk else kk[0]
  o[y,x]=v
for _ in range(6):
  for (y,x) in leeg:
    if o[y,x]: continue
    nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if mask[y+dy,x+dx] and o[y+dy,x+dx] in (3,4,13)]
    if nb: o[y,x]=max(set(nb),key=nb.count)
np.save(UIT,o); np.save(D+'sprite_r7model/r9/masker.npy',mask)
print('masker',mask.sum(),'leeg (buiten modelgezicht, buurtint)',len(leeg),leeg)
for r in range(11,33): print('%2d '%r+''.join(('%x'%o[r,c]) if mask[r,c] else ('·' if o[r,c] else ' ') for c in range(18,42)))
