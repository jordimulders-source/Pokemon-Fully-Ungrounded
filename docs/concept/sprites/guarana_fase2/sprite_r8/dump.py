# dump.py SPRITE x0 x1 y0 y1: tekenraster + oogmasker + eigenaar
import sys; import numpy as np; from PIL import Image
ch='.KLSMHlsmhWg@#$%'
a=np.array(Image.open(sys.argv[1])); x0,x1,y0,y1=map(int,sys.argv[2:6]); oog=np.load('sprite_r5/oog.npy'); own=np.load('sprite_r8/own.npy')
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    print('%2d '%y+''.join(ch[a[y,x]] for x in range(x0,x1))+'  '+''.join(('o' if oog[y,x] else '.') for x in range(x0,x1))+'  '+''.join((chr(65+own[y,x]) if own[y,x]>=0 and a[y,x] in (2,3,4,5,12,14,10,1,11) else '.') for x in range(x0,x1)))
