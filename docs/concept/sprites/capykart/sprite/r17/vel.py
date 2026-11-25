# vel.py: r17 8x | kaal 8x | model op schaal 8x | Dundragoon 8x | Zapacha 8x | r15b 8x  /  1x op wit, crème, donker + zelfde reeks 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'sprite/r17'); from gemeen import *
SP='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
def rgb_from(path,bg=(255,255,255)):
    im=Image.open(path); 
    if im.mode!='P': im=im.convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
src=[('r17',UIT_:= 'sprite/r17/capykart.png'),('kaal','sprite/r17/kaal16.png'),('model',None),('Dundragoon',SP+'dundragoon/af/dundragoon.png'),('Zapacha',SP+'viscacha/af/viscacha.png'),('Skinguin',SP+'skinguin/af/skinguin.png'),('r15b','sprite/r15b/capykart_creme.png')]
m=model_op_schaal()
pan=[]
for n,p in src:
    im=m if p is None else rgb_from(p); pan.append((n,im))
W=len(pan)*520; v=Image.new('RGB',(W,520+20+3*72+10),'white'); d=ImageDraw.Draw(v)
for i,(n,im) in enumerate(pan):
    v.paste(im.resize((512,512),Image.NEAREST),(i*520,16)); d.text((i*520+4,2),n,fill=(0,0,0))
y=540
for j,bg in enumerate([(255,255,255),(248,248,232),(40,48,56)]):
    for i,(n,p) in enumerate(src):
        im=m if p is None else rgb_from(p,bg); v.paste(im,(i*72+8,y+j*72))
v.save(sys.argv[1] if len(sys.argv)>1 else 'sprite/r17/vel.png'); print(v.size)
