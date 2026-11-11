# toon.py raster x0 y0 x1 y1 : print regio met coordinaten
import sys,cfg
a=cfg.read(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6])
print('    '+''.join(str(x//10) for x in range(x0,x1+1)))
print('    '+''.join(str(x%10) for x in range(x0,x1+1)))
for y in range(y0,y1+1): print('%3d '%y+''.join(cfg.CH[a[y,x]] for x in range(x0,x1+1)))
