# zoom.py out x0 y0 x1 y1 z : model in spritecoords, met tikjes elke px aan de rand en labels elke 2
import cfg,sys
from PIL import Image,ImageDraw
out=sys.argv[1]; x0,y0,x1,y1,z=map(int,sys.argv[2:7])
src=Image.open(cfg.MODEL).convert('RGB')
bx=cfg.X0+(x0-cfg.LEFT)*cfg.S; by=cfg.Y0+(y0-cfg.TOP)*cfg.S
big=Image.new('RGB',(3000,2000),(254,254,254)); big.paste(src,(1000,1000))
w,h=(x1-x0)*z,(y1-y0)*z
m=big.crop((int(1000+bx),int(1000+by),int(1000+bx+(x1-x0)*cfg.S),int(1000+by+(y1-y0)*cfg.S))).resize((w,h),Image.LANCZOS)
o=Image.new('RGB',(w+40,h+40),'white'); o.paste(m,(30,30)); d=ImageDraw.Draw(o)
for X in range(x0,x1+1):
  px=30+(X-x0)*z; d.line([(px,22),(px,30)],fill=(0,0,255)); d.line([(px,30+h),(px,38+h)],fill=(0,0,255))
  if X%2==0: d.text((px+2,8),str(X),fill=(0,0,200))
  if X%5==0: 
    for yy in range(30,30+h,6): d.point((px,yy),fill=(0,160,255))
for Y in range(y0,y1+1):
  py=30+(Y-y0)*z; d.line([(20,py),(30,py)],fill=(0,0,255)); d.line([(30+w,py),(38+w,py)],fill=(0,0,255))
  if Y%2==0: d.text((2,py+2),str(Y),fill=(0,0,200))
  if Y%5==0:
    for xx in range(30,30+w,6): d.point((xx,py),fill=(0,160,255))
o.save(out)
