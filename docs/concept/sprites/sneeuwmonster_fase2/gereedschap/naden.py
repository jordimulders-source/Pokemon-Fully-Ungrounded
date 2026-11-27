# Duignaden in de emmer meten: houtpixels die >=22 donkerder zijn dan het lokale houtgemiddelde (17x17) + zwart in de emmer.
# naad_kaart() -> aandeel naadpixels per spritepixel (64x64), en per spritepixel het houtaandeel.
import numpy as np; from PIL import Image, ImageFilter
from gemeen import *; from klassen import klassen
def naad_kaart():
    a,c,L=klassen(); hout=(c==3)
    def blur(v,r=8):
        k=np.cumsum(np.cumsum(np.pad(v.astype(float),((r+1,r),(r+1,r))),0),1)
        return k[2*r+1:,2*r+1:]-k[:-2*r-1,2*r+1:]-k[2*r+1:,:-2*r-1]+k[:-2*r-1,:-2*r-1]
    mean=blur(np.where(hout,L,0))/np.maximum(blur(hout.astype(float)),1e-6)
    H,W=L.shape; yy=np.arange(H)[:,None]
    naad=(hout&(L<mean-22))|((c==1)&(yy<175))
    out=np.zeros((64,64)); hw=np.zeros((64,64))
    for Y in range(0,20):
        for X in range(20,50):
            sl=(slice(max(0,int(MY0+Y*F)),int(MY0+(Y+1)*F)),slice(int(MX0+X*F),int(MX0+(X+1)*F)))
            out[Y,X]=naad[sl].mean(); hw[Y,X]=((c[sl]==3)|(c[sl]==1)).mean()
    return out,hw
if __name__=='__main__':
    n,h=naad_kaart()
    print('     '+''.join('%-3d'%(x%100) for x in range(24,48)))
    for Y in range(3,19): print('%2d   '%Y+''.join(' . ' if h[Y,X]<0.3 else '%2d '%min(99,int(n[Y,X]*100)) for X in range(24,48)))
