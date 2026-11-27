# zoom.py SPRITE x0 y0 x1 y1 out : sprite | model op 64 (BOX) | natief model, 12x met raster en coordinaten
import sys; sys.path.insert(0,'sprite_r2'); from gemeen2 import *
from PIL import Image, ImageDraw; import numpy as np
sp,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
o=np.array(Image.open(sp)); z=14
a=rgb(o,(255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),0)
m=Image.open('sprite_r1/model_64.png').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),0)
# natief model op dezelfde uitsnede
N=Image.open(NATIEF).convert('RGB'); ua=(x0-X0)/S+U0; va=(y0-Y0)/S+V0; ub=(x1-X0)/S+U0; vb=(y1-Y0)/S+V0
n=N.crop((int(ua),int(va),int(np.ceil(ub)),int(np.ceil(vb)))).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=(x1-x0)*z; H=(y1-y0)*z; img=Image.new('RGB',(3*W+40,H+20),'white')
for i,t in enumerate((a,m,n)):
    d=ImageDraw.Draw(t)
    for x in range(x0,x1):
        d.line([((x-x0)*z,0),((x-x0)*z,H)],fill=(200,200,255) if i<2 else (120,120,255))
        if i==0: d.text(((x-x0)*z+2,2),str(x%100),fill=(0,0,255))
    for y in range(y0,y1):
        d.line([(0,(y-y0)*z),(W,(y-y0)*z)],fill=(200,200,255) if i<2 else (120,120,255))
        if i==0: d.text((2,(y-y0)*z+2),str(y),fill=(0,0,255))
    img.paste(t,(i*(W+20),0))
img.save(out)
