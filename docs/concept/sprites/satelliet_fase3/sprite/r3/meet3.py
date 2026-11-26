# r3: dekking van paneelkleuren (navy vak / lavendel lijn / donkere rand) uit het model per spritepixel
import numpy as np, json
from PIL import Image
from common import load
import kaal
a,bg=load(); H,W=bg.shape
ys,xs=np.where(~bg); X0,X1,Y0,Y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
OUTW=64; s=(X1-X0)/OUTW; OH=int(np.ceil((Y1-Y0)/s))
print('s',s,'X0Y0',X0,Y0,'OH',OH)
def near(c,t): return ((a-np.array(t))**2).sum(2)
vak=near(0,(40,38,70))<14**2
lijn=near(0,(116,99,143))<22**2
donk=near(0,(28,24,45))<10**2
pan=(vak|lijn|donk)&~bg
Wx=kaal.overlap(OUTW,X0,s,W); Wy=kaal.overlap(OH,Y0,s,H)
def cov(m): return Wy@m.astype(float)@Wx.T/(s*s)
np.save('cov_pan.npy',cov(pan)); np.save('cov_lijn.npy',cov(lijn)); np.save('cov_vak.npy',cov(vak))
if __name__=='__main__':
    C=cov(pan); L=cov(lijn)
    for y in range(OH):
        print('%2d '%y+''.join('.' if C[y,x]<0.15 else str(min(9,int(C[y,x]*10))) for x in range(OUTW)))
    print()
    for y in range(OH):
        print('%2d '%y+''.join('.' if L[y,x]<0.15 else str(min(9,int(L[y,x]*10))) for x in range(OUTW)))
