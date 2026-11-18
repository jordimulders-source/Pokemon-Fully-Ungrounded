# Bouwt vel.png: r15 | r14 | model op 8x; close-up 12x oor+bel+Shuppet; 1x en 2x op licht/donker.
from PIL import Image, ImageDraw; import numpy as np
r15=Image.open('banette_evo.png').convert('RGBA'); r14=Image.open('../r14/banette_evo.png').convert('RGBA')
m=Image.open('../../model/model.png').convert('RGBA'); Sm=968/62
_a=np.array(m); _a[(_a[...,:3]>235).all(-1),3]=0; m=Image.fromarray(_a)
mx0=24-Sm; my0=1-3*Sm
def mb(x0,y0,x1,y1): return (int(mx0+x0*Sm),int(my0+y0*Sm),int(mx0+x1*Sm),int(my0+y1*Sm))
def flat(img,bg):
    b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
W=512; can=Image.new('RGB',(3*W+40,2000),(245,245,245)); d=ImageDraw.Draw(can)
for k,(im,t) in enumerate(((r15,'r15'),(r14,'r14'))):
    can.paste(flat(im.resize((W,W),Image.NEAREST),(255,255,255)),(k*(W+20),18)); d.text((k*(W+20),2),t,fill='black')
can.paste(flat(m.crop(mb(0,0,64,64)).resize((W,W),Image.LANCZOS),(255,255,255)),(2*(W+20),18)); d.text((2*(W+20),2),'model',fill='black')
y=W+30; x0,y0,x1,y1=2,14,18,60; f=12; w=(x1-x0)*f; h=(y1-y0)*f
d.text((0,y),f'close-up 12x: oor + bel + Shuppet  x{x0}-{x1-1} y{y0}-{y1-1}',fill='black')
for k,(im,t) in enumerate(((r15,'r15'),(r14,'r14'))):
    can.paste(flat(im.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(255,255,255)),(k*(w+20),y+16)); d.text((k*(w+20),y+18+h),t,fill='black')
can.paste(flat(m.crop(mb(x0,y0,x1,y1)).resize((w,h),Image.LANCZOS),(255,255,255)),(2*(w+20),y+16)); d.text((2*(w+20),y+18+h),'model',fill='black')
y2=y+h+40; xs=0
for bg in ((255,255,255),(40,40,48)):
    for im in (r15,r14):
        for s_ in (1,2):
            can.paste(flat(im.resize((64*s_,64*s_),Image.NEAREST),bg),(xs,y2)); xs+=64*s_+8
        xs+=10
d.text((xs+10,y2),'per achtergrond: r15 1x,2x | r14 1x,2x',fill='black')
can.crop((0,0,can.width,y2+140)).save('vel.png')
