# rooster.py out x0 y0 x1 y1 z [raster]: model met spritepixelraster (fijn) + labels; met raster: rechts de sprite
import cfg,sys,numpy as np
from PIL import Image,ImageDraw
out=sys.argv[1]; x0,y0,x1,y1,z=map(int,sys.argv[2:7])
src=Image.open(cfg.MODEL).convert('RGB')
bx=cfg.X0+(x0-cfg.LEFT)*cfg.S; by=cfg.Y0+(y0-cfg.TOP)*cfg.S
big=Image.new('RGB',(3000,2000),(254,254,254)); big.paste(src,(1000,1000))
w,h=(x1-x0)*z,(y1-y0)*z
m=big.crop((int(1000+bx),int(1000+by),int(1000+bx+(x1-x0)*cfg.S),int(1000+by+(y1-y0)*cfg.S))).resize((w,h),Image.LANCZOS)
panels=[m]
if len(sys.argv)>7:
  a=cfg.read(sys.argv[7]); panels.append(cfg.rgba(a,(150,210,170,255)).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST))
o=Image.new('RGB',(len(panels)*(w+30)+30,h+30),'white')
for i,p in enumerate(panels): o.paste(p,(30+i*(w+30),30))
d=ImageDraw.Draw(o)
for i in range(len(panels)):
  ox=30+i*(w+30)
  for X in range(x0,x1+1):
    col=(0,90,255) if X%5==0 else (120,170,255)
    if X%5==0 or z>=12: d.line([(ox+(X-x0)*z,30),(ox+(X-x0)*z,30+h)],fill=col,width=1)
    if X%5==0: d.text((ox+(X-x0)*z+1,12),str(X),fill=(0,0,200))
for Y in range(y0,y1+1):
  col=(0,90,255) if Y%5==0 else (120,170,255)
  for i in range(len(panels)):
    ox=30+i*(w+30)
    if Y%5==0 or z>=12: d.line([(ox,30+(Y-y0)*z),(ox+w,30+(Y-y0)*z)],fill=col)
  if Y%5==0: d.text((4,30+(Y-y0)*z+1),str(Y),fill=(0,0,200))
o.save(out)
