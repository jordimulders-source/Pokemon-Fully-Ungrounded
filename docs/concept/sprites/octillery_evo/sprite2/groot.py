# groot.py raster uit.png k [x0 y0 x1 y1]: sprite kx met raster om de 8 px
import cfg,sys
from PIL import Image,ImageDraw
a=cfg.read(sys.argv[1]); k=int(sys.argv[3]); b=list(map(int,sys.argv[4:8])) if len(sys.argv)>4 else [0,0,64,64]
im=cfg.rgba(a,(208,208,176,255)).crop(b).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST); d=ImageDraw.Draw(im)
for x in range(b[0],b[2]):
    if x%8==0: d.line([((x-b[0])*k,0),((x-b[0])*k,im.size[1])],fill=(150,150,120)); d.text(((x-b[0])*k+2,1),str(x),fill=(0,0,0))
for y in range(b[1],b[3]):
    if y%8==0: d.line([(0,(y-b[1])*k),(im.size[0],(y-b[1])*k)],fill=(150,150,120)); d.text((1,(y-b[1])*k+1),str(y),fill=(0,0,0))
im.save(sys.argv[2])
