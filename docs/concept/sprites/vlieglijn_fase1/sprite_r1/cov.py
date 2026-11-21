# Dekking per spritecel van een klasse(n) uit het model (natieve klassekaart), x10. python3 cov.py "13" i0 i1 j0 j1
import numpy as np, sys
cl=np.load('nat_cls.npy'); S=1.6; X0,Y0=17,20
ks=[int(k) for k in sys.argv[1].split(',')]; i0,i1,j0,j1=map(int,sys.argv[2:6])
def cov(i,j):
    x0=X0+i*S; x1=x0+S; y0=Y0+j*S; y1=y0+S; v=0
    for y in range(int(y0),int(np.ceil(y1))):
        wy=min(y+1,y1)-max(y,y0)
        for x in range(int(x0),int(np.ceil(x1))):
            wx=min(x+1,x1)-max(x,x0)
            if cl[y,x] in ks: v+=wx*wy
    return v/(S*S)
print('    '+''.join('%3d'%i for i in range(i0,i1)))
for j in range(j0,j1): print('%3d '%j+''.join('%3d'%round(10*cov(i,j)) if cov(i,j)>0.04 else '  .' for i in range(i0,i1)))
