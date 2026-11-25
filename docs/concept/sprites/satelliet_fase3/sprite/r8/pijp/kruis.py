# dekking per spritepixel door modelpixels van de DWARSlijnen (lijnkleur dichtbij een gemeten dwarslijn-u)
import numpy as np, kaal
from lijnen import *
s=3.515625; X0=Y0=3; OH=kaal.reduce()[0].shape[0]   # r7: 43 (bol120) of 44 (bol130)
PEAK={'PA':[0.23,0.53,0.77],'PC':[0.20,0.48,0.72],'PD':[0.24,0.48,0.75],'PE':[0.25,0.47,0.73],
      'PB':[0.33,0.60],'PF':[0.37,0.71]}   # gemeten pieken (lijnen.py); PB/PF: zwakker, zie rapport
Wx=kaal.overlap(64,X0,s,a.shape[1]); Wy=kaal.overlap(OH,Y0,s,a.shape[0])
def cov(m): return Wy@m.astype(float)@Wx.T/(s*s)
nonbg=cov(~bg)
pan=(((a-np.array((40,38,70)))**2).sum(2)<14**2)|lijn|(((a-np.array((28,24,45)))**2).sum(2)<10**2)
from common import KF,KS,VAR as _V
_LX=79+(74.9-79)*KS if _V.startswith('s') else 74.9   # r8: linkerbol geschaald vanuit de kraagkant x=79
BOLLEN=[((62.1,128.0),20.6*KF),((182.0,36.1),14.8),((_LX,64.7),11.2*KS),((189.0,91.0),11.2*KS*1.07),((128.0,72.0),20.5)]   # r7: oogbollen x K (rechts: straal 11,98 gefit)  # r2-metingen, alleen om oog/bolpixels uit te sluiten
inbol=np.zeros_like(bg)
for (cx,cy),r in BOLLEN: inbol|=(X-cx)**2+(Y-cy)**2<=(r+1.5)**2
pan&=~inbol
covpan=cov(pan&~bg)
KC={};REG={};PCOV={};LIJNFIT={}
for k,pk in PEAK.items():
    u,v=uv(k,X,Y); inpan=(u>-0.05)&(u<1.05)&(v>-0.12)&(v<1.12)
    KC[k]=[]; LIJNFIT.setdefault(k,[])
    box=(u>-0.12)&(u<1.12)&(v>-0.3)&(v<1.3)
    for p in pk:
        sel=lijn&inpan&(np.abs(u-p)<0.05)&(v>0.08)&(v<0.92)      # kern van de lijn, weg van de rand
        px,py=X[sel].astype(float),Y[sel].astype(float); c=np.array([px.mean(),py.mean()])
        w,V=np.linalg.eigh(np.cov(np.stack([px-c[0],py-c[1]]))); dirv=V[:,1]; nrm=V[:,0]
        dist=np.abs((X-c[0])*nrm[0]+(Y-c[1])*nrm[1])
        LIJNFIT[k].append((c,dirv))
        KC[k].append(cov(lijn&box&~inbol&(dist<=1.6)))
    REG[k]=cov(inpan)
    box=(u>-0.12)&(u<1.12)&(v>-0.3)&(v<1.3)
    PCOV[k]=cov(pan&~bg&box)
if __name__=='__main__':
    for k in KC:
        C=sum(KC[k]); ys,xs=np.where(C>0.05)
        print(k)
        for y in range(ys.min(),ys.max()+1):
            print('%2d '%y+''.join('.' if C[y,x]<0.08 else str(min(9,int(C[y,x]*10))) for x in range(xs.min(),xs.max()+1)),' x0=',xs.min())
