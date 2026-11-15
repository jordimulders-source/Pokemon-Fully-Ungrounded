# python3 maker/zoom.py raster.txt x0 y0 x1 y1 out.png  -> model (rooster) | sprite op 16x
import sys,numpy as np; sys.path.insert(0,'maker'); from pal import PAL
from PIL import Image, ImageDraw
rf,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
Z=16; S=(973-144)/56
c=Image.open('r8_bol_r7.png').convert('RGB')
box=(144+(x0-4)*S,215+(y0-19)*S,144+(x1-4)*S,215+(y1-19)*S)
w,h=(x1-x0)*Z,(y1-y0)*Z
m=c.crop(tuple(int(round(v)) for v in box)).resize((w,h),Image.LANCZOS)
R=[l.rstrip('\n') for l in open(rf)]
s=Image.new('RGB',(w,h),(255,0,255)); d=ImageDraw.Draw(s)
for y in range(y0,y1):
  for x in range(x0,x1):
    ch=R[y][x]
    if ch!='.': d.rectangle([(x-x0)*Z,(y-y0)*Z,(x-x0+1)*Z-1,(y-y0+1)*Z-1],fill=PAL[ch])
    else: d.rectangle([(x-x0)*Z,(y-y0)*Z,(x-x0+1)*Z-1,(y-y0+1)*Z-1],fill=(255,255,255))
im=Image.new('RGB',(2*w+60,h+30),(255,255,255)); im.paste(m,(30,30)); im.paste(s,(w+60,30))
d=ImageDraw.Draw(im)
for k,ox in ((0,30),(1,w+60)):
  for x in range(x0,x1+1):
    X=ox+(x-x0)*Z; d.line([X,30,X,30+h],fill=(255,0,0) if x%5==0 else (200,200,200),width=1)
    if x%2==0 and x<x1: d.text((X+2,15),str(x),fill=(0,0,0))
  for y in range(y0,y1+1):
    Y=30+(y-y0)*Z; d.line([ox,Y,ox+w,Y],fill=(255,0,0) if y%5==0 else (200,200,200),width=1)
    if y<y1 and y%2==0: d.text((ox-28 if k==0 else ox-28,Y+2),str(y),fill=(0,0,0))
im.save(out)
