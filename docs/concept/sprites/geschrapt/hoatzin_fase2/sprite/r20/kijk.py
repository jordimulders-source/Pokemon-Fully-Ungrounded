# kijk.py uit.png [x0 y0 x1 y1 K]: r19 | r17 | model, zelfde uitsnede
import sys, numpy as np; from PIL import Image
from raster import model_img
x0,y0,x1,y1,K=(list(map(int,sys.argv[2:7])) if len(sys.argv)>6 else [0,0,64,64,8])
def wit(p):
    s=Image.open(p).convert('RGBA'); w=Image.new('RGB',(64,64),'white'); w.paste(s,(0,0),s); return w.crop((x0,y0,x1,y1)).resize(((x1-x0)*K,(y1-y0)*K),Image.NEAREST)
ps=[wit('hoatzin.png'),wit('../r17/hoatzin.png'),model_img(K,x0,y0,x1,y1)]
c=Image.new('RGB',(sum(p.width for p in ps)+20,ps[0].height),'white'); x=0
for p in ps: c.paste(p,(x,0)); x+=p.width+10
c.save(sys.argv[1])
