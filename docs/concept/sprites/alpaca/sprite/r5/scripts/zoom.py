# zoom.py in.png out.png x0 y0 x1 y1 schaal : uitsnede met raster en coordinaten
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGBA'); x0,y0,x1,y1,s=map(int,sys.argv[3:8])
c=im.crop((x0,y0,x1,y1)); bg=Image.new('RGBA',c.size,(200,220,255,255)); bg.alpha_composite(c)
b=bg.resize((c.width*s,c.height*s),Image.NEAREST); out=Image.new('RGB',(b.width+30,b.height+20),'white'); out.paste(b,(30,20))
d=ImageDraw.Draw(out)
for i in range(c.width+1): d.line([(30+i*s,20),(30+i*s,20+b.height)],fill=(150,150,150))
for j in range(c.height+1): d.line([(30,20+j*s),(30+b.width,20+j*s)],fill=(150,150,150))
for i in range(0,c.width,2): d.text((30+i*s+2,4),str(x0+i),fill='black')
for j in range(0,c.height,2): d.text((2,20+j*s+2),str(y0+j),fill='black')
out.save(sys.argv[2])
