# Uniform (gelijkmatige) bemonstering van het natieve masker met schaal 64/148 en een (sub)pixelverschuiving.
from PIL import Image; import numpy as np
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/'
a=np.asarray(Image.open(D+'sprite/natief.png').convert('RGB')).astype(float)
lab,n=ndimage.label(a.min(2)>=226)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); rand.discard(0)
fig=~np.isin(lab,list(rand)).astype(bool)
S=64/148
def cov(dy=0.0,dx=2.0,sc=S,k=8):
    # spritecoord (y,x) -> natief (y-dy)/sc, (x-dx)/sc
    t=(np.arange(64*k)+.5)/k
    ny=np.floor((t-dy)/sc).astype(int); nx=np.floor((t-dx)/sc).astype(int)
    vy=(ny>=0)&(ny<fig.shape[0]); vx=(nx>=0)&(nx<fig.shape[1])
    B=np.zeros((64*k,64*k))
    B[np.ix_(vy,vx)]=fig[np.ix_(ny[vy],nx[vx])]
    return B.reshape(64,k,64,k).mean((1,3))
