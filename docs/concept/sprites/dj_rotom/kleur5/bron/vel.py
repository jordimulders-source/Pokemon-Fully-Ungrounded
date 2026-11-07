"""Vel kleur5: 3x en 1x licht/donker naast kleur4 en de 6 Rotoms; 8x spits, tanden, contour (kleur5 | kleur4 | game)."""
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/dj_rotom/'
def rgba(p):
    im=Image.open(p); a=np.array(im)[:64]; rgb=np.array(im.convert('RGB'))[:64]
    o=np.zeros((64,64,4),np.uint8); o[...,:3]=rgb; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
k5=rgba(D+'kleur5/dj_rotom.png'); k4=rgba(D+'kleur4/dj_rotom.png')
G=[(n,rgba(R+'graphics/pokemon/rotom/'+d+'anim_front.png')) for n,d in [('Rotom',''),('Heat','heat/'),('Wash','wash/'),('Frost','frost/'),('Fan','fan/'),('Mow','mow/')]]
LI=(236,236,228,255); DK=(40,44,56,255)
vel=Image.new('RGBA',(1620,1220),(255,255,255,255)); d=ImageDraw.Draw(vel)
def put(im,x,y,s,bg):
    b=Image.new('RGBA',(im.width*s,im.height*s),bg); b.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); vel.paste(b,(x,y))
d.text((10,4),'3x licht (boven) en donker (onder): kleur5, kleur4, Rotom, Heat, Wash, Frost, Fan, Mow',fill=(0,0,0))
x=10
for n,im in [('kleur5',k5),('kleur4',k4)]+G:
    put(im,x,20,3,LI); put(im,x,216,3,DK); d.text((x,410),n,fill=(0,0,0)); x+=200
y=430; d.text((10,y),'1x licht / donker',fill=(0,0,0)); y+=16; x=10
for n,im in [('kleur5',k5),('kleur4',k4)]+G:
    put(im,x,y,1,LI); put(im,x,y+68,1,DK); d.text((x,y+134),n,fill=(0,0,0)); x+=74
y+=156
def rij(titel,box5,games):
    global y
    d.text((10,y),titel,fill=(0,0,0)); y+=16; x=10; h=0
    for n,im,box in [('kleur5',k5,box5),('kleur4',k4,box5)]+games:
        c=im.crop(box); put(c,x,y,8,LI); d.text((x,y+c.height*8+2),n,fill=(0,0,0)); x+=c.width*8+14; h=max(h,c.height*8)
    y+=h+22
gd=dict(G)
rij('8x spits',(19,4,34,34),[('Wash',gd['Wash'],(22,3,38,20)),('Frost',gd['Frost'],(20,2,36,16))])
rij('8x tanden',(19,40,30,46),[('Wash',gd['Wash'],(22,24,32,29)),('Heat',gd['Heat'],(22,35,30,40))])
rij('8x contour rechtsonder',(46,46,63,63),[('Frost',gd['Frost'],(38,44,52,60)),('Wash',gd['Wash'],(36,40,50,56))])
vel.convert('RGB').save(D+'kleur5/vel.png')
