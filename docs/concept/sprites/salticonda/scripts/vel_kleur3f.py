"""Vel 3f: kleur3e en kleur3f naast elkaar op 4x en 1x (licht en donker) + 8x-uitsnede van de overgang kop/halsband/winding."""
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
ks=['kleur3e','kleur3f']; ims=[Image.open(D+k+'/salticonda.png').convert('RGBA') for k in ks]
LIGHT,DARK=(236,238,240,255),(44,48,56,255)
W=2*(256+110)+30; parts=[]
for bg in (LIGHT,DARK):
    P=Image.new('RGBA',(W,290),bg); d=ImageDraw.Draw(P)
    for i,im in enumerate(ims):
        x=10+i*(256+120)
        P.alpha_composite(im.resize((256,256),Image.NEAREST),(x,4)); P.alpha_composite(im,(x+280,100)); d.text((x,268),ks[i]+' 4x / 1x',fill=(128,128,128,255))
    parts.append(P)
box=(8,14,52,32); w=(box[2]-box[0])*8; h=(box[3]-box[1])*8
P=Image.new('RGBA',(max(W,2*w+30),h+20),LIGHT); d=ImageDraw.Draw(P)
for i,im in enumerate(ims):
    P.alpha_composite(im.crop(box).resize((w,h),Image.NEAREST),(10+i*(w+10),16)); d.text((10+i*(w+10),2),ks[i]+' overgang 8x',fill=(90,90,90,255))
parts.append(P)
W=max(p.width for p in parts)
V=Image.new('RGBA',(W,sum(p.height for p in parts)),LIGHT); y=0
for p in parts: V.alpha_composite(p,(0,y)); y+=p.height
V.save(D+'kleur3f/vel.png')
