# vel.py -> gnometrotter_rock_8x.png en vel.png (sprite | model op schaal, 8x; 1x op licht en donker; 1x en 2x naast Gnomini en Gnomad)
from PIL import Image, ImageDraw
from kijk import sprite, model_op_schaal
S='gnometrotter_rock.png'
sprite(S).resize((512,512),Image.NEAREST).save('gnometrotter_rock_8x.png')
V=Image.new('RGB',(2*524,24+512+20+80+20+150),'white'); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate(((sprite(S),'Gnometrotter Rock (sprite)'),(model_op_schaal(n=512),'model r8 op schaal (gedeelde reductie)'))):
    V.paste(p.resize((512,512),Image.NEAREST) if p.size[0]==64 else p,(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
y=24+512+20; x=0; d.text((0,y-14),'1x op licht en donker',fill=(0,0,0))
for bg in [(255,255,255),(248,248,232),(144,192,152),(112,120,136),(40,48,56),(16,16,16)]:
    V.paste(sprite(S,bg),(x,y)); x+=72
y2=y+80+20; d.text((0,y2-14),'1x en 2x naast Gnomini en Gnomad (af)',fill=(0,0,0)); x=0
L=['../../gnomini/af/gnomini.png','../../gnomad/af/gnomad.png',S]
for p in L: V.paste(sprite(p,(248,248,232)),(x,y2)); x+=68
x+=16
for p in L: V.paste(sprite(p,(248,248,232)).resize((128,128),Image.NEAREST),(x,y2)); x+=136
V.save('vel.png'); print(V.size)
