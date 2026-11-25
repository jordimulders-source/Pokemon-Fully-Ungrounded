# model-uitsnede met spritepixelraster eroverheen, voor het aflezen van weggevallen rasterlijnen
import sys, numpy as np
from PIL import Image, ImageDraw
from common import M
s=3.515625; X0=Y0=3
def crop(x0,y0,w,h,Z=24,out='g.png'):
    m=Image.open(M).convert('RGB')
    box=(X0+x0*s,Y0+y0*s,X0+(x0+w)*s,Y0+(y0+h)*s)
    c=m.crop(tuple(int(round(v)) for v in box))
    W,H=w*Z,h*Z; c=c.resize((W,H),Image.NEAREST); d=ImageDraw.Draw(c)
    for i in range(w+1): d.line([(i*Z,0),(i*Z,H)],fill=(255,0,0) if (x0+i)%5==0 else (0,180,0))
    for j in range(h+1): d.line([(0,j*Z),(W,j*Z)],fill=(255,0,0) if (y0+j)%5==0 else (0,180,0))
    c.save(out)
if __name__=='__main__':
    a=list(map(int,sys.argv[1:5])); crop(*a,out=sys.argv[5])
