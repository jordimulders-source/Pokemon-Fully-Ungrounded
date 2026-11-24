import sys
from PIL import Image, ImageDraw
src=sys.argv[1]; x0,y0,x1,y1,s=[int(v) for v in sys.argv[2:7]]; out=sys.argv[7]
im=Image.open(src).convert('RGBA')
w,h=x1-x0,y1-y0
c=im.crop((x0,y0,x1,y1)).resize((w*s,h*s),Image.NEAREST)
a=Image.new('RGB',(w*s+30,h*s+20),(255,255,255)); a.paste(c,(30,20),c)
d=ImageDraw.Draw(a)
for x in range(x0,x1+1):
    d.line([((x-x0)*s+30,20),((x-x0)*s+30,h*s+20)],fill=(255,0,0) if x%5==0 else (180,200,255))
    if x%2==0: d.text(((x-x0)*s+32,4),str(x),fill=(255,0,0))
for y in range(y0,y1+1):
    d.line([(30,(y-y0)*s+20),(w*s+30,(y-y0)*s+20)],fill=(255,0,0) if y%5==0 else (180,200,255))
    if y%2==0: d.text((4,(y-y0)*s+24),str(y),fill=(255,0,0))
a.save(out)
