# vel.py -> AB_8x.png (A | B, 8x) en vel.png (A | B | r2-A | Machoke-uitsnede op 8x; 1x op licht/donker; 1x naast Gnomini en r2-A)
import sys; sys.path.insert(0,'../sprite_r1')
from PIL import Image, ImageDraw
from kijk import sprite
MP='../../../../../graphics/pokemon/machoke/anim_front.png'
def mach(bg=(255,255,255)):
    im=Image.open(MP).convert('RGBA').crop((0,0,64,64)); B=Image.new('RGB',(64,64),bg)
    import numpy as np; a=np.asarray(Image.open(MP))[:64]; m=Image.fromarray(((a>0)*255).astype('uint8'))
    B.paste(im.convert('RGB'),(0,0),m); return B
P=[('gnomad_A.png','r3 A: Machoke-riem met gesp'),('gnomad_B.png','r3 B: Machoke-riem zonder gesp'),('../sprite_r2/gnomad_A.png','r2 A')]
W=Image.new('RGB',(2*524,536),'white'); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate(P[:2]): W.paste(sprite(p).resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
W.save('AB_8x.png')
M=mach().crop((16,22,48,54)).resize((256,256),Image.NEAREST)
V=Image.new('RGB',(3*524+268,24+512+20+80+20+80),'white'); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate(P): V.paste(sprite(p).resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
V.paste(M,(3*524,24)); d.text((3*524+4,6),'Machoke (uitsnede, 8x)',fill=(0,0,0))
y=24+512+20; x=0
for bg in [(255,255,255),(248,248,232),(144,192,152),(40,48,56),(16,16,16)]:
    for p in ('gnomad_A.png','gnomad_B.png'): V.paste(sprite(p,bg),(x,y)); x+=68
    x+=10
y+=100; x=0
for p in ('../../gnomini/af/gnomini.png','gnomad_A.png','gnomad_B.png','../sprite_r2/gnomad_A.png'): V.paste(sprite(p,(248,248,232)),(x,y)); x+=68
V.paste(mach((248,248,232)),(x,y))
V.save('vel.png')
