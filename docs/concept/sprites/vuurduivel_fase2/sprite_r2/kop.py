# kop.py SPRITE.png UIT [x0 y0 x1 y1]: spritegebied op 12x naast het natieve model op dezelfde schaal (6x per natieve px), met raster
import sys, numpy as np; from PIL import Image, ImageDraw
sp=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[3:7]) if len(sys.argv)>3 else (12,13,44,36)
# afbeelding sprite->natief: natief = (s - X0)*2 + nx0 ; gegevens uit info.txt
X0,Y0,NX,NY=[int(v) for v in open('info.txt').read().split()]
n=Image.open("natief.png"); z=int(__import__("os").environ.get("Z","12"))
a=n.crop((NX+(x0-X0)*2,NY+(y0-Y0)*2,NX+(x1-X0)*2,NY+(y1-Y0)*2)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
s=Image.new('RGBA',(64,64),(255,255,255,255)); s.alpha_composite(Image.open(sp).convert('RGBA'))
b=s.convert('RGB').crop((x0,y0,x1,y1)).resize(a.size,Image.NEAREST)
for im,c in ((a,(120,120,120)),(b,(120,120,120))):
    d=ImageDraw.Draw(im)
    for i,x in enumerate(range(0,im.width,z)):
        d.line([(x,0),(x,im.height)],fill=c); 
        if i%2==0: d.text((x+1,1),str(x0+i),fill=(0,200,0))
    for j,y in enumerate(range(0,im.height,z)):
        d.line([(0,y),(im.width,y)],fill=c)
        if j%2==0: d.text((1,y+1),str(y0+j),fill=(0,200,0))
v=Image.new('RGB',(a.width*2+12,a.height),'white'); v.paste(a,(0,0)); v.paste(b,(a.width+12,0)); v.save(sys.argv[2])
