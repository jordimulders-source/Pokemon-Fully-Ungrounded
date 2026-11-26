import numpy as np, sys
from PIL import Image, ImageDraw
RN=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); out=sys.argv[6]; Z=int(sys.argv[7]) if len(sys.argv)>7 else 20
sp=Image.open(f'{RN}/impala_{RN}.png'); sp.info['transparency']=0; sp=sp.convert('RGBA')
c=Image.new('RGBA',(x1-x0,y1-y0),(255,255,255,255)); cr=sp.crop((x0,y0,x1,y1)); c.paste(cr,(0,0),cr); c=c.resize((c.width*Z,c.height*Z),Image.NEAREST).convert('RGB')
d=ImageDraw.Draw(c)
for i in range(x1-x0+1): d.line([(i*Z,0),(i*Z,c.height)],fill=(210,210,210))
for j in range(y1-y0+1): d.line([(0,j*Z),(c.width,j*Z)],fill=(210,210,210))
for i in range(x1-x0):
    if (x0+i)%5==0: d.text((i*Z+2,2),str(x0+i),fill=(0,120,255))
for j in range(y1-y0):
    if (y0+j)%5==0: d.text((2,j*Z+2),str(y0+j),fill=(0,120,255))
P=np.load(sys.argv[8] if len(sys.argv)>8 else '/tmp/claude-0/s/curve.npy')
for x,y in P:
    if x0<=x<x1 and y0<=y<y1: X,Y=(x-x0)*Z,(y-y0)*Z; d.rectangle([X-1,Y-1,X+1,Y+1],fill=(255,0,0))
c.save(out)
