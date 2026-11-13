# lijnkaart.py raster out x0 y0 x1 y1 z [fr]: zwart = model en sprite donker (o/d/k-lijn), rood = alleen model (fractie zwart+donkerpaars >= fr), blauw = alleen sprite
import sys,numpy as np, pal
from PIL import Image,ImageDraw
d=np.load('meet.npz'); f=(d['fo']+d['fd'])/np.maximum(d['cov'],1e-6); fk=d['fk']/np.maximum(d['cov'],1e-6)
R=pal.load(sys.argv[1]); x0,y0,x1,y1,z=map(int,sys.argv[3:8]); fr=float(sys.argv[8]) if len(sys.argv)>8 else .34
im=Image.new('RGB',((x1-x0)*z,(y1-y0)*z),'white'); dr=ImageDraw.Draw(im); n={'beide':0,'rood':[],'blauw':[]}
for y in range(y0,y1):
  for x in range(x0,x1):
    ch=R[y][x]; md=f[y,x]>=fr and fk[y,x]<.5; sd=ch in 'od'
    if ch=='.': col=(200,230,200)
    elif md and sd: col=(0,0,0); n['beide']+=1
    elif md: col=(230,0,0); n['rood'].append((x,y))
    elif sd and fk[y,x]<.5: col=(40,80,255); n['blauw'].append((x,y))
    else: col=tuple(int(v*.5+127) for v in pal.RGB[ch])
    dr.rectangle([(x-x0)*z,(y-y0)*z,(x-x0+1)*z-1,(y-y0+1)*z-1],fill=col)
im.save(sys.argv[2]); print('beide',n['beide'],'rood',len(n['rood']),n['rood'],'\nblauw',len(n['blauw']),n['blauw'])
