# raster.py: natief model met 3x3-blokraster (= spritepixels) en X/Y-labels. python3 sprite_r8/raster.py X0 Y0 X1 Y1 uit.png [Z]
import sys; sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
from PIL import Image, ImageDraw; import basis as B
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); uit=sys.argv[5]; Z=int(sys.argv[6]) if len(sys.argv)>6 else 10
u0,v0=B.blok(X0,Y0); u1,v1=B.blok(X1,Y1)
m=Image.fromarray(B.a.astype('uint8')).crop((u0,v0,u1,v1)).resize(((u1-u0)*Z,(v1-v0)*Z),Image.NEAREST)
out=Image.new('RGB',(m.width+30,m.height+20),'white'); out.paste(m,(30,20)); d=ImageDraw.Draw(out)
for i,X in enumerate(range(X0,X1+1)):
    x=30+i*3*Z; d.line([(x,20),(x,out.height)],fill=(255,0,0) if X%5==0 else (255,180,180))
    if X<X1: d.text((x+3,4),str(X%100),fill=(200,0,0))
for j,Y in enumerate(range(Y0,Y1+1)):
    y=20+j*3*Z; d.line([(30,y),(out.width,y)],fill=(255,0,0) if Y%5==0 else (255,180,180))
    if Y<Y1: d.text((4,y+3),str(Y),fill=(200,0,0))
out.save(uit)
