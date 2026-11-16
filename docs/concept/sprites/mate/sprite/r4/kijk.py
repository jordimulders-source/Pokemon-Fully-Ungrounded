# kijk.py out sprite1 [sprite2 ...] : 8x zonder raster, uitsnede x8-55 y12-63, model rechts
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image
from meet import crop
S=8; box=(8*S,12*S,56*S,64*S); fs=sys.argv[2:]
def ld(f):
    im=Image.open(f); a=np.asarray(im); p=np.array(im.getpalette()[:768]).reshape(-1,3); r=p[a].astype('uint8'); r[a==0]=255
    return Image.fromarray(r).resize((64*S,64*S),Image.NEAREST).crop(box)
ims=[ld(f) for f in fs]+[crop.resize((64*S,64*S),Image.LANCZOS).crop(box)]
w=ims[0].size[0]; v=Image.new('RGB',((w+8)*len(ims),ims[0].size[1]),'white')
for k,i in enumerate(ims): v.paste(i,(k*(w+8),0))
v.save(sys.argv[1])
