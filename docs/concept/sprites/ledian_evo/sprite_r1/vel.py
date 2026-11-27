# vel.png: sprite 8x | kaal 8x | model verkleind, plus 1x op licht en donker; vergelijk.png: naast maatstaf + Gen 3
from PIL import Image
import os
D='docs/concept/sprites/ledian_evo/sprite_r1/'; S='docs/concept/sprites/'
def rgba(fn):
    im=Image.open(fn); return im.convert('RGBA')
def op(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
s=rgba(D+'ledian_evo_r1.png'); k=rgba(D+'kaal.png')
s.resize((512,512),Image.NEAREST).save(D+'ledian_evo_r1_8x.png')
m=Image.open(S+'ledian_evo/gemini/r6.png').convert('RGB').crop((174,153,850,829)).resize((512,512),Image.LANCZOS)
L=(240,240,232,255); Dk=(48,56,72,255)
v=Image.new('RGB',(512*3+40,512+100),(200,200,210))
v.paste(op(s.resize((512,512),Image.NEAREST),L),(0,0)); v.paste(op(k.resize((512,512),Image.NEAREST),L),(532,0)); v.paste(m,(1064,0))
v.paste(op(s,L),(10,525)); v.paste(op(s,Dk),(84,525)); v.paste(op(s.resize((128,128),Image.NEAREST),L),(160,500+12)); v.paste(op(s.resize((128,128),Image.NEAREST),Dk),(300,512))
v.save(D+'vel.png')
def first(fn):
    im=Image.open(fn).crop((0,0,64,64))
    if im.mode=='P':
        import numpy as np
        a=np.array(im); r=np.array(im.convert('RGBA')); r[a==0,3]=0; return Image.fromarray(r)
    return im.convert('RGBA')
refs=[s,first(S+'dundragoon/af/dundragoon.png'),first(S+'skinguin/af/skinguin.png'),first(S+'awki/af/awki.png'),first('graphics/pokemon/ledian/anim_front_gba.png'),first('graphics/pokemon/scizor/anim_front_gba.png')]
c=Image.new('RGB',(6*520,520),(240,240,232))
for i,r in enumerate(refs): c.paste(op(r.resize((512,512),Image.NEAREST),L),(i*520,0))
c.save(D+'vergelijk.png')
