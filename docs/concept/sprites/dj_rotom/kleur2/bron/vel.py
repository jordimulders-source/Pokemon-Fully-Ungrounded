"""Vel kleur2: varianten 4x licht/donker + 1x, kleur1, onderlaag s1.25, 6 game-Rotoms 1x/3x, gezicht 8x naast de bron.
Gebruik: python3 vel.py A [B ...]"""
import sys, numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/dj_rotom/'
def rgba(path):
    im=Image.open(path); a=np.array(im)[:64]; rgb=np.array(im.convert('RGB'))[:64]
    o=np.zeros((64,64,4),np.uint8); o[...,:3]=rgb; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
Vs=sys.argv[1:]
mes=[(v,rgba(D+'kleur2/dj_rotom_%s.png'%v)) for v in Vs]
k1=rgba(D+'kleur1/dj_rotom.png'); ond=Image.open(D+'silhouet3/s1.25/onderlaag.png').convert('RGBA')
games=[(n,rgba(R+'graphics/pokemon/rotom/'+d+'anim_front.png')) for n,d in
  [('Rotom',''),('Heat','heat/'),('Wash','wash/'),('Frost','frost/'),('Fan','fan/'),('Mow','mow/')]]
LI=(236,236,228,255); DK=(40,44,56,255)
Hh=20+len(Vs)*276+220+170+380
vel=Image.new('RGBA',(1360,Hh),(255,255,255,255)); d=ImageDraw.Draw(vel)
def put(im,x,y,s,bg):
    b=Image.new('RGBA',(im.width*s,im.height*s),bg); b.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); vel.paste(b,(x,y))
y=4
for v,me in mes:
    d.text((10,y),'kleur2 variant %s: 4x licht / 4x donker / 1x / onderlaag s1.25 4x'%v,fill=(0,0,0))
    put(me,10,y+16,4,LI); put(me,280,y+16,4,DK); put(me,550,y+16,1,LI); put(me,550,y+90,1,DK); put(ond,630,y+16,4,LI)
    y+=276
d.text((10,y),'naast kleur1 en de game-Rotoms (3x)',fill=(0,0,0)); y+=16
x=10
for n,g in mes+[('kleur1',k1)]+games[1:4]:
    put(g,x,y,3,LI); d.text((x,y+194),str(n),fill=(0,0,0)); x+=196
y+=212
x=10
for n,g in mes+[('kleur1',k1)]+games:
    put(g,x,y,1,LI); put(g,x,y+68,1,DK); d.text((x,y+134),str(n),fill=(0,0,0)); x+=74
y+=160
# gezicht 8x naast de bron
bron=Image.open(D+'referenties/pokopia_dj_rotom_bron.webp').convert('RGBA').crop((620,900,1180,1560)).resize((280,330))
vel.paste(bron,(10,y)); x=300
for v,me in mes:
    put(me.crop((12,24,36,60)),x,y,8,LI) if False else None
    c=me.crop((13,25,36,58)); put(c,x,y,8,LI); d.text((x,y+266),'gezicht %s 8x'%v,fill=(0,0,0)); x+=c.width*8+20
vel.convert('RGB').save(D+'kleur2/vel.png')
