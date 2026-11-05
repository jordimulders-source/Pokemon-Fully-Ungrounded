"""vel.png: r8 naast r7, Taillow, Starly (4x en 1x, licht en donker)."""
from PIL import Image, ImageDraw
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def spr(p,front=False):
    im=Image.open(p); im=im.crop((0,0,64,64)) if front else im; return im.convert('RGBA')
def op(im,z,bg):
    im=im.resize((im.width*z,im.height*z),Image.NEAREST); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b
L=(236,236,236); D=(40,40,56); GR=(152,208,160)
r8=spr(A+'kleur_r8/kolibrie_pre.png'); r7=spr(A+'kleur_r7/kolibrie_pre.png')
ta=spr(G+'taillow/anim_front.png',1); st=spr(G+'starly/anim_front.png',1)
rij1=[('r8 4x',op(r8,4,L)),('r8 4x donker',op(r8,4,D)),('r7 4x',op(r7,4,L)),('Taillow 4x',op(ta,4,GR)),('Starly 4x',op(st,4,GR))]
rij2=[('r8',op(r8,1,L)),('r8',op(r8,1,D)),('r7',op(r7,1,L)),('r7',op(r7,1,D)),('Taillow',op(ta,1,GR)),('Starly',op(st,1,GR))]
W=16+sum(t.width+16 for _,t in rij1); out=Image.new('RGBA',(W,380),(200,200,200,255)); d=ImageDraw.Draw(out); x=16
for n,t in rij1: out.alpha_composite(t,(x,16)); d.text((x,276),n,fill=(0,0,0)); x+=t.width+16
x=16
for n,t in rij2: out.alpha_composite(t,(x,296)); d.text((x,364),n,fill=(0,0,0)); x+=t.width+16
out.save(A+'kleur_r8/vel.png')
