# Zones per modelpixel en per spritecel voor een (bewerkt) model. Kleurregels gemeten op r3b (zie r2/NOTITIES.md):
# lijn lum<70 | staal: grijs (max-min<30) boven y335 | wit: lum>=215 onder y335 | roze oor: g<140,b>75,r>150 |
# donker (neus/hoef): lum<118, b>=42 | manen: b<42 en r>=130 (haar is blauwarm: 156,120,24 / 180,144,36 / 192,156,36) | vacht: rest
import numpy as np
ZN=['vacht','manen','staal','wit','roze','donker']
def pixzones(A,fg):
    A=A.astype(int); r,g,b=A[...,0],A[...,1],A[...,2]; lum=(A*[.299,.587,.114]).sum(2); sat=A.max(2)-A.min(2)
    yy=np.mgrid[:A.shape[0],:A.shape[1]][0]
    z=np.zeros(A.shape[:2],int)                       # 0 vacht
    xx=np.mgrid[:A.shape[0],:A.shape[1]][1]
    z[(b<42)&(r>=130)]=1
    z[(xx>=200)&(xx<345)&(yy>=440)&(yy<740)]=1     # keelfranje (lichtere lokken, zelfde vlak als in r3b)
    dk=(lum<118)&(b>=42)&(sat<75)
    z[dk&(((xx<330)&(yy>=380)&(yy<470))|(yy>=900))]=5     # alleen neus en hoeven; elders is donker een schaduw van het eigen vlak
    z[((r-g)>=40)&(b>=60)&(r>=130)&(g<150)&(yy<400)]=4     # oor binnen (licht en donker roze), alleen bij de oren
    z[(lum>=215)&(yy>=335)]=3
    z[(sat<30)&(yy<335)&(lum>=70)]=2
    z[lum<70]=-1; z[~fg]=-2
    return z,lum
def celstat(Zp,lum,y0,x0,p,H,W):
    """per cel: frac[zone] over voorgrond, lijnfractie, gem. helderheid per zone"""
    F=np.zeros((H,W,6)); LF=np.zeros((H,W)); AL=np.zeros((H,W)); LM=np.zeros((H,W,6))
    for j in range(H):
        for i in range(W):
            xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
            z=Zp[ya:yb,xa:xb]; l=lum[ya:yb,xa:xb]; f=z>=-1
            AL[j,i]=f.mean()
            if not f.any(): continue
            LF[j,i]=(z==-1).sum()/f.sum()
            for k in range(6):
                m=z==k; F[j,i,k]=m.sum()/f.sum()
                if m.any(): LM[j,i,k]=l[m].mean()
    return F,LF,AL,LM
