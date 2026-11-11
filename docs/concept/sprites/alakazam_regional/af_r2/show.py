# show.py raster x0 y0 x1 y1: rastersnede met coördinaten
import sys,pal
R=pal.load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
print('    '+''.join(str(x//10) for x in range(x0,x1))); print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:2d}  '+R[y][x0:x1])
