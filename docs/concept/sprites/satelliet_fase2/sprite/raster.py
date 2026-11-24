# Model op het spriteraster: modeluitsnede met rasterlijnen per spritepixel + coordinaten, naast de sprite (zelfde schaal)
# Gebruik: python3 raster.py SPRITE.npy i0 i1 j0 j1 UIT   (i = kolom, j = rij in het gereduceerde 64x50 raster)
import numpy as np, sys; from PIL import Image, ImageDraw
o=np.load(sys.argv[1]); i0,i1,j0,j1=map(int,sys.argv[2:6]); UIT=sys.argv[6]
PAL=np.load('pal.npy'); from cfg import MODEL, X0, Y0, s
M=Image.open(MODEL).convert('RGB'); Z=24
w,h=i1-i0,j1-j0
crop=M.crop((int(X0+i0*s),int(Y0+j0*s),int(X0+i1*s),int(Y0+j1*s))).resize((w*Z,h*Z),Image.LANCZOS)
d=ImageDraw.Draw(crop)
for i in range(w+1): d.line([(i*Z,0),(i*Z,h*Z)],fill=(255,0,0),width=1)
for j in range(h+1): d.line([(0,j*Z),(w*Z,j*Z)],fill=(255,0,0),width=1)
sp=Image.new('RGB',(w*Z,h*Z),(255,0,255)); ds=ImageDraw.Draw(sp)
for j in range(h):
  for i in range(w):
    v=o[j0+j,i0+i]
    if v: ds.rectangle([i*Z,j*Z,(i+1)*Z-1,(j+1)*Z-1],fill=tuple(int(c) for c in PAL[v]))
for i in range(w+1): ds.line([(i*Z,0),(i*Z,h*Z)],fill=(90,90,90))
for j in range(h+1): ds.line([(0,j*Z),(w*Z,j*Z)],fill=(90,90,90))
out=Image.new('RGB',(2*w*Z+30,h*Z+20),(255,255,255)); out.paste(crop,(0,20)); out.paste(sp,(w*Z+30,20))
dd=ImageDraw.Draw(out)
for i in range(0,w,2): dd.text((i*Z+4,4),str(i0+i),fill=(0,0,0)); dd.text((w*Z+30+i*Z+4,4),str(i0+i),fill=(0,0,0))
for j in range(0,h,2): dd.text((w*Z+8,20+j*Z+6),str(j0+j),fill=(0,0,0))
out.save(UIT)
