# vel.py: sprite 8x | verkleind model 8x ; oog 12x | model 12x ; sprite 1x en 2x op licht en donker
import numpy as np
from PIL import Image, ImageDraw
f=59/75; X0,Y0,OX,OY=17,16,2,6
src=Image.open('../model/model_gekozen_natief.png').convert('RGB')
x0=X0-OX/f; y0=Y0-OY/f; k=1/f
big=src.resize((990,990),Image.NEAREST)
m=big.crop((int(x0*10),int(y0*10),int((x0+64*k)*10),int((y0+64*k)*10))).resize((64,64),Image.BOX)
p=Image.open('sprite.png'); p.save('/tmp/claude-0/sat/_t.png',transparency=0); s=Image.open('/tmp/claude-0/sat/_t.png').convert('RGBA')
def on(c):
    b=Image.new('RGBA',(64,64),c+(255,)); b.alpha_composite(s); return b.convert('RGB')
G=(152,208,160)
W=1040; H=520+20+18*12+20+150
o=Image.new('RGB',(W,H),(250,250,250)); d=ImageDraw.Draw(o)
o.paste(on(G).resize((512,512),Image.NEAREST),(0,0)); o.paste(m.resize((512,512),Image.NEAREST),(528,0))
d.text((4,514),'sprite r1 (8x)',fill=(0,0,0)); d.text((532,514),'model, zelfde schaal (8x)',fill=(0,0,0))
# oog: rijen 24-41, kolommen 1-18
box=(1,24,19,42); z=12; w=(box[2]-box[0])*z; h=(box[3]-box[1])*z
yy=540
o.paste(on(G).crop(box).resize((w,h),Image.NEAREST),(0,yy)); o.paste(m.crop(box).resize((w,h),Image.NEAREST),(w+16,yy))
d.text((2*w+30,yy+4),'oog 12x: sprite | model',fill=(0,0,0))
yy+=h+20
for i,c in enumerate([(248,248,248),(40,40,48),(152,208,160)]):
    o.paste(on(c),(10+i*80,yy)); o.paste(on(c).resize((128,128),Image.NEAREST),(300+i*140,yy))
d.text((10,yy+70),'1x licht/donker/groen',fill=(0,0,0)); d.text((300,yy+132),'2x',fill=(0,0,0))
o.save('vel.png')
