# uitsneden met raster en coordinaten (alleen lezen)
import sys
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/'
im=Image.open(R+'kleur/ronde14/nachtaap.png').convert('RGBA')
x0,y0,x1,y1,s=map(int,sys.argv[2:7])
c=im.crop((x0,y0,x1,y1)); W,H=c.size
out=Image.new('RGBA',(W*s+30,H*s+20),(230,230,230,255)); d=ImageDraw.Draw(out)
for y in range(H):
    for x in range(W):
        p=c.getpixel((x,y))
        col=p if p[3] else ((200,200,200,255) if (x+y)%2 else (245,245,245,255))
        d.rectangle([30+x*s,20+y*s,30+x*s+s-1,20+y*s+s-1],fill=col)
for x in range(W):
    if (x0+x)%2==0: d.text((30+x*s+2,4),str(x0+x),fill=(0,0,0))
for y in range(H): d.text((2,20+y*s+s//3),str(y0+y),fill=(0,0,0))
out.save(sys.argv[1])
