# per spritepixel: aandeel duiglijn-pixels (donkerbruin) en hoepelkern (donkergrijs) in de modelcel
import numpy as np, json
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
a=np.asarray(Image.open(R+'referenties/model_r3.png').convert('RGB')).astype(int)
p=738/46; x0=143; y1=799; H=34
r,g,b=a[...,0],a[...,1],a[...,2]
lijn=(r>=90)&(r<=160)&(g>=38)&(g<=66)&(b<=45)
hoep=(abs(r-g)<12)&(abs(g-b)<20)&(r>=45)&(r<=100)
def frac(mask):
    out=np.zeros((H,46))
    for j in range(H):
        for i in range(46):
            ya,yb=int(round(y1-(H-j)*p)),int(round(y1-(H-j-1)*p)); xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p))
            out[j,i]=mask[max(ya,0):yb,xa:xb].mean()
    return out
np.save(R+'sprite/r2/lijnfrac.npy',frac(lijn)); np.save(R+'sprite/r2/hoepfrac.npy',frac(hoep))
