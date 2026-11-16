# vel.py: r2 | r1 | model verkleind (BOX 4x4) op 8x; gezicht 12x r2 | r1 | model (natief); 1x en 2x op licht/donker
import numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=Image.open('natief.png').convert('RGB'); r2=Image.open('blobfish_r2.png'); r1=Image.open('r1.png')
LG=(214,222,214); DG=(40,44,52)
def rgba(p,c): b=Image.new('RGBA',(64,64),c+(255,)); b.alpha_composite(p.convert('RGBA')); return b.convert('RGB')
nx=OX+4*(xmin-x0); ny=OY+4*(ymin-y0)
big=Image.new('RGB',(256+abs(nx)+4,256+abs(ny)+4),(255,255,255)); big.paste(n,(max(0,-nx),max(0,-ny)))
bx,by=max(0,nx),max(0,ny)
m=big.crop((bx,by,bx+256,by+256)).resize((64,64),Image.BOX); ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=LG; m=Image.fromarray(ma)
z=8; W=64*z; X0,Y0,X1,Y1=6,38,24,55; zz=12; fw=(X1-X0)*zz; fh=(Y1-Y0)*zz
v=Image.new('RGB',(3*W+40,W+40+fh+40),'white'); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate(((rgba(r2,LG),'r2 (8x)'),(rgba(r1,LG),'r1 (8x)'),(m,'model verkleind (BOX 4x4, 8x)'))):
    v.paste(im.resize((W,W),Image.NEAREST),(10+k*(W+10),30)); d.text((10+k*(W+10),10),t,fill='black')
yy=W+60
for k,(im,t) in enumerate(((rgba(r2,LG),'r2'),(rgba(r1,LG),'r1'))):
    v.paste(im.crop((X0,Y0,X1,Y1)).resize((fw,fh),Image.NEAREST),(10+k*(fw+10),yy)); d.text((10+k*(fw+10),yy-14),'gezicht 12x '+t,fill='black')
v.paste(big.crop((bx+4*X0,by+4*Y0,bx+4*X1,by+4*Y1)).resize((fw,fh),Image.LANCZOS),(10+2*(fw+10),yy)); d.text((10+2*(fw+10),yy-14),'model (natief)',fill='black')
xx=10+3*(fw+10)+10
d.text((xx,yy-14),'1x licht / donker  |  2x',fill='black')
v.paste(rgba(r2,LG),(xx,yy)); v.paste(rgba(r2,DG),(xx,yy+70))
v.paste(rgba(r2,LG).resize((128,128),Image.NEAREST),(xx+74,yy)); v.paste(rgba(r2,DG).resize((128,128),Image.NEAREST),(xx+74+134,yy))
v.save('vel.png'); print(v.size)
