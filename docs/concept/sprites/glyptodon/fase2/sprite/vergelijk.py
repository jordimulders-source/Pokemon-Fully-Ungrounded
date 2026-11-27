# vergelijk.py sprite.png out [x0 y0 x1 y1 z]: model (BOX op 1x) | sprite, met raster per 5
import sys,numpy as np
from PIL import Image,ImageDraw
from reduceer import X0,Y0,s,LEFT,TOP
k=10.24
def model1x():
    src=Image.open('../model.png').convert('RGB')
    bx=(X0-LEFT*s)*k; by=(Y0-TOP*s)*k; S=64*s*k
    return src.crop((int(bx),int(by),int(bx+S),int(by+S))).resize((64,64),Image.BOX)
def sprite_rgb(f):
    p=Image.open(f); p=p.convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(p); return bg.convert('RGB')
if __name__=='__main__':
    m=model1x(); sp=sprite_rgb(sys.argv[1])
    x0,y0,x1,y1,z=list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else (0,0,64,64,8)
    w,h=(x1-x0)*z,(y1-y0)*z; o=Image.new('RGB',(2*w+8,h),'white')
    for i,im in enumerate((m,sp)):
        c=im.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST); d=ImageDraw.Draw(c)
        for X in range(x0,x1+1):
            if X%5==0: d.line([((X-x0)*z,0),((X-x0)*z,h)],fill=(0,170,0)); d.text(((X-x0)*z+1,1),str(X),fill=(0,120,0))
        for Y in range(y0,y1+1):
            if Y%5==0: d.line([(0,(Y-y0)*z),(w,(Y-y0)*z)],fill=(0,170,0)); d.text((1,(Y-y0)*z+1),str(Y),fill=(0,120,0))
        o.paste(c,(i*(w+8),0))
    o.save(sys.argv[2])
