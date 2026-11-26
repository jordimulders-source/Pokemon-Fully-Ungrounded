# vel r14: r13-C | r14 (8x); close-up PB naast PF (12x, r13-C boven, r14 onder); 1x/2x naast fase 2
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
a=rgba(os.path.join(H,'..','r13','C_pb20_pflang','sprite.png')); b=rgba(os.path.join(H,'sprite.png'))
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
BG=(235,240,235,255); DK=(40,44,60,255)
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
T=512; W=2*(T+10)+10; Z=12; PB=(26,10,42,28); PF=(26,39,42,63)
Hh=T+40+2*((PF[3]-PF[1])*Z+40)+2*(64*2+30)+40
P=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(P); y=26
for i,(t,im) in enumerate((('r13-C',a),('r14',b))):
    P.paste(on(im,BG,8),(10+i*(T+10),y)); d.text((10+i*(T+10),y-14),t,fill=(0,0,0))
y+=T+40
for t,im in (('r13-C',a),('r14',b)):
    c1=on(im.crop(PB),BG,Z); c2=on(im.crop(PF),BG,Z)
    d.text((10,y-14),t+': PB (links) | PF (rechts)',fill=(0,0,0)); P.paste(c1,(10,y)); P.paste(c2,(10+c1.width+20,y))
    y+=(PF[3]-PF[1])*Z+40
d.text((10,y-12),'1x en 2x: r13-C | r14 | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y+k*(64*2+30); P.paste(Image.new('RGB',(W-20,64*2+20),bg[:3]),(10,yy)); x=20
    for im in (a,b,f2):
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); P.paste(c.convert('RGB'),(x,yy+10)); x+=70
    x+=20
    for im in (a,b,f2): P.paste(on(im,bg,2),(x,yy+10)); x+=134
P.save(os.path.join(H,'vel.png'))
