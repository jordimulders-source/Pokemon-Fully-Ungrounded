# bevroren onderdelen uit r16 (snavel, oog met blauwe vlek, buik, staart): maskers + verschuiving naar de r17-uitlijning (gemeten, als geheel)
import numpy as np
from PIL import Image
R16=np.array(Image.open('../r16/hoatzin.png'))
Y,X=np.mgrid[:64,:64]
def nb4(m):
    o=np.zeros_like(m)
    o[1:]|=m[:-1]; o[:-1]|=m[1:]; o[:,1:]|=m[:,:-1]; o[:,:-1]|=m[:,1:]; return o
def maskers():
    a=R16
    oog=np.isin(a,[8,9,10]); oog|=(a==1)&nb4(np.isin(a,[10]))&(Y<24)   # pupil
    sn=np.isin(a,[14,15])&(X<=12)&(Y>=20)&(Y<=28)
    sn|=(a==1)&(X<=13)&(Y>=24)&(Y<=28)&nb4(sn)                        # snavellijn/omlijning
    buik=np.isin(a,[11,12,13]); buik|=(a==1)&(Y>=45)&nb4(buik)&(X<36)
    st=(a>0)&(Y>=46)&(X>=35)&~np.isin(a,[11,12,13])&~((X<=38)&np.isin(a,[14,15]))
    st&=~(np.isin(a,[14,15]))
    return {'snavel':sn,'oog':oog,'buik':buik,'staart':st}
def schuif(m,dx,dy):
    o=np.zeros_like(m); ys,xs=np.where(m); ys2,xs2=ys+dy,xs+dx; ok=(ys2>=0)&(ys2<64)&(xs2>=0)&(xs2<64)
    o[ys2[ok],xs2[ok]]=m[ys[ok],xs[ok]]; return o
def zoek(m,doel,R=4):
    best=None
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            s=schuif(m,dx,dy); iou=(s&doel).sum()/max(1,(s|doel).sum())
            if best is None or iou>best[0]: best=(iou,dx,dy)
    return best
