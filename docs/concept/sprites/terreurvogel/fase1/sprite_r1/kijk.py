# Close-up: sprite | model (zelfde raster) op kx, uitsnede x0,y0,x1,y1 (spritecoordinaten)
import sys, numpy as np; from PIL import Image
from lib import *; from modelover import modelbeeld
pad,uit=sys.argv[1],sys.argv[2]; x0,y0,x1,y1=map(int,sys.argv[3:7]); k=int(sys.argv[7])
a=np.array(Image.open(pad)); sp=rgba(a,k=k); bg=Image.new('RGBA',sp.size,(236,236,236,255)); bg.alpha_composite(sp)
m=modelbeeld(k).convert('RGBA')
box=(x0*k,y0*k,x1*k,y1*k); A=bg.crop(box); M=m.crop(box)
v=Image.new('RGBA',(A.width*2+10,A.height),(255,255,255,255)); v.paste(A,(0,0)); v.paste(M,(A.width+10,0)); v.save(uit)
