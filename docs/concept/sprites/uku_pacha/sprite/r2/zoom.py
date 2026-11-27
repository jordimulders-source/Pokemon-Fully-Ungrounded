# zoom.py raster.txt out.png x0 y0 x1 y1 [z]: model (natief, met spriteraster) | sprite, met coördinaten
import sys, numpy as np, geom, raster2png
from PIL import Image, ImageDraw
R=raster2png.lees(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[3:7]); z=int(sys.argv[7]) if len(sys.argv)>7 else 16
w,h=(x1-x0)*z,(y1-y0)*z
# model: natief op spriteschaal
nat=Image.open(geom.D+'/../../model/r2_natief.png').convert('RGB')
big=nat.resize((1000,1000),Image.NEAREST)  # 10 px per cel
def s2b(i,j):
    sx=geom.X0+(i-geom.OX)/geom.F; sy=geom.Y0+(j-geom.OY)/geom.F; return sx*10,sy*10
a=s2b(x0,y0); b=s2b(x1,y1)
m=big.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize((w,h),Image.NEAREST)
s=raster2png.maak(R).convert('RGB').crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)
o=Image.new('RGB',(2*w+40,h+20),'white'); o.paste(m,(20,20)); o.paste(s,(w+40,20))
d=ImageDraw.Draw(o)
for k in range(x1-x0+1):
    for off in (20,w+40):
        d.line([(off+k*z,20),(off+k*z,20+h)],fill=(255,0,0) if (x0+k)%5==0 else (200,200,200),width=1)
    if (x0+k)%5==0: d.text((20+k*z+2,4),str(x0+k),fill='red'); d.text((w+40+k*z+2,4),str(x0+k),fill='red')
for k in range(y1-y0+1):
    for off in (20,w+40):
        d.line([(off,20+k*z),(off+w,20+k*z)],fill=(255,0,0) if (y0+k)%5==0 else (200,200,200),width=1)
    if (y0+k)%5==0: d.text((2,20+k*z+2),str(y0+k),fill='red')
o.save(sys.argv[2])
