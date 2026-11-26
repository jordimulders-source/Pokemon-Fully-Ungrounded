# vel r15: r14 | r15 (8x); close-ups van de twee plekken (12x): PA rechts van PB, PF/buis boven PE; model_gekozen erbij
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
a=rgba(os.path.join(H,'..','r14','sprite.png')); b=rgba(os.path.join(H,'sprite.png'))
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
M=Image.open(os.path.join(R,'model','model_gekozen.png')).convert('RGB')
BG=(235,240,235,255); DK=(40,44,60,255); S=3.515625
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
def mcrop(bx,h):
    c=M.crop((int(3+bx[0]*S),int(3+(bx[1]-13)*S),int(3+bx[2]*S),int(3+(bx[3]-13)*S))); return c.resize((int(c.width*h/c.height),h),Image.NEAREST)
T=512; W=2*(T+10)+10; Z=12
PLEK=[('1: PA rechts van PB (tot de achterarm)',(28,17,46,30)),('2: PF onder de voorbuis, boven PE',(22,37,40,50))]
Hh=T+40+sum((bx[3]-bx[1])*Z+40 for _,bx in PLEK)+2*(64*2+30)+40
P=Image.new('RGB',(W+300,Hh),(255,255,255)); d=ImageDraw.Draw(P); y=26
for i,(t,im) in enumerate((('r14',a),('r15',b))):
    P.paste(on(im,BG,8),(10+i*(T+10),y)); d.text((10+i*(T+10),y-14),t,fill=(0,0,0))
y+=T+40
for t,bx in PLEK:
    hh=(bx[3]-bx[1])*Z; x=10
    d.text((x,y-14),t+': r14 | r15 | model',fill=(0,0,0))
    for im in (a,b):
        c=on(im.crop(bx),BG,Z); P.paste(c,(x,y)); x+=c.width+12
    P.paste(mcrop(bx,hh),(x,y)); y+=hh+40
d.text((10,y-12),'1x en 2x: r14 | r15 | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y+k*(64*2+30); P.paste(Image.new('RGB',(W-20,64*2+20),bg[:3]),(10,yy)); x=20
    for im in (a,b,f2):
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); P.paste(c.convert('RGB'),(x,yy+10)); x+=70
    x+=20
    for im in (a,b,f2): P.paste(on(im,bg,2),(x,yy+10)); x+=134
P.save(os.path.join(H,'vel.png'))
