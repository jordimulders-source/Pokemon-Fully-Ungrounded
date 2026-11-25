# vel r7: r6 | r7-120 | r7-130 op 8x; paneel-close-ups r6 vs r7 (12x); 1x en 2x naast fase 2 op licht en donker.
import os, numpy as np
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p):
    return Image.open(p).convert('RGBA').crop((0,0,64,64))
r6=rgba(os.path.join(R,'kleur_r6','sprite.png'))
a=rgba(os.path.join(H,'sprite_bol120.png')); b=rgba(os.path.join(H,'sprite_bol130.png'))
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
BG=(235,240,235,255); DK=(40,44,60,255)
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
W=3*522+10; Z=12
CROPS=[((18,12,22,16),'PA + mast PB (boven)'),((0,36,18,10),'PD (links)'),((44,28,20,9),'PC (rechts)'),((22,44,16,12),'PE + mast PF (onder)')]
ch=sum(max(h for (x,y,w,h),_ in CROPS[i:i+2])*Z+30 for i in (0,2))
V=Image.new('RGB',(W,30+512+20+ch+2*(64*2+30)+40),(255,255,255)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(((r6,'r6 (Jordi)'),(a,'r7 bollen x1,2'),(b,'r7 bollen x1,3'))):
    V.paste(on(im,BG,8),(5+i*522,26)); d.text((5+i*522,8),t,fill=(0,0,0))
y=26+512+16
d.text((5,y-12),'panelen close-up 12x: r6 | r7 (x1,3; panelen zijn gelijk in x1,2)',fill=(0,0,0))
x=5; yy=y; rowh=0
for j,((cx,cy,w,h),t) in enumerate(CROPS):
    if j==2: x=5; yy+=rowh+30; rowh=0
    d.text((x,yy),t,fill=(0,0,0))
    for im in (r6,b):
        V.paste(on(im.crop((cx,cy,cx+w,cy+h)),BG,Z),(x,yy+12)); x+=w*Z+8
    x+=24; rowh=max(rowh,h*Z+12)
y=yy+rowh+30
d.text((5,y-12),'1x en 2x: r6 | r7-120 | r7-130 | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y+k*(64*2+30); V.paste(Image.new('RGB',(W-10,64*2+20),bg[:3]),(5,yy)); x=15
    for im in (r6,a,b,f2):
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); V.paste(c.convert('RGB'),(x,yy+10)); x+=72
    x+=30
    for im in (r6,a,b,f2):
        V.paste(on(im,bg,2),(x,yy+10)); x+=136
V.save(os.path.join(H,'vel.png'))
