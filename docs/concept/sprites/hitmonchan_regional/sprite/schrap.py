# Gengas-methode: rijen/kolommen schrappen die het meest op hun buren lijken (op het gekwantiseerde natieve raster).
# Oogzone beschermd (rijen 24-31, kolommen 28-37: oog + wenkbrauw op natieve grootte). Min. afstand tussen geschrapte lijnen.
# Kosten van lijn r schrappen = aantal pixels in r die van BEIDE buren verschillen (lijnpixels x3) = wat echt verdwijnt.
import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
def kies(q,n,besch,afst=3):
    H=q.shape[0]; cost=np.full(H,1e9)
    for r in range(1,H-1):
        if r in besch: continue
        v=(q[r]!=q[r-1])&(q[r]!=q[r+1]); w=np.where(q[r]<=3,3,1)
        cost[r]=(v*w).sum()
    gekozen=[]
    for r in np.argsort(cost,kind='stable'):
        if len(gekozen)==n or cost[r]>=1e9: break
        if all(abs(r-g)>=afst for g in gekozen): gekozen.append(int(r))
    return sorted(gekozen),cost
def schrap(q,NR=17,NC=10,RB=range(24,32),CB=range(28,38),afst=3):
    rd,rc=kies(q,NR,set(RB),afst); cd,cc=kies(q.T,NC,set(CB),afst)
    kr=[r for r in range(q.shape[0]) if r not in rd]; kc=[c for c in range(q.shape[1]) if c not in cd]
    return rd,cd,kr,kc
if __name__=='__main__':
    q=np.load(D+'natief_q.npy'); rd,cd,kr,kc=schrap(q)
    print('rijen weg',rd); print('kolommen weg',cd); print(len(kr),len(kc))
