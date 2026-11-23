# Lagen van g3r5 palet B: welke pixels zijn "kop" (worden vervangen door de r10-kop); al het andere blijft diff 0.
import os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(H,'../claydol_gemini_r3/r5/claydol_g3r5_paletB.png')
G=np.array(Image.open(SRC)).astype(int); PAL=Image.open(SRC).getpalette()
yy,xx=np.mgrid[0:64,0:64]
# krans-bolletjes (middelpunt x,y en straal incl. omlijning), gemeten op het raster
BOL=[(23,4.5,4.4),(42.5,4.5,4.6),(13.5,8.5,4.4),(50,8.5,4.6),(8.5,16.5,4.4),(55.5,15.8,4.6),
     (6.5,25.5,4.4),(57.5,25.5,4.6),(11.8,34,3.9),(51.5,34,4.4)]
KOP_E=(31.5,23.0,22.6,16.8)
def masks():
    op=G>0
    bol=np.zeros((64,64),bool)
    for cx,cy,r in BOL: bol|=((xx-cx)**2+(yy-cy)**2)<=r*r
    punt=(yy<=8)&(xx>=28)&(xx<=37)
    cx,cy,rx,ry=KOP_E
    ell=((xx-cx)/rx)**2+((yy-cy)/ry)**2<=1
    kop=op&ell&~bol&~punt&(yy<=38)&(xx>=9)&(xx<=54)
    # rand van het silhouet blijft (omlijning g3r5)
    T=np.pad(~op,1,constant_values=True)
    rand=op&(T[:-2,1:-1]|T[2:,1:-1]|T[1:-1,:-2]|T[1:-1,2:])
    return kop, kop&~rand, bol&op, punt&op
if __name__=='__main__':
    kop,kin,bol,punt=masks()
    im=Image.open(SRC).convert('RGB'); a=np.array(im).astype(float)
    a[kin]=a[kin]*0.4+np.array([0,200,0])*0.6
    a[kop&~kin]=a[kop&~kin]*0.4+np.array([0,0,255])*0.6
    a[bol]=a[bol]*0.6+np.array([255,0,0])*0.4
    import sys; sys.path.insert(0,H); from rooster import rooster
    rooster(Image.fromarray(a.astype(np.uint8)),12,os.path.join(H,'lagen_check.png'),0,0,64,42)
    print(kin.sum(), (kop&~kin).sum())
