# gezichten.py RONDE: vel met de gelaatvarianten A-E (hele sprite 1x op licht/donker + uitsnede lijf 8x) en het model
import sys, numpy as np; sys.path.insert(0,'gereedschap'); from gemeen import *
from PIL import Image, ImageDraw
R=sys.argv[1]
def rgb_from(p,bg=(255,255,255)):
    im=Image.open(p); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
UITL={'A':'model (U)','B':'ogen 2x2','C':'2x2 + glans','D':'2x3 + glans','E':'2x2 + mondje'}
box=(14,26,46,42); z=8; W=(box[2]-box[0])*z; H=(box[3]-box[1])*z
v=Image.new('RGB',(6*(W+10),H+120),'white'); d=ImageDraw.Draw(v)
for k,g in enumerate('ABCDE'):
    p='%s/vileplume_%s_gelaat%s.png'%(R,R,g)
    v.paste(rgb_from(p).crop(box).resize((W,H),Image.NEAREST),(k*(W+10),14)); d.text((k*(W+10),1),g+': '+UITL[g],fill=(0,0,0))
    v.paste(rgb_from(p),(k*(W+10),H+20)); v.paste(rgb_from(p,(40,48,56)),(k*(W+10)+70,H+20))
v.paste(model_crop(*box,z),(5*(W+10),14)); d.text((5*(W+10),1),'model',fill=(0,0,0)); v.paste(model_op_schaal(1),(5*(W+10),H+20))
v.save('%s/gezicht_varianten.png'%R)
