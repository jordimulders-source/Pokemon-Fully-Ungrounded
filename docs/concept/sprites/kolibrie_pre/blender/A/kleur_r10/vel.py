"""vel.png: r10 op 4x en 1x (licht/donker) naast r9 en een uitsnede van Jordi's foto (gespiegeld, zodat hij ook naar links kijkt)."""
from PIL import Image, ImageDraw, ImageOps
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/'
def op(im,z,bg):
    im=im.resize((im.width*z,im.height*z),Image.NEAREST); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b
L=(236,236,236); D=(40,40,56)
r10=Image.open(A+'blender/A/kleur_r10/kolibrie_pre.png').convert('RGBA'); r9=Image.open(A+'blender/A/kleur_r9/kolibrie_pre.png').convert('RGBA')
foto=Image.open(A+'referenties/jordi_8_moeder_hals_buik.png').convert('RGBA').crop((200,50,460,330))
foto=ImageOps.mirror(foto).resize((256,int(256*foto.height/foto.width)))
rij1=[('r10 4x',op(r10,4,L)),('r10 4x donker',op(r10,4,D)),('r9 4x',op(r9,4,L)),('foto (gespiegeld)',foto)]
rij2=[('r10',op(r10,1,L)),('r10',op(r10,1,D)),('r9',op(r9,1,L)),('r9',op(r9,1,D))]
H=max(t.height for _,t in rij1)
W=16+sum(t.width+16 for _,t in rij1); out=Image.new('RGBA',(W,16+H+20+64+40),(200,200,200,255)); d=ImageDraw.Draw(out); x=16
for n,t in rij1: out.alpha_composite(t,(x,16)); d.text((x,20+H),n,fill=(0,0,0)); x+=t.width+16
x=16
for n,t in rij2: out.alpha_composite(t,(x,40+H)); d.text((x,40+H+68),n,fill=(0,0,0)); x+=t.width+16
out.save(A+'blender/A/kleur_r10/vel.png')
