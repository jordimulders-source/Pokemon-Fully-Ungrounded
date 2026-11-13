# r4/kijk.py pad [y0] : raster op 20x met rooster (controle)
import sys; sys.path.insert(0,'r3'); sys.path.insert(0,'.')
import bouw3,cfg
from PIL import Image,ImageDraw
a=cfg.read(sys.argv[1]); y0=int(sys.argv[2]) if len(sys.argv)>2 else 38
s=cfg.rgba(a,(208,208,176,255)).crop((0,y0,64,64)).resize((1280,(64-y0)*20),Image.NEAREST); d=ImageDraw.Draw(s)
for x in range(64):
    d.line([(x*20,0),(x*20,s.size[1])],fill=(255,255,255) if x%5 else (0,255,0))
    if x%5==0: d.text((x*20+2,0),str(x),fill=(0,255,255))
for y in range(64-y0):
    d.line([(0,y*20),(1280,y*20)],fill=(255,255,255) if (y+y0)%5 else (0,255,0)); d.text((0,y*20+2),str(y+y0),fill=(0,255,255))
s.save(sys.argv[3])
