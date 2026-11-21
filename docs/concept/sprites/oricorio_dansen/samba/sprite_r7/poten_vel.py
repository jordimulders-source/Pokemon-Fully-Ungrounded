# poten_vel.py: poten 12x naast elkaar: gegeven pngs | model (zelfde uitsnede) | Baile
import sys; from PIL import Image
z=12; box=(18,40,40,63)
def op(p,box):
    im=Image.open(p).convert('RGBA').crop(box); b=Image.new('RGB',(im.width*z,im.height*z),'white'); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
def maak(paden,out):
    ims=[op(p,box) for p in paden]
    m=Image.open('../model/gemini_r10.png').convert('RGB'); k=950.272/64
    ims.append(m.crop((int(19.3344+box[0]*k),int(29.216+box[1]*k),int(19.3344+box[2]*k),int(29.216+box[3]*k))).resize(ims[0].size,Image.LANCZOS))
    ims.append(op('../../../../../../graphics/pokemon/oricorio/anim_front.png',(14,40,36,63)))
    W=Image.new('RGB',(len(ims)*(ims[0].width+10),ims[0].height),(230,230,230))
    for i,im in enumerate(ims): W.paste(im,(i*(im.width+10),0))
    W.save(out); return W
if __name__=='__main__': maak(sys.argv[2:],sys.argv[1])
