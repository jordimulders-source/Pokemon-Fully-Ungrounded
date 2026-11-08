# model (origineel 1024) | sprite, zelfde raster. args: raster x0 y0 x1 y1 schaal out
import sys
from PIL import Image, ImageDraw, ImageFont
from tools import *
a=load(sys.argv[1]); x0,y0,x1,y1,s=map(int,sys.argv[2:7]); out=sys.argv[7]
O=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/gemini/gekozen_r4.png').convert('RGB')
w,h=x1-x0,y1-y0
L=O.crop((16*x0-2,16*y0-1,16*x1-2,16*y1-1)).resize((w*s,h*s),Image.NEAREST)
R=rgb(a[y0:y1,x0:x1],(255,255,255)).resize((w*s,h*s),Image.NEAREST)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
v=Image.new('RGB',(2*w*s+40,h*s+16),'white'); v.paste(L,(20,14)); v.paste(R,(w*s+40,14)); d=ImageDraw.Draw(v)
for X in (20,w*s+40):
    for k in range(w+1):
        d.line([(X+k*s,14),(X+k*s,14+h*s)],fill=(255,0,0) if (x0+k)%5==0 else (190,190,190))
        if k<w: d.text((X+k*s+2,1),str((x0+k)%100),font=F,fill='black')
    for k in range(h+1):
        d.line([(X,14+k*s),(X+w*s,14+k*s)],fill=(255,0,0) if (y0+k)%5==0 else (190,190,190))
for k in range(h): d.text((1,16+k*s),str(y0+k),font=F,fill='black')
v.save(out)
