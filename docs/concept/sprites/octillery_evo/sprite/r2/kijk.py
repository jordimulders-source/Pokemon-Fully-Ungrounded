# kijk.py x0 y0 x1 y1 z out : model | r2 | r1 met raster, naast elkaar
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D+'/..')
import cfg
from PIL import Image,ImageDraw
x0,y0,x1,y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]
src=Image.open(cfg.MODEL).convert('RGB')
bx=cfg.X0+(x0-cfg.LEFT)*cfg.S; by=cfg.Y0+(y0-cfg.TOP)*cfg.S
big=Image.new('RGB',(3000,2000),(254,254,254)); big.paste(src,(1000,1000))
w,h=(x1-x0)*z,(y1-y0)*z
P=[big.crop((int(1000+bx),int(1000+by),int(1000+bx+(x1-x0)*cfg.S),int(1000+by+(y1-y0)*cfg.S))).resize((w,h),Image.LANCZOS)]
for f in [D+'/raster.txt']+sys.argv[7:]:
    a=cfg.read(f); P.append(cfg.rgba(a,(255,255,255,255)).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST))
o=Image.new('RGB',(len(P)*(w+20)+20,h+30),'white'); d=ImageDraw.Draw(o)
for i,p in enumerate(P):
    ox=20+i*(w+20); o.paste(p,(ox,25))
    for X in range(x0,x1+1):
        if X%5==0: d.line([(ox+(X-x0)*z,25),(ox+(X-x0)*z,25+h)],fill=(80,140,255)); d.text((ox+(X-x0)*z+1,10),str(X),fill=(0,0,200))
    for Y in range(y0,y1+1):
        if Y%5==0: d.line([(ox,25+(Y-y0)*z),(ox+w,25+(Y-y0)*z)],fill=(80,140,255)); d.text((ox-18,25+(Y-y0)*z),str(Y),fill=(0,0,200))
o.save(out)
