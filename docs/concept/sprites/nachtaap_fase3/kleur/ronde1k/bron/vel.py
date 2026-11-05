"""vel.png: 1h (naast 1g) op 4x licht/donker; 3x en 1x naast v7 en het model; 3 Gen 3-sprites (primeape/medicham/alakazam _gba, frame 1)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H); G=os.path.join(R,'../../../../../..')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
def laad(p):
    im=Image.open(p); idx=np.array(im); a=np.array(im.convert('RGBA')); a[idx==0,3]=0; return Image.fromarray(a).crop((0,0,64,64))
LI=(255,255,255,255); DO=(40,40,48,255)
nu=laad(os.path.join(R,'nachtaap_fase3.png')); v7=laad(os.path.join(R,'../ronde1h/nachtaap_fase3.png'))
mod=Image.open(os.path.join(R,'../../silhouet/onderlaag_256.png')).convert('RGBA')
W=Image.new('RGBA',(1100,860),LI); d=ImageDraw.Draw(W)
W.paste(Image.new('RGBA',(276,276),DO),(286,24))
W.alpha_composite(nu.resize((256,256),Image.NEAREST),(10,34)); W.alpha_composite(nu.resize((256,256),Image.NEAREST),(296,34))
d.text((10,6),'ronde 1i, 4x licht / donker',font=F,fill=(0,0,0))
W.alpha_composite(mod,(590,34)); d.text((590,6),'model (onderlaag)',font=F,fill=(0,0,0))
y=320
for i,(n,im) in enumerate([('1i 3x',nu),('1h 3x',v7)]):
    W.alpha_composite(im.resize((192,192),Image.NEAREST),(10+i*210,y+20)); d.text((10+i*210,y),n,font=F,fill=(0,0,0))
d.text((440,y),'1x: 1i, 1h, primeape, medicham, alakazam',font=F,fill=(0,0,0))
refs=[laad(os.path.join(G,'graphics/pokemon/%s/anim_front_gba.png'%p)) for p in ('primeape','medicham','alakazam')]
for i,im in enumerate([nu,v7]+refs):
    W.alpha_composite(im,(440+i*72,y+30)); W.paste(Image.new('RGBA',(64,64),DO),(440+i*72,y+110)); W.alpha_composite(im,(440+i*72,y+110))
y=540; d.text((10,y),'3x: Gen 3 ter vergelijking',font=F,fill=(0,0,0))
for i,im in enumerate(refs): W.alpha_composite(im.resize((192,192),Image.NEAREST),(10+i*210,y+20))
W.alpha_composite(mod.resize((192,192)),(650,y+20)); d.text((650,y),'model 3x-vak',font=F,fill=(0,0,0))
W.convert('RGB').save(os.path.join(R,'vel.png'))
