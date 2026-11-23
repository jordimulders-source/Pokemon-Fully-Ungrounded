# voeg.py x0 x1 y0 y1 : per spritepixel: '#'=zwarte modellijn, 'v'/'-'=voeg (donkerder dan lokaal mediaan-28), anders mediaanhelderheid/10
import sys, numpy as np
from PIL import Image
from PIL import ImageFilter
import os
L=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp').convert('L')).astype(int)
if os.path.exists('locmed.npy'): med=np.load('locmed.npy')
else: med=np.asarray(Image.fromarray(L.astype("uint8")).filter(ImageFilter.MedianFilter(21))).astype(int); np.save('locmed.npy',med)
s=(983-46)/62
def cell(x,y):
    ya,yb=int(57+(y-3)*s),int(57+(y-2)*s); xa,xb=int(46+(x-1)*s),int(46+x*s)
    b=L[ya:yb,xa:xb]; m=med[ya:yb,xa:xb]
    if (b<235).mean()<0.3: return '  .'
    ln=(b<70).mean(); vg=((b>=70)&(b<m-28)).mean()
    st=b[(b>=70)&(b>=m-28)]; v=int(np.median(st))//10 if st.size else 0
    ch='#' if ln>0.3 else ('V' if vg>0.25 else ('v' if vg>0.12 else ' '))
    return f'{ch}{v:2d}'
x0,x1,y0,y1=map(int,sys.argv[1:5])
print('    '+''.join(f'{x:3d}' for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:3d} '+''.join(cell(x,y) for x in range(x0,x1)))
