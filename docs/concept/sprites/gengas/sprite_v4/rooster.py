# Close-up met raster en coördinaten: rooster.py uit.png y0 y1 x0 x1 bestand... (schaal 16)
import sys
from toon import laad
from gemeen import *
from PIL import ImageDraw
out=sys.argv[1]; y0,y1,x0,x1=map(int,sys.argv[2:6]); fs=sys.argv[6:]; s=16
W=(x1-x0)*s; H=(y1-y0)*s
C=Image.new('RGB',((W+20)*len(fs)+20,H+20),'white'); d=ImageDraw.Draw(C)
for i,f in enumerate(fs):
    a=laad(f)[y0:y1,x0:x1]; im=Image.fromarray(a).resize((W,H),Image.NEAREST)
    ox=20+i*(W+20); C.paste(im,(ox,20))
    for x in range(x1-x0+1): d.line([(ox+x*s,20),(ox+x*s,20+H)],fill=(200,200,200) if (x0+x)%5 else (0,160,255))
    for y in range(y1-y0+1): d.line([(ox,20+y*s),(ox+W,20+y*s)],fill=(200,200,200) if (y0+y)%5 else (0,160,255))
    for x in range(x0,x1):
        if x%5==0: d.text((ox+(x-x0)*s+2,4),str(x),fill=(0,0,200))
    for y in range(y0,y1):
        if y%5==0 and i==0: d.text((2,20+(y-y0)*s+2),str(y),fill=(0,0,200))
C.save(out)
