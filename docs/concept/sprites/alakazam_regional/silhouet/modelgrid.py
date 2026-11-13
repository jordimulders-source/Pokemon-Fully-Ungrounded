# modelgrid.py out.png x0 y0 x1 y1 zoom : model met spriteraster, uitsnede in spritecoords
import sys
from PIL import Image,ImageDraw
from geo import *
x0,y0,x1,y1,z=map(int,sys.argv[2:7])
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
cr=src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
o=Image.new('RGB',((x1-x0)*z+30,(y1-y0)*z+30),'white'); o.paste(cr,(30,30)); d=ImageDraw.Draw(o)
for i in range(x0,x1+1):
  c=(255,0,0) if i%4==0 else (120,200,255); d.line([(30+(i-x0)*z,30),(30+(i-x0)*z,30+(y1-y0)*z)],fill=c,width=1)
  if i%2==0: d.text((30+(i-x0)*z+1,12),str(i),fill='black')
for j in range(y0,y1+1):
  c=(255,0,0) if j%4==0 else (120,200,255); d.line([(30,30+(j-y0)*z),(30+(x1-x0)*z,30+(j-y0)*z)],fill=c,width=1)
  if j%2==0: d.text((2,30+(j-y0)*z+1),str(j),fill='black')
o.save(sys.argv[1])
