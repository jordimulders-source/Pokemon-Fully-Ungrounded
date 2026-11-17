# vel.png: r3 | r2 | model op 8x; kop op 12x (r3 | r3 zonder tong | model | model zonder tong); 1x en 2x op licht en donker.
# Gebruik: python3 vel.py [MET.png ZONDER.png UIT.png]
import sys,numpy as np; from PIL import Image, ImageDraw
from box import mx,my
A_,B_,UIT=(sys.argv[1:4] if len(sys.argv)>3 else ('pitahaya3_r3.png','pitahaya3_r3_zonder_tong.png','vel.png'))
def rgba(p):
    im=Image.open(p); im.save('/tmp/_vel3.png',transparency=0); return Image.open('/tmp/_vel3.png').convert('RGBA')
A=rgba(A_); B=rgba(B_); R2=rgba('../sprite_r2/pitahaya3_r2.png')
def model(pad,x0,y0,x1,y1,Z):
    M=Image.open(pad).convert('RGBA'); return M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
kop=(0,12,22,36); KW=(kop[2]-kop[0])*12; KH=(kop[3]-kop[1])*12
W=64*8*3+40; H=14+56*8+24+KH+24+150
vel=Image.new('RGBA',(W,H),(200,200,200,255)); d=ImageDraw.Draw(vel)
y=14
for i,im in enumerate([op_wit(A,0,8,64,64,8),op_wit(R2,0,8,64,64,8),model('../model/model.png',0,8,64,64,8)]): vel.alpha_composite(im,(i*532,y))
for i,t in enumerate(['r3 (met tong) 8x','r2 (vorige ronde) 8x','model, zelfde uitsnede']): d.text((i*532+4,2),t,fill=(0,0,0))
y+=56*8+24
for i,(im,t) in enumerate([(op_wit(A,*kop,12),'kop r3 12x'),(op_wit(B,*kop,12),'kop r3 zonder tong'),(model('../model/model.png',*kop,12),'model'),(model('../model/model_zonder_tong.png',*kop,12),'model zonder tong'),(op_wit(R2,*kop,12),'kop r2')]):
    vel.alpha_composite(im,(i*(KW+12),y)); d.text((i*(KW+12)+4,y-12),t,fill=(0,0,0))
y+=KH+24
for j,(bgc,x) in enumerate((((255,255,255,255),10),((40,40,48,255),560))):
    vel.paste(Image.new('RGBA',(540,140),bgc),(x,y))
    for k,t in enumerate((A,B)):
        vel.alpha_composite(t,(x+10+k*70,y+10)); vel.alpha_composite(t.resize((128,128),Image.NEAREST),(x+150+k*140,y+6))
    vel.alpha_composite(R2.resize((128,128),Image.NEAREST),(x+410,y+6))
d.text((1112,y+2),'1x en 2x: r3, r3 zonder tong, r2 (2x)',fill=(0,0,0))
vel.convert('RGB').save(UIT); print(UIT,vel.size)
