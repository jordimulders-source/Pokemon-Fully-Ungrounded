# r10-kop op de maat van onze kop: rijen/kolommen schrappen waar ze (bijna) gelijk zijn aan hun buur (rustige plekken),
# geen interpolatie. Natief x 19..80 (62) -> onze x 9..54 (46); natief y Y0..66 -> onze y 6..39 (34).
import numpy as np
from r10kop import bouw
X0,X1=19,80
def schrap(A,n,as_=0,beschermd=()):
    """verwijder n lijnen (as 0 = rijen) die het minst verschillen van een buur; na elke schrap opnieuw meten"""
    idx=list(range(A.shape[as_])); weg=[]
    for _ in range(n):
        B=A[idx] if as_==0 else A[:,idx]
        L=B if as_==0 else B.T
        dif=[(L[i]!=L[i-1]).sum() for i in range(1,len(L))]
        best=None
        for i in range(1,len(L)-1):
            c=min(dif[i-1],dif[i])
            if idx[i] in beschermd: c+=1000
            if best is None or c<best[0]: best=(c,i)
        weg.append((idx[best[1]],best[0])); del idx[best[1]]
    return idx,weg
def pas(Y0=16,NY=34,NX=46,brow=(),bcol=()):
    T,kop,gev=bouw()
    A=np.where(kop,T,'.')[Y0:67,X0:X1+1]
    ri,rw=schrap(A,A.shape[0]-NY,0,[b-Y0 for b in brow])
    ci,cw=schrap(A[ri],A.shape[1]-NX,1,[b-X0 for b in bcol])
    return A[np.ix_(ri,ci)],[Y0+i for i in ri],[X0+i for i in ci],rw,cw
if __name__=='__main__':
    R,ri,ci,rw,cw=pas()
    print('rijen weg',sorted((r+16,c) for r,c in rw)); print('kol weg',sorted((x+X0,c) for x,c in cw))
    for i,r in enumerate(R): print('%2d %2d '%(i+6,ri[i])+''.join(r))

def schrap_zones(A,zones,as_=0,off=0,besch=()):
    """zones = [(van,tot,n)] in natieve coördinaten; per zone n lijnen schrappen (greedy, alleen binnen de zone)"""
    idx=list(range(A.shape[as_])); weg=[]
    for a,b,n in zones:
        for _ in range(n):
            L=A[idx] if as_==0 else A[:,idx].T
            best=None
            for i in range(1,len(L)-1):
                if not (a<=idx[i]+off<=b) or idx[i]+off in besch: continue
                c=min((L[i]!=L[i-1]).sum(),(L[i]!=L[i+1]).sum())
                if best is None or c<best[0]: best=(c,i)
            weg.append((idx[best[1]]+off,best[0])); del idx[best[1]]
    return idx,weg
BESCH_R=(44,45)
BESCH_C=(24,25,26,48,49,50,51)   # oogstreepjes heel houden (links x 23-26 rij 44, rechts x 47-51 rij 45)
def pas_z(rz,cz,Y0=16):
    T,kop,gev=bouw()
    A=np.where(kop,T,'.')[Y0:67,X0:X1+1]
    ri,rw=schrap_zones(A,rz,0,Y0,BESCH_R)
    ci,cw=schrap_zones(A[ri],cz,1,X0,BESCH_C)
    return A[np.ix_(ri,ci)],[Y0+i for i in ri],[X0+i for i in ci],rw,cw
