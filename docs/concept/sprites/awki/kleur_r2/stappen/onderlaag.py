# onderlaag.py frac out : dichtstbijzijnde paletkleur van de modelmediaan (midden frac van elk vak) per spritepixel; alleen positiegids
import sys
from tl import *
p=np.array(pal(P+'kleur_r2/normal.pal'),float); f=float(sys.argv[1]); o=(1-f)/2
R=[]
for y in range(64):
  r=''
  for x in range(64):
    if not SIL[y,x]: r+='.'; continue
    bx=x0+(x-left)*s+s*o; by=y0+(y-top)*s+s*o
    c=np.median(C[int(by):int(by+s*f)+1,int(bx):int(bx+s*f)+1].reshape(-1,3),0)
    r+='%X'%(((p[1:]-c)**2).sum(1).argmin()+1)
  R.append(r)
open(sys.argv[2],'w').write('\n'.join(R)+'\n')
