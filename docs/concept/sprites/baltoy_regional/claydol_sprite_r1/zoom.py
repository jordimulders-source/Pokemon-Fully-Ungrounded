# Uitvergroting met coördinaten: zoom.py bron.png x0 y0 x1 y1 schaal uit.png
import sys; from PIL import Image, ImageDraw
src,x0,y0,x1,y1,s,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(src).convert('RGBA').crop((x0,y0,x1,y1)); W,H=im.size
c=Image.new('RGB',(W*s+30,H*s+20),'white'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
c.paste(bg.convert('RGB').resize((W*s,H*s),Image.NEAREST),(30,20)); d=ImageDraw.Draw(c)
for i in range(W):
    d.line([(30+i*s,20),(30+i*s,20+H*s)],fill=(200,200,255) if (x0+i)%5 else (0,120,255))
    if (x0+i)%5==0: d.text((30+i*s+1,4),str(x0+i),fill='blue')
for j in range(H):
    d.line([(30,20+j*s),(30+W*s,20+j*s)],fill=(200,200,255) if (y0+j)%5 else (0,120,255))
    if (y0+j)%5==0: d.text((2,20+j*s+1),str(y0+j),fill='blue')
c.save(out)
