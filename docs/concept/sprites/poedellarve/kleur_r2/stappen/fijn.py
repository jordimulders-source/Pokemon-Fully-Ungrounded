# fijn.py X0 Y0 X1 Y1 z out [raster pal]: model met elk spritepixel-raster en labels (meten waar lijnen vallen); met raster: sprite ernaast
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/kleur_r2/stappen')
from tl import *
X0,Y0,X1,Y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]
def fg(im):
    d=ImageDraw.Draw(im)
    for i in range(X1-X0+1):
        c=(255,0,0) if (X0+i)%5==0 else (255,255,0)
        d.line([(i*z,0),(i*z,im.height)],fill=c)
        if i<X1-X0: d.text((i*z+2,1),str((X0+i)%100),fill=(255,0,0))
    for j in range(Y1-Y0+1):
        c=(255,0,0) if (Y0+j)%5==0 else (255,255,0)
        d.line([(0,j*z),(im.width,j*z)],fill=c)
        if j<Y1-Y0: d.text((1,j*z+2),str(Y0+j),fill=(255,0,0))
    return im
ims=[fg(model(X0,Y0,X1,Y1,z))]
if len(sys.argv)>7:
    ims.append(fg(rimg(sys.argv[7],sys.argv[8]).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST)))
W=sum(i.width for i in ims)+10*(len(ims)-1); o=Image.new('RGB',(W,ims[0].height),'white'); x=0
for i in ims: o.paste(i,(x,0)); x+=i.width+10
o.save(out)
