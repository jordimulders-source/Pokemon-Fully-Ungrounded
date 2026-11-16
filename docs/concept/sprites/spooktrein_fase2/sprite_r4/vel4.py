# vel: r4 | r3 | model (zelfde schaal) op 8x; close-up wielzone 12x: r4 | r3 | model r5 | r6-wiel; 1x/2x licht/donker
from PIL import Image, ImageDraw; import numpy as np
def load(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); return Image.alpha_composite(b,im).convert('RGB')
r4,r3=load('sprite.png'),load('../sprite_r3/sprite.png'); m=Image.open('../sprite_r2/model_geschaald.png').convert('RGB')
V=Image.new('RGB',(3*512+64,512+40+300+40+150),(236,236,236)); d=ImageDraw.Draw(V)
for n,(im,t) in enumerate(((r4,'r4'),(r3,'r3'),(m,'model r5, zelfde schaal'))):
    V.paste(im.resize((512,512),Image.NEAREST),(16+n*528,24)); d.text((16+n*528,8),t+' 8x',fill=0)
y=512+56; box=(16,42,36,60); Z=12
d.text((16,y-14),'wielzone 12x: r4 | r3 | model r5 (zelfde uitsnede) | r6 (niet gebruikt, ter vergelijking)',fill=0)
for n,im in enumerate((r4,r3,m)): V.paste(im.crop(box).resize((20*Z,18*Z),Image.NEAREST),(16+n*260,y))
mm=Image.open('../model/model_r5.png').convert('RGB').crop((int(39*5.12+16/0.4468*5.12+5),int(22*5.12+42/0.4468*5.12+5),int(39*5.12+36/0.4468*5.12+5),int(22*5.12+60/0.4468*5.12+5))).resize((240,216))
V.paste(mm,(16+3*260,y))
r6=Image.open('../referenties/r6.png').convert('RGB').crop((350,670,580,870)).resize((248,216)); V.paste(r6,(16+4*260,y))
y+=260; x=16
for p in ('sprite.png','../sprite_r3/sprite.png'):
    for bg in ((255,255,255),(40,44,60)):
        im=load(p,bg); V.paste(im,(x,y)); V.paste(im.resize((128,128),Image.NEAREST),(x+70,y)); x+=215
V.paste(m,(x,y)); V.paste(m.resize((128,128),Image.NEAREST),(x+70,y)); d.text((16,y-14),'1x/2x: r4 licht, r4 donker, r3 licht, r3 donker, model',fill=0)
V.save('vel.png')
