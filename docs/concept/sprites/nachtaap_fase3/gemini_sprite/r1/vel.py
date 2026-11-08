import sys,os,numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools import *
a=load(sys.argv[1]); out=sys.argv[2]
g=Image.open(os.path.join(G,'grid128.png')).convert('RGB')
m64=g.resize((64,64),Image.BOX)
def rgba(a):
    r=np.array(rgb(a).convert('RGBA')); r[a==0,3]=0; return Image.fromarray(r)
S=rgb(a); W=Image.new('RGB',(64*8*2+30,64*8+40+12*24+30+80),'white'); d=ImageDraw.Draw(W)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
W.paste(S.resize((512,512),Image.NEAREST),(10,30)); W.paste(g.resize((512,512),Image.NEAREST),(532,30))
d.text((10,8),'sprite 8x',font=F,fill='black'); d.text((532,8),'model (128-raster) 8x',font=F,fill='black')
y=560
for k,(x0,y0,x1,y1) in enumerate([(0,24,18,48),(0,12,14,24),(4,44,25,63),(29,2,44,15)]):
    pass
# close-ups 12x: kop, hand links, gloedhand, hand boven
X=10
for (x0,y0,x1,y1) in [(1,24,18,47),(0,12,13,24)]:
    s=S.crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST)
    m=g.crop((2*x0,2*y0,2*x1,2*y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST)
    W.paste(s,(X,y)); W.paste(m,(X+s.size[0]+4,y)); X+=2*s.size[0]+20
y2=y+24*12+10
X=10
for (x0,y0,x1,y1) in [(5,45,25,63),(30,3,43,14)]:
    s=S.crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST)
    m=g.crop((2*x0,2*y0,2*x1,2*y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST)
    W2=W
    if y2+s.size[1]>W.size[1]:
        W=Image.new('RGB',(W.size[0],y2+s.size[1]+120),'white'); W.paste(W2,(0,0)); d=ImageDraw.Draw(W)
    W.paste(s,(X,y2)); W.paste(m,(X+s.size[0]+4,y2)); X+=2*s.size[0]+20
y3=y2+18*12+10
if y3+80>W.size[1]:
    W2=W; W=Image.new('RGB',(W.size[0],y3+90),'white'); W.paste(W2,(0,0)); d=ImageDraw.Draw(W)
R=rgba(a)
for k,bg in enumerate([(248,248,248),(40,44,60),(152,208,160)]):
    B=Image.new('RGBA',(64,64),bg+(255,)); B.alpha_composite(R); W.paste(B.convert('RGB'),(10+k*74,y3))
W.paste(m64,(10+3*74,y3))
W.save(out)
