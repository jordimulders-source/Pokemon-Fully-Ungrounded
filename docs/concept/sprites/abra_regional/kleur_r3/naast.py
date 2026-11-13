# naast.py PNG x0 x1 y0 y1: per rij de sprite (elk teken dubbel) boven de twee modelrijen, kolommen gelijk
import sys; sys.path.insert(0,'../kleur_r2'); from PIL import Image; import numpy as np
from auto import NAAM, nlum, nbg, ndrk
NAAM=dict(NAAM); NAAM[6]='T'; NAAM[11]='I'
a=np.array(Image.open(sys.argv[1])).astype(int); X0,X1,Y0,Y1=map(int,sys.argv[2:6])
def t(l,bg,dk):
    if bg: return '.'
    if dk: return 'K'
    for th,c in ((60,'1'),(80,'2'),(102,'3'),(146,'s'),(170,'m'),(195,'b')):
        if l<th: return c
    return 'h'
print('     '+''.join('%-2d'%(x%100) if x%2==0 else '  ' for x in range(X0,X1)))
for y in range(Y0,Y1):
    print('%2d S '%y+''.join(NAAM[v]*2 for v in a[y,X0:X1]))
    for r in range(2):
        ny=2*y-14+r; print('   %s '%'ab'[r]+''.join(t(nlum[ny,2*x-1+c],nbg[ny,2*x-1+c],ndrk[ny,2*x-1+c]) for x in range(X0,X1) for c in range(2)))
