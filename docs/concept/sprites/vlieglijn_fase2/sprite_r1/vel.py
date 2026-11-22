# vel.png: kale reductie | mug_r1 | model (8x, zelfde schaal); close-up kop+naald+voorpoten 12x naast model; 1x/2x op licht en donker
import numpy as np; from PIL import Image,ImageDraw
from kaal_pal import PAL
P=np.array(PAL,'uint8'); BG=(236,244,236)
def rgb(f,bg=BG):
    a=np.loadtxt(f,dtype=int); c=P[a].copy(); c[a==0]=bg; return Image.fromarray(c)
nat=Image.open('natief.png').convert('RGB'); X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
def model(x0,y0,x1,y1,S): return nat.transform(((x1-x0)*S,(y1-y0)*S),Image.EXTENT,(X0+(x0-OX)*fx,Y0+(y0-OY)*fy,X0+(x1-OX)*fx,Y0+(y1-OY)*fy),Image.NEAREST)
W=3*512+4*20; vel=Image.new('RGB',(W,30+512+40+30*12+60),'white'); d=ImageDraw.Draw(vel)
for i,(t,im) in enumerate([('kale reductie (kaal.png)',rgb('kaal2.txt')),('mug_r1',rgb('mug_r1.idx')),('model (natief raster, zelfde schaal)',model(0,0,64,64,1))]):
    x=20+i*532; vel.paste(im.resize((512,512),Image.NEAREST),(x,30)); d.text((x,10),t+'  8x',fill='black')
y=30+512+30; x0,y0,x1,y1=2,13,32,43; S=12
d.text((20,y-18),'close-up kop + naald + voorpoten, 12x: mug_r1 | model',fill='black')
cu=rgb('mug_r1.idx').crop((x0,y0,x1,y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
vel.paste(cu,(20,y)); vel.paste(model(x0,y0,x1,y1,S),(20+cu.width+20,y))
dd=ImageDraw.Draw(vel)
for k in range(x1-x0+1):
    for off in (20,20+cu.width+20): dd.line([(off+k*S,y),(off+k*S,y+cu.height)],fill=(205,205,235))
for k in range(y1-y0+1): dd.line([(20,y+k*S),(20+2*cu.width+20,y+k*S)],fill=(205,205,235))
# 1x en 2x
sp=Image.open('mug_r1.png').convert('RGBA'); bx=20+2*cu.width+60; by=y
for j,bg in enumerate([(255,255,255),(232,236,240),(40,48,64)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(sp); vel.paste(t.convert('RGB'),(bx+j*80,by))
    t2=Image.new('RGBA',(128,128),bg+(255,)); t2.alpha_composite(sp.resize((128,128),Image.NEAREST)); vel.paste(t2.convert('RGB'),(bx+j*150,by+90))
d.text((bx,by-18),'1x en 2x op licht en donker',fill='black')
mod1=model(0,0,64,64,1).resize((64,64),Image.BOX) if False else nat.crop((int(X0-OX*fx),int(Y0-OY*fy),int(X0+60*fx),int(Y0+63*fy))).resize((64,64),Image.LANCZOS)
vel.paste(mod1,(bx,by+240)); d.text((bx+70,by+260),'model verkleind (ter vergelijking 1x)',fill='black')
vel=vel.crop((0,0,W,max(by+320,y+cu.height+10))); vel.save('vel.png'); print(vel.size)
