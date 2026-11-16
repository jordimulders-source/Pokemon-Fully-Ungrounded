# zij.py sprite x0 y0 x1 y1 S out : sprite en model naast elkaar met raster (rood = veelvoud van 5)
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image, ImageDraw
from meet import crop
sp=sys.argv[1]; x0,y0,x1,y1,S=map(int,sys.argv[2:7]); out=sys.argv[7]
im=Image.open(sp); a=np.asarray(im); p=np.array(im.getpalette()[:768]).reshape(-1,3); r=p[a].astype('uint8'); r[a==0]=255
A=Image.fromarray(r).resize((64*S,64*S),Image.NEAREST); B=crop.resize((64*S,64*S),Image.LANCZOS)
box=(x0*S,y0*S,(x1+1)*S,(y1+1)*S); A=A.crop(box); B=B.crop(box)
def grid(c):
    d=ImageDraw.Draw(c)
    for x in range(x0,x1+2): d.line([((x-x0)*S,0),((x-x0)*S,c.size[1])],fill=(255,0,0) if x%5==0 else (120,200,255))
    for y in range(y0,y1+2): d.line([(0,(y-y0)*S),(c.size[0],(y-y0)*S)],fill=(255,0,0) if y%5==0 else (120,200,255))
    d.text((2,2),'%d,%d'%(x0,y0),fill=(255,0,0))
grid(A); grid(B)
v=Image.new('RGB',(A.size[0]*2+8,A.size[1]),'white'); v.paste(A,(0,0)); v.paste(B,(A.size[0]+8,0)); v.save(out)
