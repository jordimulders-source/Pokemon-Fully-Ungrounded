import sys
from PIL import Image
import numpy as np
from collections import Counter
im=np.array(Image.open(sys.argv[1]).convert('RGBA')).astype(int)
H,W=im.shape[:2]
op=im[:,:,3]>0
names={(16,16,16):'zw',(50,36,30):'br5',(80,63,55):'br8',(110,91,79):'br1',(140,116,104):'br4',(95,26,28):'r7',(140,33,37):'ra',(200,65,70):'r3'}
def nm(y,x): return names.get(tuple(im[y,x,:3]),str(tuple(im[y,x,:3])))
# outline pixels: opaque with transparent 4-neighbour
out={}
for y in range(H):
  for x in range(W):
    if not op[y,x]: continue
    dirs=[]
    for dy,dx,d in [(-1,0,'N'),(1,0,'S'),(0,-1,'W'),(0,1,'E')]:
      yy,xx=y+dy,x+dx
      if not(0<=yy<H and 0<=xx<W) or not op[yy,xx]: dirs.append(d)
    if dirs: out[(y,x)]=(nm(y,x),''.join(dirs))
c=Counter()
for (y,x),(n,d) in out.items():
  for ch in d: c[(ch,n)]+=1
for k in sorted(c): print(k,c[k])
# non-outline-colour on the edge
print('lichte kleur op buitenrand:')
for (y,x),(n,d) in sorted(out.items()):
  if n not in ('zw','br5','r7'): print((x,y),n,d)
print('zwart N/W (alleen N of W, niet ook S/E):')
for (y,x),(n,d) in sorted(out.items(), key=lambda t:(t[0][1],t[0][0])):
  if n=='zw' and set(d)<= set('NW'): print((x,y),d, end='; ')
print()
print('br5 rand:',[((x,y),d) for (y,x),(n,d) in out.items() if n=='br5'])
