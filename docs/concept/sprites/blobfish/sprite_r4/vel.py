# vel.py: r4 (=r4a) | r3 | model (BOX 4x4) op 8x; gezicht 16x r4a | r4b | model met de oogposities uit het model (kader = spritepixels
# waarin het oog van het model valt: oogwit >= 170 + pupil < 62 binnen de oogcirkel); 1x en 2x op licht/donker; lipmasker-overlay.
import numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=Image.open('natief.png').convert('RGB'); na=np.asarray(n).astype(int); Ln=na@[0.299,0.587,0.114]
r3=Image.open('blobfish_r4.png'); r2=Image.open('r3.png'); r4b=Image.open('blobfish_r4b.png')
LG=(214,222,214); DG=(40,44,52)
def rgba(p,c): b=Image.new('RGBA',(64,64),c+(255,)); b.alpha_composite(p.convert('RGBA')); return b.convert('RGB')
nx=OX+4*(xmin-x0); ny=OY+4*(ymin-y0)
big=Image.new('RGB',(256+abs(nx)+4,256+abs(ny)+4),(255,255,255)); big.paste(n,(max(0,-nx),max(0,-ny))); bx,by=max(0,nx),max(0,ny)
m=big.crop((bx,by,bx+256,by+256)).resize((64,64),Image.BOX); ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=LG; m=Image.fromarray(ma)
# oogposities uit het model: natieve oogpixels rond de twee ogen -> spritecellen
def cel(yy,xx): return (xx-OX)//4+x0-xmin, (yy-OY)//4+y0-ymin
ogen=[]
for (cx,cy) in ((9.5,41.5),(19.5,45.5)):
    ncx=OX+4*(cx-x0+xmin); ncy=OY+4*(cy-y0+ymin); cs=set()
    for yy in range(int(ncy)-5,int(ncy)+6):
        for xx in range(int(ncx)-5,int(ncx)+6):
            r,g,b=na[yy,xx]; sat=(max(r,g,b)-min(r,g,b))/max(r,g,b,1)
            if (Ln[yy,xx]>=170 and sat<0.3) or Ln[yy,xx]<62: cs.add(cel(yy,xx))
    ogen.append(cs)
z=8; W=64*z; X0,Y0,X1,Y1=6,38,24,54; zz=16; fw=(X1-X0)*zz; fh=(Y1-Y0)*zz
v=Image.new('RGB',(3*W+40,W+60+fh+30),'white'); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate(((rgba(r3,LG),'r4 = r4a (8x)'),(rgba(r2,LG),'r3 (8x)'),(m,'model verkleind (BOX 4x4, 8x)'))):
    v.paste(im.resize((W,W),Image.NEAREST),(10+k*(W+10),30)); d.text((10+k*(W+10),10),t,fill='black')
yy=W+60
pan=[rgba(r3,LG).crop((X0,Y0,X1,Y1)).resize((fw,fh),Image.NEAREST), rgba(r4b,LG).crop((X0,Y0,X1,Y1)).resize((fw,fh),Image.NEAREST),
     big.crop((bx+4*X0,by+4*Y0,bx+4*X1,by+4*Y1)).resize((fw,fh),Image.LANCZOS)]
for k,(im,t) in enumerate(zip(pan,('gezicht 16x r4a','r4b','model; geel = oogcellen uit het model'))):
    dd=ImageDraw.Draw(im)
    for cs in ogen:
        for (x,y) in cs:
            if X0<=x<X1 and Y0<=y<Y1: dd.rectangle([(x-X0)*zz,(y-Y0)*zz,(x-X0+1)*zz-1,(y-Y0+1)*zz-1],outline=(255,220,0))
    v.paste(im,(10+k*(fw+10),yy)); d.text((10+k*(fw+10),yy-14),t,fill='black')
xx=10+3*(fw+10)+10; d.text((xx,yy-14),'1x licht / donker  |  2x',fill='black')
v.paste(rgba(r3,LG),(xx,yy)); v.paste(rgba(r3,DG),(xx,yy+70))
v.paste(rgba(r3,LG).resize((128,128),Image.NEAREST),(xx+74,yy)); v.paste(rgba(r3,DG).resize((128,128),Image.NEAREST),(xx+74+134,yy))
v.save('vel.png'); print(v.size, [sorted(c) for c in ogen])
