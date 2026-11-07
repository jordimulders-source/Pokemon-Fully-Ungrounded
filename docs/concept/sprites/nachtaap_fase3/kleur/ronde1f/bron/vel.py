"""vel_varianten.png: 1e (+0) en v3..v11 op 3x en 1x (licht), met het model."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
def laad(p):
    im=Image.open(p); idx=np.array(im); a=np.array(im.convert('RGBA')); a[idx==0,3]=0; return Image.fromarray(a)
L=(255,255,255,255)
items=[('ronde 1e: been +0 px',os.path.join(R,'../ronde1e/nachtaap_fase3.png'))]+[('been +%d px'%s,os.path.join(R,'v%d/nachtaap_fase3.png'%s)) for s in (3,5,7,9,11)]
W=Image.new('RGBA',(3*(200)+20,2*(260)+290),L); d=ImageDraw.Draw(W)
for i,(n,p) in enumerate(items):
    im=laad(p); x=10+(i%3)*200; y=10+(i//3)*260
    W.alpha_composite(im.resize((192,192),Image.NEAREST),(x,y+22)); W.alpha_composite(im,(x+130,y+190))
    d.text((x,y),n,font=F,fill=(0,0,0)); d.text((x,y+218),'1x ->',font=F,fill=(90,90,90))
m=Image.open(os.path.join(R,'../../silhouet/onderlaag_256.png')).convert('RGBA')
y=540; W.alpha_composite(m,(10,y+22)); d.text((10,y),'model (onderlaag, zelfde vak)',font=F,fill=(0,0,0))
W.convert('RGB').save(os.path.join(R,'vel_varianten.png'))
