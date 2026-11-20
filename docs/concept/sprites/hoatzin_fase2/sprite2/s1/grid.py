# grid.py x0 y0 x1 y1 (spritecoordinaten) out.png: modeluitsnede met spritepixelraster
import sys, numpy as np
from PIL import Image, ImageDraw
X0,Y0,s=97,125,833/62; ox,oy=1,5
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
m=Image.open('../../MODEL.png').convert('RGB')
box=[X0+(x0-ox)*s,Y0+(y0-oy)*s,X0+(x1-ox)*s,Y0+(y1-oy)*s]
c=m.crop([int(round(v)) for v in box]); Z=float(sys.argv[6]) /s if len(sys.argv)>6 else 40/s; G=int(round(Z*s))
c=c.resize((int(c.width*Z),int(c.height*Z)),Image.LANCZOS); d=ImageDraw.Draw(c)
for i in range(x1-x0+1):
    d.line([(i*G,0),(i*G,c.height)],fill=(0,200,0) if (x0+i)%5 else (255,0,0))
for j in range(y1-y0+1):
    d.line([(0,j*G),(c.width,j*G)],fill=(0,200,0) if (y0+j)%5 else (255,0,0))
c.save(sys.argv[5])
