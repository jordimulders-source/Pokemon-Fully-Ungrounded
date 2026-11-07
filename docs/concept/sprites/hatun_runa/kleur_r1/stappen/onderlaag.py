# onderlaag.py out.txt : model per spritepixel gekwantiseerd naar normal.pal (modus van de voorgrondpixels) = ALLEEN onderlaag, daarna handwerk
import sys
from tl import *
p=np.array(pal(P+'kleur_r1/normal.pal'),float)
fg=(C.min(-1)<200)|((C.max(-1)-C.min(-1))>40)
R=[['.']*64 for _ in range(64)]
for y in range(64):
  for x in range(64):
    if not SIL[y,x]: continue
    sl=box(x,y); c=C[sl].reshape(-1,3)
    if len(c)==0: R[y][x]='1'; continue
    d=((c[:,None,:]-p[None,1:])**2).sum(2).argmin(1)+1
    R[y][x]='%X'%np.bincount(d,minlength=16).argmax()
open(sys.argv[1],'w').write('\n'.join(''.join(r) for r in R)+'\n')
