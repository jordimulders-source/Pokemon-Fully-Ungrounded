import sys
from PIL import Image
im=Image.open(sys.argv[1]); x0,x1,y0,y1=[int(v) for v in sys.argv[2:6]]
print('   '+''.join(str(x//10) for x in range(x0,x1)));print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join('.' if im.getpixel((x,y))==0 else '0123456789ABCDEF'[im.getpixel((x,y))] for x in range(x0,x1)))
