# fijn.py X0 Y0 X1 Y1 : model op halve spritepixels (kwart-vakken) als paletletter (dichtstbijzijnde kleur); '.' = achtergrond
import sys
from tl import *
p=np.array(pal(P+'kleur_r1/normal.pal'),float)
X0,Y0,X1,Y1=map(float,sys.argv[1:5])
print('      '+''.join(('%-2d'%int(x)) if x==int(x) else '' for x in np.arange(X0,X1,0.5)))
for yy in np.arange(Y0,Y1,0.5):
  r=''
  for xx in np.arange(X0,X1,0.5):
    bx=x0+(xx-left)*s; by=y0+(yy-top)*s
    c=np.median(C[int(by)+1:int(by+s/2),int(bx)+1:int(bx+s/2)].reshape(-1,3),0)
    r+='.' if c.min()>243 else '%X'%(((p[1:]-c)**2).sum(1).argmin()+1)
  print('%5.1f '%yy+r)
