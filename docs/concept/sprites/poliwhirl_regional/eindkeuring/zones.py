# Bevroren zones en hulpfuncties voor de eindkeuring (r6_B -> ek)
import numpy as np
from PIL import Image
SRC='../sprite_r6/poliwhirl_regional_r6_B.png'
def laad():
    im=Image.open(SRC); return im, np.array(im)
YEL=(5,6,7); RED=(12,13,14); ICE=(8,9,10,11,15); DARK=(2,3,4)
def bevroren(a):
    """masker van pixels die geen enkele waarde mogen veranderen"""
    f=np.zeros(a.shape,bool)
    f[12:21,19:27]=True          # linkeroog incl. omlijning (20,15),(20,18) en oogwit (20,16),(20,17)
    f[12:21,32:41]=True          # rechteroog incl. omlijning
    f[20,:][np.isin(a[20],[7])]=True  # neusgaten (index 7 in rij 20)
    Y,X=np.mgrid[0:64,0:64]
    ys,xs=np.where(np.isin(a,RED)&(Y>=29)&(Y<=42)&(X>=23)&(X<=37))
    f[ys.min():ys.max()+1, xs.min():xs.max()+1]=True   # spiraal: hele bbox (rood + geel ertussen)
    f[np.isin(a,RED)]=True       # al het rood: mond, spiraal, kristalkernen
    return f
def vormmasker(a):
    """materiaalvormen die bevroren zijn: kristallen/handschoenen (ijs), mond, geel/zwart-patroon.
    Toegestaan: tint binnen hetzelfde materiaal. Lijnpixels (1) <-> outline base van het eigen materiaal."""
    m=np.zeros(a.shape,'uint8')
    m[np.isin(a,YEL)]=1; m[np.isin(a,DARK)]=2; m[np.isin(a,ICE)]=3; m[np.isin(a,RED)]=4; m[a==1]=5
    return m
