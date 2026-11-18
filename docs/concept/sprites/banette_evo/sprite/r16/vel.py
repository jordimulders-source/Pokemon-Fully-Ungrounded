# Bouwt vel.png: close-up 20x (x0-17, y8-34) r16 | r15 met Jordi's gele lijn; r16 op 8x; 1x/2x op licht/donker.
from PIL import Image, ImageDraw; import numpy as np
r16=Image.open('banette_evo.png').convert('RGBA'); r15=Image.open('../r15/banette_evo.png').convert('RGBA')
sk=np.array(Image.open('../r15/jordi_lijn_oor.png').convert('RGB')).astype(int)
geel=(sk[...,0]>200)&(sk[...,1]>180)&(sk[...,2]<110)
def flat(img,bg):
    b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
x0,y0,x1,y1,f=0,8,18,35,20; w,h=(x1-x0)*f,(y1-y0)*f
can=Image.new('RGB',(2*w+20+64*8+20,max(h,512)+260),(245,245,245)); d=ImageDraw.Draw(can)
a=flat(r16.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(255,255,255))
b=np.array(flat(r15.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(255,255,255)))
ys,xs=np.nonzero(geel); X=xs+20-x0*f; Y=ys+(10-y0)*f
ok=(X<w)&(Y<h); b[Y[ok],X[ok]]=(255,220,0)
for im,ox in ((a,0),(Image.fromarray(b),w+20)):
    dd=ImageDraw.Draw(im)
    for i in range(x1-x0+1): dd.line([(i*f,0),(i*f,h)],fill=(220,220,220))
    for j in range(y1-y0+1): dd.line([(0,j*f),(w,j*f)],fill=(220,220,220))
    for i in range(0,x1-x0,2): dd.text((i*f+2,2),str(x0+i),fill=(200,0,0))
    for j in range(0,y1-y0,2): dd.text((2,j*f+2),str(y0+j),fill=(200,0,0))
    can.paste(im,(ox,16))
d.text((0,0),'r16 (20x, x0-17 y8-34)',fill='black'); d.text((w+20,0),'r15 + gele lijn Jordi',fill='black')
can.paste(flat(r16.resize((512,512),Image.NEAREST),(255,255,255)),(2*w+40,16)); d.text((2*w+40,0),'r16 8x',fill='black')
y2=max(h,512)+40; xs_=0
for bg in ((255,255,255),(40,40,48)):
    for s_ in (1,2):
        can.paste(flat(r16.resize((64*s_,64*s_),Image.NEAREST),bg),(xs_,y2)); xs_+=64*s_+8
    xs_+=10
d.text((xs_+10,y2),'r16 1x,2x op licht | donker',fill='black')
can.save('vel.png')
