"""Vel kleur3: 4x licht/donker, 1x; naast B, bron, Heat/Wash/Frost (1x, 3x); bliksem en gezicht 8x naast de bron."""
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/dj_rotom/'
def rgba(path):
    im=Image.open(path); a=np.array(im)[:64]; rgb=np.array(im.convert('RGB'))[:64]
    o=np.zeros((64,64,4),np.uint8); o[...,:3]=rgb; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
me=rgba(D+'kleur3/dj_rotom.png'); B=rgba(D+'kleur2/dj_rotom_B.png')
bron=Image.open(D+'referenties/pokopia_dj_rotom_bron.webp').convert('RGBA')
g=[(n,rgba(R+'graphics/pokemon/rotom/'+d+'/anim_front.png')) for n,d in [('Heat','heat'),('Wash','wash'),('Frost','frost')]]
LI=(236,236,228,255); DK=(40,44,56,255)
vel=Image.new('RGBA',(1300,1180),(255,255,255,255)); d=ImageDraw.Draw(vel)
def put(im,x,y,s,bg):
    b=Image.new('RGBA',(im.width*s,im.height*s),bg); b.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); vel.paste(b,(x,y))
d.text((10,4),'kleur3: 4x licht / 4x donker / 1x licht+donker / bron',fill=(0,0,0))
put(me,10,20,4,LI); put(me,280,20,4,DK); put(me,550,20,1,LI); put(me,550,90,1,DK)
bk=Image.new('RGBA',bron.size,LI); bk.alpha_composite(bron); vel.paste(bk.resize((256,256)).convert('RGB'),(630,20))
y=290; d.text((10,y),'3x: kleur3, kleur2 B, Heat, Wash, Frost',fill=(0,0,0)); y+=16; x=10
for n,im in [('kleur3',me),('kleur2 B',B)]+g:
    put(im,x,y,3,LI); d.text((x,y+194),n,fill=(0,0,0)); x+=200
y+=212; x=10
for n,im in [('kleur3',me),('B',B)]+g:
    put(im,x,y,1,LI); put(im,x,y+68,1,DK); d.text((x,y+134),n,fill=(0,0,0)); x+=74
y+=152; d.text((10,y),'8x: bliksem en gezicht kleur3 | kleur2 B | bron',fill=(0,0,0)); y+=16
c=me.crop((14,12,37,58)); put(c,10,y,8,LI)
c2=B.crop((14,12,37,58)); put(c2,10+23*8+10,y,8,LI)
br=bk.crop((640,280,1190,1560)).resize((int(550*368/1280),368)); vel.paste(br.convert('RGB'),(10+2*(23*8+10),y))
vel.convert('RGB').save(D+'kleur3/vel.png')
