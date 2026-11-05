"""vel.png: sprite 1x en 4x op licht en donker, model_open 4x, Fletchling/Starly/Taillow 4x en 1x."""
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
sp=Image.open('kolibrie_pre.png').convert('RGBA')
mo=Image.open('../model_open.png').convert('RGBA').resize((256,256),Image.LANCZOS)
refs=[Image.open(G+n+'/anim_front.png').crop((0,0,64,64)).convert('RGBA') for n in ('fletchling','starly','taillow')]
L,D=(236,236,236,255),(44,44,56,255)
W=256*6+16*7; H=256*2+64+16*4+20
v=Image.new('RGBA',(W,H),(200,200,200,255)); d=ImageDraw.Draw(v)
def tile(im,x,y,bg,s=4):
    t=Image.new('RGBA',(64*s,64*s),bg); t.alpha_composite(im.resize((64*s,64*s),Image.NEAREST)); v.paste(t,(x,y))
x=16
for bg in (L,D):
    tile(sp,x,16,bg); x+=256+16
t=Image.new('RGBA',(256,256),(255,255,255,255)); t.alpha_composite(mo); v.paste(t,(x,16)); x+=256+16
for r in refs: tile(r,x,16,L); x+=256+16
x=16; y=16+256+16
for bg in (L,D):
    tile(sp,x,y,bg,s=1); x+=64+16
for r in refs: tile(r,x,y,L,s=1); x+=64+16
for bg in (L,D):
    tile(sp,x,y,bg,s=1); x+=64+16
y2=y+64+16
for i,bg in enumerate((L,D)):
    tile(sp,16+i*(64*3+16),y2,bg,s=3)
d.text((16,H-14),'kolibrie pre-evo kleur r1  |  1x/4x licht+donker | model_open | Fletchling | Starly | Taillow',fill=(0,0,0,255))
v.save('vel.png')
