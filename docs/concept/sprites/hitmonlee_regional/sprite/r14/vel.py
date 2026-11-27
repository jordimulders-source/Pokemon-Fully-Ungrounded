# Overlay rechte lijnen (op ek2), diff ek2->r14 en het vel.
import sys; sys.path.insert(0,'docs/concept/sprites/hitmonlee_regional/sprite/r14')
from PIL import Image, ImageDraw; import numpy as np
from recht import runs
D='docs/concept/sprites/hitmonlee_regional/'
O=D+'sprite/r14/'
ek=Image.open(D+'eindkeuring/ek2.png'); e=np.array(ek); r=np.array(Image.open(O+'r14.png'))
Z=8
def big(im,z=Z,bg=(255,255,255,255)):
    im=im.convert('RGBA'); b=Image.new('RGBA',(im.width*z,im.height*z),bg); t=im.resize((im.width*z,im.height*z),0); b.paste(t,(0,0),t); return b
# --- overlay ---
gerep={('h-boven',21),('v-rechts',48),('v-links',52)}
model_recht={('h-boven',0),('v-links',10),('v-links',12),('v-links',37),('h-onder',42),('h-onder',46),('v-rechts',56)}
ov=big(ek); d=ImageDraw.Draw(ov)
def box(y0,x0,y1,x1,c): d.rectangle([x0*Z,y0*Z,(x1+1)*Z-1,(y1+1)*Z-1],outline=c,width=2)
for kind,i,j,n in runs(e):
    if kind.startswith('h') or kind=='binnen-h': y0,x0,y1,x1=i,j,i,j+n-1
    elif kind.startswith('v'): y0,x0,y1,x1=j,i,j+n-1,i
    else: continue
    key=(kind,i)
    if kind=='binnen-h':
        c=(255,0,0,255) if (13<=i<=20 or i in (44,51,53)) else (255,200,0,255)
    else: c=(255,0,0,255) if key in gerep else (255,200,0,255)
    box(y0,x0,y1,x1,c)
# handmatig gevonden runs (niet door de detector, maar wel recht t.o.v. het model)
box(43,15,50,16,(255,0,0,255))   # arm rechterrand zonder taps
box(12,41,22,48,(255,0,0,255))   # trapbeen: ladder van rechte ringen
box(44,51,53,57,(255,0,0,255))   # standbeen: ladder
d.text((4,64*Z-30),'rood = gerepareerd in r14; geel = gemeten: ook recht in het model (zie NOTITIES)',fill=(0,0,0,255))
ov.save(O+'rechte_lijnen_overlay.png')
# --- diff ---
df=big(Image.fromarray(np.where(r>0,1,0).astype('uint8')*0).convert('RGBA'))
eb=big(ek).convert('RGBA'); g=Image.blend(eb,Image.new('RGBA',eb.size,(255,255,255,255)),0.6)
dd=ImageDraw.Draw(g)
for y,x in zip(*np.where(r!=e)):
    c=(0,160,255,255) if e[y,x]==0 else ((255,0,255,255) if r[y,x]==0 else (255,80,0,255))
    dd.rectangle([x*Z+1,y*Z+1,x*Z+Z-2,y*Z+Z-2],outline=c,width=2)
g.save(O+'diff_ek2_r14.png')
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
for i,(t,nm) in enumerate([(big(ek),'ek2 8x'),(big(Image.open(O+'r14.png')),'r14 8x'),(m,'model r2 (natief, zelfde schaal)'),(g3,'Gen 3 Hitmonlee 8x')]):
    vel.paste(t,(i*(W+10),20)); dv.text((i*(W+10)+4,4),nm,fill=(0,0,0,255))
y=W+40
vel.paste(g,(0,y)); dv.text((4,y-14),'diff ek2 -> r14 (oranje = andere tint, blauw = erbij, roze = weg)',fill=(0,0,0,255))
x=W+10
for k,bgc in enumerate([(255,255,255,255),(40,40,48,255)]):
    for j,(im) in enumerate([ek,Image.open(O+'r14.png')]):
        bx=Image.new('RGBA',(72,72),bgc); t=im.convert('RGBA'); bx.paste(t,(4,4),t)
        vel.paste(bx,(x+j*80,y+k*80))
        t2=im.convert('RGBA').resize((128,128),0); bx2=Image.new('RGBA',(136,136),bgc); bx2.paste(t2,(4,4),t2); vel.paste(bx2,(x+170+j*144,y+k*144))
dv.text((x,y+165),'1x en 2x: ek2 | r14, licht en donker',fill=(0,0,0,255))
vel.save(O+'vel.png')
