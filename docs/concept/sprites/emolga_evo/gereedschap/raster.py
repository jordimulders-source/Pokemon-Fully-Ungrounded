# raster.py: model per spritecel met rasterlijnen en coordinaten naast de sprite (robotmug-les: niet gokken).
# gebruik: raster(o, s, ox, oy, x0,y0,x1,y1, uit, z=40, model=pad)
from gemeen import *
from PIL import ImageDraw
P=10.238; C0=9.35+0.5
def modelcrop(s,ox,oy,x0,y0,x1,y1,z,model=None):
    m=Image.open(model or D+'model/model.png').convert('RGB')
    f=lambda X,o:C0+(X-o)/s*P
    return m.transform(((x1-x0)*z,(y1-y0)*z),Image.EXTENT,(f(x0,ox),f(y0,oy),f(x1,ox),f(y1,oy)),Image.BILINEAR)
def grid(im,x0,y0,z,kl=(255,0,0)):
    d=ImageDraw.Draw(im)
    for i in range(im.width//z+1):
        d.line([(i*z,0),(i*z,im.height)],fill=kl); 
        if i<im.width//z: d.text((i*z+2,2),str(x0+i),fill=(255,0,255))
    for j in range(im.height//z+1):
        d.line([(0,j*z),(im.width,j*z)],fill=kl)
        if j<im.height//z: d.text((2,j*z+2),str(y0+j),fill=(255,0,255))
    return im
def raster(o,s,ox,oy,x0,y0,x1,y1,uit,z=40,model=None,kleuren=None):
    A=grid(modelcrop(s,ox,oy,x0,y0,x1,y1,z,model),x0,y0,z)
    B=grid(rgbk(o[y0:y1,x0:x1],(200,230,200),kleuren).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),x0,y0,z,(120,120,120))
    v=Image.new('RGB',(A.width*2+10,A.height),'white'); v.paste(A,(0,0)); v.paste(B,(A.width+10,0)); v.save(uit)
