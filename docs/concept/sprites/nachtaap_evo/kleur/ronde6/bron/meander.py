import sys
from PIL import Image
import numpy as np
pts=[]
def run(y,x0,x1): pts.extend((x,y) for x in range(x0,x1+1))
def col(x,y0,y1): pts.extend((x,y) for y in range(min(y0,y1),max(y0,y1)+1))
# meander (rechthoekige treden), boven: hoog, onder: laag; volgt de rugboog
run(31,17,18); col(18,29,31)
run(29,18,20); col(20,29,31); run(31,20,22); col(22,28,31)
run(28,22,24); col(24,28,30); run(30,24,26); col(26,27,30)
run(27,26,29); col(29,27,29); run(29,29,31); col(31,27,29)
run(27,31,33); col(33,27,29); run(29,33,35); col(35,29,31)
run(31,35,37); col(37,31,33); run(33,37,39); col(39,33,34)
pts=sorted(set(pts))
im=Image.open(sys.argv[1]); a=np.array(im)
out=[]
for x,y in pts:
    v=a[y,x]
    ch='l' if v==3 else 'm'   # schaduwkant idx5, verder idx6
    out.append('%d %d %s'%(y,x,ch))
print('\n'.join(out))
