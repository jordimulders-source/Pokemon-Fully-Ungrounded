# gem.py raster X0 Y0 X1 Y1 : per spritepixel de gemiddelde modelkleur (binnenste vak) naar het palet, naast het raster
import sys
from tl import *
p=np.array(pal(P+'kleur_r2/normal.pal'),float); R=raster(sys.argv[1])
X0,Y0,X1,Y1=map(int,sys.argv[2:6])
for y in range(Y0,Y1):
  a='';b=''
  for x in range(X0,X1):
    if not SIL[y,x]: a+='.';b+='.';continue
    bx=x0+(x-left)*s; by=y0+(y-top)*s
    c=C[int(by)+1:int(by+s)-1,int(bx)+1:int(bx+s)-1].reshape(-1,3).mean(0)
    a+='%X'%(((p[1:]-c)**2).sum(1).argmin()+1); b+=R[y][x]
  print('%2d %s  %s'%(y,a,b))
