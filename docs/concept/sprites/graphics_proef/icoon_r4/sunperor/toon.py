import sys,numpy as np
from PIL import Image
a=np.array(Image.open(sys.argv[1]));y0=int(sys.argv[2]) if len(sys.argv)>2 else 0;y1=int(sys.argv[3]) if len(sys.argv)>3 else 32
print('   '+''.join(str(i%10) for i in range(a.shape[1])))
for y in range(y0,y1): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in a[y]))
