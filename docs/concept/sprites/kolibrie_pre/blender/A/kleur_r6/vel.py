"""vel.png (r6 M naast r5, Taillow, Starly, toonkaart; 4x/1x licht+donker) en oog_maten.png (S/M/L op 4x en 1x naast Starly en Taillow)."""
from PIL import Image, ImageDraw
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def spr(p,front=False):
    im=Image.open(p); im=im.crop((0,0,64,64)) if front else im; return im.convert('RGBA')
def op(im,z,bg):
    im=im.resize((im.width*z,im.height*z),Image.NEAREST); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b
L=(236,236,236); D=(40,40,56); GR=(152,208,160)
ta=spr(G+'taillow/anim_front.png',1); st=spr(G+'starly/anim_front.png',1)
def vel(rij1,rij2,titel,pad):
    W=16+max(sum(t.width+16 for _,t in rij1),sum(t.width+16 for _,t in rij2))
    out=Image.new('RGBA',(W,16+256+20+64+40),(200,200,200,255)); d=ImageDraw.Draw(out); x=16
    for n,t in rij1: out.alpha_composite(t,(x,16)); d.text((x,276),n,fill=(0,0,0)); x+=t.width+16
    x=16
    for n,t in rij2: out.alpha_composite(t,(x,296)); d.text((x,364),n,fill=(0,0,0)); x+=t.width+16
    d.text((16,out.height-14),titel,fill=(0,0,0)); out.save(pad)
r6=spr(A+'kleur_r6/kolibrie_pre.png'); r5=spr(A+'kleur_r5/kolibrie_pre.png')
toon=Image.open(A+'toonkaart_8x.png').convert('RGBA').resize((256,256),Image.NEAREST)
vel([('r6 4x',op(r6,4,L)),('r6 4x donker',op(r6,4,D)),('r5 4x',op(r5,4,L)),('Taillow 4x',op(ta,4,GR)),('Starly 4x',op(st,4,GR)),('toonkaart',toon)],
    [('r6',op(r6,1,L)),('r6',op(r6,1,D)),('r5',op(r5,1,L)),('r5',op(r5,1,D)),('Taillow',op(ta,1,GR)),('Starly',op(st,1,GR))],
    'kolibrie pre-evo kleur r6 (oog M = Starly-oog) naast r5, Taillow, Starly',A+'kleur_r6/vel.png')
S,M,Lg=[spr(A+f'kleur_r6/kolibrie_pre_{m}.png') for m in 'SML']
vel([('S 4x',op(S,4,L)),('M 4x',op(M,4,L)),('L 4x',op(Lg,4,L)),('Starly 4x',op(st,4,GR)),('Taillow 4x',op(ta,4,GR))],
    [('S',op(S,1,L)),('M',op(M,1,L)),('L',op(Lg,1,L)),('S',op(S,1,D)),('M',op(M,1,D)),('L',op(Lg,1,D)),('Starly',op(st,1,GR)),('Taillow',op(ta,1,GR))],
    'oogmaten: S 5x4, M 5x5 (Starly-oog), L 6x6 rond; verder dezelfde sprite',A+'kleur_r6/oog_maten.png')
