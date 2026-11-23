# Natieve modelcoördinaten (ny,nx) per spritepixel van r3: hoofd + linkerstaf via kaal3, rechterstaf via staf2 (r2).
import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r2')
from kaal3 import kaal, RIJEN
from staf import K
from cc import label
from PIL import Image
S3=np.load('r3/sprite_r3.npy')
_,_,NY,NX=kaal()
H,W=K.shape; yy,xx=np.mgrid[0:H,0:W]
rows=sorted(set(RIJEN)|{62,78,80}); cols=[83]
d=lambda z:np.delete(np.delete(z,rows,0),cols,1)
kk,ny,nx=d(K),d(yy),d(xx); ys,xs=np.where(kk>0); sl=(slice(ys.min(),ys.max()+1),slice(xs.min(),xs.max()+1))
kk,ny,nx=kk[sl],ny[sl],nx[sl]; h,w=kk.shape; y0,x0=64-h,64-w
comp,_=label(S3>0,diag=True); RST=comp==comp[45,60]; LST=comp==comp[38,3]
NY=NY.copy(); NX=NX.copy()
NY[RST]=-1; NX[RST]=-1
m=kk>0; NY[y0:y0+h,x0:x0+w][m]=ny[m]; NX[y0:y0+h,x0:x0+w][m]=nx[m]
NAT=np.asarray(Image.open('natief.png')).astype(int); LUMN=(NAT*[0.299,0.587,0.114]).sum(2)
def lum(y,x): return LUMN[NY[y,x],NX[y,x]]
