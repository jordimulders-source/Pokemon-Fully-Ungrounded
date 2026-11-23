# zone.py raster.txt out x0 y0 x1 y1 z : model met spritelijnen (rood=X, oranje=+), skeletkandidaten (blauw), naast sprite met raster
import sys, numpy as np
from PIL import Image, ImageDraw
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
s=(983-46)/62; X0,Y0,left,top=46,57,1,3
C='.X+abcdemnopz'
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]; G=np.array([[C.index(ch) for ch in r] for r in R])
from pal import PAL
sk=np.load('skthick.npy')
x0,y0,x1,y1,z=map(int,sys.argv[3:8])
src=Image.open(M).convert('RGB')
mc=src.crop((int(X0+(x0-left)*s),int(Y0+(y0-top)*s),int(X0+(x1-left)*s),int(Y0+(y1-top)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
d=ImageDraw.Draw(mc)
rgb=np.array(PAL,dtype='uint8')[G]; rgb[G==0]=255
sc=Image.fromarray(rgb).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); d2=ImageDraw.Draw(sc)
for y in range(y0,y1):
  for x in range(x0,x1):
    cx,cy=(x-x0)*z+z//2,(y-y0)*z+z//2
    if sk[y,x]>=0.15*s: d.ellipse((cx-z//5,cy-z//5,cx+z//5,cy+z//5),outline=(0,90,255),width=2)
    if G[y,x]==1: d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=(255,0,0))
    elif G[y,x]==2: d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=(255,140,0))
for dd in (d,d2):
  for i in range(x0,x1+1): dd.line(((i-x0)*z,0,(i-x0)*z,(y1-y0)*z),fill=(0,0,255) if i%4==0 else (170,210,255))
  for i in range(y0,y1+1): dd.line((0,(i-y0)*z,(x1-x0)*z,(i-y0)*z),fill=(0,0,255) if i%4==0 else (170,210,255))
  for i in range(x0,x1,2):
    for j in range(y0,y1,4): dd.text(((i-x0)*z+2,(j-y0)*z+1),f'{i}',fill=(200,0,200))
  for j in range(y0,y1): dd.text((2,(j-y0)*z+z//2-5),f'{j}',fill=(0,120,0))
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'white'); o.paste(mc,(0,0)); o.paste(sc,((x1-x0)*z+8,0)); o.save(sys.argv[2])
