# los1.py raster : omlijningspixels (1) die niet aan transparant grenzen en maximaal 1 andere 1 als 8-buur hebben (losse lijnpixels midden in een vlak)
import sys
from tl import raster
R=raster(sys.argv[1])
def g(x,y): return R[y][x] if 0<=x<64 and 0<=y<64 else '.'
for y in range(64):
  for x in range(64):
    if R[y][x]!='1': continue
    nb=[g(x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy]
    if '.' in nb: continue
    if nb.count('1')<=1: print('los',x,y,''.join(nb))
