import numpy as np; from PIL import Image; import sys
from legmask import N,BG,Lum
from legmask2 import leg
H,W=BG.shape; yy,xx=np.mgrid[0:H,0:W]
def make(DX,DY,t0=172,tA=212,out='natief_been14.png'):
    u=np.array([0.84,0.54])
    shoe=leg&(yy>=158)&(xx>=148)
    t=xx*u[0]+yy*u[1]
    A=N.copy(); A[leg]=255  # leg weg
    # forward map with supersampling (no holes)
    cov=np.zeros((H,W),bool); acc=np.zeros((H,W,3)); cnt=np.zeros((H,W))
    ys,xs=np.where(leg)
    for sy in (0.25,0.75):
        for sx in (0.25,0.75):
            X=xs+sx; Y=ys+sy; tt=X*u[0]+Y*u[1]
            f=np.clip((tt-t0)/(tA-t0),0,1); f[shoe[ys,xs]]=1
            Xn=X+DX*f; Yn=Y+DY*f
            xi=np.floor(Xn).astype(int); yi=np.floor(Yn).astype(int)
            ok=(xi>=0)&(xi<W)&(yi>=0)&(yi<H)
            # draw order: later (more front) - the leg is one layer; take darkest? use last write by t order
            np.add.at(acc,(yi[ok],xi[ok]),N[ys[ok],xs[ok]].astype(float)); np.add.at(cnt,(yi[ok],xi[ok]),1)
    m=cnt>=2
    A[m]=(acc[m]/cnt[m][:,None]).astype('uint8')
    Image.fromarray(A).save(out); return A,m
if __name__=='__main__':
    make(float(sys.argv[1]),float(sys.argv[2]),out=sys.argv[3])
