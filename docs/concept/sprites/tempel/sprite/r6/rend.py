# rend.py a.txt b.txt out.png [z] : twee rasters naast elkaar + model, op zoom z
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'../r1/stappen'); from pal import PAL
C='.X+abcdemnopz'
def img(f,z):
    R=[l.rstrip('\n') for l in open(f)][:64]; G=np.array([[C.index(ch) for ch in r] for r in R])
    rgb=np.array(PAL,dtype='uint8')[G]; rgb[G==0]=255
    return Image.fromarray(rgb).resize((64*z,64*z),Image.NEAREST)
z=int(sys.argv[4]) if len(sys.argv)>4 else 8
s=(983-46)/62; X0,Y0=46-s,57-3*s
m=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp').convert('RGB').crop((int(X0),int(Y0),int(X0+64*s),int(Y0+64*s))).resize((64*z,64*z),Image.LANCZOS)
o=Image.new('RGB',(3*64*z+16,64*z),'white'); o.paste(img(sys.argv[1],z),(0,0)); o.paste(img(sys.argv[2],z),(64*z+8,0)); o.paste(m,(128*z+16,0)); o.save(sys.argv[3])
