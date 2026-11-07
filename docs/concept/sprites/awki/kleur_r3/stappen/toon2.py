# toon2.py raster X0 Y0 X1 Y1 : alleen vlakpixels (geen 0/1), helderheid sprite vs mediaan van het modelblok (methode hatun runa)
import sys
from tl import *
R=raster(sys.argv[1]); p=pal(P+'kleur_r3/normal.pal'); X0,Y0,X1,Y1=map(int,sys.argv[2:6]); a=[];b=[]
for y in range(Y0,Y1):
  for x in range(X0,X1):
    if R[y][x] in '.1': continue
    a.append(np.mean(p[int(R[y][x],16)])); b.append(np.median(LUM[box(x,y)]))
print('sprite',int(np.mean(a)),'model',int(np.mean(b)),'n',len(a))
