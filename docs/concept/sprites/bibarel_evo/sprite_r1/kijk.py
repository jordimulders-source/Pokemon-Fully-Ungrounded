# kijk.py SPRITE.png x0 y0 x1 y1 uit.png : spriteregio op 12x met raster en coordinaten naast het model op dezelfde schaal
import sys, numpy as np; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image, ImageDraw
o=laad(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); Z=14
a=Image.open('model/r10_k8.png').convert('RGB'); fig=np.load('sprite_r1/masker.npy')
yy,xx=np.where(fig); mx0,my0=xx.min(),yy.min(); s=64/(xx.max()-mx0+1); H=round((yy.max()-my0+1)*s); oy=64-H
def m2s(): # model op spriteschaal: spritepixel (x,y) <-> model (mx0+x/s, my0+(y-oy)/s)
    W=int((x1-x0)*Z); Hh=int((y1-y0)*Z); im=Image.new('RGB',(W,Hh),'white'); A=np.asarray(a)
    for py in range(Hh):
        for px in range(W):
            X=mx0+(x0+px/Z)/s; Y=my0+(y0+py/Z-oy)/s
            if 0<=X<99 and 0<=Y<99: im.putpixel((px,py),tuple(A[int(Y),int(X)]))
    return im
sp=Image.fromarray(rgb(o[y0:y1,x0:x1])).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
mm=m2s()
c=Image.new('RGB',(sp.width*2+30,sp.height+20),'white'); c.paste(sp,(20,20)); c.paste(mm,(sp.width+30,20))
d=ImageDraw.Draw(c)
for X in range(x0,x1+1):
    for off in (20,sp.width+30): d.line([(off+(X-x0)*Z,20),(off+(X-x0)*Z,20+sp.height)],fill=(90,90,90) if X%5 else (255,0,255))
    if X%5==0: d.text((20+(X-x0)*Z+1,4),str(X),fill='black')
for Y in range(y0,y1+1):
    for off in (20,sp.width+30): d.line([(off,20+(Y-y0)*Z),(off+sp.width,20+(Y-y0)*Z)],fill=(90,90,90) if Y%5 else (255,0,255))
    if Y%5==0: d.text((2,20+(Y-y0)*Z+1),str(Y),fill='black')
c.save(sys.argv[6])
