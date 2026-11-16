# vel.py: sprite 8x | model verkleind (BOX van de natieve 4x4-blokken, zelfde plaats) 8x | gezicht 12x sprite naast model | 1x licht en donker
import numpy as np; from PIL import Image, ImageDraw
SP='blobfish_r1.png'; OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=Image.open('natief.png').convert('RGB'); s=Image.open(SP)
def rgba(p,bgc):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(p.convert('RGBA')); return b.convert('RGB')
# model op dezelfde plaats: natief vanaf (OX+4*(xmin-x0), OY+4*(ymin-y0)), 256x256 -> 64x64
nx=OX+4*(xmin-x0); ny=OY+4*(ymin-y0)
big=Image.new('RGB',(256+abs(nx)+4,256+abs(ny)+4),(255,255,255)); big.paste(n,(max(0,-nx),max(0,-ny)))
m=big.crop((max(0,nx),max(0,ny),max(0,nx)+256,max(0,ny)+256)).resize((64,64),Image.BOX)
ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=(214,222,214); m=Image.fromarray(ma)
LG=(214,222,214); DG=(40,44,52)
z=8; W=64*z
v=Image.new('RGB',(2*W+30,W+40+17*12+20),'white'); d=ImageDraw.Draw(v)
v.paste(rgba(s,LG).resize((W,W),Image.NEAREST),(10,30)); d.text((10,10),'blobfish r1 (8x)',fill='black')
v.paste(m.resize((W,W),Image.NEAREST),(W+20,30)); d.text((W+20,10),'model verkleind (BOX 4x4, 8x)',fill='black')
X0,Y0,X1,Y1=6,38,26,55; zz=12
gs=rgba(s,LG).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*zz,(Y1-Y0)*zz),Image.NEAREST)
ax=nx+4*X0; ay=ny+4*Y0
gm=big.crop((max(0,nx)+4*X0,max(0,ny)+4*Y0,max(0,nx)+4*X1,max(0,ny)+4*Y1)).resize(((X1-X0)*zz,(Y1-Y0)*zz),Image.NEAREST)
yy=W+40; v.paste(gs,(10,yy)); v.paste(gm,(10+gs.size[0]+10,yy)); d.text((10,yy-12),'gezicht 12x: sprite | model (natief)',fill='black')
xx=10+2*gs.size[0]+30
v.paste(rgba(s,LG),(xx,yy)); v.paste(rgba(s,DG),(xx+70,yy)); v.paste(rgba(s,(255,255,255)),(xx+140,yy)); d.text((xx,yy-12),'1x licht / donker / wit',fill='black')
v.paste(rgba(s,LG).resize((128,128),Image.NEAREST),(xx,yy+70)); v.paste(rgba(s,DG).resize((128,128),Image.NEAREST),(xx+138,yy+70)); d.text((xx,yy+58),'2x',fill='black')
v.save('vel.png'); print(v.size)
