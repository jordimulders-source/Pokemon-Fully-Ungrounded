# Uitsnede op 14x met rasterlijnen elke 5 px en coordinaten (voor handwerk). gebruik: zie.py png x0 y0 x1 y1 uit.png
import sys
from PIL import Image, ImageDraw
f,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]; S=14
im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
c=bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
o=Image.new('RGB',(c.width+30,c.height+20),'white'); o.paste(c,(30,20)); d=ImageDraw.Draw(o)
for x in range(x0,x1):
    if x%5==0: d.line([(30+(x-x0)*S,20),(30+(x-x0)*S,o.height)],fill=(0,160,255)); d.text((30+(x-x0)*S+1,4),str(x),fill='black')
for y in range(y0,y1):
    if y%5==0: d.line([(30,20+(y-y0)*S),(o.width,20+(y-y0)*S)],fill=(0,160,255)); d.text((2,20+(y-y0)*S+1),str(y),fill='black')
o.save(uit)
