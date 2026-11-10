# cmp.py out.png x0 y0 x1 y1 zoom : model (met spriteraster) | raster.txt, zelfde uitsnede
import sys
sys.path.insert(0,'../silhouet')
from PIL import Image,ImageDraw
from geo import *
from pal import *
x0,y0,x1,y1,z=map(int,sys.argv[2:7]); w,h=(x1-x0)*z,(y1-y0)*z
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
mo=src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize((w,h),Image.LANCZOS)
sp=topng(load('raster.txt'),'/tmp/_r.png').convert('RGB').crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)
o=Image.new('RGB',(2*w+50,h+30),'white'); o.paste(mo,(30,30)); o.paste(sp,(w+50,30)); d=ImageDraw.Draw(o)
for off in (30,w+50):
  for i in range(x0,x1+1):
    c=(255,0,0) if i%4==0 else (120,200,255); d.line([(off+(i-x0)*z,30),(off+(i-x0)*z,30+h)],fill=c)
    if i%2==0: d.text((off+(i-x0)*z+1,12),str(i),fill='black')
  for j in range(y0,y1+1):
    c=(255,0,0) if j%4==0 else (120,200,255); d.line([(off,30+(j-y0)*z),(off+w,30+(j-y0)*z)],fill=c)
    if j%2==0: d.text((off-28,30+(j-y0)*z+1),str(j),fill='black')
o.save(sys.argv[1])
