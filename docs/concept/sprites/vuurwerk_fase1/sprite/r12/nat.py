# Natief raster (r10/natief.png) vergroot met spritegrid (64-coordinaten) erover
import sys; from PIL import Image, ImageDraw
F,OX,OY=2.4,76.6,14.6; Z=int(sys.argv[6]) if len(sys.argv)>6 else 20
r0,r1,c0,c1=map(int,sys.argv[1:5]); out=sys.argv[5]
n=Image.open('../r10/natief.png').convert('RGB')
nx=lambda c:OX+F*(c-17); ny=lambda r:OY+F*(r-1)
x0,y0=int(nx(c0)),int(ny(r0)); x1,y1=int(nx(c1))+1,int(ny(r1))+1
im=n.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST); d=ImageDraw.Draw(im)
for c in range(c0,c1+1):
    x=(nx(c)-x0)*Z; d.line([(x,0),(x,im.height)],fill=(0,0,255) if c%5==0 else (0,170,255))
    d.text((x+2,2),str(c%100),fill=(0,0,0))
for r in range(r0,r1+1):
    y=(ny(r)-y0)*Z; d.line([(0,y),(im.width,y)],fill=(0,0,255) if r%5==0 else (0,170,255))
    d.text((2,y+2),str(r),fill=(0,0,0))
im.save(out)
