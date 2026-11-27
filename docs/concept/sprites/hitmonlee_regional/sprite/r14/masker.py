# Gelijkmatig oppervlakgewogen masker van het natieve model (136x148 -> 59x64), x-offset 2 zoals ek2.
from PIL import Image; import numpy as np
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/'
a=np.asarray(Image.open(D+'sprite/natief.png').convert('RGB')).astype(float)
lab,n=ndimage.label(a.min(2)>=226)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); rand.discard(0)
fig=~np.isin(lab,list(rand))
H,W=fig.shape; s=64/H
# supersample: elk natief pixel 25 subpixels
k=25
big=np.kron(fig.astype(float),np.ones((k,k)))
SH,SW=64,int(round(W*s))
cov=np.zeros((SH,SW))
BH,BW=big.shape
for y in range(SH):
  y0=int(round(y/s*k)); y1=int(round((y+1)/s*k))
  for x in range(SW):
    x0=int(round(x/s*k)); x1=int(round((x+1)/s*k))
    cov[y,x]=big[y0:y1,x0:x1].mean()
C=np.zeros((64,64)); C[:,2:2+SW]=cov
np.save(D+'sprite/r14/cov.npy',C)
print(SW)
