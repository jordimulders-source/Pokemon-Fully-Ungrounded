# raster.py SPRITE x0 y0 x1 y1 schaal uit: uitsnede met rasterlijnen en coördinaten (om randen per pixel te bepalen)
import sys; sys.path.insert(0,'sprite_r9'); from gemeen2 import *; import numpy as np; from PIL import Image, ImageDraw
a=np.array(Image.open(sys.argv[1])); x0,y0,x1,y1,s=map(int,sys.argv[2:7])
im=rgb(a,(255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),0); B=Image.new('RGB',(im.width+30,im.height+20),'white'); B.paste(im,(30,20)); d=ImageDraw.Draw(B)
for i in range(x1-x0+1): d.line([(30+i*s,20),(30+i*s,20+im.height)],fill=(200,200,255))
for j in range(y1-y0+1): d.line([(30,20+j*s),(30+im.width,20+j*s)],fill=(200,200,255))
for i in range(x1-x0): d.text((30+i*s+3,4),str((x0+i)%100),fill='blue')
for j in range(y1-y0): d.text((2,20+j*s+5),str(y0+j),fill='blue')
B.save(sys.argv[7])
