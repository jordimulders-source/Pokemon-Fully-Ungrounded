# vel r6b | r6 | r5 | model 8x; 1x licht/donker: r6b, r6, r5, Haunter, Banette + r6b 2x
from PIL import Image, ImageDraw; import numpy as np
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def load(p,bg=(255,255,255)):
    src=Image.open(p).crop((0,0,64,64)); idx=np.asarray(src)
    a=np.asarray(src.convert('RGBA')).copy(); a[...,3]=np.where(idx==0,0,255)
    b=Image.new('RGBA',(64,64),bg+(255,)); return Image.alpha_composite(b,Image.fromarray(a)).convert('RGB')
m=Image.open('../sprite_r6/model_geschaald.png').convert('RGB')
F=[('sprite.png','r6b'),('r6.png','r6'),('../sprite_r6/r5.png','r5')]
V=Image.new('RGB',(4*528+16,512+40+190),(236,236,236)); d=ImageDraw.Draw(V)
for n,(im,t) in enumerate([(load(f),t) for f,t in F]+[(m,'model, zelfde schaal')]):
    V.paste(im.resize((512,512),Image.NEAREST),(16+n*528,24)); d.text((16+n*528,8),t+' 8x',fill=0)
y=512+50; x=16
for bg in ((255,255,255),(40,44,60)):
    for p in [f for f,_ in F]+[G+'haunter/anim_front.png',G+'banette/anim_front.png']:
        V.paste(load(p,bg),(x,y)); x+=70
    V.paste(load('sprite.png',bg).resize((128,128),Image.NEAREST),(x,y)); x+=150
d.text((16,y-14),'1x: r6b, r6, r5, Haunter, Banette (licht | donker) + r6b 2x',fill=0); V.save('vel.png')
