# Per spritepixel: aandeel achtergrond / zwart / gem. kleur van het natieve model. Gebruik: dekking.py x0 y0 x1 y1
import sys,numpy as np; from PIL import Image
from groepen import masks
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); m,lum=masks(a)
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
def wts(lo,hi,n):
    w=np.zeros(n)
    for k in range(int(np.floor(lo)),int(np.ceil(hi))):
        if 0<=k<n: w[k]=min(hi,k+1)-max(lo,k)
    return w
def cel(sx,sy):
    ly=NY0+(sy-top+oy0)*s; lx=NX0+(sx-fx+ox0)*s
    w=wts(ly,ly+s,100)[:,None]*wts(lx,lx+s,100)[None,:]; t=w.sum()
    return (w*m['bg']).sum()/t,(w*m['blk']).sum()/t
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
print('bg%/zw%'); 
for y in range(Y0,Y1+1): print(y,' '.join('%2d/%2d'%tuple(int(99*v) for v in cel(x,y)) for x in range(X0,X1+1)))
