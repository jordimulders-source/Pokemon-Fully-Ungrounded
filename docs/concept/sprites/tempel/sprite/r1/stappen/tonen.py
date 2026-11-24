# tonen.py x0 x1 y0 y1: per spritepixel lijnmarkering (# >35% lijn, - >18%) + mediaanhelderheid/10 van het model
import sys, numpy as np
from PIL import Image
med=np.load('medL.npy'); L=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp').convert('L')).astype(int)
s=(983-46)/62
def cell(x,y):
    ya,yb=int(57+(y-3)*s),int(57+(y-2)*s); xa,xb=int(46+(x-1)*s),int(46+x*s)
    b=L[ya:yb,xa:xb]; m=med[ya:yb,xa:xb]; f=b<235
    if f.mean()<0.3: return '  .'
    ln=((b<70)&f).mean()
    v=np.median(m[f&(b>=70)]) if (f&(b>=70)).any() else 0
    ch='#' if ln>0.35 else ('-' if ln>0.18 else ' ')
    return f'{ch}{int(v)//10:2d}'
x0,x1,y0,y1=map(int,sys.argv[1:5])
print('    '+''.join(f'{x:3d}' for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:3d} '+''.join(cell(x,y) for x in range(x0,x1)))
