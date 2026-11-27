# close-up van rN (64x64-coordinaten x0 y0 x1 y1) met de modelcurves: buitenrand + zwarte modellijn (rood) en toongrenzen (lichtrood).
# Punten: r7/zones/curve.py (curve.npy, rand.npy) en r9/toongrens.py (toon.npy) in /tmp/claude-0/s/.
import numpy as np, sys
from PIL import Image, ImageDraw
RN,x0,y0,x1,y1,out,Z=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6],int(sys.argv[7])
sp=Image.open(f'{RN}/impala_{RN}.png'); sp.info['transparency']=0; sp=sp.convert('RGBA')
c=Image.new('RGBA',(x1-x0,y1-y0),(200,230,200,255)); cr=sp.crop((x0,y0,x1,y1)); c.paste(cr,(0,0),cr); c=c.resize((c.width*Z,c.height*Z),Image.NEAREST).convert('RGB')
d=ImageDraw.Draw(c)
for i in range(x1-x0):
    if (x0+i)%5==0: d.text((i*Z+2,2),str(x0+i),fill=(0,120,255))
for j in range(y1-y0):
    if (y0+j)%5==0: d.text((2,j*Z+2),str(y0+j),fill=(0,120,255))
for f,col,r in (('rand',(255,0,0),1),('curve',(255,0,0),1),('toon',(255,120,120),1)):
    for x,y in np.load(f'/tmp/claude-0/s/{f}.npy')[::(3 if f=='rand' else 1)]:
        if x0<=x<x1 and y0<=y<y1: X,Y=(x-x0)*Z,(y-y0)*Z; d.rectangle([X-r,Y-r,X+r,Y+r],fill=col)
c.save(out)
