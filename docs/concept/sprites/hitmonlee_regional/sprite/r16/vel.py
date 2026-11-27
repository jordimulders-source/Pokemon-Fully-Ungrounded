# Overlay rechte lijnen (op ek2), diff ek2->r14 en het vel.
import sys; sys.path.insert(0,'docs/concept/sprites/hitmonlee_regional/sprite/r14')
from PIL import Image, ImageDraw; import numpy as np
sys.path.insert(0,'docs/concept/sprites/hitmonlee_regional/sprite/r14'); from recht import runs
D='docs/concept/sprites/hitmonlee_regional/'
O=D+'sprite/r16/'
ek=Image.open(D+'eindkeuring/ek2.png'); e=np.array(ek); r=np.array(Image.open(O+'r16.png'))
Z=8
def big(im,z=Z,bg=(255,255,255,255)):
    im=im.convert('RGBA'); b=Image.new('RGBA',(im.width*z,im.height*z),bg); t=im.resize((im.width*z,im.height*z),0); b.paste(t,(0,0),t); return b
# --- diff ---
df=big(Image.fromarray(np.where(r>0,1,0).astype('uint8')*0).convert('RGBA'))
eb=big(ek).convert('RGBA'); g=Image.blend(eb,Image.new('RGBA',eb.size,(255,255,255,255)),0.6)
dd=ImageDraw.Draw(g)
for y,x in zip(*np.where(r!=e)):
    c=(0,160,255,255) if e[y,x]==0 else ((255,0,255,255) if r[y,x]==0 else (255,80,0,255))
    dd.rectangle([x*Z+1,y*Z+1,x*Z+Z-2,y*Z+Z-2],outline=c,width=2)
g.save(O+'diff_ek2_r16.png')
# --- model op dezelfde schaal (natief 136x148 -> 64 hoog, x-offset 2) ---
n=Image.open(D+'sprite/natief.png').convert('RGBA')
m=Image.new('RGBA',(64*Z,64*Z),(255,255,255,255)); nn=n.resize((round(136*64/148*Z),64*Z),Image.LANCZOS); m.paste(nn,(2*Z,0))
# --- Gen 3 Hitmonlee ---
gp=np.array(Image.open('graphics/pokemon/hitmonlee/anim_front_gba.png'))[:64]
L=open('graphics/pokemon/hitmonlee/normal_gba.pal').read().split('\n')[3:19]
pal=np.array([list(map(int,l.split())) for l in L],np.uint8)
rgba=np.dstack([pal[gp],np.where(gp==0,0,255).astype(np.uint8)])
g3=big(Image.fromarray(rgba,'RGBA'))
W=64*Z; vel=Image.new('RGBA',(W*4+30,W+40+W+20),(235,235,235,255))
dv=ImageDraw.Draw(vel)
for i,(t,nm) in enumerate([(big(ek),'ek2 8x'),(big(Image.open(O+'r16.png')),'r16 8x'),(m,'model r2 (natief, zelfde schaal)'),(g3,'Gen 3 Hitmonlee 8x')]):
    vel.paste(t,(i*(W+10),20)); dv.text((i*(W+10)+4,4),nm,fill=(0,0,0,255))
y=W+40
vel.paste(g,(0,y)); dv.text((4,y-14),'diff ek2 -> r16 (oranje = andere tint, blauw = erbij, roze = weg)',fill=(0,0,0,255))
x=W+10
for k,bgc in enumerate([(255,255,255,255),(40,40,48,255)]):
    for j,(im) in enumerate([ek,Image.open(O+'r16.png')]):
        bx=Image.new('RGBA',(72,72),bgc); t=im.convert('RGBA'); bx.paste(t,(4,4),t)
        vel.paste(bx,(x+j*80,y+k*80))
        t2=im.convert('RGBA').resize((128,128),0); bx2=Image.new('RGBA',(136,136),bgc); bx2.paste(t2,(4,4),t2); vel.paste(bx2,(x+170+j*144,y+k*144))
dv.text((x,y+165),'1x en 2x: ek2 | r16, licht en donker',fill=(0,0,0,255))
vel.save(O+'vel.png')
