import sys
from PIL import Image, ImageDraw
# zie.py sprite.png x0 y0 x1 y1 scale out
src=sys.argv[1]; x0,y0,x1,y1,s=[int(v) for v in sys.argv[2:7]]; out=sys.argv[7]
im=Image.open(src).convert('RGBA')
model=Image.open('../../referenties/model.webp').convert('RGB')
w,h=x1-x0,y1-y0
a=Image.new('RGB',(w*s,h*s),(255,255,255))
a.paste(im.crop((x0,y0,x1,y1)).resize((w*s,h*s),Image.NEAREST),(0,0),im.crop((x0,y0,x1,y1)).resize((w*s,h*s),Image.NEAREST))
d=ImageDraw.Draw(a)
for x in range(x0,x1+1):
    if x%4==0:
        d.line([((x-x0)*s,0),((x-x0)*s,h*s)],fill=(255,0,0) if x%8==0 else (0,160,255),width=1)
        if x%8==0: d.text(((x-x0)*s+2,2),str(x),fill=(255,0,0))
for y in range(y0,y1+1):
    if y%4==0:
        d.line([(0,(y-y0)*s),(w*s,(y-y0)*s)],fill=(255,0,0) if y%8==0 else (0,160,255),width=1)
        if y%8==0: d.text((2,(y-y0)*s+2),str(y),fill=(255,0,0))
S=(983-46)/62
m=model.crop((int(46+(x0-1)*S),int(57+(y0-3)*S),int(46+(x1-1)*S),int(57+(y1-3)*S))).resize((w*s,h*s),Image.LANCZOS)
dm=ImageDraw.Draw(m)
for x in range(x0,x1+1):
    if x%4==0: dm.line([((x-x0)*s,0),((x-x0)*s,h*s)],fill=(255,0,0))
for y in range(y0,y1+1):
    if y%4==0: dm.line([(0,(y-y0)*s),(w*s,(y-y0)*s)],fill=(255,0,0))
o=Image.new('RGB',(w*s*2+10,h*s),(255,255,255)); o.paste(a,(0,0)); o.paste(m,(w*s+10,0)); o.save(out)
