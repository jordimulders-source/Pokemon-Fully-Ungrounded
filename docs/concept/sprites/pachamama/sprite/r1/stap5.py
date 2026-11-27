# Laatste technische stap: gezichtscontour dicht op gemeten modellijnen; losse zwarte lijnpixels -> donkerste eigen tint
# (geen zwart en donkere tint om en om op een lijn). Schrijft pachamama_r1.png.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
o=np.load('stap4.npy'); oud=o.copy(); log={}
def tel(k): log[k]=log.get(k,0)+1
# gezichtscontour: modelblok heeft hier een kolom/rij donkere modelpixels (L<75: 3 resp. 2-3 px), zie verslag
for p in ((23,34),(25,23),(27,23),(28,23)):
  if o[p]!=1: o[p]=1; tel('gezichtscontour op modellijn')
DONK={2:2,3:2,4:3,5:3,6:3,7:7,8:7,9:7,10:7,11:2,12:11,13:13,14:13,15:13}
for y in range(1,63):
  for x in range(1,63):
    if o[y,x]!=1: continue
    if any(o[y+dy,x+dx] in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): continue
    c=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx]>1]
    t=min({DONK[v] for v in c},key=lambda i:lum(P[i])); o[y,x]=t; tel('losse zwarte lijnpixel -> donkere eigen tint')
# donkerrood (7) op plekken waar het model bruin/olijf is (plantjes, okerbarsten): G/R >= 0.72 -> dichtstbijzijnde niet-rode tint
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float)
for y in range(64):
  for x in range(64):
    if o[y,x]!=7 or 3*y-9<0: continue
    md=np.median(a[3*y-9:3*y-6,3*x+3:3*x+6].reshape(-1,3),0)
    if md[1]/max(md[0],1)>=0.72: o[y,x]=nearest(md[None],(2,3,11,12,13,14))[0]; tel('7 -> bruin/olijf zoals het model')
np.save('pachamama_r1.npy',o); print(log,'gewijzigd',int((o!=oud).sum()))
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('pachamama_r1.png',transparency=0)
