# r18 kop: toonkaart van het model (kop-ijzer, luminantie sterk gladgestreken, 4 tonen) op spritemaat; bruin en lichte platen daarop.
from kopmask import *
WIT=N.min(2)>215; G=(N[...,1]>N[...,0]+20)
IJ_=~G&~WIT&(LUM>=70)
def glad(V,M,s):
    rr=int(np.ceil(3*s)); k=np.exp(-np.arange(-rr,rr+1)**2/(2*s*s))
    cv=lambda a: np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,a))
    return cv(V*M)/np.maximum(cv(M.astype(float)),1e-6)
def toonkaart(r,kop,sig=4.0):
    GB=glad(LUM,IJ_,sig)
    T=np.full((64,64),np.nan)
    for y in range(64):
        for x in range(64):
            if kop[y,x]:
                nx,ny=s2n(x+.5,y+.5,0); T[y,x]=GB[int(ny),int(nx)]
    return T
def tonen(T,sel,q=(20,60,85)):
    qs=np.percentile(T[sel],q)
    Q=np.full(T.shape,-1)
    Q[sel]=3-np.searchsorted(qs,T[sel])   # 0 = licht
    return Q,qs

LICHTBRUIN=(188,128,88)   # nieuwe index 14: lichtste kopbruin (model: lichtste 5-10% bruin ±(178,137,110); warmer gehouden)
def bouwkop(r,a,pal,sikkel=True):
    kop,gez,rnd=masks(r)
    T=toonkaart(r,kop)
    sel=kop&np.isin(r,[7,8,9,10])&~rnd&~gez
    Q,qs=tonen(T,sel)
    bruin=sel&np.isin(r,[8,9])
    plaat=sel&np.isin(r,[7,10])
    # plaattonen: toonkaart binnen de platen in drie delen (licht 7 / 10 / schaduw 11)
    qp=np.percentile(T[plaat],[45,80])
    for y,x in zip(*np.where(bruin)):
        t=Q[y,x]; a[y,x]=14 if t==0 else (9 if t==3 else 8)
    for y,x in zip(*np.where(plaat)):
        v=T[y,x]; a[y,x]=7 if v>=qp[1] else (10 if v>=qp[0] else 11)
    if sikkel:
        # sikkel: T2-bruin binnen 2 px van de rechter-/onderrand van de kop wordt schaduw 9
        for y,x in zip(*np.where(bruin&(Q==2))):
            for d in (1,2):
                if (ok(y,x+d) and not kop[y,x+d] and r[y,x+d] not in (2,3,4,5,6,13)) or (ok(y+d,x) and not kop[y+d,x] and r[y+d,x]==0):
                    a[y,x]=9; break
    return a,Q,T,kop,gez,rnd
