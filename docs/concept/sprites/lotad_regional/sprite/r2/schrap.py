# Kleine variant: rijen/kolommen schrappen (Gengas-methode, niets hertekenen): telkens de kolom (rij) die het meest op zijn
# buur lijkt (minste verschillende pixels) weghalen; oogkolommen/-rijen en de buitenste 2 van de figuur blijven.
import numpy as np
def schrap(arrs,nkol,nrij,beschermd_x=(),beschermd_y=()):
    o=arrs[0]
    ys,xs=np.where(o>0); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    A=[a[y0:y1,x0:x1].copy() for a in arrs]; bx=[x-x0 for x in beschermd_x]; by=[y-y0 for y in beschermd_y]
    weg_x=[]; weg_y=[]
    for _ in range(nkol):
        o_=A[0]; best=None
        for x in range(6,o_.shape[1]-5):
            if x in bx or x-1 in bx or any(abs(x-w)<6 for w,_ in weg_x): continue
            d=(o_[:,x]!=o_[:,x-1]).sum()
            if best is None or d<best[0]: best=(d,x)
        x=best[1]; weg_x.append((x,int(best[0]))); A=[np.delete(a,x,1) for a in A]; bx=[b-1 if b>x else b for b in bx]
    for _ in range(nrij):
        o_=A[0]; best=None
        for y in range(5,o_.shape[0]-4):
            if y in by or y-1 in by or any(abs(y-w)<6 for w,_ in weg_y): continue
            d=(o_[y,:]!=o_[y-1,:]).sum()
            if best is None or d<best[0]: best=(d,y)
        y=best[1]; weg_y.append((y,int(best[0]))); A=[np.delete(a,y,0) for a in A]; by=[b-1 if b>y else b for b in by]
    hh,ww=A[0].shape; X0=(64-ww)//2; Y0=63-hh; uit=[]
    for a,orig in zip(A,arrs):
        f=np.zeros((64,64),orig.dtype); f[Y0:63,X0:X0+ww]=a; uit.append(f)
    return uit,weg_x,weg_y
