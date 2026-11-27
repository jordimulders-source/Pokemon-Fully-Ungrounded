# natief gezicht 16x met spritecelraster (3 natief) en spritecoordinaten
from PIL import Image, ImageDraw; import numpy as np
MY,MX=np.load('fase/f01_map.npy'); S=16
import sys
sy0,sy1,sx0,sx1=[int(v) for v in sys.argv[3:7]] if len(sys.argv)>6 else (12,34,19,40)
S=int(sys.argv[7]) if len(sys.argv)>7 else 16
a=Image.open(sys.argv[1]).crop((MX+3*sx0,MY+3*sy0,MX+3*sx1,MY+3*sy1))
im=a.resize((a.width*S,a.height*S),Image.NEAREST).convert('RGB'); d=ImageDraw.Draw(im)
for k in range(sx1-sx0+1): d.line([(3*S*k,0),(3*S*k,im.height)],fill=(0,200,255),width=1)
for k in range(sy1-sy0+1): d.line([(0,3*S*k),(im.width,3*S*k)],fill=(0,200,255),width=1)
for k in range(sx1-sx0): d.text((3*S*k+2,2),str(sx0+k),fill=(255,0,0))
for k in range(sy1-sy0): d.text((2,3*S*k+2),str(sy0+k),fill=(255,0,0))
im.save(sys.argv[2]); print(im.size)
