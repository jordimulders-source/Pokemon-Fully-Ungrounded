# Plakt de stenen van r3a (ruwe gloeiende stenen) op r1a. Gebruik: plak_r3.py breedte cy1 cy2 uit.png
import sys
from PIL import Image
import numpy as np
src=np.array(Image.open('r3/r3a.png').convert('RGB')).astype(int)
dst=np.array(Image.open('r1/r1a.png').convert('RGB')).astype(int)
def fill_snow(a,y0,y1,x0,x1):
    for y in range(y0,y1):
        L=a[y,x0-3].copy(); R=a[y,x1+3].copy()
        for x in range(x0-2,x1+3):
            t=(x-(x0-3))/(x1-x0+6); a[y,x]=(1-t)*L+t*R
out=dst.copy()
fill_snow(out,305,376,408,478); fill_snow(out,376,448,403,472)
def stone(y0,y1,x0,x1):
    c=src[y0:y1,x0:x1]; r,g,b=c[...,0],c[...,1],c[...,2]
    m=((r+g+b)<260)|((r>170)&(r-b>60))
    f=np.zeros_like(m)
    for y in range(m.shape[0]):
        xs=np.nonzero(m[y])[0]
        if len(xs): f[y,xs.min():xs.max()+1]=True
    return c,f
W=int(sys.argv[1]); cys=[int(sys.argv[2]),int(sys.argv[3])]; cxs=[442,437]
for (y0,y1,x0,x1),cy,cx in zip([(520,657,336,483),(676,820,322,483)],cys,cxs):
    c,f=stone(y0,y1,x0,x1)
    h=int(round(c.shape[0]*W/c.shape[1]))
    rgba=np.dstack([c,f*255]).astype(np.uint8)
    im=np.array(Image.fromarray(rgba,'RGBA').resize((W,h),Image.BOX)).astype(int)
    al=im[...,3]>127
    ty,tx=cy-h//2,cx-W//2
    reg=out[ty:ty+h,tx:tx+W]; reg[al]=im[...,:3][al]
Image.fromarray(out.astype(np.uint8)).save(sys.argv[4])
