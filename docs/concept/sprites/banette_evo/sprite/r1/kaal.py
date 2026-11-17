# Kale reductie: model -> 62 px breed, vlakgemiddelde (alleen niet-witte pixels) + alpha-dekking
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float)
X0,Y0,S=24-0.0,1-0.0,968/62
OX,OY=1,4   # spritepositie van de bbox-linksboven
fig=a.min(2)<232
H=W=64
avg=np.zeros((H,W,3)); cov=np.zeros((H,W)); dark=np.zeros((H,W,3)); mn=np.zeros((H,W))
for j in range(H):
  for i in range(W):
    x0=X0+(i-OX)*S; y0=Y0+(j-OY)*S
    xa,xb,ya,yb=int(round(x0)),int(round(x0+S)),int(round(y0)),int(round(y0+S))
    if xb<=0 or yb<=0 or xa>=1024 or ya>=1024: continue
    xa,ya=max(xa,0),max(ya,0); xb,yb=min(xb,1024),min(yb,1024)
    blk=a[ya:yb,xa:xb].reshape(-1,3); f=fig[ya:yb,xa:xb].reshape(-1)
    cov[j,i]=f.mean()
    if f.sum(): 
      avg[j,i]=blk[f].mean(0); L=blk[f].sum(1); dark[j,i]=blk[f][L.argmin()]; mn[j,i]=(L<210).mean()
np.save('kaal_avg.npy',avg); np.save('kaal_cov.npy',cov); np.save('kaal_dark.npy',dark); np.save('kaal_mn.npy',mn)
img=np.where(cov[...,None]>=0.45,avg,255).astype('uint8')
Image.fromarray(img).save('kaal_rgb.png'); Image.fromarray(img).resize((512,512),Image.NEAREST).save('kaal_8x.png')
