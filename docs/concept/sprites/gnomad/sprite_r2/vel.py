# vel.py -> AB_8x.png (A | B, 8x) en vel.png (A | B | r1-A op 8x; 1x op licht/donker; 1x naast Gnomini en r1-A)
import sys; sys.path.insert(0,'../sprite_r1')
from PIL import Image, ImageDraw
from kijk import sprite
P=[('gnomad_A.png','r2 A: riem bruin'),('gnomad_B.png','r2 B: riem donkerblauw'),('../sprite_r1/gnomad_A.png','r1 A')]
W=Image.new('RGB',(2*524,536),'white'); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate(P[:2]): W.paste(sprite(p).resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
W.save('AB_8x.png')
V=Image.new('RGB',(3*524,24+512+20+80+20+80),'white'); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate(P): V.paste(sprite(p).resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
y=24+512+20; x=0
for bg in [(255,255,255),(248,248,232),(144,192,152),(40,48,56),(16,16,16)]:
    for p in ('gnomad_A.png','gnomad_B.png'): V.paste(sprite(p,bg),(x,y)); x+=68
    x+=10
y+=100; x=0
for p in ('../../gnomini/af/gnomini.png','gnomad_A.png','gnomad_B.png','../sprite_r1/gnomad_A.png'): V.paste(sprite(p,(248,248,232)),(x,y)); x+=68
V.save('vel.png')
