# vel r13: r11 | r12 | varianten A-D (8x); close-ups PB en PF per versie (12x); 1x/2x naast fase 2
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
V=[('r11',rgba(os.path.join(H,'..','r11','sprite.png'))),('r12',rgba(os.path.join(H,'..','r12','sprite.png')))]
for n,t in (('A_pb15_pflang','A: PB -1,5 | PF lang, r11-plek'),('B_pb15_pflang15','B: PB -1,5 | PF lang -1,5'),
            ('C_pb20_pflang','C: PB -2 | PF lang, r11-plek'),('D_pb20_pflang15','D: PB -2 | PF lang -1,5')):
    V.append((t,rgba(os.path.join(H,n,'sprite.png'))))
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
BG=(235,240,235,255); DK=(40,44,60,255)
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
T=512; W=3*(T+10)+10; Z=12
PB=(26,9,42,29); PF=(28,38,44,61)
Hh=2*(T+30)+30+2*(24*Z+40)+2*(64*2+30)+40
P=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(P)
y=26
for i,(t,im) in enumerate(V):
    x=10+(i%3)*(T+10); yy=y+(i//3)*(T+30); P.paste(on(im,BG,8),(x,yy)); d.text((x,yy-14),t,fill=(0,0,0))
y+=2*(T+30)+10
for naam,bx in (('mast PB',PB),('mast PF',PF)):
    x=10
    for t,im in V:
        c=on(im.crop(bx),BG,Z); P.paste(c,(x,y)); d.text((x,y-14),naam+' '+t.split(':')[0],fill=(0,0,0)); x+=c.width+8
    y+=(bx[3]-bx[1])*Z+40
d.text((10,y-12),'1x en 2x: r11 | r12 | A | B | C | D | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y+k*(64*2+30); P.paste(Image.new('RGB',(W-20,64*2+20),bg[:3]),(10,yy)); x=20
    for _,im in V+[('f2',f2)]:
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); P.paste(c.convert('RGB'),(x,yy+10)); x+=68
    x+=10
    for _,im in V[2:]+[('f2',f2)]:
        P.paste(on(im,bg,2),(x,yy+10)); x+=132
P.save(os.path.join(H,'vel.png'))
