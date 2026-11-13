# r.py raster x0 y0 x1 y1: uitsnede van het raster met liniaal
import sys,pal
R=pal.load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
print('   '+''.join(str(x//10) for x in range(x0,x1))); print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+R[y][x0:x1])
