# vel r11: r10 | r11 | model (8x); close-ups van de drie ogen (r10 | r11 | modeloog), PB-top en PF; 1x/2x naast fase 2
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
a=rgba(os.path.join(H,'..','r10','sprite.png')); b=rgba(os.path.join(H,'sprite.png'))
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
model=Image.open(os.path.join(R,'model','model_gekozen.png')).convert('RGB')
BG=(235,240,235,255); DK=(40,44,60,255)
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
T=512; W=3*(T+10)+10; Z=12
OGEN=[('oog voor',(8,43,20,56),(40,112,80,152)),('oog links',(12,25,22,36),(56,52,84,80)),('oog rechts',(44,32,58,45),(170,80,200,110))]
DEL=[('mast PB boven',(30,10,44,22)),('mast PF onder PE',(30,44,44,58)),('rechterbol',(43,29,61,46))]
Hh=30+T+40+3*(13*Z+30)+40+(16*Z+30)+2*(64*2+30)+40
P=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(P)
y=26
for i,(im,t) in enumerate(((on(a,BG,8),'r10'),(on(b,BG,8),'r11'),(model.resize((T,int(model.height*T/model.width)),Image.LANCZOS),'model (r13b, gekozen)'))):
    x=10+i*(T+10); P.paste(im,(x,y)); d.text((x,y-14),t,fill=(0,0,0))
y+=T+40
for t,bx,mb in OGEN:
    hh=(bx[3]-bx[1])*Z; x=10
    d.text((x,y-14),t+': r10 | r11 | model',fill=(0,0,0))
    for im in (a,b):
        c=on(im.crop(bx),BG,Z); P.paste(c,(x,y)); x+=c.width+16
    m=model.crop(mb); m=m.resize((int(m.width*hh/m.height),hh),Image.NEAREST); P.paste(m,(x,y))
    y+=max(hh,13*Z)+30
x=10
for t,bx in DEL:
    hh=(bx[3]-bx[1])*Z
    d.text((x,y-14),t+': r10 | r11',fill=(0,0,0))
    for im in (a,b):
        c=on(im.crop(bx),BG,Z); P.paste(c,(x,y)); x+=c.width+8
    x+=24
y+=16*Z+40
d.text((10,y-12),'1x en 2x: r10 | r11 | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y+k*(64*2+30); P.paste(Image.new('RGB',(W-20,64*2+20),bg[:3]),(10,yy)); x=20
    for im in (a,b,f2):
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); P.paste(c.convert('RGB'),(x,yy+10)); x+=70
    x+=20
    for im in (a,b,f2):
        P.paste(on(im,bg,2),(x,yy+10)); x+=134
P.save(os.path.join(H,'vel.png'))
