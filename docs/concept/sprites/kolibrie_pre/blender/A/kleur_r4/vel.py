"""vel.png: r4 op 4x en 1x (licht en donker) naast r3, Taillow, Starly en de toonkaart."""
from PIL import Image, ImageDraw
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def spr(p,front=False):
    im=Image.open(p)
    if front: im=im.crop((0,0,64,64))
    return im.convert('RGBA')
def op(im,z,bg):
    im=im.resize((im.width*z,im.height*z),Image.NEAREST); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b
L=(236,236,236); D=(40,40,56); GR=(152,208,160)
r4=spr(H+'kleur_r4/kolibrie_pre.png'); r3=spr(H+'kleur_r3/kolibrie_pre.png')
ta=spr(G+'taillow/anim_front.png',1); st=spr(G+'starly/anim_front.png',1)
toon=Image.open(H+'toonkaart_8x.png').convert('RGBA').resize((256,256),Image.NEAREST)
row1=[('r4 4x',op(r4,4,L)),('r4 4x donker',op(r4,4,D)),('r3 4x',op(r3,4,L)),('Taillow 4x',op(ta,4,GR)),('Starly 4x',op(st,4,GR)),('toonkaart (4x)',toon)]
row2=[('r4',op(r4,1,L)),('r4',op(r4,1,D)),('r3',op(r3,1,L)),('r3',op(r3,1,D)),('Taillow',op(ta,1,GR)),('Starly',op(st,1,GR)),('r4 2x',op(r4,2,L)),('r4 2x',op(r4,2,D))]
W=16+sum(t.width+16 for _,t in row1); out=Image.new('RGBA',(W,256+16+16+128+16+40),(200,200,200,255)); d=ImageDraw.Draw(out)
x=16
for n,t in row1: out.alpha_composite(t,(x,16)); d.text((x,276),n,fill=(0,0,0)); x+=t.width+16
x=16; y=300
for n,t in row2: out.alpha_composite(t,(x,y)); d.text((x,y+t.height+4),n,fill=(0,0,0)); x+=t.width+16
d.text((16,out.height-14),'kolibrie pre-evo kleur r4 | oog: Latias (graphics/pokemon/latias) | toonkaart = 3D-model wit gerenderd, 4 tonen',fill=(0,0,0))
out.save(H+'kleur_r4/vel.png')
