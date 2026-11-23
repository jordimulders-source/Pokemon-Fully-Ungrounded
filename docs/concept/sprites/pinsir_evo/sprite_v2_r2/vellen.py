# Vellen voor r2. Draaien vanuit docs/concept/sprites/pinsir_evo/:  python3 sprite_v2_r2/vellen.py
import sys, numpy as np
sys.path.insert(0,'sprite_v2_r2')
from vergelijk import modelstuk, spritestuk, raster
from PIL import Image, ImageDraw
D='sprite_v2_r2/'
A=Image.open(D+'pinsir_evo_v2_r2_A.png'); B=Image.open(D+'pinsir_evo_v2_r2_B.png'); R1=Image.open('sprite_v2/pinsir_evo_v2_r1.png')
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def ref(n):
    im_=Image.open(G+n+'/anim_front.png'); a_=np.asarray(im_)[:64]
    rgba=np.array(im_.convert('RGBA'))[:64]; rgba[a_==0,3]=0; return Image.fromarray(rgba,'RGBA')
def zwart(t): return (0,0,0)

# ---- onderdelen_12x: per onderdeel  r1 | A | model  (12x, spriteraster) ----
DELEN=[('kopschild',(5,8,39,22)),('gezicht',(10,19,26,34)),('kaken',(0,22,26,45)),('schouder + koepel',(23,19,41,38)),
       ('nabije arm + klauwen',(28,28,44,48)),('verre arm + klauwen',(3,37,21,50)),('buik',(17,32,36,54)),
       ('nabije dij + knie',(30,43,49,58)),('scheen + voet',(32,54,50,64)),('verre been',(10,44,28,64)),
       ('staart',(42,34,64,58)),('rug (A)',(28,14,62,46))]
Z=12; rijen=[]
for naam,b in DELEN:
    x0,y0,x1,y1=b
    ims=[raster(spritestuk(s,*b,Z),x0,y0,Z) for s in (R1,A)]+[raster(modelstuk(*b,Z),x0,y0,Z,(170,170,170))]
    w,h=ims[0].size; c=Image.new('RGB',(3*(w+10)+10,h+24),'white'); d=ImageDraw.Draw(c)
    d.text((10,4),naam+'   (r1 | r2 A | model, x %d-%d, y %d-%d)'%(x0,x1-1,y0,y1-1),fill=(0,0,0))
    for k,im in enumerate(ims): c.paste(im,(10+k*(w+10),20))
    rijen.append(c)
# twee kolommen
kol=[rijen[0::2],rijen[1::2]]
kw=[max(r.width for r in k) for k in kol]; kh=[sum(r.height+8 for r in k) for k in kol]
vel=Image.new('RGB',(sum(kw)+20,max(kh)),'white'); x=0
for k,w in zip(kol,kw):
    y=0
    for r in k: vel.paste(r,(x,y)); y+=r.height+8
    x+=w+20
vel.save(D+'onderdelen_12x.png')

# ---- rug_8x: rug A | B | model (8x) + Aggron / Turtonator / Tyranitar ter vergelijking (4x, hele sprite) ----
b=(28,14,62,46); Z=8
ims=[spritestuk(A,*b,Z),spritestuk(B,*b,Z),modelstuk(*b,Z)]
w,h=ims[0].size
refs=[ref(n).resize((256,256),Image.NEAREST) for n in ('aggron','turtonator','tyranitar')]
rv=Image.new('RGB',(3*(w+12)+12,h+30+256+30),'white'); d=ImageDraw.Draw(rv)
for k,(t,im) in enumerate(zip(['A: schild zo trouw mogelijk (modelnaden)','B: 4 grootste modelplaten','model v2_r4, zelfde maat'],ims)):
    rv.paste(im,(12+k*(w+12),24)); d.text((12+k*(w+12),6),t,fill=(0,0,0))
for k,(n,im) in enumerate(zip(('aggron','turtonator','tyranitar'),refs)):
    X=12+k*(256+40); rv.paste(im,(X,h+50),im); d.text((X,h+34),n+' (4x)',fill=(0,0,0))
rv.save(D+'rug_8x.png')

# ---- vel: A | B | model op 6x; daarna 1x en 2x naast Tyranitar/Aggron/Pinsir op wit en donker ----
Z=6
top=[spritestuk(A,0,6,64,64,Z),spritestuk(B,0,6,64,64,Z),modelstuk(0,6,64,64,Z)]
rij=[('r2 A',A.convert('RGBA')),('r2 B',B.convert('RGBA')),('r1',R1.convert('RGBA'))]+[(n,ref(n)) for n in ('tyranitar','aggron','pinsir')]
cw=64+128+24; W_=max(3*(top[0].width+12)+12,len(rij)*cw+16)
vel=Image.new('RGB',(W_,top[0].height+40+2*(128+44)),'white'); d=ImageDraw.Draw(vel)
for k,(t,im) in enumerate(zip(['A','B','model'],top)):
    vel.paste(im,(12+k*(im.width+12),24)); d.text((12+k*(im.width+12),6),t,fill=(0,0,0))
for bi,bgc in enumerate([(255,255,255),(40,48,56)]):
    y0=top[0].height+40+bi*(128+44)
    vel.paste(Image.new('RGB',(W_,128+44),bgc),(0,y0))
    for i,(n,s_) in enumerate(rij):
        x=8+i*cw
        vel.paste(s_,(x,y0+20+64),s_); b2=s_.resize((128,128),Image.NEAREST); vel.paste(b2,(x+64+8,y0+20),b2)
        d.text((x,y0+4),n,fill=(0,0,0) if bi==0 else (230,230,230))
vel.save(D+'vel.png')
print('ok')
