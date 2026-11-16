# ov2.py y0 y1 x0 x1 out [seamtxt]: model 24x met raster + r5-naden (rood) + kandidaat modelranden (groen, Fl)
import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'.'); sys.path.insert(0,'r6w')
from proj import *; from PIL import ImageDraw
import p6
y0,y1,x0,x1=map(int,sys.argv[1:5]); out=sys.argv[5]
s=24; im=model_s(s).crop((x0*s,y0*s,x1*s,y1*s)).convert('RGB'); d=ImageDraw.Draw(im)
Fl=np.load('r7w/Fl.npy')
o=p6.from_txt(sys.argv[6]) if len(sys.argv)>6 else None
if o is None:
    sys.path.insert(0,'r7w'); from zones import R; o=R
for i in range(x0,x1+1):
    d.line([(i-x0)*s,0,(i-x0)*s,(y1-y0)*s],fill=(255,0,0) if i%5==0 else (150,150,150))
for j in range(y0,y1+1):
    d.line([0,(j-y0)*s,(x1-x0)*s,(j-y0)*s],fill=(255,0,0) if j%5==0 else (150,150,150))
for j in range(y0,y1):
  for i in range(x0,x1):
    X=(i-x0)*s; Y=(j-y0)*s
    v=o[j,i]
    if v>=0 and p6.CH[v] in 'SK': d.rectangle([X+3,Y+3,X+9,Y+9],fill=(255,0,0))
    if Fl[j,i]>=0.1: d.rectangle([X+14,Y+14,X+20,Y+20],fill=(0,220,0))
    if i%5==0 and j%5==0: d.text((X+2,Y+12),'%d,%d'%(i,j),fill=(255,0,255))
im.save(out)
