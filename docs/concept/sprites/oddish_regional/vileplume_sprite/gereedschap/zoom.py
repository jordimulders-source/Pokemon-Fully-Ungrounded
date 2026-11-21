# zoom.py SPRITE x0 y0 x1 y1 z UIT : sprite-uitsnede (raster) naast model op dezelfde uitsnede
import sys; sys.path.insert(0,'gereedschap'); from gemeen import *; from PIL import Image, ImageDraw; import numpy as np
im=Image.open(sys.argv[1]); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
x0,y0,x1,y1,z=map(int,sys.argv[2:7])
img=np.full((64,64,3),255,'uint8')
for k in range(1,16): img[o==k]=pal[k]
a=Image.fromarray(img).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); d=ImageDraw.Draw(a)
for x in range(x0,x1):
    d.line([((x-x0)*z,0),((x-x0)*z,a.height)],fill=(200,200,200) if x%5 else (90,90,255))
for y in range(y0,y1):
    d.line([(0,(y-y0)*z),(a.width,(y-y0)*z)],fill=(200,200,200) if y%5 else (90,90,255))
b=model_crop(x0,y0,x1,y1,z)
v=Image.new('RGB',(a.width*2+8,a.height),'white'); v.paste(a,(0,0)); v.paste(b,(a.width+8,0)); v.save(sys.argv[7])
