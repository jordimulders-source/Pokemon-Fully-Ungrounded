# Natief model 12x met coordinaatraster (hulpbeeld, alleen om te meten)
import numpy as np, sys; from PIL import Image, ImageDraw
src=sys.argv[1]; out=sys.argv[2]; x0,y0,x1,y1=map(int,sys.argv[3:7]); k=int(sys.argv[7]) if len(sys.argv)>7 else 14
im=Image.open(src).convert('RGB').crop((x0,y0,x1,y1)); w,h=im.size
big=im.resize((w*k,h*k),Image.NEAREST); d=ImageDraw.Draw(big)
for i in range(w):
    d.line([(i*k,0),(i*k,h*k)],fill=(200,200,255) if (x0+i)%5 else (255,0,0))
for j in range(h):
    d.line([(0,j*k),(w*k,j*k)],fill=(200,200,255) if (y0+j)%5 else (255,0,0))
for i in range(0,w):
    if (x0+i)%5==0: d.text((i*k+1,1),str(x0+i),fill=(255,0,0))
for j in range(0,h):
    if (y0+j)%5==0: d.text((1,j*k+1),str(y0+j),fill=(255,0,0))
big.save(out)
