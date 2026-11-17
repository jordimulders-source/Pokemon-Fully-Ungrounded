# Stap 1: kale reductie naar klassen + tonen (zonder draden), als tekstraster en png
from PIL import Image; import numpy as np
K=np.load('klassen.npy').copy(); dr=np.load('draden_mask.npy'); K[dr]=0
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); L=a.sum(2)/3
S=968/62; X0,Y0,OX,OY=24,1,1,4
H=W=64; cov=np.zeros((H,W)); lf=np.zeros((H,W)); maj=np.zeros((H,W),int); lum=np.zeros((H,W))
for j in range(H):
  for i in range(W):
    x0=X0+(i-OX)*S; y0=Y0+(j-OY)*S
    xa,ya,xb,yb=max(int(round(x0)),0),max(int(round(y0)),0),min(int(round(x0+S)),1024),min(int(round(y0+S)),1024)
    if xb<=xa or yb<=ya: continue
    k=K[ya:yb,xa:xb].ravel(); l=L[ya:yb,xa:xb].ravel()
    c=np.bincount(k,minlength=8)/k.size
    cov[j,i]=1-c[0]; lf[j,i]=c[1]/max(1-c[0],1e-6)
    cc=c.copy(); cc[0]=cc[1]=0
    if cc.sum()>0: maj[j,i]=cc.argmax(); lum[j,i]=l[k==maj[j,i]].mean()
np.savez('stap1.npz',cov=cov,lf=lf,maj=maj,lum=lum)
