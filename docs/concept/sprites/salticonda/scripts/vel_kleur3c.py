"""Vel kleurronde 3c: kleur3, 3b en 3c naast elkaar; koppen op 9x, geheel op 4x en 1x (licht en donker)."""
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
ks=['kleur3','kleur3b','kleur3c']
ims=[Image.open(D+k+'/salticonda.png').convert('RGBA') for k in ks]
LIGHT,DARK=(236,238,240,255),(44,48,56,255)
cw9=(52-2)*9
W=3*cw9+40
kop=Image.new('RGBA',(W,26*9+18),LIGHT); d=ImageDraw.Draw(kop)
for i,im in enumerate(ims):
    kop.alpha_composite(im.crop((2,0,52,26)).resize((cw9,26*9),Image.NEAREST),(10+i*(cw9+10),16)); d.text((10+i*(cw9+10),2),ks[i]+' kop 9x',fill=(90,90,90,255))
parts=[kop]
for bg in (LIGHT,DARK):
    P=Image.new('RGBA',(W,256+90),bg); d=ImageDraw.Draw(P)
    for i,im in enumerate(ims):
        x=10+i*(cw9+10)
        P.alpha_composite(im.resize((256,256),Image.NEAREST),(x,4)); P.alpha_composite(im,(x+290,100)); d.text((x,264),ks[i]+' 4x / 1x',fill=(128,128,128,255))
    parts.append(P)
V=Image.new('RGBA',(W,sum(p.height for p in parts)),LIGHT); y=0
for p in parts: V.alpha_composite(p,(0,y)); y+=p.height
V.save(D+'kleur3c/vel.png')
