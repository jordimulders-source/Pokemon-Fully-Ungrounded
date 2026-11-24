# vel r6: r6 | r5 | model verkleind (BOX), op 8x; onder op 1x en 2x, licht en donker.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import *; from PIL import ImageDraw; import numpy as np
A=rgba(Image.open('sprite_r6/baltoy_r6.png')); B=rgba(Image.open('sprite_r5/baltoy_r5.png'))
nat=Image.open('gereedschap/natief.png').convert('RGB').crop((15,13,83,83)); mask=Image.fromarray((np.asarray(nat).min(2)<215).astype('uint8')*255)
mo=Image.new('RGBA',(64,64),(0,0,0,0)); W,H=34,35; mi=nat.resize((W,H),Image.BOX).convert('RGBA')
mi.putalpha(mask.resize((W,H),Image.BOX).point(lambda v:255 if v>110 else 0)); mo.paste(mi,((64-W)//2,64-H-1))
Z=8; pan=[('r6',A),('r5',B),('model verkleind (BOX)',mo)]
v=Image.new('RGB',(len(pan)*(64*Z+10)+10,64*Z+30+150),(255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(pan):
    x=10+i*(64*Z+10); v.paste(op(im,(255,255,255,255),Z),(x,24)); d.text((x,6),t,fill=(0,0,0)); y=64*Z+36
    v.paste(op(im,(248,248,240,255),1),(x,y)); v.paste(op(im,(40,44,52,255),1),(x+70,y))
    v.paste(op(im,(248,248,240,255),2),(x+150,y)); v.paste(op(im,(40,44,52,255),2),(x+290,y))
v.save('sprite_r6/vel.png')
