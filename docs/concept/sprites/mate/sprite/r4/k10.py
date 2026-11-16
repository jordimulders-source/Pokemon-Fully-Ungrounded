import sys; sys.path.insert(0,'r4')
from PIL import Image; import numpy as np
from meet import crop
out=sys.argv[1]; fs=sys.argv[2:]
S=10; box=(8*S,12*S,56*S,64*S)
def ld(f):
    im=Image.open(f); a=np.asarray(im); p=np.array(im.getpalette()[:768]).reshape(-1,3); r=p[a].astype('uint8'); r[a==0]=255
    return Image.fromarray(r).resize((640,640),Image.NEAREST).crop(box)
ims=[ld(f) for f in fs]+[crop.resize((640,640),Image.LANCZOS).crop(box)]
w=ims[0].size[0]; v=Image.new('RGB',((w+10)*len(ims),ims[0].size[1]),'white')
for k,i in enumerate(ims): v.paste(i,(k*(w+10),0))
v.save(out)
