# Staart (r3_3, natief verschoven -2,+3): per spritepixel uit de herkomst-3-cellen
# tonen: K zwart, D donkerbruin (lum<95), M midden, L licht ; lijn = K-fractie, ringscheiding = D-rug
import numpy as np
from reduceer import X0,Y0,s,LEFT,TOP
def staart(AL=0.35):
    nat=np.load('comp_nat.npy').astype(float); H=np.load('comp_bron.npy')
    lum=nat.mean(2); wit=nat.sum(2)>740
    T=(H=='3')&~wit
    R={}
    for sy in range(26,60):
        for sx in range(44,64):
            ya=Y0+(sy-TOP)*s; xa=X0+(sx-LEFT)*s; tot=0; w3=0; wk=0; wd=0; c=np.zeros(3); cw=0; wg=0; wo=0
            for y in range(int(np.floor(ya)),int(np.ceil(ya+s))):
                for x in range(int(np.floor(xa)),int(np.ceil(xa+s))):
                    w=max(0,min(y+1,ya+s)-max(y,ya))*max(0,min(x+1,xa+s)-max(x,xa))
                    if w<=0 or not(0<=y<100 and 0<=x<100): continue
                    tot+=w
                    if wit[y,x]: continue
                    if not T[y,x]: wo+=w; continue
                    w3+=w; L=lum[y,x]; r,g,b=nat[y,x]
                    if L<45: wk+=w
                    elif abs(r-b)<16: wg+=w; c+=w*nat[y,x]; cw+=w   # grijze punt
                    elif L<95: wd+=w
                    else: c+=w*nat[y,x]; cw+=w
            if tot and w3/tot>=AL*0.5:
                R[(sy,sx)]=dict(a3=w3/tot,ao=wo/tot,k=wk/max(w3,1e-9),d=wd/max(w3,1e-9),g=wg/max(w3,1e-9),c=c/cw if cw else None)
    return R
