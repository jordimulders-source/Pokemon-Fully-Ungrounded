# verg.py raster x0 x1 y0 y1: modelkaart (frac.txt) | raster naast elkaar
import sys
R=open('frac.txt').read().split('\n')[2:]
g={}
for r in R:
  if r.strip():
    y=int(r[:2])
    for x,ch in enumerate(r[3:]): g[(x,y)]=ch
S=[l.rstrip('\n') for l in open(sys.argv[1])]
x0,x1,y0,y1=map(int,sys.argv[2:6])
h=''.join(str(x%10) for x in range(x0,x1))
print('   '+h+'   '+h)
for y in range(y0,y1):
  print('%2d '%y+''.join(g.get((x,y),' ') for x in range(x0,x1))+'   '+S[y][x0:x1])
