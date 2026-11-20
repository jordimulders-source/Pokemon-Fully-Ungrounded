# kop_vel.png: kop 12x (model | varianten | r7) en daaronder 1x/2x op licht en donker
import sys, numpy as np; from PIL import Image, ImageDraw
V=sys.argv[1:] or ['kop_K1_oogA.png','kop_K1_oogB.png','kop_K2_oogA.png','kop_K2_oogB.png']
BX=(3,2,31,28); K=10
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB'); a=f(BX[0],BX[1]); b=f(BX[2],BX[3])
W_,H_=(BX[2]-BX[0])*K,(BX[3]-BX[1])*K
mod=M.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize((W_,H_),Image.LANCZOS)
def wit(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); w=Image.new('RGBA',(64,64),bg+(255,)); w.alpha_composite(im); return w.convert('RGB')
rij=[(mod,'model')]+[(wit(p).crop(BX).resize((W_,H_),Image.NEAREST),p[4:-4]) for p in V+['r7.png']]
vel=Image.new('RGB',(len(rij)*(W_+12)+12,H_+40+170),(225,225,225)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(rij): vel.paste(im,(12+i*(W_+12),28)); d.text((12+i*(W_+12),8),t,fill=(0,0,0))
y=H_+50
for i,p in enumerate(V+['r7.png']):
    x=12+(i+1)*(W_+12)
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        vel.paste(wit(p,bg),(x+j*70,y)); vel.paste(wit(p,bg).resize((128,128),Image.NEAREST),(x+j*136,y+36) if False else (x+140+j*0,y) if j==0 else (x+140,y+0))
    vel.paste(wit(p,(40,40,48)),(x,y+70))
vel.save(sys.argv[0].replace('kopvel.py','')+'kop_vel.png'); print(vel.size)
