# vel.py: AB_8x.png (A | B, 8x, wit) en vel.png (A | B | r2 op 8x + 1x op licht/donker; ook B met p-roze streep op 1x/8x klein)
import numpy as np; from PIL import Image, ImageDraw
def lees(p,bg=(255,255,255)):
    im=Image.open(p); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
AB=Image.new('RGB',(1024+12,512),'white')
for i,p in enumerate(('gnomini_A.png','gnomini_B.png')): AB.paste(lees(p).resize((512,512),Image.NEAREST),(i*524,0))
AB.save('AB_8x.png')
W=Image.new('RGB',(3*524,24+512+80),'white'); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate([('gnomini_A.png','A: gebogen grens'),('gnomini_B.png','B: A + streep (donkerblauw)'),('r2.png','r2')]):
    W.paste(lees(p).resize((512,512),Image.NEAREST),(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
x=0
for bg in [(255,255,255),(248,248,232),(144,192,152),(40,48,56),(16,16,16)]:
    for p in ('gnomini_A.png','gnomini_B.png','r2.png'): W.paste(lees(p,bg),(x,24+520)); x+=68
    x+=10
W.save('vel.png')
