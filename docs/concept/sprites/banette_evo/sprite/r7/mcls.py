# per spritepixel: fractie zwart (L<38), donkerbruin (38<=L<80, laag verzadigd), rest. python3 mcls.py x0 y0 x1 y1
import sys,numpy as np
from mcov import a,L,S
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
sat=a.max(2)-a.min(2)
def blk(i,j):
    xa,ya=24+(i-1)*S,1+(j-4)*S; return (slice(max(0,int(round(ya))),int(round(ya+S))),slice(max(0,int(round(xa))),int(round(xa+S))))
print('     '+''.join('%5d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        sl=blk(i,j); l=L[sl]; k=(l<38).mean(); sa=sat[sl]; b=((l>=38)&(l<95)&(sa<40)).mean()
        s+='  %d%d%s'%(min(9,int(k*10)),min(9,int(b*10)),'#' if k+b>=0.5 and b>k else ('K' if k+b>=0.5 else ' '))
    print('%3d  '%j+s)
