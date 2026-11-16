# Stap A: lijfvulling opnieuw in 3 bruintinten (b schaduw, c midden, d licht) uit de GEMETEN modelhelderheid,
# laagdoorlaat (sigma) zodat de vlekken verdwijnen en alleen de grote licht/schaduwverdeling blijft.
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image
from meet import m
SG=float(sys.argv[1]); T1=float(sys.argv[2]); T2=float(sys.argv[3]); out=sys.argv[4]
im=Image.open('r3/mate.png'); PAL=im.getpalette(); a=np.asarray(im).astype(int)
M=m(64); lum=0.299*M[...,0]+0.587*M[...,1]+0.114*M[...,2]
def gf(x,sg):
    k=int(3*sg); t=np.arange(-k,k+1); g=np.exp(-t*t/2/sg/sg); g/=g.sum()
    x=np.apply_along_axis(lambda r:np.convolve(r,g,'same'),0,x); return np.apply_along_axis(lambda r:np.convolve(r,g,'same'),1,x)
H,W=a.shape
# vulpixels: bruin (3,4,5) en a (2) die niet aan transparant grenzen (selout blijft) en niet in de mondholte
op=a>0
def rand(y,x): return any(not op[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
mond=np.zeros_like(op); mond[48:54,19:30]=True
fill=np.zeros_like(op)
for y in range(1,H-1):
    for x in range(1,W-1):
        if a[y,x] in (3,4,5) and not rand(y,x): fill[y,x]=True
        if a[y,x]==2 and not rand(y,x) and not mond[y,x] and not (22<=y<=30 and 17<=x<=24): fill[y,x]=True
w=gf(fill.astype(float),SG); l=gf(lum*fill,SG)/np.maximum(w,1e-6)
b=a.copy()
b[fill&(l>=T2)]=5; b[fill&(l<T2)&(l>=T1)]=4; b[fill&(l<T1)]=3
np.save(out+'.npy',b)
p=Image.fromarray(b.astype('uint8'),'P'); p.putpalette(PAL); p.save(out,transparency=0)
print('gewijzigd',int((b!=a).sum()))
