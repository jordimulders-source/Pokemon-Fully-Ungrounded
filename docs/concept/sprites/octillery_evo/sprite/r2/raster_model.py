# raster_model.py x0 y0 x1 y1 k out : model op eigen resolutie (k x NEAREST) met de echte celgrenzen van cfg.cell
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D+'/..')
import cfg
from PIL import Image,ImageDraw
x0,y0,x1,y1,k=map(int,sys.argv[1:6]); out=sys.argv[6]
src=Image.open(cfg.MODEL).convert('RGB')
px0=cfg.X0+(x0-cfg.LEFT)*cfg.S; py0=cfg.Y0+(y0-cfg.TOP)*cfg.S
px1=cfg.X0+(x1-cfg.LEFT)*cfg.S; py1=cfg.Y0+(y1-cfg.TOP)*cfg.S
X,Y=int(px0),int(py0)
m=src.crop((X,Y,int(px1)+1,int(py1)+1)); m=m.resize((m.width*k,m.height*k),Image.NEAREST)
o=Image.new('RGB',(m.width+40,m.height+40),'white'); o.paste(m,(30,30)); d=ImageDraw.Draw(o)
for x in range(x0,x1+1):
    p=30+(cfg.X0+(x-cfg.LEFT)*cfg.S-X)*k; d.line([(p,30),(p,30+m.height)],fill=(0,200,255) if x%5 else (0,0,255))
    d.text((p+2,14),str(x%100),fill=(0,0,200))
for y in range(y0,y1+1):
    p=30+(cfg.Y0+(y-cfg.TOP)*cfg.S-Y)*k; d.line([(30,p),(30+m.width,p)],fill=(0,200,255) if y%5 else (0,0,255))
    d.text((2,p+2),str(y),fill=(0,0,200))
o.save(out)
