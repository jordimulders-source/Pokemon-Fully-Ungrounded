# vel.py (awki: close-ups kop+kuif x20-46 y2-30 en opgeheven vleugel x3-25 y2-40) raster.txt pal out.png [vorige_raster vorige_pal]: sprite | (vorige) | model op 8x; close-ups kop en vleugel op 12x; 1x (licht, donker, model BOX) + 2x
import sys
import tl
from tl import Image,ImageDraw,model,rimg,src
rf,pf,out=sys.argv[1:4]
BG=(248,248,240)
def label(im,t):
    d=ImageDraw.Draw(im); d.rectangle([0,0,len(t)*6+4,11],fill=(255,255,255)); d.text((2,0),t,fill=(0,0,0)); return im
ims=[label(rimg(rf,pf,BG).resize((512,512),Image.NEAREST),'sprite')]
if len(sys.argv)>5: ims.append(label(rimg(sys.argv[4],sys.argv[5],BG).resize((512,512),Image.NEAREST),'vorige ronde'))
ims.append(label(model(0,0,64,64,8),'model'))
def row(ims,gap=10):
    o=Image.new('RGB',(sum(i.width for i in ims)+gap*(len(ims)-1),max(i.height for i in ims)),'white'); x=0
    for i in ims: o.paste(i,(x,0)); x+=i.width+gap
    return o
def cu(X0,Y0,X1,Y1,z,t):
    return row([label(rimg(rf,pf,BG).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST),t+' sprite'),label(model(X0,Y0,X1,Y1,z),t+' model')])
top=row(ims); mid=row([cu(20,2,46,30,12,'kop+kuif'),cu(3,2,25,40,12,'vleugel')],20)
# vleugellijnen: alleen de lijnpixels (5, 2, 1 en 8/9-lijnen) vol, de rest vervaagd; naast het model (opgeheven vleugel x3-25 y8-40, gevouwen x32-50 y26-50)
import numpy as np
def lijnen(X0,Y0,X1,Y1,z,t,keep):
    R=tl.raster(rf); a=np.asarray(rimg(rf,pf,BG)).astype(float).copy()
    for y in range(64):
        for x in range(64):
            if R[y][x] not in keep: a[y,x]=a[y,x]*0.3+np.array(BG)*0.7
    im=Image.fromarray(a.astype('uint8')).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST)
    return row([label(im,t+' lijnen sprite'),label(model(X0,Y0,X1,Y1,z),t+' model')])
lin=row([lijnen(3,8,25,40,12,'vleugel','125'),lijnen(32,26,50,50,12,'gevouwen','12')],20)
mid=Image.fromarray(np.vstack([np.asarray(row([mid],0)),np.full((10,mid.width,3),255,'uint8')])) if False else mid
_m=Image.new('RGB',(max(mid.width,lin.width),mid.height+lin.height+10),'white'); _m.paste(mid,(0,0)); _m.paste(lin,(0,mid.height+10)); mid=_m
mb=model(0,0,64,64,1) if False else tl.model(0,0,64,64,8).resize((64,64),Image.BOX)
ones=[rimg(rf,pf,BG),rimg(rf,pf,(40,48,64)),mb]
bot=row(ones+[i.resize((128,128),Image.NEAREST) for i in ones],16)
W=max(top.width,mid.width,bot.width); O=Image.new('RGB',(W,top.height+mid.height+bot.height+20),'white')
O.paste(top,(0,0)); O.paste(mid,(0,top.height+10)); O.paste(bot,(0,top.height+mid.height+20)); O.save(out)
