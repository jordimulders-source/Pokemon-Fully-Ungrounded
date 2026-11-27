# Ronde 6: modellijnen in het omcirkelde gebied 1-op-1 naar het spriteraster.
# Elke natieve lijnpixel (L<20, natief_bewerkt.png) wordt op zijn middelpunt naar het 64x64-raster gezet (zelfde schaal als kaal.py:
# x*40/70+12, y*44/77+20); een spritepixel is lijn als er genoeg natieve lijn doorheen loopt (aandeel >= DREMPEL van zijn vlak).
import numpy as np
from PIL import Image
from scipy import ndimage as nd
nat=np.array(Image.open('natief_bewerkt.png')).astype(float)
m=nat[...,3]>0; ys,xs=np.nonzero(m); nat=nat[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
Hn,Wn=m.shape; H,W=44,40
L=nat[...,:3].mean(2); line=(L<20)&m
# aandeel lijn per spritevlak (8x oversampling, zoals kaal.py)
up=8; Lu=np.repeat(np.repeat(line,up,0),up,1); Mu=np.repeat(np.repeat(m,up,0),up,1)
frac=np.zeros((64,64)); hit=np.zeros((64,64),int)
for y in range(H):
  for x in range(W):
    y0,y1=round(y*Hn*up/H),round((y+1)*Hn*up/H); x0,x1=round(x*Wn*up/W),round((x+1)*Wn*up/W)
    mm=Mu[y0:y1,x0:x1]
    if mm.any(): frac[y+20,x+12]=Lu[y0:y1,x0:x1][mm].mean()
for y,x in zip(*np.nonzero(line)):
    hit[int((y+.5)*H/Hn)+20,int((x+.5)*W/Wn)+12]+=1
np.save('frac64.npy',frac); np.save('hit64.npy',hit)
