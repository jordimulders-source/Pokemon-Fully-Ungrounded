# tooi.py: bovenste groene tooiveren (rij 2-12) als gebogen bladvormen op de plek van r4.
# Per veer per rij (xl,xr); kleur: selout 5 links/boven, zwart 1 rechts, gele punt 6/7, nerf 7, lichte helft 2, schaduwhelft 3/4.
import numpy as np
from render import lees
H='.123456789abcdef'
V={ # naam: (rijen {y:(xl,xr)}, puntrijen, nerfrijen)
 'D':({10:(17,20),11:(17,22),12:(17,23),13:(18,23)},1,0),
 'E':({9:(46,48),10:(44,50),11:(43,50),12:(42,49),13:(41,47)},1,0),
 'A':({4:(24,25),5:(23,26),6:(23,27),7:(22,28),8:(22,28),9:(22,28),10:(23,28),11:(23,28),12:(24,28)},3,2),
 'C':({4:(40,42),5:(39,43),6:(38,43),7:(37,43),8:(36,43),9:(36,42),10:(36,42),11:(36,41),12:(36,41)},3,2),
 'B':({2:(31,32),3:(30,33),4:(30,34),5:(29,34),6:(29,35),7:(28,35),8:(28,36),9:(28,36),10:(28,36),11:(29,35),12:(29,35)},4,3),
}
def teken(a):
    for n,(R,npunt,nnerf) in V.items():
        ys=sorted(R); y0=ys[0]
        for y in ys:
            xl,xr=R[y]; c=(xl+xr)/2; prev=R.get(y-1)
            for x in range(xl,xr+1):
                rel=y-y0
                if x==xl: v=5
                elif x==xr: v=1
                elif rel==0: v=5 if x<c else 1
                elif prev and (x<prev[0] ): v=5
                elif prev and x>prev[1]: v=1
                elif rel<=npunt: v=6 if x<=c else 7
                elif rel<=npunt+nnerf and abs(x-round(c))==0: v=7
                else:
                    t=(x-xl)/(xr-xl)
                    laag=y>=ys[-1]-1
                    if t<0.5: v=3 if laag else 2
                    elif t<0.78: v=4 if laag else 3
                    else: v=4
                a[y,x]=v
    return a
if __name__=='__main__':
    a=lees('work.txt'); a[2:13,15:52]=np.where(np.isin(a[2:13,15:52],[0]),0,a[2:13,15:52])
    # wis het oude bovenste tooideel (rij 2-12, kol 15-51) behalve wat niet tot de veren hoort
    a[2:13,15:52]=0
    teken(a)
    print('   0123456789012345678901234567890123456789012345678901234567890123')
    for y in range(0,16): print('%02d '%y+''.join(H[v] for v in a[y]))
    np.save('tooi_tmp.npy',a)
