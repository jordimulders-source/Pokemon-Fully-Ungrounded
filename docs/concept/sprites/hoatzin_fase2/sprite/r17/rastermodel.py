# raster_model.png: r17 op raster | model op raster (zelfde schaal/plek), 10x
import sys; from PIL import Image
from raster import *
K=10; src=sys.argv[1] if len(sys.argv)>1 else 'hoatzin.png'; out=sys.argv[2] if len(sys.argv)>2 else 'raster_model.png'
s=Image.open(src).convert('RGBA'); w=Image.new('RGB',(64,64),'white'); w.paste(s,(0,0),s)
a=labels(grid(w.resize((64*K,64*K),Image.NEAREST),K),K,18); b=labels(grid(model_img(K),K),K,18)
c=Image.new('RGB',(a.width*2+10,a.height),'white'); c.paste(a,(0,0)); c.paste(b,(a.width+10,0)); c.save(out)
