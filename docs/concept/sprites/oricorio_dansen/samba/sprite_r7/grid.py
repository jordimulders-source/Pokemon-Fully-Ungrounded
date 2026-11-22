# grid.py x0 y0 x1 y1 out : modeluitsnede met spriteraster (1 cel = 1 spritepixel) + dezelfde uitsnede van een sprite ernaast
import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); out=sys.argv[5]; spr=sys.argv[6]; z=24
m=Image.open('../model/gemini_r10.png').convert('RGB'); k=950.272/64
c=m.crop((int(19.3344+x0*k),int(29.216+y0*k),int(19.3344+x1*k),int(29.216+y1*k))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
s=Image.open(spr).convert('RGB').crop((x0,y0,x1,y1)).resize(c.size,Image.NEAREST)
W=Image.new('RGB',(c.width*2+10,c.height),(230,230,230))
for i,im in enumerate((c,s)):
    d=ImageDraw.Draw(im)
    for x in range(x0,x1):
        d.line([((x-x0)*z,0),((x-x0)*z,im.height)],fill=(170,170,170) if x%5 else (255,0,0))
        if x%5==0: d.text(((x-x0)*z+2,2),str(x),fill=(255,0,0))
    for y in range(y0,y1):
        d.line([(0,(y-y0)*z),(im.width,(y-y0)*z)],fill=(170,170,170) if y%5 else (255,0,0))
        if y%5==0: d.text((2,(y-y0)*z+2),str(y),fill=(255,0,0))
    W.paste(im,(i*(c.width+10),0))
W.save(out)
