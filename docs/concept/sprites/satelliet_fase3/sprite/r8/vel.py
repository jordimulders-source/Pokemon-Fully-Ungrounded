# vel r8: r7-130 en de 4 varianten op 8x; 1x en 2x naast fase 2 op licht en donker
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
V=['s16p13','s16p15','s18p13','s18p15']
ims=[(rgba(os.path.join(H,'..','r7','sprite_bol130.png')),'r7 x1,3 (basis)')]+[(rgba(os.path.join(H,'sprite_%s.png'%v)),'r8 zijbol x1,%s, panelen x1,%s'%(v[2],v[5])) for v in V]
f2=rgba(os.path.join(R,'..','satelliet_fase2','af','satelliet.png'))
BG=(235,240,235,255); DK=(40,44,60,255)
def on(im,bg,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
Z=8; T=64*Z
W=3*(T+10)+10; Hh=30+2*(T+30)+2*(64*2+30)+20
P=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(P)
pos=[(0,0),(1,0),(2,0),(0,1),(1,1)]
for (im,t),(cx,cy) in zip(ims,pos):
    x=10+cx*(T+10); y=26+cy*(T+30); P.paste(on(im,BG,Z),(x,y)); d.text((x,y-14),t,fill=(0,0,0))
y0=26+2*(T+30)+10
d.text((10,y0-12),'1x en 2x: r7-130 | s16p13 | s16p15 | s18p13 | s18p15 | fase 2, op licht en donker',fill=(0,0,0))
for k,bg in enumerate((BG,DK)):
    yy=y0+k*(64*2+30); P.paste(Image.new('RGB',(W-20,64*2+20),bg[:3]),(10,yy)); x=20
    for im,_ in ims+[(f2,'')]:
        c=Image.new('RGBA',(64,64),bg); c.alpha_composite(im); P.paste(c.convert('RGB'),(x,yy+10)); x+=70
    x+=20
    for im,_ in ims+[(f2,'')]:
        P.paste(on(im,bg,2),(x,yy+10)); x+=134
P.save(os.path.join(H,'vel.png'))
