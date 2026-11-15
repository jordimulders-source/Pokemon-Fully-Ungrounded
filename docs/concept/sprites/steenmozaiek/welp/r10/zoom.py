# Modeluitsnede met spriteraster en coordinaten; optioneel sprite ernaast. python3 zoom.py x0,y0,x1,y1 z out [a.npy]
import sys,numpy as np
from PIL import Image, ImageDraw
from zie import mod, raster, F
from toon6 import big
def lab(c,b,z):
    d=ImageDraw.Draw(c)
    for i in range(b[2]-b[0]): d.text((i*z+2,2),str(b[0]+i),fill=(0,0,255))
    for j in range(b[3]-b[1]): d.text((2,j*z+2),str(b[1]+j),fill=(0,0,255))
    return c
b=tuple(map(int,sys.argv[1].split(','))); z=int(sys.argv[2])
c=lab(raster(mod(b,z),b,z),b,z)
if len(sys.argv)>4:
    a=np.load(sys.argv[4])[b[1]:b[3],b[0]:b[2]]; s=lab(raster(big(a,z,F),b,z),b,z)
    V=Image.new('RGBA',(c.width*2+8,c.height),(255,255,255,255)); V.alpha_composite(s,(0,0)); V.alpha_composite(c,(c.width+8,0)); c=V
c.save(sys.argv[3])
