# model_12x uitsnede met spriteraster en coördinaten (per 2 px label)
import sys; from PIL import Image, ImageDraw; import numpy as np
x0,y0,x1,y1=map(int,sys.argv[1:5]); S=int(sys.argv[6]) if len(sys.argv)>6 else 16
src=Image.open(sys.argv[7] if len(sys.argv)>7 else 'model_12x.png').convert('RGB')
k=src.size[0]/64
im=src.crop((int(x0*k),int(y0*k),int(x1*k),int(y1*k))).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS if k!=int(k) or True else Image.NEAREST)
d=ImageDraw.Draw(im)
for i in range(x1-x0+1):
    d.line([(i*S,0),(i*S,im.size[1])],fill=(255,0,0) if (x0+i)%5==0 else (200,200,200),width=1)
for j in range(y1-y0+1):
    d.line([(0,j*S),(im.size[0],j*S)],fill=(255,0,0) if (y0+j)%5==0 else (200,200,200),width=1)
for i in range(x0,x1):
    if i%5==0: d.text(((i-x0)*S+2,2),str(i),fill=(255,0,0))
for j in range(y0,y1):
    if j%5==0: d.text((2,(j-y0)*S+2),str(j),fill=(255,0,0))
im.save(sys.argv[5])
