# kijk.py: sprite (klassen of index) 8x naast het model op dezelfde schaal 8x, met raster. gebruik: kijk(o, uit, rgbfun, dx, x0,x1,y0,y1, z)
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *
from PIL import ImageDraw
def modelblok(dx,x0,y0,x1,y1,z):
    m=Image.open(D+'model/model.png').convert('RGB')
    return m.transform(((x1-x0)*z,(y1-y0)*z),Image.EXTENT,(x0*16+dx,y0*16,x1*16+dx,y1*16),Image.BILINEAR)
def grid(im,x0,y0,z,kl):
    d=ImageDraw.Draw(im)
    for i in range(im.width//z+1):
        d.line([(i*z,0),(i*z,im.height)],fill=kl)
        if i<im.width//z and z>=12: d.text((i*z+1,1),str((x0+i)%100),fill=(255,0,255))
    for j in range(im.height//z+1):
        d.line([(0,j*z),(im.width,j*z)],fill=kl)
        if j<im.height//z and z>=12: d.text((1,j*z+1),str(y0+j),fill=(255,0,255))
    return im
def kijk(o,uit,rgb,dx=16,x0=14,x1=50,y0=0,y1=64,z=8,raster=True):
    A=rgb(o[y0:y1,x0:x1]).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    B=modelblok(dx,x0,y0,x1,y1,z)
    if raster: A=grid(A,x0,y0,z,(200,200,200)); B=grid(B,x0,y0,z,(255,190,190))
    v=Image.new('RGB',(A.width*2+10,A.height),'white'); v.paste(A,(0,0)); v.paste(B,(A.width+10,0)); v.save(uit); return v
