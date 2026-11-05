# Masker van de vogel uit foto 4 (kleursegmentatie), gespiegeld zodat hij naar links kijkt.
import numpy as np, sys
from PIL import Image, ImageFilter
from scipy import ndimage
R='docs/concept/sprites/picapau/referenties/'
im=Image.open(R+'jordi_foto4_rechtop_snavel_omhoog.png').convert('RGB')
a=np.asarray(im).astype(float)/255
r,g,b=a[...,0],a[...,1],a[...,2]
mx=a.max(-1); mn=a.min(-1); s=(mx-mn)/(mx+1e-6)
h=np.zeros_like(mx)
d=mx-mn+1e-6
h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
geel=(h>30)&(h<68)&(s>0.14)&(mx>0.62)&(r>g*0.88)
bruin=((h<40)|(h>330))&(mx<0.62)&(s>0.18)
rood=((h<20)|(h>320))&(s>0.4)
m=geel|bruin|rood
m=ndimage.binary_opening(m,iterations=2)
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
m=lab==(np.argmax(sizes)+1)
m=ndimage.binary_closing(m,iterations=6); m=ndimage.binary_fill_holes(m)
out=Image.fromarray((m*255).astype('uint8')).transpose(Image.FLIP_LEFT_RIGHT)
out.save('docs/concept/sprites/picapau/silhouet/masker_foto4.png')
ov=im.transpose(Image.FLIP_LEFT_RIGHT).copy(); ovp=np.asarray(ov).copy(); mm=np.asarray(out)>0
edge=mm ^ ndimage.binary_erosion(mm,iterations=3)
ovp[edge]=[255,0,0]; Image.fromarray(ovp).resize((320,512)).save('docs/concept/sprites/picapau/silhouet/masker_foto4_check.png')
