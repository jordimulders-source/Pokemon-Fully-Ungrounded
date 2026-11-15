# Controle: sprite en model naast elkaar voor een vak, zelfde schaal, met raster en coordinaten.
import sys,numpy as np; from PIL import Image, ImageDraw
x0,y0,x1,y1,z=map(int,sys.argv[2:7]); UIT=sys.argv[7]
P,PH=5.12,4.1; s=165/46; top=22; left=9; k=P*s
ox=PH+P*(18-left*s); oy=PH+P*(37-top*s)
mod=Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')
pad=Image.new('RGB',(1400,1400),(255,255,255)); pad.paste(mod,(200,200))
mc=pad.crop((int(ox+x0*k)+200,int(oy+y0*k)+200,int(ox+x1*k)+200,int(oy+y1*k)+200)).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
sp=Image.open(sys.argv[1]); sp.save('/tmp/_n.png',transparency=0); sp=Image.open('/tmp/_n.png').convert('RGBA')
b=Image.new('RGBA',sp.size,(255,255,255,255)); b.alpha_composite(sp)
sc=b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=(x1-x0)*z; H=(y1-y0)*z
im=Image.new('RGB',(2*W+60,H+20),(255,255,255)); im.paste(sc,(30,20)); im.paste(mc,(W+60,20)); d=ImageDraw.Draw(im)
for off in (30,W+60):
  for i in range(x1-x0+1):
    X=off+i*z; d.line([(X,20),(X,20+H)],fill=(255,0,0) if (x0+i)%5==0 else (150,220,255))
    if (x0+i)%5==0: d.text((X+2,6),str(x0+i),fill=(255,0,0))
  for j in range(y1-y0+1):
    Y=20+j*z; d.line([(off,Y),(off+W,Y)],fill=(255,0,0) if (y0+j)%5==0 else (150,220,255))
    if (y0+j)%5==0: d.text((off-26,Y+2),str(y0+j),fill=(255,0,0))
im.save(UIT)
