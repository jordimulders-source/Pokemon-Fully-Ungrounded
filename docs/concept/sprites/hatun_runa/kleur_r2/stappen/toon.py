# toon.py raster X0 Y0 X1 Y1 : gemiddelde helderheid sprite vs model (BOX) per zone, en per pixel het verschil (//10, + = sprite lichter)
import sys
from tl import *
R=raster(sys.argv[1]); p=pal(P+'kleur_r2/normal.pal')
X0,Y0,X1,Y1=map(int,sys.argv[2:6])
ds=[];dm=[]
print('    '+''.join(f'{x:>3}' for x in range(X0,X1)))
for y in range(Y0,Y1):
  r=''
  for x in range(X0,X1):
    if R[y][x]=='.': r+='  .'; continue
    a=np.mean(p[int(R[y][x],16)]); b=LUM[box(x,y)].mean(); ds.append(a); dm.append(b)
    r+=f'{int(a-b)//10:>3}'
  print(f'{y:>2} '+r)
print('sprite',int(np.mean(ds)),'model',int(np.mean(dm)))
