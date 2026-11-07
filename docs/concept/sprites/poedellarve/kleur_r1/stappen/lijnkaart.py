# lijnkaart X0 Y0 X1 Y1 z out raster [th] [frac]: zwart=beide donker, rood=alleen model, blauw=alleen sprite(1/2/3), grijs=sprite 4/5 waar model donker
import sys,numpy as np
from PIL import Image,ImageDraw
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/'
x0,y0=236,346; s=13.55; top,left=33,12
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float)
lum=c.mean(2); g=(c[...,1]>c[...,0]+15)
X0,Y0,X1,Y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]; R=[l.rstrip('\n') for l in open(sys.argv[7])]
th=int(sys.argv[8]) if len(sys.argv)>8 else 75; fr=float(sys.argv[9]) if len(sys.argv)>9 else .3
im=Image.new('RGB',((X1-X0)*z,(Y1-Y0)*z),(255,255,255)); d=ImageDraw.Draw(im)
for y in range(Y0,Y1):
  for x in range(X0,X1):
    bx=x0+(x-left)*s; by=y0+(y-top)*s
    sl=(slice(int(by),int(by+s)),slice(int(bx),int(bx+s))); L=lum[sl]; fg=~g[sl]
    md=((L<th)&fg).sum()/max(1,fg.sum())>=fr
    ch=R[y][x]
    if ch=='.': col=(200,230,200)
    else:
      sd=ch in '123'
      col=(0,0,0) if (md and sd) else (230,0,0) if md and ch in '45' else (255,120,120) if md else (40,80,255) if sd else (int(L[fg].mean()) if fg.any() else 255,)*3
      if not md and not sd and ch in '45': col=(240,200,60)
    d.rectangle([(x-X0)*z,(y-Y0)*z,(x-X0+1)*z-1,(y-Y0+1)*z-1],fill=col)
for i in range(X1-X0+1):
  if (X0+i)%5==0: d.line([(i*z,0),(i*z,im.height)],fill=(0,160,0)); d.text((i*z+1,1),str(X0+i),fill=(0,140,0))
for j in range(Y1-Y0+1):
  if (Y0+j)%5==0: d.line([(0,j*z),(im.width,j*z)],fill=(0,160,0)); d.text((1,j*z+1),str(Y0+j),fill=(0,140,0))
im.save(out)
