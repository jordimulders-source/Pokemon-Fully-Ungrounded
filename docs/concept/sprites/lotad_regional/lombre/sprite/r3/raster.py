# Hulpmiddel: uitsnede van een 64x64-index (npy of png) op Z-voud met rasterlijnen en coördinaten -> png.
import sys, numpy as np; from PIL import Image, ImageDraw
from gemeen import rgb
def raster(o,box,Z,uit):
    x0,y0,x1,y1=box; a=rgb(o,(255,255,255))[y0:y1,x0:x1]
    im=Image.fromarray(a).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    c=Image.new('RGB',(im.width+24,im.height+14),(255,255,255)); c.paste(im,(24,14)); d=ImageDraw.Draw(c)
    for i in range(x1-x0+1): d.line([(24+i*Z,14),(24+i*Z,14+im.height)],fill=(200,200,200) if (x0+i)%5 else (0,120,255))
    for j in range(y1-y0+1): d.line([(24,14+j*Z),(24+im.width,14+j*Z)],fill=(200,200,200) if (y0+j)%5 else (0,120,255))
    for i in range(0,x1-x0,2): d.text((24+i*Z+2,1),str(x0+i),fill=(0,0,0))
    for j in range(0,y1-y0,2): d.text((1,14+j*Z+2),str(y0+j),fill=(0,0,0))
    c.save(uit)
if __name__=='__main__':
    f=sys.argv[1]; o=np.load(f) if f.endswith('.npy') else np.array(Image.open(f))
    raster(o,tuple(int(v) for v in sys.argv[2].split(',')),int(sys.argv[3]),sys.argv[4])
