# origineel model met spritepixelraster (16 px per spritepixel) + labels
import sys
from PIL import Image, ImageDraw, ImageFont
x0,y0,x1,y1,s=map(int,sys.argv[1:6]); out=sys.argv[6]
a=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/gemini/gekozen_r4.png').convert('RGB')
c=a.crop((16*x0-2,16*y0-1,16*x1-2,16*y1-1)); c=c.resize((c.size[0]*s//16*1,c.size[1]*s//16),Image.NEAREST) if False else c.resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
v=Image.new('RGB',(c.size[0]+22,c.size[1]+14),'white'); v.paste(c,(22,14)); d=ImageDraw.Draw(v)
for k in range(x1-x0+1):
    d.line([(22+k*s,14),(22+k*s,14+c.size[1])],fill=(255,0,0) if (x0+k)%5==0 else (190,190,190))
    if k<x1-x0: d.text((24+k*s,1),str(x0+k),font=F,fill='black')
for k in range(y1-y0+1):
    d.line([(22,14+k*s),(22+c.size[0],14+k*s)],fill=(255,0,0) if (y0+k)%5==0 else (190,190,190))
    if k<y1-y0: d.text((1,16+k*s),str(y0+k),font=F,fill='black')
v.save(out)
