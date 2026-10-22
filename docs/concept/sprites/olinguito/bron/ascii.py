import sys
from PIL import Image
import numpy as np
a=np.array(Image.open(sys.argv[1])); f=int(sys.argv[2]) if len(sys.argv)>2 else 0
a=a[f*64:(f+1)*64]
ch='.123456789ABCDEF'
print('   '+''.join(str(x//10) for x in range(64))); print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64):
    r=''.join(ch[v] if v else ' ' for v in a[y])
    if r.strip(): print('%2d %s'%(y,r))
