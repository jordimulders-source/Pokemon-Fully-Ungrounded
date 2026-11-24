# raster_model.py out x0 y0 x1 y1 z : model met spriteraster (elke px dun, elke 4 dik + label) om hoekpunten in spritecoordinaten te lezen
import sys
from PIL import Image, ImageDraw
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
s=(983-46)/62; X0,Y0,left,top=46,57,1,3
x0,y0,x1,y1,z=map(int,sys.argv[2:7])
src=Image.open(M).convert('RGB')
mc=src.crop((int(X0+(x0-left)*s),int(Y0+(y0-top)*s),int(X0+(x1-left)*s),int(Y0+(y1-top)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
d=ImageDraw.Draw(mc)
for i in range(x0,x1+1):
    d.line(((i-x0)*z,0,(i-x0)*z,(y1-y0)*z),fill=(0,0,255) if i%4==0 else (150,200,255))
for i in range(y0,y1+1):
    d.line((0,(i-y0)*z,(x1-x0)*z,(i-y0)*z),fill=(0,0,255) if i%4==0 else (150,200,255))
for i in range(x0,x1,4):
    for j in range(y0,y1,8): d.text(((i-x0)*z+2,(j-y0)*z+2),f'{i},{j}',fill=(255,0,0))
mc.save(sys.argv[1])
