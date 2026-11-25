# meet de rasterlijnen van elk paneel in het model: histogram van lijnpixels langs de paneelas
import numpy as np
from common import load
a,bg=load()
GEO={'PA':((86,24),(137,40),(71,36)),'PC':((176,58),(227,72),(163,70)),'PD':((20,86),(61,101),(3,96)),
     'PF':((123,100),(123,136),(133,104)),'PE':((102,117),(149,134),(88,132)),'PB':((123,3),(123,50),(132,8))}
GEO0=dict(GEO)
# r8: panelen verbreed in hun korte richting (v, T->L) met factor KP rond de middellijn v=0,5; lengte (u) gelijk
from common import KP, KPK, ANKER
# r9: ANKER uit common (PF vanaf de linkerrand)
def breed(g,f,an):
    T,R,L=map(np.array,g); d=(f-1)*an*(L-T); T2=T-d; return (tuple(T2),tuple(R-d),tuple(T2+f*(L-T)))
GEO={k:breed(g,KPK[k],ANKER[k]) for k,g in GEO0.items()}   # r9: factor per paneel (mast KM)
from common import VAR as _VV
if _VV=='r10':
    from geo10 import GEO10; GEO=dict(GEO10)   # r10: consistente paneelmaten met perspectief
lijn=(((a-np.array((116,99,143)))**2).sum(2)<24**2)&((a[:,:,0]-a[:,:,1])<30)&~bg   # R-G<30: geen paarse kragen
Y,X=np.mgrid[0:a.shape[0],0:a.shape[1]]
def uv(k,px,py):
    T,R,L=map(np.array,GEO[k]); Mx=np.array([R-T,L-T]).T.astype(float); inv=np.linalg.inv(Mx)
    d=np.stack([px-T[0],py-T[1]]); r=np.tensordot(inv,d,1); return r[0],r[1]
if __name__=='__main__':
    for k in GEO:
        u,v=uv(k,X,Y); m=lijn&(u>-0.08)&(u<1.08)&(v>-0.15)&(v<1.15)
        h,_=np.histogram(u[m],bins=40,range=(-0.1,1.1)); print(k,'u',' '.join('%d'%x for x in h))
        h,_=np.histogram(v[m],bins=24,range=(-0.1,1.1)); print(k,'v',' '.join('%d'%x for x in h))
