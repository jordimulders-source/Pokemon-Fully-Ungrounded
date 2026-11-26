# Bevroren zones en hulpfuncties voor de eindkeuring (r2_E2M1 -> ek)
import numpy as np
from PIL import Image
SRC='../sprite_r2/poliwrath_regional_r2_E2M1.png'
def laad():
    im=Image.open(SRC); return im, np.array(im)
YEL=(5,6,7); RED=(12,13,14); ICE=(8,9,10,11,15); DARK=(2,3,4)
def bevroren(a):
    """pixels die geen enkele waarde mogen veranderen"""
    f=np.zeros(a.shape,bool)
    f[0:14,14:26]=True           # linkeroog E2 incl. lid, omlijning en onderrand (x14-25, y1-13)
    f[0:14,31:45]=True           # rechteroog E2 incl. onderrand (x31-44, y1-13)
    Y,X=np.mgrid[0:64,0:64]
    f[(Y>=14)&(Y<=16)&(X>=20)&(X<=31)&(a==7)]=True   # neusgaatjes (geel 7, rij 15)
    f[(Y>=16)&(Y<=19)&np.isin(a,RED)]=True   # mond M1
    ys,xs=np.where(np.isin(a,RED)&(Y>=24)&(Y<=41)&(X>=18)&(X<=39))
    f[ys.min():ys.max()+1, xs.min():xs.max()+1]=True   # spiraal: hele bbox (rood + geel ertussen)
    f[np.isin(a,RED)]=True       # al het rood: mond, spiraal, kristalkernen
    return f
