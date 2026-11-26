import sys
from vergelijk import *
k=18
A=modelk(k); B=rast(sys.argv[1],k)
x0,x1,y0,y1=map(int,sys.argv[2:6])
for img in (A,B):
    d=ImageDraw.Draw(img)
    for x in range(OUTW+1): d.line([(x*k,0),(x*k,OH*k)],fill=(255,0,0) if x%5==0 else (235,200,200))
    for y in range(OH+1): d.line([(0,y*k),(OUTW*k,y*k)],fill=(255,0,0) if y%5==0 else (235,200,200))
    for x in range(x0,x1): d.text((x*k+3,y0*k+2),str(x%10),fill=(0,0,255))
    for y in range(y0,y1): d.text((x0*k+3,y*k+3),str(y%10),fill=(0,0,255))
box=(x0*k,y0*k,x1*k,y1*k)
a,b=A.crop(box),B.crop(box)
out=Image.new('RGB',(a.width*2+6,a.height),(0,0,0)); out.paste(b,(0,0)); out.paste(a,(a.width+6,0)); out.save(sys.argv[6])
