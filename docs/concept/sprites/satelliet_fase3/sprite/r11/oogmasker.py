# r11: oogzone per modeloog = convex omhulsel van (iris + ringpixels 6/7/8 binnen FR x irisstraal van het irismiddelpunt).
#   Iris = convex omhulsel van de teal pixels; binnen de iris: teal = iris, donker (1,2,3,D,E) = pupil, de rest = ring (geen wit binnen de ring, Jordi).
import numpy as np
def hull(pts):
    pts=sorted(set(pts))
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def inpoly(poly,X,Y):
    n=len(poly); ok=np.ones(X.shape,bool)
    for i in range(n):
        (x1,y1),(x2,y2)=poly[i],poly[(i+1)%n]
        ok&=((x2-x1)*(Y-y1)-(y2-y1)*(X-x1))>=-1e-9
    return ok
def masker(sub,FR,fill):
    teal=np.isin(sub,(9,10))
    Y,X=np.mgrid[0:sub.shape[0],0:sub.shape[1]]
    # iris = convex omhulsel van de teal pixels (de pupil zit erbinnen)
    tp=[]
    for y,x in zip(*np.where(teal)): tp+=[(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
    iris_s=inpoly(hull(tp),X+.5,Y+.5)
    ys,xs=np.where(iris_s); cx,cy=xs.mean()+.5,ys.mean()+.5; r=np.sqrt(iris_s.sum()/np.pi)
    ringc=np.isin(sub,(6,7,8))&(np.hypot(X+.5-cx,Y+.5-cy)<=FR*r)
    pts=[]
    for y,x in zip(*np.where(ringc|iris_s)): pts+= [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
    poly=hull(pts)
    # pixel in de zone als zijn middelpunt binnen het omhulsel ligt
    eye=inpoly(poly,X+.5,Y+.5)
    pup=iris_s&np.isin(sub,(1,2,3,13,14))
    return eye,iris_s&~pup,pup,eye&~iris_s,(cx,cy),r
