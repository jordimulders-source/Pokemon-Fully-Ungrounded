# zoom.py x0 y0 x1 y1 uit.png [sprite.png|blad64]: uitsnede blad/sprite | model, 16x met raster
import sys, numpy as np; from PIL import Image
from raster import *
x0,y0,x1,y1=map(int,sys.argv[1:5]); K=16
src=sys.argv[6] if len(sys.argv)>6 else 'blad64'
if src=='blad64':
    B=np.load('blad64.npy',allow_pickle=True).item(); im=Image.fromarray(B['rgb'].astype('uint8'))
else:
    s=Image.open(src).convert('RGBA'); im=Image.new('RGB',(64,64),'white'); im.paste(s,(0,0),s)
a=labels(grid(im.crop((x0,y0,x1,y1)).resize(((x1-x0)*K,(y1-y0)*K),Image.NEAREST),K,x0,y0),K,18,x0,y0,max(x1-x0,y1-y0))
b=labels(grid(model_img(K,x0,y0,x1,y1),K,x0,y0),K,18,x0,y0,max(x1-x0,y1-y0))
c=Image.new('RGB',(a.width*2+10,a.height),'white'); c.paste(a,(0,0)); c.paste(b,(a.width+10,0)); c.save(sys.argv[5])
