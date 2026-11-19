# Frame 2 verkleinen door hele natieve rijen/kolommen te schrappen (Gengas-methode: niets hertekenen).
# Per stap de rij/kolom die het minst verschilt van haar buur, met straf als een buur al geschrapt is (gelijkmatig verdelen).
import numpy as np; from PIL import Image
from palet import nearest
def natief_index(nat):
    a=np.asarray(Image.open(nat).convert('RGB')).astype(float)
    m=a.min(axis=2)<242; ys,xs=np.where(m); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    lum=a@[0.3,0.6,0.1]; ni=np.where(m, nearest(a), 0); ni[(lum<23)&m]=1
    return ni.astype(int), a, m
def kosten(ni,a,m):
    # verschil met de vorige kolom (RGB + masker), per kolom
    d=np.abs(np.diff(a,axis=1)).sum(axis=2)*(m[:,1:]|m[:,:-1]) + 400*(ni[:,1:]!=ni[:,:-1])*((ni[:,1:]==1)|(ni[:,:-1]==1))
    return d.sum(axis=0)
def schrap(ni,a,m,doel,as_):
    keep=list(range(ni.shape[as_])); weg=[]
    A,N,M=(a,ni,m) if as_==1 else (a.transpose(1,0,2),ni.T,m.T)
    while len(keep)>doel:
        sub=np.array(keep); c=kosten(N[:,sub],A[:,sub],M[:,sub])  # kosten van kolom k (k>=1) t.o.v. k-1
        best=None
        for k in range(1,len(sub)):
            o=sub[k]; straf=sum(1 for w in weg if abs(w-o)<=2)*c.mean()*0.8
            v=c[k-1]+straf
            if best is None or v<best[0]: best=(v,k)
        weg.append(sub[best[1]]); keep.pop(best[1])
    return keep,sorted(weg)
def verklein(nat,S):
    ni,a,m=natief_index(nat); H,W=ni.shape
    kx,wx=schrap(ni,a,m,round(W*S),1); ky,wy=schrap(ni,a,m,round(H*S),0)
    return ni[np.ix_(ky,kx)], (kx,wx,ky,wy)
