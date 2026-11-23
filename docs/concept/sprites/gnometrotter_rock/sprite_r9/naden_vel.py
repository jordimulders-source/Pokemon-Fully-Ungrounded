# naden_vel.py: naden_12x.png = model | r8 | r9 (rode stippen = modelnaden, skelet) op 12x met raster
import sys; sys.path.insert(0,'../sprite')
import numpy as np
from PIL import Image, ImageDraw
from kijk import model_op_schaal
z=12; x0,y0,x1,y1=12,0,54,60
P=8.1; sk=np.load('model_skelet.npy')
def raster(im):
    d=ImageDraw.Draw(im)
    for i in range(x0,x1+1): d.line([((i-x0)*z,0),((i-x0)*z,im.height)],fill=(255,120,120) if i%5==0 else (205,205,240))
    for j in range(y0,y1+1): d.line([(0,(j-y0)*z),(im.width,(j-y0)*z)],fill=(255,120,120) if j%5==0 else (205,205,240))
    return im
def sp(p):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im)
    return raster(b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST))
m=raster(model_op_schaal(n=64*z).crop((x0*z,y0*z,x1*z,y1*z)))
ims=[m,sp('../sprite_r8/gnometrotter_rock.png'),sp('gnometrotter_rock.png')]
ys,xs=np.nonzero(sk)
for im in ims[1:]:
    d=ImageDraw.Draw(im)
    for my,mx in zip(ys,xs):
        sx=(mx-512)/P+32; sy=(my-523)/P+60
        if x0<=sx<x1 and y0<=sy<y1: d.point(((sx-x0)*z,(sy-y0)*z),fill=(255,0,0))
w=m.width; O=Image.new('RGB',(3*w+20,m.height),'white')
for i,im in enumerate(ims): O.paste(im,(i*(w+10),0))
O.save('naden_12x.png')
