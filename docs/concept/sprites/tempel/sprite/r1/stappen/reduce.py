# reduce.py: kale reductie van het model (vlakgemiddelde) + lijnfractie per spritepixel
import numpy as np
from PIL import Image
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
c=np.asarray(Image.open(M).convert('RGB')).astype(float); L=c.mean(2)
fg=L<235
X0,X1,Y0,Y1=46,983,57,958
W=62; s=(X1-X0)/W; H=int(round((Y1-Y0)/s)); left=1; top=63-H
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64)); line=np.zeros((64,64)); lum=np.zeros((64,64)); p15=np.zeros((64,64))
for by in range(H):
  for bx in range(W):
    ya,yb=int(Y0+by*s),int(Y0+(by+1)*s); xa,xb=int(X0+bx*s),int(X0+(bx+1)*s)
    f=fg[ya:yb,xa:xb]; blk=c[ya:yb,xa:xb]; l=L[ya:yb,xa:xb]
    y,x=top+by,left+bx
    alpha[y,x]=f.mean()
    if f.any():
      ln=(l<45)&f; line[y,x]=ln.sum()/f.size
      nl=f&~ln
      mean[y,x]=blk[nl].mean(0) if nl.any() else blk[f].mean(0)
      lum[y,x]=l[nl].mean() if nl.any() else l[f].mean()
      p15[y,x]=np.percentile(l[f],15)
np.savez('red.npz',mean=mean,alpha=alpha,line=line,lum=lum,p15=p15,s=s,top=top,left=left)
print('s',s,'H',H,'top',top)
