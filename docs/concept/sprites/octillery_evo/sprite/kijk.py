# kijk.py raster out [x0 y0 x1 y1 z]: model (bron, uitsnede) | sprite, zelfde schaal, met raster elke 5 px
import cfg,sys,numpy as np
from PIL import Image,ImageDraw
a=cfg.read(sys.argv[1]); out=sys.argv[2]
x0,y0,x1,y1,z=map(int,sys.argv[3:8]) if len(sys.argv)>3 else (0,22,64,64,8)
src=Image.open(cfg.MODEL).convert('RGB')
bx=cfg.X0+(x0-cfg.LEFT)*cfg.S; by=cfg.Y0+(y0-cfg.TOP)*cfg.S
big=Image.new('RGB',(3000,2000),(254,254,254)); big.paste(src,(1000,1000))
m=big.crop((int(1000+bx),int(1000+by),int(1000+bx+(x1-x0)*cfg.S),int(1000+by+(y1-y0)*cfg.S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
s=cfg.rgba(a,(150,210,170,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
w=(x1-x0)*z; o=Image.new('RGB',(2*w+10,(y1-y0)*z),'white'); o.paste(m,(0,0)); o.paste(s,(w+10,0))
d=ImageDraw.Draw(o)
for X in range(x0,x1+1):
  if X%5==0:
    for off in (0,w+10): d.line([(off+(X-x0)*z,0),(off+(X-x0)*z,o.height)],fill=(0,140,255)); d.text((off+(X-x0)*z+2,2),str(X),fill=(0,0,255))
for Y in range(y0,y1+1):
  if Y%5==0:
    d.line([(0,(Y-y0)*z),(o.width,(Y-y0)*z)],fill=(0,140,255)); d.text((2,(Y-y0)*z+2),str(Y),fill=(0,0,255))
o.save(out)
