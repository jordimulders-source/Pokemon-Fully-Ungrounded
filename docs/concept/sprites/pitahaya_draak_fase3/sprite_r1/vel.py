# vel.png: r1 | r1 zonder tong | model (zelfde schaal) op 8x; kop/bek/tong op 12x (r1 | zonder tong | model | model zonder tong);
# onderaan 1x en 2x op licht en donker. Gebruik: python3 vel.py
import numpy as np; from PIL import Image, ImageDraw
def rgba(p):
    im=Image.open(p); im.save('/tmp/_vel.png',transparency=0); return Image.open('/tmp/_vel.png').convert('RGBA')
A=rgba('pitahaya3_r1.png'); B=rgba('pitahaya3_r1_zonder_tong.png')
geo=np.load('kaal_info.npz')['geo']; S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
P=3.998; PH=3.25
mx=lambda X: PH+P*(bx0-S+OX+S*(X-X0+xmin)); my=lambda Y: PH+P*(by0-S+OY+S*(Y-Y0+ymin))
def model(pad,x0,y0,x1,y1,Z):
    M=Image.open(pad).convert('RGBA'); return M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=64*8*3+40; H=12+56*8+20+22*12+20+140
vel=Image.new('RGBA',(W,H),(200,200,200,255)); d=ImageDraw.Draw(vel)
y=12
for i,im in enumerate([op_wit(A,0,8,64,64,8),op_wit(B,0,8,64,64,8),model('../model/model.png',0,8,64,64,8)]):
    vel.alpha_composite(im,(i*(512+20),y))
for i,t in enumerate(['r1 (met tong) 8x','r1 zonder tong 8x','model, zelfde uitsnede']): d.text((i*532+4,0),t,fill=(0,0,0))
y+=56*8+20
kop=(0,14,22,36)
ims=[op_wit(A,*kop,12),op_wit(B,*kop,12),model('../model/model.png',*kop,12),model('../model/model_zonder_tong.png',*kop,12)]
for i,im in enumerate(ims): vel.alpha_composite(im,(i*(22*12+12),y))
for i,t in enumerate(['kop r1 12x','kop zonder tong 12x','model','model zonder tong']): d.text((i*276+4,y-12),t,fill=(0,0,0))
y+=22*12+20
for j,(bgc,x) in enumerate((((255,255,255,255),10),((40,40,48,255),460))):
    vel.paste(Image.new('RGBA',(430,140),bgc),(x,y))
    for k,t in enumerate((A,B)):
        vel.alpha_composite(t,(x+10+k*70,y+10)); vel.alpha_composite(t.resize((128,128),Image.NEAREST),(x+150+k*140,y+6))
vel.convert('RGB').save('vel.png'); print('vel.png',vel.size)
