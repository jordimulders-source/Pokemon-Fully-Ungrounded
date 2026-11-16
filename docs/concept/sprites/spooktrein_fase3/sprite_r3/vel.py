# Vel r3: r3 | r2 | r1 | model (8x); close-ups 12x r3 | r2 | r1 | model; uitsnedes voor/na schrappen; 1x/2x.
import sys; sys.path.insert(0,'.')
from schrap_deel import *
from PIL import Image, ImageDraw
def op(f,bg=(255,255,255)):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
r3=op('sprite.png'); r2=op('../sprite_r2/sprite.png'); r1=op('../sprite_r1/sprite.png'); m=Image.open('../model/model.webp').convert('RGB')
K=13.77; BX,BY,OY=102,71,2
def mcrop(x0,y0,x1,y1,s): return m.crop((int(BX+x0*K),int(BY+(y0-OY)*K),int(BX+x1*K),int(BY+(y1-OY)*K))).resize(((x1-x0)*s,(y1-y0)*s),Image.LANCZOS)
def rgb(o):
    a=np.full(o.shape+(3,),255,'uint8')
    for y in range(o.shape[0]):
        for x in range(o.shape[1]):
            if o[y,x]: a[y,x]=PAL[o[y,x]]
    return Image.fromarray(a)
V=Image.new('RGB',(4*400+20,3000),(235,235,235)); d=ImageDraw.Draw(V)
mm=mcrop(0,0,64,64,6)
for i,(im,t) in enumerate([(r3,'r3'),(r2,'r2'),(r1,'r1'),(mm,'model')]):
    V.paste(im.resize((384,384),Image.NEAREST) if im.size[0]==64 else im,(10+i*400,24)); d.text((10+i*400,6),t+' (6x)',fill=(0,0,0))
Y=420
for naam,(x0,y0,x1,y1) in [('gezicht',(0,26,28,48)),('koeienvanger',(0,44,26,62)),('kleine geest',(12,0,42,15)),('wolkpunten',(40,14,64,50))]:
    s=12 if naam!='wolkpunten' else 8; h=(y1-y0)*s
    d.text((10,Y),naam+' %dx: r3 | r2 | r1 | model'%s,fill=(0,0,0)); x=10
    for im in [r3,r2,r1]:
        c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,h),Image.NEAREST); V.paste(c,(x,Y+16)); x+=c.size[0]+10
    V.paste(mcrop(x0,y0,x1,y1,s),(x,Y+16)); Y+=h+30
d.text((10,Y),'uitsnede natief model 12x | na schrappen 12x (gezicht, koeienvanger, geest)',fill=(0,0,0)); Y+=16
for b in [(10,42,42,67,25,20,(13,14,15,16,28,29,30),(43,44,48,49,50)),(9,40,64,84,24,16,(13,14,15,16,17,22,23,24,31,32,33),()),(29,62,6,22,26,13,(),())]:
    x0,x1,y0,y1,W,H,vk,vr=b; o,*_=verklein(*b)
    n=Image.fromarray(NAT[y0:y1+1,x0:x1+1].astype('uint8')).resize(((x1-x0+1)*12,(y1-y0+1)*12),Image.NEAREST)
    V.paste(n,(10,Y)); V.paste(rgb(o).resize((W*12,H*12),Image.NEAREST),(30+n.size[0],Y)); Y+=n.size[1]+20
d.text((10,Y),'r3 op 1x en 2x, licht en donker',fill=(0,0,0)); x=10
for bg in [(255,255,255),(48,48,64)]:
    s=op('sprite.png',bg); V.paste(s,(x,Y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+80,Y+16)); x+=240
V=V.crop((0,0,V.size[0],Y+160)); V.save('vel.png'); print(V.size)
