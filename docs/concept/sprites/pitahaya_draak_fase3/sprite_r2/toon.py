# Hulp: sprite op Z x op wit, met een rasterlabel om de 5 px (voor pixelcoordinaten)
import sys; from PIL import Image, ImageDraw
sp,Z,UIT=sys.argv[1],int(sys.argv[2]),sys.argv[3]
x0,y0,x1,y1=map(int,sys.argv[4:8]) if len(sys.argv)>7 else (0,0,64,64)
im=Image.open(sp); im.save('/tmp/_t.png',transparency=0); t=Image.open('/tmp/_t.png').convert('RGBA')
bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t)
c=bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST).convert('RGB')
out=Image.new('RGB',(c.size[0]+30,c.size[1]+30),(255,255,255)); out.paste(c,(30,30)); d=ImageDraw.Draw(out)
for x in range(x0,x1):
    if x%5==0: d.text((30+(x-x0)*Z+2,8),str(x),fill=(0,0,255)); d.line([(30+(x-x0)*Z,25),(30+(x-x0)*Z,30+c.size[1])],fill=(180,180,255))
for y in range(y0,y1):
    if y%5==0: d.text((2,30+(y-y0)*Z+2),str(y),fill=(0,0,255)); d.line([(25,30+(y-y0)*Z),(30+c.size[0],30+(y-y0)*Z)],fill=(180,180,255))
out.save(UIT)
