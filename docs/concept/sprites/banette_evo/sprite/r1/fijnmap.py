# Fracties van fijne klassen per spritepixel -> fijn.npz (draden eruit)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]; L=a.sum(2)/3
dr=np.load('draden_mask.npy')
NAMES='.kdgwroyb'
C=np.zeros(L.shape,int)
sat=a.max(2)-a.min(2)
C[(sat<30)&(L>=100)&(L<180)]=3; C[(sat<30)&(L>=45)&(L<100)]=2; C[(sat<30)&(L>=180)]=4
C[(r-np.maximum(g,b)>40)]=5; C[(r>200)&(g>95)&(g<180)&(b<140)]=6; C[(r>190)&(g>170)&(b<170)&(r-b>30)]=7
C[(b-r>12)&(b>=g)]=8
C[L<45]=1; C[a.min(2)>=235]=0; C[dr]=0
S=968/62; F=np.zeros((64,64,9))
for j in range(64):
  for i in range(64):
    x0=24+(i-1)*S; y0=1+(j-4)*S
    xa,ya,xb,yb=max(int(round(x0)),0),max(int(round(y0)),0),min(int(round(x0+S)),1024),min(int(round(y0+S)),1024)
    if xb>xa and yb>ya: F[j,i]=np.bincount(C[ya:yb,xa:xb].ravel(),minlength=9)/((yb-ya)*(xb-xa))
    else: F[j,i,0]=1
np.save('fijn.npy',F); np.save('fijnC.npy',C)
