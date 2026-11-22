# vel.py: A | B | model verkleind (8x) + rij 1x op licht en donker (A, B, model) -> vel.png
import numpy as np; from PIL import Image, ImageDraw
from kijk import lees, model_op_schaal
def lees_bg(p,bg):
    im=Image.open(p); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
m=model_op_schaal(); z=8
pan=[lees('gnomini_A.png'),lees('gnomini_B.png'),m]
tit=['A: lijfvorm als model','B: ronder lijf','model (natief, op schaal)']
W=Image.new('RGB',(3*512+2*12,512+24+16+70+140),'white'); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate(zip(pan,tit)):
    W.paste(p.resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
y=24+512+16; x=0
for bg in [(255,255,255),(248,248,232),(144,192,152),(40,48,56),(16,16,16)]:
    for p in ('gnomini_A.png','gnomini_B.png'):
        W.paste(lees_bg(p,bg),(x,y)); x+=68
    x+=10
mm=m.copy(); W.paste(mm,(x,y))
# 2x rij
y2=y+70; x=0
for p in ('gnomini_A.png','gnomini_B.png'):
    W.paste(lees_bg(p,(248,248,232)).resize((128,128),Image.NEAREST),(x,y2-4)); x+=136
W.save('vel.png'); print('vel.png',W.size)
