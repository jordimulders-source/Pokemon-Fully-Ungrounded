"""Vel 3e: kleur3 en kleur3e naast elkaar; koppen op 9x, geheel op 4x en 1x, licht en donker."""
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
ks=['kleur3','kleur3e']; ims=[Image.open(D+k+'/salticonda.png').convert('RGBA') for k in ks]
LIGHT,DARK=(236,238,240,255),(44,48,56,255)
cw=48*9; W=2*cw+30
parts=[]
for bg in (LIGHT,DARK):
    P=Image.new('RGBA',(W,24*9+22+300),bg); d=ImageDraw.Draw(P)
    for i,im in enumerate(ims):
        x=10+i*(cw+10)
        P.alpha_composite(im.crop((2,0,50,24)).resize((cw,24*9),Image.NEAREST),(x,16)); d.text((x,2),ks[i]+' kop 9x',fill=(128,128,128,255))
        P.alpha_composite(im.resize((256,256),Image.NEAREST),(x,24*9+28)); P.alpha_composite(im,(x+300,24*9+120)); d.text((x+290,24*9+200),ks[i]+' 4x / 1x',fill=(128,128,128,255))
    parts.append(P)
V=Image.new('RGBA',(W,sum(p.height for p in parts)),LIGHT); y=0
for p in parts: V.alpha_composite(p,(0,y)); y+=p.height
V.save(D+'kleur3e/vel.png')
