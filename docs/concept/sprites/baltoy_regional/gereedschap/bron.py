# Bronpixels: per spritepixel (y,x) van kaal34 de 4 natieve modelpixels (klassen) van zijn 2x2-blok.
import numpy as np, sys
sys.path.insert(0,'gereedschap'); from klassen import laad
S='.KDdmMlhRr'
k,_=laad(); H,W=k.shape
# kaal34 = reduceer(0,0): blok (j,i) = rijen 2j..2j+1, kol 2i..2i+1, daarna bijgesneden op de bbox
def _bbox():
    o=np.zeros((H//2,W//2),bool)
    for j in range(H//2):
        for i in range(W//2):
            o[j,i]=(k[2*j:2*j+2,2*i:2*i+2]==0).sum()<3
    ys,xs=np.where(o); return ys.min(),xs.min()
OY,OX=_bbox()
def bron(y,x):
    b=k[2*(y+OY):2*(y+OY)+2,2*(x+OX):2*(x+OX)+2]
    return ''.join(S[v] for v in b.ravel())   # volgorde: lb rb lo ro
if __name__=='__main__':
    y0,y1,x0,x1=map(int,sys.argv[1:5])
    print('OY,OX',OY,OX)
    for y in range(y0,y1+1):
        print('%2d '%y+' '.join('%2d:%s'%(x,bron(y,x)) for x in range(x0,x1+1)))
