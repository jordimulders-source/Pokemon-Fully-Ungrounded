# Model (model.webp, op het natieve raster uitgelijnd: cel nx = 10,25+nx*10,24 px) op 16x met de spritecontour (blauw) van r20/r21.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r21'); sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from vorm import *
from vel import bg,rij,label
from PIL import ImageDraw
M=Image.open(D+'model/model.webp').convert('RGB')
x0,y0,x1,y1=0,40,36,62; Z=16
m2=lambda n:10.25+n*10.24
def cont(im,SI,col):
    d=ImageDraw.Draw(im)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if not SI[y,x]: continue
            X,Y=(x-x0)*Z,(y-y0)*Z
            if not SI[y-1,x]: d.line((X,Y,X+Z,Y),fill=col,width=2)
            if not SI[y+1,x]: d.line((X,Y+Z,X+Z,Y+Z),fill=col,width=2)
            if x==0 or not SI[y,x-1]: d.line((X,Y,X,Y+Z),fill=col,width=2)
            if not SI[y,x+1]: d.line((X+Z,Y,X+Z,Y+Z),fill=col,width=2)
    return im
nx0,ny0=s2n(x0,y0); nx1,ny1=s2n(x1,y1)
mod=M.crop((int(m2(nx0)),int(m2(ny0)),int(m2(nx1)),int(m2(ny1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS).convert('RGBA')
outs=[]
for p in ('sprite_r21/sprite.png','sprite_r20/sprite.png'):
    r=np.array(Image.open(D+p)).astype(int); SI=(r!=0)&~np.isin(r,GRS)
    sp=bg(Image.open(D+p)).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    outs.append(label(cont(sp,MI,(255,0,0)),p[:10]+' + modelijzer (rood)'))
outs.append(label(cont(mod.copy(),SI,(0,90,255)),'model.webp + spriteijzer (blauw)'))
rij(outs).convert('RGB').save(D+'sprite_r21/vorm_16x.png')
