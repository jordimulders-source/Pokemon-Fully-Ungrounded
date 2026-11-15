# Meethulp: modeluitsnede op spriteschaal met spritepixelraster en coordinaten (x,y van het 64-canvas).
import sys,numpy as np; from PIL import Image, ImageDraw
x0,y0,x1,y1,z=map(int,sys.argv[1:6]); UIT=sys.argv[6]
P,PH=5.12,4.1; s=165/46; top=22; left=9; k=P*s
ox=PH+P*(18-left*s); oy=PH+P*(37-top*s)
mod=Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')
pad=Image.new('RGB',(1400,1400),(255,255,255)); pad.paste(mod,(200,200))
c=pad.crop((int(ox+x0*k)+200,int(oy+y0*k)+200,int(ox+x1*k)+200,int(oy+y1*k)+200)).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
im=Image.new('RGB',(c.width+30,c.height+20),(255,255,255)); im.paste(c,(30,20)); d=ImageDraw.Draw(im)
for i in range(x1-x0+1):
  X=30+i*z; d.line([(X,20),(X,im.height)],fill=(0,200,255) if (x0+i)%5 else (255,0,0))
  if (x0+i)%5==0 and i<x1-x0: d.text((X+2,4),str(x0+i),fill=(255,0,0))
for j in range(y1-y0+1):
  Y=20+j*z; d.line([(30,Y),(im.width,Y)],fill=(0,200,255) if (y0+j)%5 else (255,0,0))
  if (y0+j)%5==0 and j<y1-y0: d.text((2,Y+2),str(y0+j),fill=(255,0,0))
im.save(UIT)
