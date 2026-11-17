# Model-uitsnede met spritepixelraster (box.py-geometrie) naast de sprite, zelfde schaal. Gebruik: grid.py SPRITE MODEL x0 y0 x1 y1 Z UIT
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'.'); from box import mx,my
sp,mo=sys.argv[1],sys.argv[2]; x0,y0,x1,y1,Z=map(int,sys.argv[3:8]); uit=sys.argv[8]
M=Image.open(mo).convert('RGB'); S=Image.open(sp).convert('RGBA')
w,h=(x1-x0)*Z,(y1-y0)*Z
mc=M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize((w,h),Image.BICUBIC)
sc=Image.new('RGB',(64,64),(200,200,200)); sc.paste(S,(0,0),S); sc=sc.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)
out=Image.new('RGB',(2*w+Z*2+30,h+30),(255,255,255)); out.paste(mc,(30,30)); out.paste(sc,(w+Z*2+30,30))
d=ImageDraw.Draw(out)
for ox in (30,w+Z*2+30):
  for X in range(x0,x1+1):
    d.line([(ox+(X-x0)*Z,30),(ox+(X-x0)*Z,30+h)],fill=(0,0,255) if X%5==0 else (150,150,255),width=1)
    if X%2==0 and X<x1: d.text((ox+(X-x0)*Z+2,2+(X%4)*6),str(X),fill=(0,0,0))
  for Y in range(y0,y1+1):
    d.line([(ox,30+(Y-y0)*Z),(ox+w,30+(Y-y0)*Z)],fill=(0,0,255) if Y%5==0 else (150,150,255),width=1)
for Y in range(y0,y1): d.text((2,30+(Y-y0)*Z+2),str(Y),fill=(0,0,0))
out.save(uit)
