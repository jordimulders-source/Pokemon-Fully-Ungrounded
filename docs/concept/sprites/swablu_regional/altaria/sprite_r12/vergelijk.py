# vergelijk.py: r11A | K1 | K2 op 8x, koppen 16x, 1x op licht/donker. python3 sprite_r12/vergelijk.py
from PIL import Image, ImageDraw
P=[('r11A','sprite_r11/altaria_r11A.png'),('r12 K1 (kuif blijft)','sprite_r12/altaria_r12_K1.png'),('r12 K2 (kuif schuift mee)','sprite_r12/altaria_r12_K2.png')]
def plat(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
box=(14,4,40,32); Z=16
w=(box[2]-box[0])*Z
vel=Image.new('RGB',(3*528,24+512+30+(box[3]-box[1])*Z+20+90),'white'); d=ImageDraw.Draw(vel)
for i,(t,p) in enumerate(P):
    vel.paste(plat(p).resize((512,512),Image.NEAREST),(i*528,24)); d.text((i*528+4,6),t,fill=(0,0,0))
    y=24+512+24; vel.paste(plat(p).crop(box).resize((w,(box[3]-box[1])*Z),Image.NEAREST),(i*528,y))
    y2=y+(box[3]-box[1])*Z+16
    for j,bg in enumerate(((255,255,255),(232,224,200),(80,96,120),(24,24,32))): vel.paste(plat(p,bg),(i*528+j*76,y2))
d.text((4,24+512+8),'koppen 16x (X14-39, Y4-31)',fill=(0,0,0))
vel.save('sprite_r12/vergelijking.png')
