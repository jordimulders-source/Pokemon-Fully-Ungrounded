# lijnkaart.py raster out x0 y0 x1 y1 z [fr]: zwart = model en sprite donker (o), rood = alleen model (fractie L<20 >= fr), blauw = alleen sprite; anders spritekleur licht
import sys,numpy as np, pal
from PIL import Image,ImageDraw
d=np.load('meet5.npz'); fo=d['fo']
R=pal.load(sys.argv[1]); x0,y0,x1,y1,z=map(int,sys.argv[3:8]); fr=float(sys.argv[8]) if len(sys.argv)>8 else .3
im=Image.new('RGB',((x1-x0)*z,(y1-y0)*z),'white'); dr=ImageDraw.Draw(im); n={'rood':[],'blauw':[]}
for y in range(y0,y1):
  for x in range(x0,x1):
    ch=R[y][x]; md=fo[y,x]>=fr; sd=ch=='o'
    if ch=='.': col=(200,230,200)
    elif md and sd: col=(0,0,0)
    elif md: col=(230,0,0); n['rood'].append((x,y))
    elif sd: col=(40,80,255); n['blauw'].append((x,y))
    else: col=tuple(int(v*.5+127) for v in pal.RGB[ch])
    dr.rectangle([(x-x0)*z,(y-y0)*z,(x-x0+1)*z-1,(y-y0+1)*z-1],fill=col)
for i in range(x0,x1+1):
  if i%4==0: dr.line([(( i-x0)*z,0),((i-x0)*z,im.height)],fill=(0,160,0)); dr.text(((i-x0)*z+1,1),str(i),fill=(0,140,0))
for j in range(y0,y1+1):
  if j%4==0: dr.line([(0,(j-y0)*z),(im.width,(j-y0)*z)],fill=(0,160,0)); dr.text((1,(j-y0)*z+1),str(j),fill=(0,140,0))
im.save(sys.argv[2]); print(n)
