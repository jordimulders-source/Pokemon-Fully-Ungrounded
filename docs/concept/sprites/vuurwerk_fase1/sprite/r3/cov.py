# Meting: per spritepixel aandeel van elke modelklasse (natief_q) bij F=2.4, ox=76, oy=14 (zelfde als reduce4).
import sys, numpy as np
from txt import CH
q=np.load('natief_q.npy'); F,OX,OY=2.4,76.0,14.0
def cov(j,i):
    x0,x1=OX+i*F,OX+(i+1)*F; y0,y1=OY+j*F,OY+(j+1)*F; w=np.zeros(16); 
    for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
        wy=min(y1,yy+1)-max(y0,yy)
        for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
            wx=min(x1,xx+1)-max(x0,xx)
            if wx>0 and wy>0: w[q[yy,xx]]+=wx*wy
    return w/w.sum()
if __name__=='__main__':
    r0,r1,c0,c1=map(int,sys.argv[1:5]); cls=sys.argv[5]  # cls: tekens, bv 'E' of '#d' of 'sml'
    idx=[CH.index(c) for c in cls]
    print('     '+''.join('%3d'%c for c in range(c0,c1)))
    for j in range(r0,r1):
        print('%3d  '%j+''.join('%3d'%round(100*cov(j,i)[idx].sum()) if True else '' for i in range(c0,c1)))
