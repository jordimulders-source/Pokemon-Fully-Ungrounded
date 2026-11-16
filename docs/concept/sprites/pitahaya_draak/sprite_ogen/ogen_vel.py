# ogen_vel.png: r3 | A | B | C op 8x (hele sprite), kop-uitsnede op 12x met het model, en 1x/2x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
L=[('r3','pitahaya_r3.png'),('A','A.png'),('B','B.png'),('C','C.png')]
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
LG=(214,222,214); DG=(40,44,52)
def rgba(f,bg):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
C=(13,4,51,58); z=8; w=(C[2]-C[0])*z; h=(C[3]-C[1])*z
K=(16,17,40,33); kz=12; kw=(K[2]-K[0])*kz; kh=(K[3]-K[1])*kz
n=Image.open('natief.png').convert('RGB'); nx=OX+3*(xmin-x0); ny=OY+3*(ymin-y0)
mk=n.crop((nx+3*K[0],ny+3*K[1],nx+3*K[2],ny+3*K[3])).resize((kw,kh),Image.LANCZOS)
v=Image.new('RGB',(max(4*(w+10),3*(kw+10),4*290)+20,h+50+2*(kh+24)+20+230),'white'); d=ImageDraw.Draw(v)
for k,(t,f) in enumerate(L):
    v.paste(rgba(f,LG).crop(C).resize((w,h),Image.NEAREST),(10+k*(w+10),24)); d.text((10+k*(w+10),6),t+' (8x)',fill='black')
yy=h+50
for k,(t,f) in enumerate(L+[('model',None)]):
    X=10+(k%3)*(kw+10); Y=yy+(k//3)*(kh+24)
    im=mk if f is None else rgba(f,LG).crop(K).resize((kw,kh),Image.NEAREST)
    v.paste(im,(X,Y+14)); d.text((X,Y),t+(' (kop 12x)' if f else ' (natief, zelfde uitsnede)'),fill='black')
yy=yy+2*(kh+24)+20
for k,(t,f) in enumerate(L):
    X=10+k*290; d.text((X,yy),t+': 1x licht/donker, 2x licht/donker',fill='black')
    v.paste(rgba(f,LG),(X,yy+14)); v.paste(rgba(f,DG),(X+70,yy+14))
    v.paste(rgba(f,LG).resize((128,128),Image.NEAREST),(X,yy+84)); v.paste(rgba(f,DG).resize((128,128),Image.NEAREST),(X+136,yy+84))
v.save('ogen_vel.png'); print(v.size)
