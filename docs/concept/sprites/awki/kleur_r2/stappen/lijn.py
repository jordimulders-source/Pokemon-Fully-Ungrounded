# lijn.py X0 Y0 X1 Y1 : per spritepixel de 4 halve modelvakken (fijn.py); toont donkerste half (lijn) of de meeste kleur
import sys
from tl import *
p=np.array(pal(P+'kleur_r2/normal.pal'),float)
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
def cl(xx,yy):
    bx=x0+(xx-left)*s; by=y0+(yy-top)*s
    c=np.median(C[int(by)+1:int(by+s/2),int(bx)+1:int(bx+s/2)].reshape(-1,3),0)
    return '.' if c.min()>243 else '%X'%(((p[1:]-c)**2).sum(1).argmin()+1), c.mean()
print('   '+''.join(str(x%10) for x in range(X0,X1)))
for y in range(Y0,Y1):
  r=''
  for x in range(X0,X1):
    h=[cl(x+a,y+b) for a in (0,.5) for b in (0,.5)]
    lum=[v for k,v in h]; ks=[k for k,v in h]
    k=min(h,key=lambda t:t[1])[0] if min(lum)<120 and max(lum)>130 else max(set(ks),key=ks.count)
    r+=k
  print('%2d '%y+r)
