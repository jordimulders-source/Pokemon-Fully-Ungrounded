# kijk.py SPRITE x0 y0 x1 y1 out [z]: uitsnede op z (16) met raster, naast het model op spriteschaal (sprite_r1/model_64.png)
import sys; sys.path.insert(0,'sprite_r4'); from gemeen2 import *; import numpy as np; from PIL import Image, ImageDraw
sp=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); out=sys.argv[6]; z=int(sys.argv[7]) if len(sys.argv)>7 else 16
o=np.array(Image.open(sp)); a=rgb(o,(255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),0)
m=Image.open('sprite_r1/model_64.png').crop((x0,y0,x1,y1)).resize(a.size,0)
for t in (a,):
    d=ImageDraw.Draw(t)
    for X in range(x0,x1+1): d.line([((X-x0)*z,0),((X-x0)*z,t.height)],fill=(210,210,220))
    for Y in range(y0,y1+1): d.line([(0,(Y-y0)*z),(t.width,(Y-y0)*z)],fill=(210,210,220))
    for X in range(x0,x1,5): d.text(((X-x0)*z+2,2),str(X),fill=(0,0,200))
    for Y in range(y0,y1,5): d.text((2,(Y-y0)*z+2),str(Y),fill=(0,0,200))
T=Image.new('RGB',(a.width*2+10,a.height),'white'); T.paste(a,(0,0)); T.paste(m,(a.width+10,0)); T.save(out)
