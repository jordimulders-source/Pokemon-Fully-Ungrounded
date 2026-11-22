# naast.py UIT A.png [B.png ...]: elk 4x en 2x en 1x naast het model op dezelfde schaal
import sys; sys.path.insert(0,'gereedschap'); from gemeen import model_op_schaal; from PIL import Image; import numpy as np
def r(p,z):
    im=Image.open(p); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3); img=np.full((64,64,3),255,'uint8')
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img).resize((64*z,64*z),Image.NEAREST)
fs=sys.argv[2:]; n=len(fs)+1
v=Image.new('RGB',(n*264,264+140),'white')
for j,f in enumerate(fs):
    v.paste(r(f,4),(j*264,0)); v.paste(r(f,2),(j*264,268)); v.paste(r(f,1),(j*264+140,268))
v.paste(model_op_schaal(4),(len(fs)*264,0)); v.paste(model_op_schaal(2),(len(fs)*264,268)); v.paste(model_op_schaal(1),(len(fs)*264+140,268))
v.save(sys.argv[1])
