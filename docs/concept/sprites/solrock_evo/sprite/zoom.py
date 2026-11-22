# zoom.py sprite.png x0 y0 x1 y1 uit.png : sprite-uitsnede op 12x naast hetzelfde stuk model
import sys,numpy as np; from PIL import Image
S=11.87; X0=138-0.5*S; Y0=107-1.2*S
f=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); z=12
Image.open(f).save('/tmp/_z.png',transparency=0)
sp=Image.open('/tmp/_z.png').convert('RGBA'); bgc=Image.new('RGBA',sp.size,(200,220,200,255)); bgc.alpha_composite(sp)
a=bgc.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
m=Image.open('../referenties/model.png').convert('RGBA')
b=m.crop((int(X0+x0*S),int(Y0+y0*S),int(X0+x1*S),int(Y0+y1*S))).resize(a.size,Image.LANCZOS)
o=Image.new('RGBA',(a.width*2+8,a.height),(255,255,255,255)); o.paste(a,(0,0)); o.paste(b,(a.width+8,0))
# raster op 12x
from PIL import ImageDraw; d=ImageDraw.Draw(o)

o.save(sys.argv[6])
