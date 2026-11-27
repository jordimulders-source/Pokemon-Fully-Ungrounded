# vel.png: r1 (haren A) 1x en 8x | variant haren B 8x | kale reductie 8x | model verkleind 8x | close-up kop 12x (r1 | model)
import numpy as np
from PIL import Image, ImageDraw
from gemeen import *
k=np.load('kaal.npy'); A=np.load('haar_A.npy'); B=np.load('haar_B.npy')
cA=save(A,'kuiken_r1.png'); cB=save(B,'kuiken_r1_haarB.png'); cK=save(k,'kaal.png')
# zones (spritecoördinaten in het 40x44-vak)
H_,W_=k.shape; Y,X=np.mgrid[0:H_,0:W_]
zones={'kop+oog+snavel':(Y<=11)&(X<=16),'vleugel links':(Y>11)&(Y<=32)&(X<=13),
       'lijf+vleugel rechts+staart':(Y>9)&(Y<=31)&(X>13),'poten+tenen':(Y>31)}
for nm,v in (('r1 (haren A)',A),('variant haren B',B)):
    d=v!=k; print(nm,'afwijkend t.o.v. kaal:',d.sum(),{z:int((d&m).sum()) for z,m in zones.items()}, 'px gevuld',int((v>0).sum()))
for nm,c in (('r1',cA),('B',cB)): print(nm,'kleuren gebruikt',len(set(c.flatten())-{0}))
def rg(c,z,bg=(255,255,255)):
    im=Image.fromarray(rgba(c)).resize((c.shape[1]*z,c.shape[0]*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
mo=Image.open('../../model/fase1_model.png').convert('RGB'); a=np.array(mo).sum(2)<700; ys,xs=np.nonzero(a)
mc=mo.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); w=round(mc.width*44/mc.height)
mv=Image.new('RGB',(64,64),'white'); mv.paste(mc.resize((w,44),Image.LANCZOS),((64-w)//2,20))
z=8; P=64*z; vel=Image.new('RGB',(64+10+4*(P+10)+ 2*(24*12)+20, P+40),(200,200,200)); d=ImageDraw.Draw(vel)
x=0
vel.paste(rg(cA,1),(0,20)); vel.paste(rg(cA,1,(40,40,40)),(0,100)); d.text((0,2),'r1 1x',fill=0); x=74
for nm,im in (('r1 (haren A)',rg(cA,z)),('variant haren B',rg(cB,z)),('kale reductie',rg(cK,z)),('model verkleind',mv.resize((P,P),Image.NEAREST))):
    vel.paste(im,(x,20)); d.text((x,2),nm,fill=0); x+=P+10
# close-up kop
kop=rg(cA[20:36,12:36],12); vel.paste(kop,(x,20)); d.text((x,2),'kop r1 12x',fill=0)
mk=mc.crop((0,0,int(mc.width*24/40),int(mc.height*16/44))).resize((24*12,16*12),Image.LANCZOS); vel.paste(mk,(x,20+16*12+10)); d.text((x,20+16*12),'kop model',fill=0)
vel.save('vel.png')
