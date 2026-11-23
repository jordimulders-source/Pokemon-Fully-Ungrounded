# vel.py: r2 | r1 | model op schaal (8x) + 1x op licht/donker -> vel.png; en gnomini_8x.png
import sys, os, numpy as np; from PIL import Image, ImageDraw
os.chdir('../sprite_r1'); sys.path.insert(0,'.'); from kijk import model_op_schaal; m=model_op_schaal(); os.chdir('../sprite_r2')
def lees(p,bg=(255,255,255)):
    im=Image.open(p); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
lees('gnomini.png').resize((512,512),Image.NEAREST).save('gnomini_8x.png')
W=Image.new('RGB',(3*524,512+24+80),'white'); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate([(lees('gnomini.png'),'r2'),(lees('r1.png'),'r1 (A)'),(m,'model op schaal')]):
    W.paste(p.resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
x=0
for bg in [(255,255,255),(248,248,232),(144,192,152),(40,48,56),(16,16,16)]:
    for p in ('gnomini.png','r1.png'): W.paste(lees(p,bg),(x,24+512+8)); x+=68
    x+=10
W.paste(m,(x,24+520)); W.save('vel.png')
