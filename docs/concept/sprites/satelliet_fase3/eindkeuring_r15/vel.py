import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..','..','..')
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.info.setdefault('transparency',0)
    return im.convert('RGBA').crop((0,0,64,64)) if im.size[0]==64 else im.convert('RGBA')
r15=rgba(os.path.join(H,'..','sprite','r15','sprite.png')); fx=rgba(os.path.join(H,'sprite.png'))
mod=Image.open(os.path.join(H,'..','model','model_gekozen.png')).convert('RGBA')
f2=rgba(os.path.join(H,'..','..','satelliet_fase2','af','satelliet.png'))
mag=rgba(os.path.join(R,'graphics','pokemon','magneton','anim_front_gba.png'))
LB=(232,236,230,255); DB=(40,42,58,255)
def on(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
# 8x sprite alleen
on(fx,LB,8).save(os.path.join(H,'sprite_8x.png'))
W=1600; V=Image.new('RGBA',(W,1370),(255,255,255,255)); d=ImageDraw.Draw(V)
d.text((10,4),'r15',fill=(0,0,0)); d.text((532,4),'gecorrigeerd (eindkeuring)',fill=(0,0,0)); d.text((1054,4),'model (model_gekozen)',fill=(0,0,0))
V.alpha_composite(on(r15,LB,8),(10,20)); V.alpha_composite(on(fx,LB,8),(532,20))
m=on(mod,(255,255,255,255),2); V.alpha_composite(m,(1054,20))
# close-ups 16x: PE/PF/buis en PB
y=560
for (bx,lab) in [((24,38,42,62),'PE/PF/voorbuis'),((30,11,40,28),'PB')]:
    pass
d.text((10,y-14),'close-up 14x: PE/PF/voorbuis (x24-41, y38-61)  r15 | gecorrigeerd      PB + PA (x24-43, y11-27)  r15 | gecorrigeerd',fill=(0,0,0))
c=(24,38,42,62)
V.alpha_composite(on(r15.crop(c),LB,14),(10,y)); V.alpha_composite(on(fx.crop(c),LB,14),(10+18*14+10,y))
c2=(24,11,44,28)
V.alpha_composite(on(r15.crop(c2),LB,14),(560,y)); V.alpha_composite(on(fx.crop(c2),LB,14),(560+20*14+10,y))
c3=(44,28,62,36)
d.text((1140,y-14),'PC (x44-61,y28-35)',fill=(0,0,0))
V.alpha_composite(on(r15.crop(c3),LB,12),(1140,y)); V.alpha_composite(on(fx.crop(c3),LB,12),(1140,y+110))
# 1x en 2x
y=1170
for i,bg in enumerate((LB,DB)):
    yy=y-260+i*210+40
    d.rectangle((0,yy-10,W,yy+190),fill=bg)
    x=10
    for im in (fx,f2,mag):
        V.alpha_composite(on(im,bg,1),(x,yy)); x+=74
    x+=20
    for im in (r15,fx,f2,mag):
        V.alpha_composite(on(im,bg,2),(x,yy)); x+=138
    x+=20
    for im in (fx,f2):
        V.alpha_composite(on(im,bg,3),(x,yy-8)); x+=200
d.text((10,904),'1x: gecorrigeerd | fase 2 | Magneton     2x: r15 | gecorrigeerd | fase 2 | Magneton     3x: gecorrigeerd | fase 2',fill=(0,0,0))
V.convert('RGB').save(os.path.join(H,'vel.png'))
