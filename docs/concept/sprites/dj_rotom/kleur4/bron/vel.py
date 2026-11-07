"""Vel kleur4: 1x/3x licht+donker naast kleur3 en de bron; bliksem 8x naast kleur3 en de bron; ogen 8x naast Rotom en Frost; 1x naast Heat/Wash/Frost."""
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/dj_rotom/'
def rgba(p):
    im=Image.open(p); a=np.array(im)[:64]; rgb=np.array(im.convert('RGB'))[:64]
    o=np.zeros((64,64,4),np.uint8); o[...,:3]=rgb; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
k4=rgba(D+'kleur4/dj_rotom.png'); k3=rgba(D+'kleur3/dj_rotom.png')
G={n:rgba(R+'graphics/pokemon/rotom/'+d+'anim_front.png') for n,d in [('Rotom',''),('Heat','heat/'),('Wash','wash/'),('Frost','frost/')]}
bron=Image.open(D+'referenties/pokopia_dj_rotom_bron.webp').convert('RGBA')
LI=(236,236,228,255); DK=(40,44,56,255)
vel=Image.new('RGBA',(1240,1200),(255,255,255,255)); d=ImageDraw.Draw(vel)
def put(im,x,y,s,bg):
    b=Image.new('RGBA',(im.width*s,im.height*s),bg); b.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); vel.paste(b,(x,y))
def putbron(box,x,y,h,bg):
    c=bron.crop(box); w=int(c.width*h/c.height); b=Image.new('RGBA',(w,h),bg); b.alpha_composite(c.resize((w,h))); vel.paste(b,(x,y))
d.text((10,4),'3x licht / donker: kleur4 | kleur3 | bron',fill=(0,0,0))
put(k4,10,20,3,LI); put(k4,210,20,3,DK); put(k3,410,20,3,LI); put(k3,610,20,3,DK); putbron((0,200,1920,1700),810,20,192,LI)
y=225; d.text((10,y),'1x licht / donker: kleur4, kleur3, Heat, Wash, Frost, Rotom',fill=(0,0,0)); y+=16; x=10
for n,im in [('kleur4',k4),('kleur3',k3)]+list(G.items()):
    put(im,x,y,1,LI); put(im,x,y+68,1,DK); d.text((x,y+134),n,fill=(0,0,0)); x+=74
y+=156; d.text((10,y),'8x bliksem: kleur4 licht | kleur4 donker | kleur3 | bron',fill=(0,0,0)); y+=16
c=k4.crop((16,6,34,28)); put(c,10,y,8,LI); put(c,10+18*8+10,y,8,DK); put(k3.crop((16,6,34,28)),10+2*(18*8+10),y,8,LI)
putbron((680,280,1000,960),10+3*(18*8+10),y,176,LI)
y+=190; d.text((10,y),'8x ogen: kleur4 | kleur3 | Frost | Rotom',fill=(0,0,0)); y+=16
put(k4.crop((16,33,32,44)),10,y,8,LI); put(k3.crop((16,33,32,44)),150,y,8,LI)
put(G['Frost'].crop((17,15,35,24)),290,y,8,LI); put(G['Rotom'].crop((19,25,36,34)),450,y,8,LI)
y+=100; d.text((10,y),'gezicht 8x: kleur4 | bron',fill=(0,0,0)); y+=16
put(k4.crop((14,30,36,58)),10,y,8,LI); putbron((620,900,1180,1560),200,y,224,LI)
vel.convert('RGB').save(D+'kleur4/vel.png')
