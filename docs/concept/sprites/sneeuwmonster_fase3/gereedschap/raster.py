# raster.py X0 Y0 X1 Y1 UIT.png [SPRITE.png]: natief model (en sprite) van een spritezone op 24x met het spriteraster erover (rood, elke 5e px dikker)
import sys, os, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); Z=24
n=Image.open(NATIEF).convert('RGB'); a0,b0=s2n(X0,Y0); a1,b1=s2n(X1,Y1)
k=Z/F; c=n.resize((int(240*k),int(130*k)),Image.NEAREST).crop((int(a0*k),int(b0*k),int(a1*k),int(b1*k)))
d=ImageDraw.Draw(c)
for X in range(X1-X0+1): d.line([(X*Z,0),(X*Z,c.height)],fill=(255,0,0),width=2 if (X0+X)%5==0 else 1)
for Y in range(Y1-Y0+1): d.line([(0,Y*Z),(c.width,Y*Z)],fill=(255,0,0),width=2 if (Y0+Y)%5==0 else 1)
out=[c]
if len(sys.argv)>6:
    im=Image.open(sys.argv[6]); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    rgbim=pal[o][Y0:Y1,X0:X1].astype('uint8'); rgbim[o[Y0:Y1,X0:X1]==0]=255
    s=Image.fromarray(rgbim).resize(c.size,Image.NEAREST); out.append(s)
W=sum(i.width+10 for i in out); v=Image.new('RGB',(W,c.height),'white'); x=0
for i in out: v.paste(i,(x,0)); x+=i.width+10
v.save(sys.argv[5])
