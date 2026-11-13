# vel.py -> vel.png: r1 | r2 op 8x; kop 12x naast het model; klavervarianten 12x en 1x; 1x en 3x op licht en donker naast de echte Kadabra en de charlatan-Alakazam
import numpy as np, pal
from PIL import Image, ImageDraw
from zij import model, sprite
BG=(152,208,160); A=pal.load('basis_r1.txt'); R=pal.load('raster.txt'); KA=pal.load('klaver_A.txt'); KB=pal.load('klaver_B.txt')
V=Image.new('RGB',(1500,1460),'white'); D=ImageDraw.Draw(V)
def put(im,x,y,t): D.text((x,y),t,fill=(0,0,0)); V.paste(im,(x,y+14))
put(pal.rgb(A,BG).resize((512,512),0),8,4,'kleur_r1, 8x'); put(pal.rgb(R,BG).resize((512,512),0),530,4,'kleur_r2, 8x')
box=(19,8,41,32); y=540
put(sprite(A,*box,12),8,y,'kop r1, 12x'); put(sprite(R,*box,12),280,y,'kop r2, 12x'); put(model(*box,12,False),552,y,'model')
kb=(21,15,31,24); x=840
for nm,r in (('klaver r2 (hoofdsprite)',R),('variant A (4x4)',KA),('variant B (5x5)',KB)):
    put(sprite(r,*kb,12),x,y,nm)
    for i,bg in enumerate(((248,248,240),(40,40,56))):
        V.paste(pal.rgb(r,bg).crop((14,6,46,38)),(x+i*36,y+130)); V.paste(pal.rgb(r,bg).crop((14,6,46,38)).resize((96,96),0),(x+i*100,y+170))
    x+=215
def echt(fn,bg):
    q=Image.open(fn).crop((0,0,64,64)); p=q.convert('RGBA'); arr=np.asarray(q)
    if q.mode=='P' and 'transparency' not in q.info: p.putalpha(Image.fromarray(((arr!=arr[0,0])*255).astype('uint8')))
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(p); return c.convert('RGB')
KAD='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/kadabra/anim_front_gba.png'; ALA='../../alakazam_regional/af_r2/alakazam_charlatan.png'
y3=y+12*24+40
for r,(bg,lab) in enumerate([((248,248,240),'licht'),((40,40,56),'donker')]):
    yy=y3+r*230; D.text((8,yy),'1x en 3x op '+lab+': echte Kadabra | kleur_r1 | kleur_r2 | charlatan-Alakazam',fill=(0,0,0))
    ims=[echt(KAD,bg),pal.rgb(A,bg),pal.rgb(R,bg),echt(ALA,bg)]; x=8
    for im in ims: V.paste(im,(x,yy+16)); x+=70
    x+=20
    for im in ims: V.paste(im.resize((192,192),0),(x,yy+16)); x+=200
V=V.crop((0,0,1500,y3+460)); V.save('vel.png'); print(V.size)
