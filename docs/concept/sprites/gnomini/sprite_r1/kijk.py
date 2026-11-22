# kijk.py UIT.png sprite1.png [sprite2.png ...]: snel naast elkaar op 8x (uitsnede figuur) + model op schaal
import sys, numpy as np; from PIL import Image
from gemeen import *
def lees(p):
    im=Image.open(p); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.full((64,64,3),255,'uint8')
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def model_op_schaal():
    a=np.asarray(Image.open('natief.png')).astype(float); out=np.full((64,64,3),255.)
    for Y in range(64):
        for X in range(64):
            ua=CXN+(X-CXS)/S; ub=ua+1/S; va=BOTN-(BOTS-Y)/S; vb=va+1/S; acc=np.zeros(3); tw=0
            for v in range(int(np.floor(va)),int(np.ceil(vb))):
                for u in range(int(np.floor(ua)),int(np.ceil(ub))):
                    w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))
                    if w>1e-9: acc+=w*a[v,u]; tw+=w
            out[Y,X]=acc/tw
    return Image.fromarray(out.astype('uint8'))
ims=[lees(p) for p in sys.argv[2:]]+[model_op_schaal()]
box=(10,14,54,62); z=8
W=Image.new('RGB',((box[2]-box[0])*z*len(ims)+8*len(ims),(box[3]-box[1])*z),'white')
for i,im in enumerate(ims): W.paste(im.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST),(i*((box[2]-box[0])*z+8),0))
W.save(sys.argv[1])
