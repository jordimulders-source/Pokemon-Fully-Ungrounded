# vel r2: r2 8x | r1 8x | model verkleind (BOX 3x3, zelfde plaats) 8x ; daaronder 1x en 2x van r2 en r1 op licht en donker
import numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=Image.open('natief.png').convert('RGB')
def rgba(p,bgc):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(p.convert('RGBA')); return b.convert('RGB')
nx=OX+3*(xmin-x0); ny=OY+3*(ymin-y0); P=60
big=Image.new('RGB',(n.size[0]+2*P,n.size[1]+2*P),(255,255,255)); big.paste(n,(P,P))
m=big.crop((P+nx,P+ny,P+nx+192,P+ny+192)).resize((64,64),Image.BOX)
ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=(214,222,214); m=Image.fromarray(ma)
LG=(214,222,214); DG=(40,44,52); C=(12,2,52,60); z=8; w=(C[2]-C[0])*z; h=(C[3]-C[1])*z
r2=Image.open('pitahaya_r2.png'); r1=Image.open('pitahaya_r1.png')
v=Image.new('RGB',(3*w+40,h+40+300),'white'); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate(((rgba(r2,LG),'r2 (8x)'),(rgba(r1,LG),'r1 (8x)'),(m,'model verkleind (BOX 3x3, 8x)'))):
    v.paste(im.crop(C).resize((w,h),Image.NEAREST),(10+k*(w+10),30)); d.text((10+k*(w+10),10),t,fill='black')
yy=h+60; d.text((10,yy-14),'1x: r2 licht | r1 licht | r2 donker | r1 donker        2x: r2 | r1 (licht), r2 | r1 (donker)',fill='black')
for k,(im,bg) in enumerate(((r2,LG),(r1,LG),(r2,DG),(r1,DG))): v.paste(rgba(im,bg),(10+k*70,yy))
for k,(im,bg) in enumerate(((r2,LG),(r1,LG),(r2,DG),(r1,DG))): v.paste(rgba(im,bg).resize((128,128),Image.NEAREST),(300+k*134,yy))
v.save('vel.png'); print(v.size)
