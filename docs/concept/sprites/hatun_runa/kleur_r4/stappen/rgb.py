# rgb.py X0 Y0 X1 Y1 : dichtstbijzijnde paletkleur van de modelmediaan (midden 60%) per spritepixel
import sys
from tl import *
p=np.array(pal(P+'kleur_r4/normal.pal'),float)
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(X0,X1)))
for y in range(Y0,Y1):
  r=''
  for x in range(X0,X1):
    if not SIL[y,x]: r+='.'; continue
    bx=x0+(x-left)*s+s*.2; by=y0+(y-top)*s+s*.2
    c=np.median(C[int(by):int(by+s*.6),int(bx):int(bx+s*.6)].reshape(-1,3),0)
    r+='%X'%(((p[1:]-c)**2).sum(1).argmin()+1)
  print('%2d  '%y+r)
