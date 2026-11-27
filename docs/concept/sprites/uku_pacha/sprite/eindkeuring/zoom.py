# python3 zoom.py raster.txt x0 y0 x1 y1 [s] out.png  -> sprite | model (met spritegrid)
import sys; from lib import *
R=lees(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); s=int(sys.argv[6]); out=sys.argv[7]
a=rgb(R).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
b=model_in_sprite(x0,y0,x1,y1,s)
grid(a,s); grid(b,s,(255,0,0))
v=Image.new('RGB',(a.width*2+10,a.height),(255,255,255)); v.paste(a,(0,0)); v.paste(b,(a.width+10,0)); v.save(out)
