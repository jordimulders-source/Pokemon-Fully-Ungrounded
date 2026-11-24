# overlay.py sprite.png out.png [x0 y0 x1 y1 z]: spritelijnen (index 1/2) als rode/oranje rasterpunten over het model + sprite ernaast
import sys, numpy as np
from PIL import Image, ImageDraw
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
s=(983-46)/62; X0,Y0,left,top=46,57,1,3
src=Image.open(M).convert('RGB')
sp=Image.open(sys.argv[1]); G=np.asarray(sp)
x0,y0,x1,y1,z=list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else (0,0,64,64,12)
mc=src.crop((int(X0+(x0-left)*s),int(Y0+(y0-top)*s),int(X0+(x1-left)*s),int(Y0+(y1-top)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
d=ImageDraw.Draw(mc)
for y in range(y0,y1):
  for x in range(x0,x1):
    g=G[y,x]; cx,cy=(x-x0)*z+z//2,(y-y0)*z+z//2
    if g==1: d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=(255,0,0))
    elif g==2: d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=(255,150,0))
for i in range(x0,x1+1,4): d.line(((i-x0)*z,0,(i-x0)*z,(y1-y0)*z),fill=(0,160,255) if i%8 else (0,0,255))
for i in range(y0,y1+1,4): d.line((0,(i-y0)*z,(x1-x0)*z,(i-y0)*z),fill=(0,160,255) if i%8 else (0,0,255))
from PIL import ImageFont
for i in range(x0,x1,4): d.text(((i-x0)*z+1,1),str(i),fill=(255,255,0))
for i in range(y0,y1,4): d.text((1,(i-y0)*z+1),str(i),fill=(255,255,0))
rgb=sp.convert('RGBA'); b=Image.new('RGBA',rgb.size,(255,255,255,255)); b.alpha_composite(rgb)
sc=b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'white'); o.paste(mc,(0,0)); d2=ImageDraw.Draw(sc)
for i in range(x0,x1+1,4): d2.line(((i-x0)*z,0,(i-x0)*z,(y1-y0)*z),fill=(0,160,255))
for i in range(y0,y1+1,4): d2.line((0,(i-y0)*z,(x1-x0)*z,(i-y0)*z),fill=(0,160,255))
for i in range(x0,x1,4): d2.text(((i-x0)*z+1,1),str(i),fill=(255,0,0))
for i in range(y0,y1,4): d2.text((1,(i-y0)*z+1),str(i),fill=(255,0,0))
o.paste(sc,((x1-x0)*z+8,0)); o.save(sys.argv[2])
