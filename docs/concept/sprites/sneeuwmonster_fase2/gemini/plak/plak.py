# Plakt de stenen van r2a op r1a (geschaald), gecentreerd op de lijfas van r1a.
import sys
from PIL import Image
import numpy as np
src=np.array(Image.open('r2/r2a.png').convert('RGB')).astype(int)
dst=np.array(Image.open('r1/r1a.png').convert('RGB')).astype(int)
def snow(a):
    r,g,b=a[...,0],a[...,1],a[...,2]
    return (b>=r-5)&((r+g+b)>420)
def fill_snow(a,y0,y1,x0,x1):
    # oude steen weg: per rij horizontaal interpoleren tussen sneeuw links en rechts
    for y in range(y0,y1):
        L=a[y,x0-3].copy(); R=a[y,x1+3].copy()
        for x in range(x0-2,x1+3):
            t=(x-(x0-3))/(x1-x0+6); a[y,x]=(1-t)*L+t*R
out=dst.copy()
fill_snow(out,309,369,412,474); fill_snow(out,382,442,408,468)
stones=[(278,357,401,476),(371,451,401,472)]
scale=float(sys.argv[1]); centers=[(int(sys.argv[2]),440),(int(sys.argv[3]),436)]
for (y0,y1,x0,x1),(cy,cx) in zip(stones,centers):
    crop=src[y0:y1,x0:x1]; m=~snow(crop)
    im=Image.fromarray(crop.astype(np.uint8)); mi=Image.fromarray((m*255).astype(np.uint8))
    w,h=int(round((x1-x0)*scale)),int(round((y1-y0)*scale))
    im=np.array(im.resize((w,h),Image.NEAREST)).astype(int); mi=np.array(mi.resize((w,h),Image.NEAREST))>0
    ty,tx=cy-h//2,cx-w//2
    reg=out[ty:ty+h,tx:tx+w]; reg[mi]=im[mi]
Image.fromarray(out.astype(np.uint8)).save(sys.argv[4])
