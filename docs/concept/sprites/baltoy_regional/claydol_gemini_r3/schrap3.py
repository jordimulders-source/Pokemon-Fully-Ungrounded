# Schrappen (GEMINI.md, Gengas): figuur 73x72 natief -> <=64x64 door rijen/kolommen weg te laten (niet schalen).
# Kosten van rij/kolom i = gewogen aantal pixels dat verschilt van i-1. Zwaar: rood, donkere streepjes binnen licht (oog/krans),
# punt. Eén schrapping per gelijk stuk (verhoudingen blijven), goedkoopste in het stuk (+-speling), nooit twee naast elkaar.
import numpy as np, sys
from klas import klasse
k,a=klasse()
ys,xs=np.where(k>0); Y0,Y1,X0,X1=ys.min(),ys.max(),xs.min(),xs.max()
H,W=k.shape; yy,xx=np.mgrid[0:H,0:W]
w=np.ones((H,W))
w[k>=11]=15
licht=(k>=1)&(k<=4); donker=(k>=7)&(k<=10)
for y in range(1,H-1):
    for x in range(1,W-1):
        if donker[y,x] and licht[y-1:y+2,x-1:x+2].sum()>=4: w[y-1:y+2,x-1:x+2]=np.maximum(w[y-1:y+2,x-1:x+2],10)
w[(xx>=44)&(xx<=55)&(yy>=12)&(yy<=24)]=np.maximum(w[(xx>=44)&(xx<=55)&(yy>=12)&(yy<=24)],5)
def kosten(axis):
    A=k if axis==0 else k.T; Wt=w if axis==0 else w.T
    # pixel gaat alleen 'verloren' als hij van BEIDE buren verschilt (anders is hij een duplicaat)
    return np.array([1e9]+[(((A[i]!=A[i-1])&(A[i]!=A[i+1]))*Wt[i]).sum()+0.2*((A[i]!=A[i-1])*Wt[i]).sum() for i in range(1,len(A)-1)]+[1e9])
def kies(n,lo,hi,axis,speling=2):
    c=kosten(axis); seg=np.linspace(lo+1,hi,n+1); gek=[]
    for s in range(n):
        a_,b_=int(np.ceil(seg[s]))-speling,int(np.floor(seg[s+1]))+speling
        kand=[i for i in range(max(lo+2,a_),min(hi-1,b_)+1) if all(abs(i-j)>=2 for j in gek)]
        gek.append(min(kand,key=lambda i:(c[i],abs(i-(a_+b_)/2))))
    return sorted(gek),c
def schrap(rows,cols):
    yy_,xx_=np.mgrid[0:H,0:W]
    d=lambda z:np.delete(np.delete(z,rows,0),cols,1)
    kk,aa,ny,nx=d(k),d(a),d(yy_),d(xx_)
    ys,xs=np.where(kk>0); sl=(slice(ys.min(),ys.max()+1),slice(xs.min(),xs.max()+1))
    return kk[sl],aa[sl],ny[sl],nx[sl]
if __name__=='__main__':
    nr,nk=int(sys.argv[1]),int(sys.argv[2])
    rows,cr=kies(nr,Y0,Y1,0); cols,cc=kies(nk,X0,X1,1)
    kk,*_=schrap(rows,cols)
    print(kk.shape,'rijen',rows,[int(cr[i]) for i in rows]); print('kolommen',cols,[int(cc[i]) for i in cols])
    print('goedkoopste kolommen',sorted(range(X0+1,X1+1),key=lambda i:cc[i])[:25])
    print('goedkoopste rijen',sorted(range(Y0+1,Y1+1),key=lambda i:cr[i])[:25])
