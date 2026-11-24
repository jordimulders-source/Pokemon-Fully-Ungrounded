# vel.py -> AB_8x.png (A | B op 8x, wit) en vel.png (A | B | model op schaal 8x; 1x op licht/donker; 1x naast Gnomini voor de lijn)
from PIL import Image, ImageDraw
from kijk import sprite, model_op_schaal
z=8
A=sprite('gnomad_A.png'); B=sprite('gnomad_B.png'); M=model_op_schaal()
W=Image.new('RGB',(2*512+12,512+24),'white'); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate(((A,'A: riem warm bruin'),(B,'B: riem donkerblauw (Gnomini-streep)'))):
    W.paste(p.resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
W.save('AB_8x.png')
V=Image.new('RGB',(3*524,24+512+20+80+20+140),'white'); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate(((A,'A: riem warm bruin'),(B,'B: riem donkerblauw (Gnomini-streep)'),(M,'model r1 (natief, op schaal)'))):
    V.paste(p.resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
y=24+512+20; x=0; d.text((0,y-14),'1x op licht en donker (A, B)',fill=(0,0,0))
for bg in [(255,255,255),(248,248,232),(144,192,152),(40,48,56),(16,16,16)]:
    for p in ('gnomad_A.png','gnomad_B.png'):
        V.paste(sprite(p,bg),(x,y)); x+=68
    x+=10
y2=y+80+20; d.text((0,y2-14),'1x en 2x naast Gnomini (af) - lijn',fill=(0,0,0)); x=0
G='../../gnomini/af/gnomini.png'
for p in (G,'gnomad_A.png','gnomad_B.png'):
    V.paste(sprite(p,(248,248,232)),(x,y2)); x+=68
x+=20
for p in (G,'gnomad_A.png','gnomad_B.png'):
    V.paste(sprite(p,(248,248,232)).resize((128,128),Image.NEAREST),(x,y2)); x+=136
V.save('vel.png'); print(V.size)
