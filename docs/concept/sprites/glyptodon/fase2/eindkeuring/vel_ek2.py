# vel_ek2.png: ek1 8x | ek2 8x | wijzigingen | poten 12x model naast ek2 | ek2 1x/2x licht en donker
import sys; sys.path.insert(0,'../sprite')
import numpy as np
from PIL import Image,ImageDraw
from reduceer import X0,Y0,s,LEFT,TOP
def S(f,bg=(255,255,255)):
    sp=Image.open(f).convert('RGBA'); b=Image.new('RGBA',sp.size,bg+(255,)); b.alpha_composite(sp); return b.convert('RGB')
W=[tuple(p) for p in np.load('ek2_W.npy')]
o=Image.new('RGB',(3*512+40,512+40+260+150),(235,235,235)); d=ImageDraw.Draw(o)
d.text((10,6),'ek1 8x',fill=0); d.text((532,6),'ek2 8x',fill=0); d.text((1054,6),'gewijzigd ek1->ek2 (%d px): magenta = nieuw/gewijzigd, cyaan kader = weggehaald'%len(W),fill=0)
o.paste(S('ek1.png').resize((512,512),Image.NEAREST),(10,22)); o.paste(S('ek2.png').resize((512,512),Image.NEAREST),(532,22))
e=np.array(S('ek2.png')).astype(float); g=e.mean(2,keepdims=True); dim=(0.35*g+0.65*235).repeat(3,2).astype('uint8')
D=Image.fromarray(dim).resize((512,512),Image.NEAREST); dd=ImageDraw.Draw(D); I=np.load('ek2_I.npy')
for x,y in W:
    if I[y,x]==0: dd.rectangle([x*8,y*8,x*8+7,y*8+7],outline=(0,200,220),width=2)
    else: dd.rectangle([x*8,y*8,x*8+7,y*8+7],fill=(255,0,255))
o.paste(D,(1054,22))
# close-up poten 12x: model op hetzelfde raster
x0,y0,x1,y1,Z=4,46,52,63,12; k=10.24
M=Image.open('../model.png').convert('RGB')
A=M.crop((int((X0+(x0-LEFT)*s)*k),int((Y0+(y0-TOP)*s)*k),int((X0+(x1-LEFT)*s)*k),int((Y0+(y1-TOP)*s)*k))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
B=S('ek2.png').crop((x0,y0,x1,y1)).resize(A.size,Image.NEAREST)
Y=560; d.text((10,Y-14),'model (hoge resolutie, zelfde raster) 12x',fill=0); d.text((A.width+30,Y-14),'ek2 poten 12x',fill=0)
o.paste(A,(10,Y)); o.paste(B,(A.width+30,Y))
Y2=Y+A.height+20; d.text((10,Y2),'ek2 2x / 1x op licht en donker',fill=0)
o.paste(S('ek2.png').resize((128,128),Image.NEAREST),(10,Y2+14)); o.paste(S('ek2.png',(40,44,52)).resize((128,128),Image.NEAREST),(146,Y2+14))
o.paste(S('ek2.png'),(282,Y2+14)); o.paste(S('ek2.png',(40,44,52)),(282,Y2+80))
o.save('vel_ek2.png')
