# Kale reductie r2: niet-gehele factor F (natief 200x200 -> doel), oppervlakgewogen per doelpixel op het gekwantiseerde
# natieve raster (natief_q). Regels als r1, omgerekend naar aandelen: dekking >= ALPHA; oogzwart >= EYE; lijn (# of d) >= LINE;
# anders de vlakkleur met het grootste oppervlak (gelijkspel: dichtst bij het gemiddelde in natief.png).
import sys, numpy as np
from reduce2 import PAL, n, save
q=np.load('natief_q.npy')
def reduce(F=2.4, ox=76.0, oy=14.0, W=30, H=62, ALPHA=0.55, EYE=0.22, LINE=0.33):
    out=np.zeros((H,W),'uint8')
    for j in range(H):
        for i in range(W):
            x0,x1=ox+i*F,ox+(i+1)*F; y0,y1=oy+j*F,oy+(j+1)*F
            wsum=np.zeros(16); col=np.zeros(3); tot=0
            for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
                wy=min(y1,yy+1)-max(y0,yy)
                if wy<=0 or yy<0 or yy>=200: continue
                for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
                    wx=min(x1,xx+1)-max(x0,xx)
                    if wx<=0 or xx<0 or xx>=200: continue
                    w=wx*wy; v=q[yy,xx]; wsum[v]+=w; tot+=w
                    if v: col+=w*n[yy,xx]
            A=1-wsum[0]/tot
            if A<ALPHA: continue
            fr=wsum/tot
            if fr[2]>=EYE: out[j,i]=2; continue
            if fr[1]+fr[3]+fr[2]>=LINE: out[j,i]=1 if fr[1]+fr[2]>=fr[3] else 3; continue
            f=wsum.copy(); f[[0,1,2,3]]=0
            best=np.where(f>=f.max()-1e-9)[0]
            if len(best)>1:
                m=col/max(1e-9,wsum[1:].sum()); best=[best[np.argmin(((PAL[best]-m)**2).sum(1))]]
            out[j,i]=best[0]
    return out
if __name__=='__main__':
    F=float(sys.argv[1]); ox=float(sys.argv[2]); oy=float(sys.argv[3])
    a=reduce(F,ox,oy); np.save('kaal.npy',a); save(a,'kaal.png')
    ys,xs=np.where(a>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
