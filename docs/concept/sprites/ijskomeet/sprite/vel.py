# vel: sprite 8x | model verkleind 8x (zelfde schaal) | 1x op licht en donker
import sys; import numpy as np; from PIL import Image, ImageDraw
from gio import from_txt
from pal import PAL
o=from_txt(sys.argv[1]); out=sys.argv[2]
def rgba(o):
    img=np.zeros((64,64,4),'uint8')
    for k,c in enumerate(PAL): img[o==k,:3]=c; img[o==k,3]=255
    return Image.fromarray(img,'RGBA')
sp=rgba(o)
mod=Image.open('model64.png').convert('RGB')
W=512*2+40+64*2+60; H=512+40
V=Image.new('RGB',(W,H),(245,245,245)); d=ImageDraw.Draw(V)
bg=Image.new('RGBA',(512,512),(255,255,255,255)); bg.alpha_composite(sp.resize((512,512),Image.NEAREST)); V.paste(bg.convert('RGB'),(10,30))
V.paste(mod.resize((512,512),Image.NEAREST),(532,30))
x=1064
for col in [(248,248,240),(40,44,60)]:
    t=Image.new('RGBA',(80,80),col+(255,)); t.alpha_composite(sp,(8,8)); V.paste(t.convert('RGB'),(x,30)); x+=0
    x=x; 
    V.paste(t.convert('RGB').resize((160,160),Image.NEAREST),(x-4 if False else x, 130 if col[0]>100 else 300))
    x=x
d.text((10,10),'sprite 8x',fill=(0,0,0)); d.text((532,10),'model verkleind (zelfde schaal) 8x',fill=(0,0,0)); d.text((1064,10),'1x / 2x licht, donker',fill=(0,0,0))
t=Image.new('RGBA',(80,80),(40,44,60,255)); t.alpha_composite(sp,(8,8)); V.paste(t.convert('RGB'),(1064+90,30))
V.save(out)
