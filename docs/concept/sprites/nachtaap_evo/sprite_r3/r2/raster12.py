# sprite-uitsnede groot met coordinatenraster (python3 r2/raster12.py map x0 y0 x1 y1 uit)
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import ImageDraw
f,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
g=np.array(Image.open(f+'/anim_front.png'))[:64].astype(int); s=24
a=naar_img(g[y0:y1,x0:x1],s,(255,255,255)).convert('RGB')
V=Image.new('RGB',(a.width+30,a.height+16),(255,255,255)); V.paste(a,(30,16)); d=ImageDraw.Draw(V)
for i in range(x1-x0+1): d.line([(30+i*s,16),(30+i*s,16+a.height)],fill=(170,170,170))
for j in range(y1-y0+1): d.line([(30,16+j*s),(30+a.width,16+j*s)],fill=(170,170,170))
for i in range(x1-x0): d.text((30+i*s+6,2),str(x0+i),fill=(200,0,0))
for j in range(y1-y0): d.text((2,16+j*s+6),str(y0+j),fill=(0,120,0))
V.save(uit)
