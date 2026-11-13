# zij.py raster out [x0 y0 x1 y1 z]: sprite | model (LANCZOS) met spriteraster, zelfde schaal
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image,ImageDraw
from geo import *
import pal
R=pal.load(sys.argv[1]); a=list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else [0,0,64,64,8]
x0,y0,x1,y1,z=a; W,Hh=(x1-x0)*z,(y1-y0)*z
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
m=src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize((W,Hh),Image.LANCZOS)
s=pal.rgb(R).crop((x0,y0,x1,y1)).resize((W,Hh),Image.NEAREST)
o=Image.new('RGB',(2*W+10,Hh+14),'white'); o.paste(s,(0,14)); o.paste(m,(W+10,14)); d=ImageDraw.Draw(o)
for off in (0,W+10):
  for i in range(x0,x1+1):
    if z>=10 or i%4==0:
      d.line([(off+(i-x0)*z,14),(off+(i-x0)*z,14+Hh)],fill=(255,0,0) if i%4==0 else (170,170,255))
    if i%4==0: d.text((off+(i-x0)*z+1,2),str(i),fill='black')
  for j in range(y0,y1+1):
    if z>=10 or j%4==0:
      d.line([(off,14+(j-y0)*z),(off+W,14+(j-y0)*z)],fill=(255,0,0) if j%4==0 else (170,170,255))
    if j%4==0: d.text((off+1,14+(j-y0)*z+1),str(j),fill='black')
o.save(sys.argv[2])
