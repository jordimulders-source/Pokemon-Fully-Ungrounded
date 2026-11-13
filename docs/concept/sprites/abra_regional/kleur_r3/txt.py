# txt.py PNG: raster als tekst (x 4..59, y 14..63) + model op 2x als tekst met dezelfde tekens
import sys; from PIL import Image; import numpy as np
import sys; sys.path.insert(0,'../kleur_r2'); from auto import NAAM, nat, nlum, nbg, ndrk; NAAM=dict(NAAM); NAAM[6]='T'; NAAM[11]='I'
a=np.array(Image.open(sys.argv[1])).astype(int)
X0,X1,Y0,Y1=[int(v) for v in sys.argv[2:6]] if len(sys.argv)>5 else (4,60,14,64)
print('    '+''.join(str((x//10)%10) for x in range(X0,X1))); print('    '+''.join(str(x%10) for x in range(X0,X1)))
for y in range(Y0,Y1): print('%2d  '%y+''.join(NAAM[v] for v in a[y,X0:X1]))
if '-m' in sys.argv:
    def t(l,bg,dk):
        if bg: return '.'
        if dk: return 'K'
        for th,c in ((60,'1'),(80,'2'),(102,'3'),(122,'d'),(146,'s'),(170,'m'),(195,'b')):
            if l<th: return c
        return 'h'
    print('model 2x (elke spritepixel = 2 tekens breed, 2 rijen)')
    for y in range(Y0,Y1):
        for r in range(2):
            ny=2*y-14+r
            print('%2d%s '%(y,'ab'[r])+''.join(t(nlum[ny,2*x-1+c],nbg[ny,2*x-1+c],ndrk[ny,2*x-1+c]) for x in range(X0,X1) for c in range(2)))
