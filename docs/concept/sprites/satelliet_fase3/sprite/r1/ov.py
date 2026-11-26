import sys
from PIL import Image, ImageDraw
import numpy as np
exec(open('bouw.py').read().split("# ---- 1.")[0])
k=20
x0,y0,w,h=map(int,sys.argv[1:5])
im=Image.open(kaal.M).convert('RGB'); f=k/s
big=im.resize((int(W*f),int(H*f)),Image.NEAREST)
A=Image.new('RGB',(OUTW*k,OH*k),(255,255,255)); A.paste(big,(int(round(-X0*f)),int(round(-Y0*f))))
d=ImageDraw.Draw(A)
for x in range(OUTW+1): d.line([(x*k,0),(x*k,OH*k)],fill=(255,0,0) if x%5==0 else (255,170,170))
for y in range(OH+1): d.line([(0,y*k),(OUTW*k,y*k)],fill=(255,0,0) if y%5==0 else (255,170,170))
for x in range(x0,x0+w): d.text((x*k+4,y0*k+4),str(x),fill=(0,0,255))
for y in range(y0,y0+h): d.text((x0*k+4,y*k+4),str(y),fill=(0,0,255))
A.crop((x0*k,y0*k,(x0+w)*k,(y0+h)*k)).save(sys.argv[5])
