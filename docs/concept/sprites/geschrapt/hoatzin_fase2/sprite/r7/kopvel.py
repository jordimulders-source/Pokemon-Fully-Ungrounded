# kop_vel.png: kop 12x (model | A | B | C | r6) en daaronder de hele sprite 1x en 2x (A B C) op licht en donker
import numpy as np; from PIL import Image, ImageDraw
BX=(3,2,31,28); K=12
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB'); a=f(BX[0],BX[1]); b=f(BX[2],BX[3])
W_,H_=(BX[2]-BX[0])*K,(BX[3]-BX[1])*K
mod=M.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize((W_,H_),Image.LANCZOS)
def wit(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); w=Image.new('RGBA',(64,64),bg+(255,)); w.alpha_composite(im); return w.convert('RGB')
rij=[(mod,'model')]+[(wit(p).crop(BX).resize((W_,H_),Image.NEAREST),t) for p,t in [('kop_A.png','A'),('kop_B.png','B'),('kop_C.png','C'),('r6.png','r6')]]
vel=Image.new('RGB',(len(rij)*(W_+16)+16,H_+40+300),(225,225,225)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(rij): vel.paste(im,(16+i*(W_+16),28)); d.text((16+i*(W_+16),8),t+' 12x',fill=(0,0,0))
y=H_+60
for i,v in enumerate('ABC'):
    x=16+i*420; d.text((x,y-14),v+' 1x / 2x',fill=(0,0,0))
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        vel.paste(wit('kop_%s.png'%v,bg),(x+j*72,y)); vel.paste(wit('kop_%s.png'%v,bg).resize((128,128),Image.NEAREST),(x+150+j*136,y))
vel.save('kop_vel.png'); print(vel.size)
