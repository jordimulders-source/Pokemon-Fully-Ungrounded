# kopraster.py SPRITE.png UIT.png [x0 y0 x1 y1]: kop van de sprite naast het model met hetzelfde raster (kopzone is niet geschrapt: sprite x,y = natieve x,y)
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image, ImageDraw; import numpy as np
from gemeen import *
x0,y0,x1,y1=(list(map(int,sys.argv[3:7])) if len(sys.argv)>6 else [0,12,18,31])
M=Image.open(MODEL).convert('RGB'); z=28
f=lambda u:9.20+0.5+10.24*u
b=M.crop((int(f(U0+x0)),int(f(V0+y0)),int(f(U0+x1)),int(f(V0+y1)))).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
k=np.asarray(Image.open(sys.argv[1])).astype(int)
a=rgb(k,(255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
v=Image.new('RGB',(a.width*2+10,a.height),'white'); v.paste(a,(0,0)); v.paste(b,(a.width+10,0))
d=ImageDraw.Draw(v)
for off in (0,a.width+10):
    for i in range(x1-x0+1): d.line([(off+i*z,0),(off+i*z,a.height)],fill=(0,160,255))
    for j in range(y1-y0+1): d.line([(off,j*z),(off+a.width,j*z)],fill=(0,160,255))
    for i in range(x1-x0): d.text((off+i*z+2,2),str(x0+i),fill=(255,0,255))
    for j in range(y1-y0): d.text((off+2,j*z+2),str(y0+j),fill=(255,0,255))
v.save(sys.argv[2])
