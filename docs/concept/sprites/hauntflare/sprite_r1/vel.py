# Vel: sprite 8x | verkleind model (zelfde schrapping, zonder kleur/gezichtwijziging) 8x | Haunter Gen 3 8x,
# plus 1x (en 2x) op licht en donker.
from PIL import Image, ImageDraw; import numpy as np
S='docs/concept/sprites/hauntflare/sprite_r1/'
spr=Image.open(S+'hauntflare_r1.png').convert('RGBA')
mod=np.asarray(Image.open(S+'model64.png').convert('RGB'))
ma=np.dstack([mod,np.where(mod.min(2)>=0xf0,0,255).astype('uint8')]); mod=Image.fromarray(ma,'RGBA')
h=Image.open('graphics/pokemon/haunter/anim_front.png'); hi=np.array(h)[:64]; hp=np.array(h.getpalette()[:48]).reshape(16,3)
ha=np.dstack([hp[hi],np.where(hi==0,0,255)]).astype('uint8'); hau=Image.fromarray(ha,'RGBA')
def op(im,bg,f):
    b=Image.new('RGBA',(64*f,64*f),bg); b.alpha_composite(im.resize((64*f,64*f),Image.NEAREST)); return b
W=3*512+4*16; H=16+512+40+128+40
v=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate([(spr,'Hauntflare r1'),(mod,'model geschrapt (64x64)'),(hau,'Haunter Gen 3')]):
    x=16+k*(512+16); v.paste(op(im,(255,255,255,255),8),(x,16)); d.rectangle([x-1,15,x+512,16+512],outline=(200,200,200)); d.text((x,16+512+4),t,fill=(0,0,0))
y=16+512+40; x=16
for bg in [(255,255,255,255),(248,248,232,255),(40,40,48,255),(16,16,16,255)]:
    v.paste(op(spr,bg,1),(x,y)); x+=64+12
for bg in [(248,248,232,255),(40,40,48,255)]:
    v.paste(op(spr,bg,2),(x,y)); x+=128+12
v.convert('RGB').save(S+'vel.png')
