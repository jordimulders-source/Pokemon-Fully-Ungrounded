# Achterbeen inschuiven (telescoop): onderbeen + schoen als geheel langs de beenas naar binnen/hoger
# verschuiven over het bovenbeen. Alleen knippen-plakken van modelpixels. -> natief_been.png
import sys; from PIL import Image; import numpy as np
DX,DY=int(sys.argv[1]),int(sys.argv[2]); T=float(sys.argv[3]) if len(sys.argv)>3 else 210
a=np.asarray(Image.open('natief.png').convert('RGB')).copy(); H,W,_=a.shape
from bgmask import bgmask; bg=bgmask(a)
yy,xx=np.mgrid[0:H,0:W]
m=(0.8*xx+0.6*yy>T)&(xx>=128)&(yy>=130)&~bg
out=a.copy(); out[m]=255
ys,xs=np.where(m); out[ys+DY,xs+DX]=a[ys,xs]
Image.fromarray(out).save('natief_been.png')
g=out.astype(int).mean(axis=2); y2,x2=np.where(g<235); print('bbox',x2.min(),x2.max(),y2.min(),y2.max(), 'pixels verplaatst',m.sum())
