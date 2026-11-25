# mgrid.py raster.txt out.png x0 y0 x1 y1 z : model (links) en sprite (rechts) met spriteraster, labels
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'../r1/stappen'); from pal import PAL
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
s=(983-46)/62; X0,Y0,left,top=46,57,1,3
C='.X+abcdemnopz'
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]; G=np.array([[C.index(ch) for ch in r] for r in R])
x0,y0,x1,y1,z=map(int,sys.argv[3:8])
src=Image.open(M).convert('RGB')
mc=src.crop((int(X0+(x0-left)*s),int(Y0+(y0-top)*s),int(X0+(x1-left)*s),int(Y0+(y1-top)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
rgb=np.array(PAL,dtype='uint8')[G]; rgb[G==0]=255
sc=Image.fromarray(rgb).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
for im in (mc,sc):
  d=ImageDraw.Draw(im)
  for i in range(x0,x1+1): d.line(((i-x0)*z,0,(i-x0)*z,(y1-y0)*z),fill=(0,0,255) if i%5==0 else (150,190,255))
  for i in range(y0,y1+1): d.line((0,(i-y0)*z,(x1-x0)*z,(i-y0)*z),fill=(0,0,255) if i%5==0 else (150,190,255))
  for i in range(x0,x1):
    if i%5==0: d.text(((i-x0)*z+2,1),f'{i}',fill=(220,0,220))
  for j in range(y0,y1):
    if j%5==0: d.text((2,(j-y0)*z+2),f'{j}',fill=(0,150,0))
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'white'); o.paste(mc,(0,0)); o.paste(sc,((x1-x0)*z+8,0)); o.save(sys.argv[2])
