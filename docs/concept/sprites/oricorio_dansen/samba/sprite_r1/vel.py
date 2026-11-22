# vel.png: sprite 8x | model op dezelfde schaal (natief 4x = 1 spritepixel per 2x2 modelblok) ; kop 12x | Pom-Pom-kop 12x ;
# snavels 12x (verkleinde modelsnavel, Baile, Pom-Pom, Pa'u, Sensu; Gen 3 frame 1) ; 1x en 2x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
from render import save
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/'
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
spr=Image.open('samba.png').convert('RGBA')
PY,PX=9,4            # plaatsing uitsnede -> 64x64 (build.py log 'plaats')
NY,NX=13,67          # uitsnede (0,0) = natief (13,67); natief = (NY+2r, NX+2c)
nat=Image.open('natief.png').convert('RGB')
pad=Image.new('RGB',(nat.width+80,nat.height+80),'white'); pad.paste(nat,(40,40))
mod=pad.crop((40+NX-2*PX,40+NY-2*PY,40+NX-2*PX+128,40+NY-2*PY+128)).resize((512,512),Image.NEAREST)
W=Image.new('RGB',(1044,30+512+30+250+30+250),(230,230,230)); d=ImageDraw.Draw(W)
W.paste(op(spr,'white',8),(0,30)); W.paste(mod,(532,30))
d.text((4,8),'samba r1 (8x; oog en snavel Pom-Pom)',fill='black'); d.text((536,8),'model gemini_r6, natief raster, zelfde schaal',fill='black')
y=30+512+8; d.text((4,y),'kop 12x  |  Pom-Pom (bron oog en snavel) 12x',fill='black'); y+=20
W.paste(op(spr.crop((14,18,34,38)),'white',12),(0,y))
pom=Image.open(G+'pom_pom/anim_front.png').convert('RGBA').crop((22,13,42,33)); W.paste(op(pom,(153,211,165),12),(260,y))
W.paste(op(spr,(255,255,255),1),(540,y)); W.paste(op(spr,(40,40,48),1),(610,y))
W.paste(op(spr,(255,255,255),2),(690,y)); W.paste(op(spr,(40,40,48),2),(830,y))
y+=250; d.text((4,y),'snavels 12x: model verkleind (vervangen door Pom-Pom) | Baile | Pom-Pom | Pa\'u | Sensu',fill='black'); y+=20
kaal=np.load('kaal_11geel.npy'); ys,xs=np.where(kaal>0); kaal=kaal[ys.min():ys.max()+1,xs.min():xs.max()+1]
save(kaal,'/tmp/claude-0/kaalcrop.png'); kc=Image.open('/tmp/claude-0/kaalcrop.png').convert('RGBA')
crops=[kc.crop((9,12,25,23)),
       Image.open(G+'anim_front.png').convert('RGBA').crop((16,16,32,27)),
       Image.open(G+'pom_pom/anim_front.png').convert('RGBA').crop((21,16,37,27)),
       Image.open(G+'pau/anim_front.png').convert('RGBA').crop((14,17,30,28)),
       Image.open(G+'sensu/anim_front.png').convert('RGBA').crop((26,17,42,28))]
for k,c in enumerate(crops): W.paste(op(c,(153,211,165),12),(k*205,y))
W.save('vel.png'); print(W.size)
