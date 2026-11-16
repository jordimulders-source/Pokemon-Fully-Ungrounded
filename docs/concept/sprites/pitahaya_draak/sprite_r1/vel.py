# vel.py (afgeleid van blobfish/sprite_r1/vel.py): sprite 8x | model verkleind (BOX van de natieve 3x3-blokken, zelfde plaats) 8x
#   | gezicht 12x sprite naast model (natief) | 1x en 2x op licht, donker, wit
import sys,numpy as np; from PIL import Image, ImageDraw
SP=sys.argv[1] if len(sys.argv)>1 else 'pitahaya_r1.png'; UIT=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=Image.open('natief.png').convert('RGB'); s=Image.open(SP)
def rgba(p,bgc):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(p.convert('RGBA')); return b.convert('RGB')
nx=OX+3*(xmin-x0); ny=OY+3*(ymin-y0); P=60
big=Image.new('RGB',(n.size[0]+2*P,n.size[1]+2*P),(255,255,255)); big.paste(n,(P,P))
m=big.crop((P+nx,P+ny,P+nx+192,P+ny+192)).resize((64,64),Image.BOX)
ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=(214,222,214); m=Image.fromarray(ma)
LG=(214,222,214); DG=(40,44,52); z=8; W=64*z
X0,Y0,X1,Y1=16,18,47,37; zz=12
gs=rgba(s,LG).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*zz,(Y1-Y0)*zz),Image.NEAREST)
gm=big.crop((P+nx+3*X0,P+ny+3*Y0,P+nx+3*X1,P+ny+3*Y1)).resize(gs.size,Image.NEAREST)
v=Image.new('RGB',(max(2*W+30,2*gs.size[0]+20+300),W+40+gs.size[1]+40),'white'); d=ImageDraw.Draw(v)
v.paste(rgba(s,LG).resize((W,W),Image.NEAREST),(10,30)); d.text((10,10),SP+' (8x)',fill='black')
v.paste(m.resize((W,W),Image.NEAREST),(W+20,30)); d.text((W+20,10),'model verkleind (BOX 3x3, 8x)',fill='black')
yy=W+50; v.paste(gs,(10,yy)); v.paste(gm,(20+gs.size[0],yy)); d.text((10,yy-12),'gezicht 12x: sprite | model (natief)',fill='black')
xx=30+2*gs.size[0]
v.paste(rgba(s,LG),(xx,yy)); v.paste(rgba(s,DG),(xx+70,yy)); v.paste(rgba(s,(255,255,255)),(xx+140,yy)); d.text((xx,yy-12),'1x licht / donker / wit',fill='black')
v.paste(rgba(s,LG).resize((128,128),Image.NEAREST),(xx,yy+82)); v.paste(rgba(s,DG).resize((128,128),Image.NEAREST),(xx+138,yy+82)); d.text((xx,yy+70),'2x',fill='black')
v.save(UIT); print(v.size)
