import sys,numpy as np
from PIL import Image
f=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6])
a=np.array(Image.open(f))
print('    '+''.join(str(x//10) for x in range(x0,x1)))
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d  '%y+''.join('.' if v==0 else '%X'%v for v in a[y,x0:x1]))
