# onderlaag2.py out.txt [frac]: als onderlaag.py maar alleen het midden (frac) van elk modelvak -> minder overloop. ALLEEN onderlaag
import sys
from tl import *
p=np.array(pal(P+'kleur_r1/normal.pal'),float)
f=float(sys.argv[2]) if len(sys.argv)>2 else .6
R=[['.']*64 for _ in range(64)]
for y in range(64):
  for x in range(64):
    if not SIL[y,x]: continue
    bx=x0+(x-left)*s+s*(1-f)/2; by=y0+(y-top)*s+s*(1-f)/2
    c=C[int(by):int(by+s*f),int(bx):int(bx+s*f)].reshape(-1,3)
    d=((c[:,None,:]-p[None,1:])**2).sum(2).argmin(1)+1
    R[y][x]='%X'%np.bincount(d,minlength=16).argmax()
open(sys.argv[1],'w').write('\n'.join(''.join(r) for r in R)+'\n')
