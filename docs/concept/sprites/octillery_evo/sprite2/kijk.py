# kijk.py raster uit.png [schaal] : sprite Nx naast model64
import cfg,sys
from PIL import Image
a=cfg.read(sys.argv[1]); k=int(sys.argv[3]) if len(sys.argv)>3 else 8
m=cfg.model64().resize((64*k,64*k),Image.NEAREST); s=cfg.rgba(a,(208,208,176,255)).resize((64*k,64*k),Image.NEAREST)
v=Image.new('RGB',(64*k*2+8,64*k),(255,255,255)); v.paste(m,(0,0)); v.paste(s,(64*k+8,0)); v.save(sys.argv[2])
