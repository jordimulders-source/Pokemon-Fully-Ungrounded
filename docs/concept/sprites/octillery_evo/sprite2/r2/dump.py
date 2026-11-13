# r2/dump.py x0 y0 x1 y1 : rasterblok uit r2/raster.txt met liniaal, klaar om als '@ x0 y0'-blok te bewerken
import sys
x0,y0,x1,y1=map(int,sys.argv[1:5]); R=open('r2/raster.txt').read().split('\n')
print('#    '+''.join(str(x//10) for x in range(x0,x1))); print('#    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%s # %d'%(R[y][x0:x1],y))
