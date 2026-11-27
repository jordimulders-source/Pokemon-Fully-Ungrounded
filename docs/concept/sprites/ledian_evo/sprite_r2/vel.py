# vel.png: r2 8x | r1 8x | Gen 3-Ledian 8x; daaronder rood a/b/c 8x; daaronder 1x en 2x op licht en donker.
# vergelijk.png: r2 naast Dundragoon, Skinguin, Princadee (maatstaf) en Ledian G3, alles 8x.
from PIL import Image, ImageDraw
import numpy as np
D='docs/concept/sprites/ledian_evo/sprite_r2/'; S='docs/concept/sprites/'
def first(fn):
    im=Image.open(fn).crop((0,0,64,64))
    if im.mode=='P':
        a=np.array(im); r=np.array(im.convert('RGBA')); r[a==0,3]=0; return Image.fromarray(r)
    return im.convert('RGBA')
def op(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
def x8(im): return im.resize((512,512),Image.NEAREST)
L=(240,240,232,255); Dk=(48,56,72,255)
r2=first(D+'ledian_evo_r2.png'); x8(r2).save(D+'ledian_evo_r2_8x.png')
r1=first(S+'ledian_evo/sprite_r1/ledian_evo_r1.png'); led=first('graphics/pokemon/ledian/anim_front_gba.png')
var={k:first(D+f'rood_{k}.png') for k in 'abc'}
for k,v in var.items(): x8(v).save(D+f'rood_{k}_8x.png')
v=Image.new('RGB',(3*532,2*532+150),(200,200,210)); d=ImageDraw.Draw(v)
for i,(im,t) in enumerate([(r2,'r2 (= rood b)'),(r1,'r1'),(led,'Ledian Gen 3')]):
    v.paste(op(x8(im),L),(i*532,0)); d.text((i*532+4,4),t,fill=(0,0,0))
for i,k in enumerate('abc'):
    v.paste(op(x8(var[k]),L),(i*532,532)); d.text((i*532+4,536),f'rood {k}'+(' (hoofd)' if k=='b' else ''),fill=(0,0,0))
y=1064+10; x=10
for im in [r2,var['a'],var['c'],r1,led]:
    v.paste(op(im,L),(x,y)); v.paste(op(im,Dk),(x,y+70)); x+=74
for im in [r2,led]:
    v.paste(op(im.resize((128,128),Image.NEAREST),L),(x,y)); v.paste(op(im.resize((128,128),Image.NEAREST),Dk),(x+136,y)); x+=280
v.save(D+'vel.png')
refs=[r2,first(S+'dundragoon/af/dundragoon.png'),first(S+'skinguin/af/skinguin.png'),first(S+'awki/af/awki.png'),led]
c=Image.new('RGB',(5*520,520),(240,240,232))
for i,r in enumerate(refs): c.paste(op(x8(r),L),(i*520,0))
c.save(D+'vergelijk.png')
