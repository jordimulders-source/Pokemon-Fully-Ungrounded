import sys
from PIL import Image, ImageDraw
im=Image.open('../../model/model_gekozen.png').convert('RGB')
x0,y0,x1,y1,k=map(int,sys.argv[1:6])
b=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*k,(y1-y0)*k),Image.NEAREST); d=ImageDraw.Draw(b)
for x in range(x0,x1):
    if x%5==0: d.line([((x-x0)*k,0),((x-x0)*k,b.height)],fill=(255,0,0) if x%10==0 else (255,180,180))
    if x%10==0: d.text(((x-x0)*k+2,2),str(x),fill=(0,0,255))
for y in range(y0,y1):
    if y%5==0: d.line([(0,(y-y0)*k),(b.width,(y-y0)*k)],fill=(255,0,0) if y%10==0 else (255,180,180))
    if y%10==0: d.text((2,(y-y0)*k+2),str(y),fill=(0,0,255))
b.save(sys.argv[6])
