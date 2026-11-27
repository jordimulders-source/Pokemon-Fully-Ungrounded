# grid.py SPRITE x0 x1 y0 y1: tekenraster met kolomnummers (tientallen + eenheden)
import sys; import numpy as np; from PIL import Image
ch='.KLSMHlsmhWg@#$%'; a=np.array(Image.open(sys.argv[1])); x0,x1,y0,y1=map(int,sys.argv[2:6])
print('   '+''.join(str(x//10) for x in range(x0,x1))); print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(ch[a[y,x]] for x in range(x0,x1)))
