# vel.png: r3 1x (licht/donker, B) | r3 haren A 8x | r3 haren B 8x | r2 8x | model verkleind | close-ups kop (r3 | model) en voeten
import numpy as np
from PIL import Image, ImageDraw
from gemeen import *
k=np.load('kaal.npy'); A=np.load('haar_A.npy'); B=np.load('haar_B.npy')
cA=save(A,'kuiken_r3.png'); cB=save(B,'kuiken_r3_haarB.png'); save(k,'kaal.png')
H_,W_=k.shape; Y,X=np.mgrid[0:H_,0:W_]
zones={'kop+oog+snavel':(Y<=11)&(X<=16),'vleugel links':(Y>11)&(Y<=32)&(X<=13),
       'lijf (dons+geel)':(Y>9)&(Y<=31)&(X>13)&np.isin(k,[2,3,4,6,7]),
       'vleugel rechts+staart+dij':(Y>9)&(Y<=31)&(X>13)&~np.isin(k,[2,3,4,6,7]),'poten+tenen':(Y>31)}
for nm,v in (('r3 haren A',A),('r3 haren B',B)):
    d=v!=k; print(nm,'afwijkend t.o.v. kaal:',int(d.sum()),{z:int((d&m).sum()) for z,m in zones.items()},
                 'gevuld',int((v>0).sum()),'zwart %',round((v==1).sum()/(v>0).sum()*100,1))
print('kleuren gebruikt',len(set(cA.flatten())-{0}))
def rg(c,z,bg=(255,255,255)):
    im=Image.fromarray(rgba(c)).resize((c.shape[1]*z,c.shape[0]*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
r1=np.array(Image.open('../r2/kuiken_r2.png'))
mo=Image.open('../../model/fase1_model.png').convert('RGB'); a=np.array(mo).sum(2)<700; ys,xs=np.nonzero(a)
mc=mo.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); w=round(mc.width*44/mc.height)
mv=Image.new('RGB',(64,64),'white'); mv.paste(mc.resize((w,44),Image.LANCZOS),((64-w)//2,20))
z=8; P=64*z; Pc=24*12
vel=Image.new('RGB',(74+4*(P+10)+Pc+10, P+40),(200,200,200)); d=ImageDraw.Draw(vel)
vel.paste(rg(cA,1),(0,20)); vel.paste(rg(cA,1,(40,40,40)),(0,100)); vel.paste(rg(cB,1),(0,180)); d.text((0,2),'r3 1x',fill=0); d.text((0,168),'B 1x',fill=0); x=74
for nm,im in (('r3 haren A',rg(cA,z)),('r3 haren B',rg(cB,z)),('r2',rg(r1,z)),('model verkleind (zonder Jordis wijzigingen)',mv.resize((P,P),Image.NEAREST))):
    vel.paste(im,(x,20)); d.text((x,2),nm,fill=0); x+=P+10
fx=lambda x0,y0,ww,hh: mc.crop((int(mc.width*x0/40),int(mc.height*y0/44),int(mc.width*(x0+ww)/40),int(mc.height*(y0+hh)/44))).resize((ww*12,hh*12),Image.LANCZOS)
vel.paste(rg(cA[20:32,12:30],12),(x,20)); d.text((x,2),'kop r3 | model',fill=0)
vel.paste(fx(0,0,18,12),(x,20+144+4))
vel.paste(rg(cA[52:64,26:50],12),(x,20+2*148+10)); d.text((x,20+2*148),'voeten r3',fill=0)
vel.save('vel.png')
