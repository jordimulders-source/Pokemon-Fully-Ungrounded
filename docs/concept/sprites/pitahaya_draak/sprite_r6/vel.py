# vel r6: r6 | af | model op 8x; rechterarm 12x (r6 | af | natief model); 1x/2x licht/donker van r6 en af
import numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']; n=Image.open('natief.png').convert('RGB')
def rgba(f,bg):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
LG=(214,222,214); DG=(40,44,52); C=(12,4,50,58); z=8; w=(C[2]-C[0])*z; h=(C[3]-C[1])*z
nx=OX+3*(xmin-x0); ny=OY+3*(ymin-y0); P=60
big=Image.new('RGB',(n.size[0]+2*P,n.size[1]+2*P),(255,255,255)); big.paste(n,(P,P))
m=big.crop((P+nx,P+ny,P+nx+192,P+ny+192)).resize((64,64),Image.BOX); ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=LG; m=Image.fromarray(ma)
A=(31,35,48,50); az=12; aw=(A[2]-A[0])*az; ah=(A[3]-A[1])*az
am=big.crop((P+nx+3*A[0],P+ny+3*A[1],P+nx+3*A[2],P+ny+3*A[3])).resize((aw,ah),Image.NEAREST)
v=Image.new('RGB',(max(3*(w+10),3*(aw+10))+20,h+40+ah+40+250),'white'); d=ImageDraw.Draw(v)
for k,(t,im) in enumerate((('r6 (8x)',rgba('pitahaya_r6.png',LG)),('af (8x)',rgba('af.png',LG)),('model verkleind (BOX 3x3, 8x)',m))):
    v.paste(im.crop(C).resize((w,h),Image.NEAREST),(10+k*(w+10),24)); d.text((10+k*(w+10),6),t,fill='black')
yy=h+50
for k,(t,im) in enumerate((('r6 arm 12x',rgba('pitahaya_r6.png',LG).crop(A).resize((aw,ah),Image.NEAREST)),('af arm 12x',rgba('af.png',LG).crop(A).resize((aw,ah),Image.NEAREST)),('model natief',am))):
    v.paste(im,(10+k*(aw+10),yy+14)); d.text((10+k*(aw+10),yy),t,fill='black')
yy+=ah+40
for k,(t,f) in enumerate((('r6','pitahaya_r6.png'),('af','af.png'))):
    X=10+k*300; d.text((X,yy),t+': 1x licht/donker, 2x licht/donker',fill='black')
    v.paste(rgba(f,LG),(X,yy+14)); v.paste(rgba(f,DG),(X+70,yy+14))
    v.paste(rgba(f,LG).resize((128,128),Image.NEAREST),(X,yy+84)); v.paste(rgba(f,DG).resize((128,128),Image.NEAREST),(X+136,yy+84))
v.save('vel.png'); print(v.size)
