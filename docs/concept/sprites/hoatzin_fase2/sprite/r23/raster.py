# hulpfuncties: beeld op raster (K px per spritepixel), rode lijnen per 8, coördinaten
from PIL import Image, ImageDraw
import numpy as np
from geom import *
def grid(img,K,x0=0,y0=0,label=True):
    d=ImageDraw.Draw(img); W,H=img.size; n=W//K; m=H//K
    for i in range(n+1):
        x=x0+i; d.line([(i*K,0),(i*K,H)],fill=(220,0,0) if x%8==0 else (170,170,170),width=1)
    for j in range(m+1):
        y=y0+j; d.line([(0,j*K),(W,j*K)],fill=(220,0,0) if y%8==0 else (170,170,170),width=1)
    return img
def labels(img,K,pad,x0=0,y0=0,n=64):
    W,H=img.size; c=Image.new('RGB',(W+pad,H+pad),'white'); c.paste(img,(pad,pad)); d=ImageDraw.Draw(c)
    for i in range(n):
        if (x0+i)%2==0: d.text((pad+i*K+1,2),str(x0+i),fill=(200,0,0) if (x0+i)%8==0 else (0,0,0))
    for j in range(n):
        if (y0+j)%2==0: d.text((1,pad+j*K+2),str(y0+j),fill=(200,0,0) if (y0+j)%8==0 else (0,0,0))
    return c
def sprite_rgb(arr,bgcol=(255,255,255)):
    """arr: HxWx3 int, mask: None"""
    return Image.fromarray(arr.astype('uint8'))
def model_img(K,sx0=0,sy0=0,sx1=64,sy1=64):
    im=Image.open('../../MODEL.png').convert('RGB')
    a,b,c,d=model_box(sx0,sy0,sx1,sy1)
    # model buiten 1024 opvullen met wit
    big=Image.new('RGB',(2048,2048),'white'); big.paste(im,(512,512))
    return big.crop((int(round(a))+512,int(round(b))+512,int(round(c))+512,int(round(d))+512)).resize(((sx1-sx0)*K,(sy1-sy0)*K),Image.LANCZOS)
