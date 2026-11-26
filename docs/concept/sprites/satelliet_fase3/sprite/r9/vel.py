# vel r9: r8-s18p15 | r9 | model (8x); close-ups ogen en panelen (r8 boven, r9 onder, 12x); 1x en 2x naast fase 2 op licht en donker
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
r8=rgba(os.path.join(H,'..','r8','sprite_s18p15.png')); r9=rgba(os.path.join(H,'sprite.png'))
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
model=Image.open(os.path.join(H,'model_r9.png')).convert('RGB')
BG=(235,240,235,255); DK=(40,44,60,255)
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
T=512; W=3*(T+10)+10
CL=[('oog voor',(8,44,20,56)),('oog links',(12,25,24,37)),('oog rechts',(44,33,56,45)),
    ('mast PB',(30,12,42,28)),('mast PF + PE',(22,39,42,56)),('PA',(16,16,36,28)),('PD',(0,34,18,45)),('PC',(42,27,64,37))]
Z2=12
cw=[(b[2]-b[0])*Z2 for _,b in CL]
rows=[CL[:3],CL[3:6],CL[6:]]
Hh=30+T+30+sum(2*max((b[3]-b[1])*Z2 for _,b in r)+50 for r in rows)+2*(64*2+30)+30
P=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(P)
y=26
for i,(im,t) in enumerate(((on(r8,BG,8),'r8 s18p15 (basis)'),(on(r9,BG,8),'r9 (vormherstel)'),(model.resize((T,int(model.height*T/model.width)),Image.LANCZOS),'model r9 (mast PB x2,0 / PF x2,5)'))):
    x=10+i*(T+10); P.paste(im,(x,y)); d.text((x,y-14),t,fill=(0,0,0))
y+=T+30
for r in rows:
    hmax=max((b[3]-b[1])*Z2 for _,b in r); x=10
    for t,b in r:
        a=on(r8.crop(b),BG,Z2); c=on(r9.crop(b),BG,Z2)
        d.text((x,y-14),t+' (boven r8, onder r9)',fill=(0,0,0)); P.paste(a,(x,y)); P.paste(c,(x,y+hmax+8)); x+=a.width+16
    y+=2*hmax+50
d.text((10,y-12),'1x en 2x: r8 s18p15 | r9 | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y+k*(64*2+30); P.paste(Image.new('RGB',(W-20,64*2+20),bg[:3]),(10,yy)); x=20
    for im in (r8,r9,f2):
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); P.paste(c.convert('RGB'),(x,yy+10)); x+=70
    x+=20
    for im in (r8,r9,f2):
        P.paste(on(im,bg,2),(x,yy+10)); x+=134
P.save(os.path.join(H,'vel.png'))
