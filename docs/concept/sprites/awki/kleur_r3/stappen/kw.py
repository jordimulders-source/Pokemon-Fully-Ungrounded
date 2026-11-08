# kw.py X0 Y0 X1 Y1 [raster] : per spritepixel de 4 kwartvakken van het model (lb,rb/lo,ro) als paletletters; met raster ook de huidige letter ervoor
import sys
from tl import *
p=np.array(pal(P+'kleur_r3/normal.pal'),float)
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
R=raster(sys.argv[5]) if len(sys.argv)>5 else None
def cl(xx,yy):
    bx=x0+(xx-left)*s; by=y0+(yy-top)*s
    c=np.median(C[int(by)+1:int(by+s/2),int(bx)+1:int(bx+s/2)].reshape(-1,3),0)
    return '.' if c.min()>243 else '%X'%(((p[1:]-c)**2).sum(1).argmin()+1)
print('    '+''.join('%-6d'%x for x in range(X0,X1)))
for y in range(Y0,Y1):
  r='%2d  '%y
  for x in range(X0,X1):
    q=cl(x,y)+cl(x+.5,y)+cl(x,y+.5)+cl(x+.5,y+.5)
    r+=(R[y][x] if R else '')+':'+q+' '
  print(r)
