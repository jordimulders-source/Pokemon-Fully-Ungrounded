# maakt ../vel.png: kop op 8x (ronde 2 | ronde 3 | onderlaag), sprite 4x en 1x op licht en donker
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(H,'../../../')
def ld(p):
    im=Image.open(p); idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
r2=ld(os.path.join(H,'../../ronde2/nachtaap.png')); r3=ld(os.path.join(H,'../nachtaap.png'))
ond=Image.open(os.path.join(D,'silhouet/onderlaag_256.png')).convert('RGBA')
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(980,480),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
put(r2.crop((2,34,28,57)),0,0,L,'ronde 2, kop 8x',8); put(r3.crop((2,34,28,57)),216,0,L,'ronde 3, kop 8x',8)
put(ond.crop((8,136,112,228)),432,0,(255,255,255,255),'onderlaag, zelfde plek',2)
put(r3,0,210,L,'ronde 3, 4x',4); put(r3,266,210,DK,'op donker',4)
put(r2,560,210,L,'r2 1x'); put(r3,640,210,L,'r3 1x'); put(r3,720,210,DK,'r3 donker')
put(r3,560,300,L,'r3 3x',3)
o.save(os.path.join(H,'../vel.png'))
