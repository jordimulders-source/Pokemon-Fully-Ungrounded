# vel r4: A | model (natief, BOX-verkleind tot 34x35) | kale reductie | Gen 3-Baltoy, op 8x; onder op 1x en 2x, licht en donker.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import *; from PIL import ImageDraw
import numpy as np
uit=sys.argv[1] if len(sys.argv)>1 else 'sprite_r4/vel.png'
A=Image.open('sprite_r4/baltoy_r4A.png'); A=rgba(A)
kp=png(lees('gereedschap/kaal34.txt'),sys.argv[2] if len(sys.argv)>2 else 'gereedschap/kaal34.png'); kaal=rgba(kp)
nat=Image.open('gereedschap/natief.png').convert('RGB').crop((15,13,83,83))
mask=Image.fromarray((np.asarray(nat).min(2)<215).astype('uint8')*255)
mo=Image.new('RGBA',(64,64),(0,0,0,0)); W,H=34,35
mi=nat.resize((W,H),Image.BOX).convert('RGBA'); mi.putalpha(mask.resize((W,H),Image.BOX).point(lambda v:255 if v>110 else 0)); mo.paste(mi,((64-W)//2,64-H-1))
g3=Image.open('../../../../graphics/pokemon/baltoy/anim_front_gba.png').crop((0,0,64,64)); g3=rgba(g3)
Z=8; pan=[('r4A',A),('model verkleind (BOX)',mo),('kale 2x-reductie',kaal),('Gen 3-Baltoy',g3)]
v=Image.new('RGB',(len(pan)*(64*Z+10)+10,64*Z+30+150),(255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(pan):
    v.paste(op(im,(255,255,255,255),Z),(10+i*(64*Z+10),24)); d.text((10+i*(64*Z+10),6),t,fill=(0,0,0))
y=64*Z+36
for i,(t,im) in enumerate(pan):
    x=10+i*(64*Z+10)
    v.paste(op(im,(248,248,240,255),1),(x,y)); v.paste(op(im,(40,44,52,255),1),(x+70,y))
    v.paste(op(im,(248,248,240,255),2),(x+150,y)); v.paste(op(im,(40,44,52,255),2),(x+290,y))
v.save(uit)
