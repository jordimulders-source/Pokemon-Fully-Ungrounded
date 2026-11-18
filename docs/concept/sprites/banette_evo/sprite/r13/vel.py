# Bouwt vel.png: r13 | r12 | model op 8x; close-ups 12x; 1x en 2x op licht/donker.
from PIL import Image, ImageDraw
r13=Image.open('banette_evo.png').convert('RGBA'); r12=Image.open('../r12/banette_evo.png').convert('RGBA')
m=Image.open('../../model/model.png').convert('RGBA'); Sm=968/62
import numpy as np
_a=np.array(m); _a[(_a[...,:3]>235).all(-1),3]=0; m=Image.fromarray(_a)  # wit model-achtergrond transparant
# model in spriteruimte: pixel i -> 24+(i-1)*S ; sprite 0..63 -> model x 24-S .. 24+63S
mx0=24-Sm; my0=1-3*Sm
def model_box(x0,y0,x1,y1):
    return (int(mx0+x0*Sm),int(my0+y0*Sm),int(mx0+x1*Sm),int(my0+y1*Sm))
def flat(img,bg):
    b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
W=64*8; can=Image.new('RGB',(3*W+40,W+1400),(245,245,245)); d=ImageDraw.Draw(can)
for k,(im,t) in enumerate(((r13,'r13'),(r12,'r12'))):
    can.paste(flat(im.resize((W,W),Image.NEAREST),(255,255,255)),(k*(W+20),18)); d.text((k*(W+20),2),t,fill='black')
mm=m.crop(model_box(0,0,64,64)).resize((W,W),Image.LANCZOS)
can.paste(flat(mm,(255,255,255)),(2*(W+20),18)); d.text((2*(W+20),2),'model',fill='black')
y=W+30
zones=[('rechterbel',(46,14,58,26),12),('rode helft',(24,4,48,48),6),('linkeroog',(14,24,25,34),12),('flappunt',(4,24,16,34),12)]
x=0; maxh=0
for t,(x0,y0,x1,y1),f in zones:
    w=(x1-x0)*f;h=(y1-y0)*f
    d.text((x,y),t,fill='black'); d.text((x,y+11),f'x{x0}-{x1-1} y{y0}-{y1-1}',fill='black')
    for k,im in enumerate((r13,r12)):
        c=flat(im.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(255,255,255))
        can.paste(c,(x,y+26+k*(h+16))); d.text((x,y+26+k*(h+16)+h+2),('r13','r12')[k],fill='black')
    mc=flat(m.crop(model_box(x0,y0,x1,y1)).resize((w,h),Image.LANCZOS),(255,255,255))
    can.paste(mc,(x,y+26+2*(h+16))); d.text((x,y+26+2*(h+16)+h+2),'model',fill='black')
    maxh=max(maxh,26+3*(h+16)); x+=max(w,150)+20
y2=y+maxh+10
xs=0
for bg in ((255,255,255),(40,40,48)):
    for s_ in (1,2):
        can.paste(flat(r13.resize((64*s_,64*s_),Image.NEAREST),bg),(xs,y2)); xs+=64*s_+8
    mm=flat(m.crop(model_box(0,0,64,64)).resize((64,64),Image.LANCZOS),bg); can.paste(mm,(xs,y2)); xs+=72
    mm=flat(m.crop(model_box(0,0,64,64)).resize((128,128),Image.LANCZOS),bg); can.paste(mm,(xs,y2)); xs+=150
d.text((xs+10,y2),'r13 1x, 2x | model 1x, 2x; licht en donker',fill='black')
can=can.crop((0,0,can.width,y2+140)); can.save('vel.png')
