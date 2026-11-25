# Hulpmiddel: uitsnede van een sprite op schaal S met raster en coördinaten (elke 5 px een label). python3 raster.py in.npy/png uit.png x0 y0 x1 y1 [S]
import sys, numpy as np; from PIL import Image, ImageDraw
from gemeen import rgb
f=sys.argv[1]; o=np.load(f) if f.endswith('.npy') else np.array(Image.open(f))
x0,y0,x1,y1=[int(v) for v in sys.argv[3:7]]; S=int(sys.argv[7]) if len(sys.argv)>7 else 16; M=24
a=Image.fromarray(rgb(o,bg=(255,255,255))).crop((x0,y0,x1,y1)); a=a.resize((a.width*S,a.height*S),Image.NEAREST)
c=Image.new('RGB',(a.width+M,a.height+M),'white'); c.paste(a,(M,M)); d=ImageDraw.Draw(c)
for x in range(x0,x1+1):
    X=M+(x-x0)*S; d.line([(X,M),(X,c.height)],fill=(0,0,255) if x%5==0 else (190,190,190))
    if x%5==0: d.text((X+2,4),str(x),fill=(0,0,255))
for y in range(y0,y1+1):
    Y=M+(y-y0)*S; d.line([(M,Y),(c.width,Y)],fill=(0,0,255) if y%5==0 else (190,190,190))
    if y%5==0: d.text((2,Y+2),str(y),fill=(0,0,255))
c.save(sys.argv[2])
