# Technische opschoning van basis.npy (kale 3x3-reductie, fase 0,0). Niets getekend; elke wijziging geteld.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); Lm=lum(a)
DONK={2:2,3:2,4:3,5:3,6:3,7:7,8:7,9:7,10:7,11:2,12:11,13:13,14:13,15:13}
o=np.load('basis.npy'); deel=np.load('basis_deel.npy'); raw=o.copy(); log={}
def tel(k): log[k]=log.get(k,0)+1
N4=((1,0),(-1,0),(0,1),(0,-1))
def nb(y,x,n=N4): return [(y+dy,x+dx) for dy,dx in n if 0<=y+dy<64 and 0<=x+dx<64]
N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
# 1. buitenrand dicht: randpixel -> omlijning; kap bovenaan/links grijs zoals het model (a1aaae) -> 3
m=o>0
for y in range(64):
  for x in range(64):
    if not m[y,x] or o[y,x]==1: continue
    leeg=[(yy,xx) for yy,xx in nb(y,x) if not m[yy,xx]]
    if not leeg: continue
    b=Lm[max(3*y-11,0):3*y-4,3*x+1:3*x+8]   # blok + 2 modelpixels rondom
    if b.size and b.min()>=90 and raw[y,x]>1: o[y,x]=DONK[raw[y,x]]; tel('rand: model heeft hier geen zwarte lijn -> donkerste eigen tint (selout)')
    else: o[y,x]=1; tel('rand zwart')
# 2. ruis: losse pixel (geen 4-buur gelijk) uit een gemengd blok -> meest voorkomende 8-buur
GEZ=(slice(13,26),slice(24,40))
for it in range(2):
  for y in range(64):
    for x in range(64):
      v=o[y,x]
      if v in (0,1,5,6) or deel[y,x]>=0.6: continue
      if GEZ[0].start<=y<GEZ[0].stop and GEZ[1].start<=x<GEZ[1].stop: continue
      if any(o[p]==v for p in nb(y,x)): continue
      c=[o[p] for p in nb(y,x,N8) if o[p] not in (0,1)]
      if c: o[y,x]=np.bincount(c).argmax(); tel('ruis')
# 3. losse zwarte pixel binnenin (geen 4-buur zwart, niet op de rand)
for y in range(64):
  for x in range(64):
    if o[y,x]!=1: continue
    if any(o[p]==0 for p in nb(y,x,N8)): continue
    if any(o[p]==1 for p in nb(y,x)): continue
    if GEZ[0].start<=y<GEZ[0].stop and GEZ[1].start<=x<GEZ[1].stop: continue
    c=[o[p] for p in nb(y,x,N8) if o[p]>1]; o[y,x]=np.bincount(c).argmax(); tel('losse zwarte')
np.save('stap2.npy',o); print(log)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('stap2.png',transparency=0)
