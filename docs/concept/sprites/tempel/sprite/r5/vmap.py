# vmap.py: hele sprite: '#' zwarte modellijn, 'V' voeg sterk, 'v' zwak, letter = sprite-tint (raster r3) anders '.'
import sys, numpy as np
from PIL import Image
L=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp').convert('L')).astype(int)
med=np.load('locmed.npy'); s=(983-46)/62
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
thr=int(sys.argv[2]) if len(sys.argv)>2 else 28
x0,x1,y0,y1=map(int,sys.argv[3:7]) if len(sys.argv)>6 else (0,64,0,64)
print('    '+''.join(str(x//10) for x in range(x0,x1))); print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
  row=''
  for x in range(x0,x1):
    ya,yb=int(57+(y-3)*s),int(57+(y-2)*s); xa,xb=int(46+(x-1)*s),int(46+x*s)
    b=L[max(ya,0):yb,max(xa,0):xb]; m=med[max(ya,0):yb,max(xa,0):xb]
    if b.size==0 or (b<235).mean()<0.3: row+=' '; continue
    ln=(b<70).mean(); vg=((b>=70)&(b<m-thr)).mean()
    row+='#' if ln>0.3 else ('V' if vg>0.25 else ('v' if vg>0.12 else '.'))
  print(f'{y:3d} '+row+'   '+R[y][x0:x1])
