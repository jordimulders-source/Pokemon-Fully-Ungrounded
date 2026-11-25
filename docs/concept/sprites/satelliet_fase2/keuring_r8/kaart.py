import sys
from PIL import Image
import numpy as np
im=Image.open(sys.argv[1]).convert('RGBA'); a=np.array(im).astype(int)
cols=sorted({tuple(c[:3]) for c in a.reshape(-1,4) if c[3]},key=lambda c:c[0]+c[1]+c[2])
L='0123456789ABCDEF'
for i,c in enumerate(cols): print(L[i],c)
ys=[y for y in range(64) if a[y,:,3].any()]; xs=[x for x in range(64) if a[:,x,3].any()]
x0,x1=min(xs),max(xs)
print('    '+''.join(str(x//10) for x in range(x0,x1+1)))
print('    '+''.join(str(x%10) for x in range(x0,x1+1)))
for y in ys:
  print('%2d  '%y+''.join(L[cols.index(tuple(a[y,x,:3]))] if a[y,x,3] else '.' for x in range(x0,x1+1)))
