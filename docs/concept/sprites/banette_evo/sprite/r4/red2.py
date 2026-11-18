import sys,numpy as np
from mcov import *
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
fg=a.min(2)<235
def blk(i,j):
    xa,ya=24+(i-1)*S,1+(j-4)*S; sl=(slice(max(0,int(round(ya))),int(round(ya+S))),slice(max(0,int(round(xa))),int(round(xa+S)))); return sl
print('     '+''.join('%4d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        sl=blk(i,j); f=fg[sl]; c=f.mean()
        if c<0.5: s+='   .'; continue
        l=L[sl][f]; dk=(l<70).mean()
        if dk>=0.45: s+='   K'; continue
        lb=l[l>=70]; s+='%4d'%int(np.median(lb))
    print('%3d  '%j+s)
