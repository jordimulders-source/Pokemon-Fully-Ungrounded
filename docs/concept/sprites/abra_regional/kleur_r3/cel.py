# cel.py PNG x0 x1 y0 y1: per spritepixel 'sprite|ab/cd' (modelblok 2x2) in een rooster
import sys; sys.path.insert(0,'../kleur_r2'); from PIL import Image; import numpy as np
from auto import NAAM, nlum, nbg, ndrk
NAAM=dict(NAAM); NAAM[6]='T'; NAAM[11]='I'
a=np.array(Image.open(sys.argv[1])).astype(int); X0,X1,Y0,Y1=map(int,sys.argv[2:6])
def t(ny,nx):
    if nbg[ny,nx]: return '.'
    if ndrk[ny,nx]: return 'K'
    l=nlum[ny,nx]
    for th,c in ((60,'1'),(80,'2'),(102,'3'),(146,'s'),(170,'m'),(195,'b')):
        if l<th: return c
    return 'h'
print('    '+'|'.join('%4d'%x for x in range(X0,X1)))
for y in range(Y0,Y1):
    r1=[];r2=[]
    for x in range(X0,X1):
        ny,nx=2*y-14,2*x-1
        r1.append(NAAM[a[y,x]]+' '+t(ny,nx)+t(ny,nx+1)); r2.append('  '+t(ny+1,nx)+t(ny+1,nx+1))
    print('%2d  '%y+'|'.join(r1)); print('    '+'|'.join(r2))
