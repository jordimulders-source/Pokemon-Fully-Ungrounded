# zoom.py UIT.png x0 y0 x1 y1 sprite.png [...]: uitsnede op 12x met raster + coordinaten, plus model op schaal
import sys, numpy as np; from PIL import Image, ImageDraw
from kijk import lees, model_op_schaal
out=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); z=12
ims=[lees(p) for p in sys.argv[6:]]+[model_op_schaal()]
pan=[]
for im in ims:
    a=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); d=ImageDraw.Draw(a)
    for i,x in enumerate(range(0,a.width,z)):
        d.line([(x,0),(x,a.height)],fill=(210,210,210))
        if (x0+i)%5==0: d.text((x+1,1),str(x0+i),fill=(0,0,200))
    for j,y in enumerate(range(0,a.height,z)):
        d.line([(0,y),(a.width,y)],fill=(210,210,210))
        if (y0+j)%5==0: d.text((1,y+1),str(y0+j),fill=(200,0,0))
    pan.append(a)
W=Image.new('RGB',(sum(p.width+6 for p in pan),pan[0].height),'white'); x=0
for p in pan: W.paste(p,(x,0)); x+=p.width+6
W.save(out)
