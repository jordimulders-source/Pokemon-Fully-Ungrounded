# naast.py raster.txt x0 y0 w h out : overlay model | raster op 16x met coordinaten
import sys
from PIL import Image, ImageDraw
import numpy as np
exec(open('bouw.py').read().split("import sys\ndef dump")[0].split("# ---- 1.")[0])
k=16
rows=[l.rstrip('\n') for l in open(sys.argv[1])]
x0,y0,w,h=map(int,sys.argv[2:6])
im=Image.open(kaal.M).convert('RGB'); f=k/s
big=im.resize((int(W*f),int(H*f)),Image.NEAREST)
A=Image.new('RGB',(OUTW*k,OH*k),(255,255,255)); A.paste(big,(int(-X0*f),int(-Y0*f)))
B=Image.new('RGB',(OUTW*k,OH*k),(200,230,200)); d=ImageDraw.Draw(B)
for y,r in enumerate(rows):
    for x,ch in enumerate(r):
        if ch!='.': d.rectangle([x*k,y*k,x*k+k-1,y*k+k-1],fill=kaal.PAL[int(ch,16)])
def grid(img):
    d=ImageDraw.Draw(img)
    for x in range(OUTW+1): d.line([(x*k,0),(x*k,OH*k)],fill=(255,0,0) if x%4==0 else (255,190,190))
    for y in range(OH+1): d.line([(0,y*k),(OUTW*k,y*k)],fill=(255,0,0) if y%4==0 else (255,190,190))
    for x in range(0,OUTW): d.text((x*k+3,y0*k+2),str(x%10),fill=(220,0,0))
    for y in range(0,OH): d.text((x0*k+3,y*k+3),str(y%10),fill=(220,0,0))
grid(A); grid(B)
box=(x0*k,y0*k,(x0+w)*k,(y0+h)*k)
a1=A.crop(box); b1=B.crop(box)
out=Image.new('RGB',(a1.width*2+8,a1.height),(0,0,0)); out.paste(a1,(0,0)); out.paste(b1,(a1.width+8,0))
out.save(sys.argv[6])
