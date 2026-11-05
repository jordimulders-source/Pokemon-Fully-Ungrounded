"""Vel: DJ Rotom 1x en 4x op licht en donker, onderlaag, 6 game-Rotoms 1x en 3x."""
import sys, numpy as np
from PIL import Image, ImageDraw
REPO='/home/user/Pokemon-Fully-Ungrounded/'
def rgba(path, frame=0):
    im=Image.open(path); a=np.array(im)[frame*64:frame*64+64]
    rgb=np.array(im.convert('RGB'))[frame*64:frame*64+64]
    out=np.zeros((64,64,4),np.uint8); out[...,:3]=rgb; out[...,3]=(a!=0)*255
    return Image.fromarray(out,'RGBA')
me=rgba('../dj_rotom.png')
ond=Image.open(REPO+'docs/concept/sprites/dj_rotom/silhouet_af/onderlaag.png').convert('RGBA')
games=[(n,rgba(REPO+'graphics/pokemon/rotom/'+d+'anim_front.png')) for n,d in
       [('Rotom',''),('Heat','heat/'),('Wash','wash/'),('Frost','frost/'),('Fan','fan/'),('Mow','mow/')]]
LI=(236,236,228,255); DK=(40,44,56,255)
W=64*4*2+64*4+40; H=64*4+20+64*3+20+64+40
vel=Image.new('RGBA',(1200,700),(255,255,255,255)); d=ImageDraw.Draw(vel)
def put(im,x,y,s,bg):
    b=Image.new('RGBA',(64*s,64*s),bg); b.alpha_composite(im.resize((64*s,64*s),Image.NEAREST)); vel.paste(b,(x,y))
d.text((10,4),'DJ Rotom kleur1: 4x licht / 4x donker / onderlaag 4x / 1x',fill=(0,0,0))
put(me,10,20,4,LI); put(me,280,20,4,DK); put(ond,550,20,4,LI)
for i,bg in enumerate([LI,DK]): put(me,820+i*74,20,1,bg)
put(me,820,100,2,LI)
d.text((10,286),'naast de game-Rotoms op 3x (licht) en 1x (licht/donker)',fill=(0,0,0))
x=10
for n,g in [('DJ',me)]+games:
    put(g,x,300,3,LI); d.text((x,494),n,fill=(0,0,0)); x+=196
    if x>1100: break
x=10; y=520
for n,g in [('DJ',me)]+games:
    put(g,x,y,1,LI); put(g,x,y+70,1,DK); d.text((x,y+138),n,fill=(0,0,0)); x+=80
vel.convert('RGB').save(sys.argv[1] if len(sys.argv)>1 else '../vel.png')
